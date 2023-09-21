import os

import requests

from config_handlers import load_config
from messages_builder import messages_generator


def send_message(message, channel_id):
    config = load_config()
    bot_token = config['bot_token']
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('Message sent successfully!\n')
    else:
        print(f'Failed to send message. Error code: {response.status_code}\n')


def parse_websites_and_send_messages(channel_id: str):
    dates_and_messages = messages_generator()
    for date, message_text in dates_and_messages:
        print(date)
        send_message(message_text, channel_id)


def send_messages_from_files(channel_id: str):
    for file_name in os.listdir("tg_messages"):
        print(file_name)
        with open(f"tg_messages/{file_name}", 'r', encoding='utf-8') as f:
            send_message(f.read(), channel_id)
