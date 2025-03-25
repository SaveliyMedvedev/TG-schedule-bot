import time
from telebot import TeleBot
from telebot.types import InputMediaPhoto

from conf import TG_BOT_TOKEN, TG_CANNEL_ID
from parser import get_updates, get_post


bot = TeleBot(TG_BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Hi there, I am ScheduleBot.")


def send_to_telegram_channel(post_data):
    text = post_data.get("text")
    attachments = post_data.get("links_photo")

    bot.send_message(chat_id=TG_CANNEL_ID, text=text)

    if attachments:
        media = [InputMediaPhoto(photo) for photo in attachments]
        bot.send_media_group(chat_id=TG_CANNEL_ID, media=media)


def main():
    while True:
        try:
            updates = get_updates()
            print(updates)
            if updates:
                if updates[0]["type"] == "wall_post_new":
                    send_to_telegram_channel(get_post())
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    main()
