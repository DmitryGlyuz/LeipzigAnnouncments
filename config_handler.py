import json


def load_config():
    with open("config.json", 'r') as json_file:
        return json.load(json_file)


def save_config(config: dict):
    with open("config.json", 'w') as json_file:
        json.dump(config, json_file, indent=4)
