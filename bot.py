import time
from telebot import TeleBot
from telebot.types import InputMediaPhoto

from conf import TG_BOT_TOKEN, TG_CANNEL_ID
from parser import get_post


bot = TeleBot(TG_BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Hi there, I am ScheduleBot.")


def my_send_message(text: str, links_photo: tuple[str]):
    bot.send_message(chat_id=TG_CANNEL_ID, text=text)

    if links_photo:
        media = [InputMediaPhoto(photo) for photo in links_photo]
        bot.send_media_group(chat_id=TG_CANNEL_ID, media=media)


old_hash = " "
while True:
    result = get_post(old_hash)
    if result:
        text, hash_photo, links_photo = result
        my_send_message(text=text, links_photo=tuple(links_photo))
        old_hash = hash_photo

    time.sleep(600)
