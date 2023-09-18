import requests
import os
from config_handlers import load_config
from cli_functions import run_after_confirm_screen


config = load_config()
BOT_TOKEN = config['bot_token']
URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'


def send_message(message, channel_id):
    data = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(URL, data=data)
    if response.status_code == 200:
        print('Message sent successfully!\n')
    else:
        print(f'Failed to send message. Error code: {response.status_code}\n')


def send_all_messages(channel_id: str):
    for file_name in os.listdir("tg_messages"):
        print(file_name)
        with open(f"tg_messages/{file_name}", 'r', encoding='utf-8') as f:
            send_message(f.read(), channel_id)


def send_messages_screen(channel_id: str):
    run_after_confirm_screen("post announcements to TESTING channel", send_all_messages, channel_id)