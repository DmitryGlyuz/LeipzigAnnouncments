from datetime import datetime
import json
import re


CONFIG_FILE_PATH = "config.json"


class InvalidConfigError(Exception):
    pass


def validate_date(date: str):
    error_message = "Wrong date format. The start date should have YYYY-MM-DD format"
    try:
        if not re.fullmatch(r"""\d{4}-\d{2}-\d{2}""", date):
            raise ValueError()
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise InvalidConfigError(error_message)


def validate_days_limit(days_limit):
    error_message = "Days limit value should be a positive integer number"
    if isinstance(days_limit, str):
        if not re.fullmatch(r"\d+", days_limit):
            raise InvalidConfigError(error_message)
        else:
            days_limit = int(days_limit)
    if days_limit < 1:
        raise InvalidConfigError(error_message)


def validate_config_format(config: dict):
    expected_keys_and_types = {
        "bot_token": str,
        "channel_id": str,
        "testing_channel_id": str,
        "start_date": str,
        "move_start_date_week_forward_after_parsing": bool,
        "days_limit": int
    }

    for expected_key, expected_type in expected_keys_and_types.items():
        if expected_key not in config:
            raise InvalidConfigError(f"Key {expected_key} is missing in configuration file")

        if not isinstance(config[expected_key], expected_type):
            raise InvalidConfigError(f"Value for {expected_key} should be {expected_type}")

    validate_date(config["start_date"])
    validate_days_limit(config["days_limit"])


def load_config():
    with open(CONFIG_FILE_PATH, 'r') as json_file:
        config = json.load(json_file)
        validate_config_format(config)
        return config


def save_config(config: dict):
    with open(CONFIG_FILE_PATH, 'w') as json_file:
        json.dump(config, json_file, indent=4)


def set_config_property(_property: str, _value):
    config = load_config()
    config[_property] = _value
    save_config(config)
