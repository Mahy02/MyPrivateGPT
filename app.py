#note that everything installed will only be in our virtual env for this app
#Dependencies we are going to need => * pip install streamlit           : to create GUI
#                                     * pip install pypdf2              : to download our pdfs
#                                     * pip install langchain           : to interact with our language models
#                                     * pip install python-dotevn       : to download our secrets from .env file "hidden" #python-dotenv   => to be able to read the .env 
#                                     * pip install faiss-cpu           : As our vector store
#                                     * pip install openai              : Our Model
#    
#                                  * pip install huggingface_hub     : Our Model

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
#from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings,
from langchain.embeddings import HuggingFaceEmbeddings
#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template, text_input_template
import argparse
#from constants import CHROMA_SETTINGS
from langchain.docstore.document import Document

#our language models:
#from langchain.llms import OpenAI
#from langchain.llms import HuggingFaceHub
#from langchain.chat_models import ChatOpenAI
from langchain.llms import GPT4All, LlamaCpp


import os

#print("this comes from .env:", os.getenv('MODEL_TYPE'))

from langchain.document_loaders import (
    CSVLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)



#embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))


# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}


def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()

#The function takes our pdf docs [list of pdf files] and retruns a single String of text wth all of the text content of those pdfs
def get_pdf_text(pdf_docs):
    text =""
    for pdf in pdf_docs:
        #Pdf reader object creates pdf object that has pages
        pdf_reader = PdfReader(pdf)
        #now we will loop through the pages and read the content
        for page in pdf_reader.pages:
            #extrating all raw text
            text+=page.extract_text()
    return text
#end get_pdf_text fn


#the fn takes a string of text and returns a list of chunks of text to feed our DB
#to divide text to chunks we need langchain library by using a class from it
def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,  #1000 chars
        chunk_overlap=200,   #to avoid overlapping so it can start few chars before to avoid losing meaning of text
        length_function=len
    )
    chunks= text_splitter.split_text(raw_text)
    return chunks
#end get_text_chunks fn

#we get the vector store
def get_vectorstore(text_chunks,embeddings_model_name):
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    #embeddings= HuggingFaceInstructEmbeddings(model_name= "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore
#end get_vectorstore


def get_conversation_chain(vectorstore):
    #llm = OpenAI()
    #our Large Language Model:
    #llm = ChatOpenAI()
    # Prepare the LLM
    # Parse the command line arguments
    args = parse_arguments()
   # callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    match model_type:
        case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, n_batch=model_n_batch,  verbose=False)
        case "GPT4All":
            llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', n_batch=model_n_batch, verbose=False)
        case _default:
            # raise exception if model_type is not supported
            raise Exception(f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")
        
    #Memory in langchain
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    #initialize convo
    conversation_chain = ConversationalRetrievalChain.from_llm(
        #1. language model
        llm= llm,
        #2. vector store
        retriever= vectorstore.as_retriever(),
        #3. memory
        memory= memory
    )
    return conversation_chain
#end get_conversation_chain

def handle_userinput(user_question):
    #converstation has info from vectorstore + memory
    response = st.session_state.conversation({'question': user_question})
    #response from language model
    #the response returns all the object, total history and question and answer
    #st.write(response)
    
    #creating new session state var
    st.session_state.chat_history= response['chat_history']

    for i, message in enumerate( st.session_state.chat_history):
        if i % 2 ==0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
#end handle_userinput




def main():

    #this function allows us to read the .env file tp get API keys
    load_dotenv()

    embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')

    #------------------------------------GUI-----------------------------------
    #setting the page configuration:
    st.set_page_config(page_title="Chat With Multiple Pdfs", page_icon=":books:")

    #Initializing the CSS
    st.write(css, unsafe_allow_html= True)

    #initialize session state objects before
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    


    #setting main header of app
    #Show the header onlyy before conversation start
    if st.session_state.conversation is None:
        st.header("Chat with YOUR own PDFs privately :books: :lock: ")
    #st.header("Chat with YOUR own PDFs privately :books: :lock: ")

   
    

    #text input so users can add their questions:
    user_question= st.text_input("Ask a Question about your documents:")
    if user_question:
        handle_userinput(user_question)
    #endif
    
    
    #Side bar for chats
    #with is used for putting things inside your side bar
    with st.sidebar:
        st.subheader("Upload your Documents here and click on process")

        #uploading files:
        pdf_docs=  st.file_uploader("", accept_multiple_files= True)

        #button:
        #if user presses on it do a certain function
        if st.button("Process"):
            #for the loading we use spinner 
            with st.spinner("Processing"):
                #get pdf text
                raw_text = get_pdf_text(pdf_docs)
                #st.write(raw_text)   #to make sure the raw data appears

                #get text chunks         
                text_chunks = get_text_chunks(raw_text)
                #st.write(text_chunks)

                # create vector store with embeddings
                vectorstore = get_vectorstore(text_chunks, embeddings_model_name)

                #create conversation chain
                #generate new messages of conversation
                #takes histoy of convo and returns next element of convo
                #so we need it to be presistent by using session_state to avoid reinitializing
                st.session_state.conversation = get_conversation_chain(vectorstore)
            #end with
        #endif
    #end with


    #------------------------------------------------------------------------


#endMain
    


#test check to test app is being executed 
if __name__ == '__main__':
    main()
#endTest










