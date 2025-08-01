import os
import re
from datetime import datetime
from random import randint
from time import sleep

from dateutil.parser import parse
import pandas as pd
import requests

from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = (
        f"https://api.telegram.org/bot{token}/"
        f"sendMessage?chat_id={chat_id}&"
        f"parse_mode=MarkdownV2&text={message}"
    )

    response = requests.get(url).json()
    if response.get("ok") is False:
        raise Exception(f"Failed to send message. Error: {response}")
    else:
        print("Message sent.")


def escape_markdown(text):
    text = text.replace("&", "and")
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


def send_new_courses():
    available_statuses = {"waiting list": "📖", "available": "💥"}
    message = "🆕 [{course_title}]({course_url}) from {start} to {end} {status}"
    df = pd.read_csv("courses.csv")
    for _, row in df[df["updated_at"].isna()].iterrows():
        try:
            start_date = parse(row['start'], dayfirst=True)
        except TypeError:
            print(f"TypeError: {row['start']} {row}")
            continue
        in_the_future = start_date > datetime.now()
        has_spots = row['availability'] in available_statuses.keys()
        if in_the_future and has_spots:
            formatted_message = message.format(
                course_title=escape_markdown(row['title']),
                course_url=row['course_url'],
                start=escape_markdown(row['start']),
                end=escape_markdown(row['end']),
                status=available_statuses.get(row['availability'])
            )
            print(formatted_message)
            sleep(randint(1,5))  # take some time so it doesn't reach the api's limits
            send_telegram_message(formatted_message)
            df['updated_at'] = str(datetime.now())

    df.to_csv('courses.csv', index=False)


send_new_courses()
