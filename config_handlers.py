import json


CONFIG_FILE_PATH = "config.json"


class InvalidConfigError(Exception):
    pass


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


def load_config():
    with open(CONFIG_FILE_PATH, 'r') as json_file:
        config = json.load(json_file)
        validate_config_format(config)
        return config


def save_config(config: dict):
    with open(CONFIG_FILE_PATH, 'w') as json_file:
        json.dump(config, json_file, indent=4)


def set_config_property(_property: str, value):
    config = load_config()
    config[_property] = value
    save_config(config)


if __name__ == "__main__":
    for property, value in load_config().items():
        print(f"Property: {property}\n"
              f"Value: {value}\n"
              f"Value type: {type(value)}\n\n")
