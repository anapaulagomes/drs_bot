import os

import requests

from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = (
        f"https://api.telegram.org/bot{token}/"
        f"sendMessage?chat_id={chat_id}&"
        f"parse_mode=Markdown&text={message}"
    )

    response = requests.get(url).json()
    if response.get("ok") is False:
        raise Exception(f"Failed to send message. Error: {response}")
    else:
        print("Message sent.")
