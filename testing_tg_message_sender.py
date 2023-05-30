import requests
import json
import os

with open("config.json", 'r') as json_file:
    config = json.load(json_file)


BOT_TOKEN = config['bot_token']
CHANNEL_ID = config['testing_channel_id']


def send_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('Message sent successfully!\n')
    else:
        print(f'Failed to send message. Error code: {response.status_code}\n')


user_input = input("Press Y if you want to post announcements to TESTING channel: ")
if user_input.lower() == 'y':
    for file_name in os.listdir("tg_messages"):
        print(file_name)
        with open(f"tg_messages/{file_name}", 'r', encoding='utf-8') as f:
            send_message(f.read())
