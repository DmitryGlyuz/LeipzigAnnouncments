import json


CONFIG_FILE_PATH = "config.json"


def load_config():
    with open(CONFIG_FILE_PATH, 'r') as json_file:
        return json.load(json_file)


def save_config(config: dict):
    with open(CONFIG_FILE_PATH, 'w') as json_file:
        json.dump(config, json_file, indent=4)
