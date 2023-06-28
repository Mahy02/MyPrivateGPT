#css
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

.uploader {
        position: fixed;
        bottom: 20px;
        right: 20px;
    }
.text-input-container {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 400px;
    height: 60px;
    background-color: #f5f5f5;
    border-radius: 30px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.text-input-container input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 16px;
    padding: 0 20px;
    background-color: transparent;
}


'''



# Text input template
text_input_template = '''
<div class="text-input-container">
    <input type="text" placeholder="Ask a Question about your documents" id="user-question" style="flex: 1; border: none; outline: none; font-size: 16px; padding: 10px;">
    <button onclick="submitQuestion()" style="margin-left: 10px; padding: 10px 20px; background-color: #4CAF50; color: #fff; border: none; border-radius: 20px; cursor: pointer;">Submit</button>
</div>
'''
#bot template
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="images/bot.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png

#user template

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="images/user.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

# https://i.ibb.co/rdZC7LZ/Photo-logo-1.png