import time
from telebot import TeleBot

from conf import TG_BOT_TOKEN, MY_CHAT_ID 
from parser import get_post

bot = TeleBot(TG_BOT_TOKEN)

chat_ids = set()
chat_ids.add(MY_CHAT_ID)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id 
    chat_ids.add(chat_id)
    bot.reply_to(message , "Hi there, I am ScheduleBot.")


def my_send_message(text: str, links_photo: list[str]):
    for chat_id in chat_ids:
        bot.send_message(chat_id, text=text)
        if links_photo:
            for link in links_photo:
                bot.send_photo(chat_id, link)



# @bot.message_handler(commands=['get_chat_id'])
# def get_chat_id(message):
#    chat_id = message.chat.id
#    bot.reply_to(message, f"Your chat ID is {chat_id}")

# bot.infinity_polling()

old_hash = " "
while True:
    result = get_post(old_hash)
    if not result:
         continue
    else:
        text, hash_photo, links_photo = result
        my_send_message(text=text, links_photo=links_photo)
        old_hash = hash_photo 
    
    time.sleep(600)


