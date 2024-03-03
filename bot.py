import os
import re
from datetime import datetime

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
    message = "🆕 [{course_title}]({course_url}) from {start} to {end}"
    df = pd.read_csv("courses.csv", sep='\t')
    for _, row in df[df["sent_at"].isna()].iterrows():
        start_date = parse(row['start'])
        in_the_future = start_date > datetime.now()
        has_spots = row['availability'] == "available"
        if in_the_future and has_spots:
            formatted_message = message.format(
                course_title=escape_markdown(row['title']),
                course_url=row['course_url'],
                start=escape_markdown(row['start']),
                end=escape_markdown(row['end'])
            )
            print(formatted_message)
            send_telegram_message(formatted_message)
            df['sent_at'] = str(datetime.now())

    df.to_csv('courses.csv', index=False, sep='\t')  # scrapy friendly


send_new_courses()
