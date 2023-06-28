#css
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #0D6078;
    color: #000000;
}
.chat-message.bot {
    background-color: #D3E4E8;
    color: #000000;
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
  width: 100%;
  padding: 0 1.5rem;
  color: #000000;
}

.sidebar .sidebar-content {
        background-color: #f8f9fa;
    }


</style>

'''

#<a href="https://imgbb.com/"><img src="https://i.ibb.co/Cms0Hm7/bot.png" alt="bot" border="0" /></a>

#bot template
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/Cms0Hm7/bot.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png

#user template
#<a href="https://imgbb.com/"><img src="https://i.ibb.co/9Z0D51x/user.png" alt="user" border="0" /></a>
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/9Z0D51x/user.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

# https://i.ibb.co/rdZC7LZ/Photo-logo-1.png