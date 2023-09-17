import json
import parsers
from config_handler import load_config
from cl_functions import run_after_confirm


config = load_config()


def get_dict() -> dict:
    all_events = {
            "planlos": parsers.get_planlos_events(),
            "sachsenpunk": parsers.get_sachsenpunk_events(),
            "songkick": parsers.get_songkick_events()
        }
    return all_events


def make_json():
    with open("all_events.json", 'w') as json_file:
        json.dump(get_dict(), json_file, indent=4)


def get_events():
    read_from_json = config["read_events_from_json"]
    if read_from_json:
        with open("all_events.json", 'r') as json_events_file:
            return json.load(json_events_file)
    else:
        return get_dict()


def create_json_after_confirm():
    run_after_confirm("create JSON file with announcements", make_json)


if __name__ == "__main__":
    create_json_after_confirm()
