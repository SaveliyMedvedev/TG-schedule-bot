import time
from telebot import TeleBot

from conf import TG_BOT_TOKEN, CHAT_ID
from parser import get_post

bot = TeleBot(TG_BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am ScheduleBot.
""")


def my_send_message(text: str, links_photo: list[str]):
    bot.send_message(CHAT_ID, text=text)
    if links_photo:
        for link in links_photo:
            bot.send_photo(CHAT_ID, link)



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


