import json
from config_handlers import load_config
from cli_functions import run_after_confirm_screen
import parsers


config = load_config()


def get_events_from_parsers() -> dict:
    all_events = {
            "planlos": parsers.get_planlos_events(),
            "sachsenpunk": parsers.get_sachsenpunk_events(),
            "songkick": parsers.get_songkick_events()
        }
    return all_events


def write_events_to_json():
    with open("all_events.json", 'w') as json_file:
        json.dump(get_events_from_parsers(), json_file, indent=4)


def get_events():
    read_from_json = config.get("read_events_from_json", False)
    if read_from_json:
        with open("all_events.json", 'r') as json_events_file:
            return json.load(json_events_file)
    else:
        return get_events_from_parsers()


def create_json_screen():
    run_after_confirm_screen("create JSON file with announcements", write_events_to_json)


if __name__ == "__main__":
    create_json_screen()
