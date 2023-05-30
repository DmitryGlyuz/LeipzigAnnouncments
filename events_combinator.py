import json
import parser_planlos
import parser_sachsenpunk
import parser_songkick


def get_dict() -> dict:
    all_events = {
            "planlos": parser_planlos.events,
            "sachsenpunk": parser_sachsenpunk.events,
            "songkick":parser_songkick.events
        }
    return all_events

def make_json():
    with open("all_events.json", 'w') as json_file:
        json.dump(get_dict(), json_file, indent=4)


def get_events():
    with open("config.json") as json_config_file:
        config = json.load(json_config_file)
        read_from_json = config["read_events_from_json"]

    if read_from_json:
        with open("all_events.json", 'r') as json_events_file:
            return json.load(json_events_file)
    else:
        return get_dict()


if __name__ == "__main__":
    user_input = input("Press Y if you want to create JSON file with announcements").lower()
    if user_input == 'y':
        make_json()
