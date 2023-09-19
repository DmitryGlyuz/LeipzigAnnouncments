from datetime import datetime
from date_handlers import move_start_date_in_config_week_forward
from cli_functions import run_after_confirm_screen
from config_handlers import load_config, save_config
from messages_builder import create_files
from events_combinator import write_events_to_json
from telegram_sender import send_messages_from_files, parse_websites_and_send_messages
import re
import os

config = load_config()
MAIN_CHANNEL_ID = config['channel_id']
TESTING_CHANNEL_ID = config['testing_channel_id']

HORIZONTAL_LINE = '_' * 50


def print_config():
    # After parsing, the start date may change in the configuration file,
    # this has no effect on anything in the command line interface except the output of the configuration itself,
    # but to avoid possible problems in the future, it is updated globally here.
    global config
    config = load_config()
    print(f"""Current configuration:
    Read events from JSON: {config["read_events_from_json"]}
    Start date: {config["start_date"]}
    Move start date property a week_forward after parsing: {config["move_start_date_week_forward_after_parsing"]}
    Days limit: {config["days_limit"]}""")


def print_caption(caption: str):
    print(caption)
    print(HORIZONTAL_LINE)


def print_caption_and_config(caption: str):
    print_caption(caption)
    print_config()
    print(HORIZONTAL_LINE)


def print_error(message: str):
    print(f"Error: {message}. Try again.")


def choose_item_screen(actions: tuple, caption="Available actions:", prompt="Enter your choice: ") -> str:
    print(f"\n{caption}")
    for index, action in enumerate(actions):
        print(f"{index + 1}. {action}")

    while True:
        user_choice = input(prompt)
        if not user_choice.isdigit():
            print_error("Your input is not an integer number")
        else:
            user_choice = int(user_choice)
            last_point_number = len(actions)
            if user_choice not in range(1, last_point_number + 1):
                print_error(f"Your input must be a number from 1 to {last_point_number}")
            else:
                print()
                return actions[user_choice - 1]


# Menu items for configuration editing screen
READING_FROM_JSON = "Reading data from JSON"
START_DATE = "Start date"
MANUALLY_MOVE_START_DATE = "Manually move the start date a week forward"
MOVE_START_DATE = "Move the start date a week forward after parsing"
DAYS_LIMIT = "Days limit"
BACK = "Go back"
ON = "On"
OFF = "Off"


def set_config_property(_property: str, value):
    config[_property] = value


def change_setting(message, _property: str, value):
    run_after_confirm_screen(message, set_config_property, _property, value, show_starting=False)
    save_config(config)


def change_boolean_config_property_screen(caption: str, _property):
    print_caption(f"Edit: {caption}")
    available_options = (ON, OFF, BACK)
    chosen_option = choose_item_screen(available_options, "Available options:")
    if chosen_option == ON:
        change_setting(f"turn on: {caption}", _property, True)
    elif chosen_option == OFF:
        change_setting(f"turn off: {caption}", _property, False)
    else:
        return


def valid_date(date: str):
    if not re.fullmatch(r"""\d{4}-\d{2}-\d{2}""", date):
        return False
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def edit_start_date_screen():
    while True:
        user_input = input("Input the new start date in YYYY-MM-DD format or press Enter to go back: ").strip()
        if not user_input:
            return
        elif not valid_date(user_input):
            print_error("Wrong date format")
        else:
            change_setting(f"change start date to {user_input}", "start_date", user_input)
            return


def edit_days_limit_screen():
    while True:
        user_input = input("Input the new days limit format or press Enter to go back: ").strip()
        if not user_input:
            return
        elif not re.fullmatch(r"\d+", user_input) or int(user_input) < 1:
            print_error("Days limit value should be a positive integer number ")
        else:
            change_setting(f"change days limit to {user_input}", "days_limit", int(user_input))
            return


def edit_config_screen():
    while True:
        print_caption_and_config("Editing configuration")
        config_items = (READING_FROM_JSON, START_DATE, MANUALLY_MOVE_START_DATE, MOVE_START_DATE, DAYS_LIMIT, BACK)
        item_to_edit = choose_item_screen(config_items, "Available config items:")
        if item_to_edit == READING_FROM_JSON:
            change_boolean_config_property_screen(READING_FROM_JSON, 'read_events_from_json')
        elif item_to_edit == START_DATE:
            edit_start_date_screen()
        elif item_to_edit == MANUALLY_MOVE_START_DATE:
            run_after_confirm_screen(MANUALLY_MOVE_START_DATE, move_start_date_in_config_week_forward,
                                     show_starting=False)
        elif item_to_edit == MOVE_START_DATE:
            change_boolean_config_property_screen(MOVE_START_DATE, 'move_start_date_week_forward_after_parsing')
        elif item_to_edit == DAYS_LIMIT:
            edit_days_limit_screen()
        else:
            break


def delete_all_files_with_messages():
    dir_path = "tg_messages"
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"{file_path} - deleted")


PARSE_AND_SEND_TO_TESTING = "Parse websites and send messages directly to the TESTING channel"
PARSE_AND_SEND_TO_MAIN = "Parse websites and send messages directly to the MAIN channel"
CREATE_FILES = "Create files with announcements"
CREATE_JSON = "Create JSON file with announcements"
POST_TO_TESTING = "Post announcements from files to the TESTING channel"
POST_TO_MAIN = "Post announcements from files to the MAIN channel"
PRINT_CONFIG = "Print configuration"
EDIT_CONFIG = "Edit configuration"
DELETE_FILES = "Delete files with texts for Telegram posts"
EXIT = "Exit"
main_menu_actions = (
    PARSE_AND_SEND_TO_TESTING, PARSE_AND_SEND_TO_MAIN, CREATE_FILES, CREATE_JSON, POST_TO_TESTING, POST_TO_MAIN,
    PRINT_CONFIG, DELETE_FILES,
    EDIT_CONFIG, EXIT)

print_caption_and_config("Leipzig Announcements Bot command line interface")

first_run = True
while True:
    if first_run:
        first_run = False
    else:
        print_caption("Main menu")

    main_menu_action = choose_item_screen(main_menu_actions)
    if main_menu_action == EXIT:
        break
    elif main_menu_action == PARSE_AND_SEND_TO_TESTING:
        run_after_confirm_screen(PARSE_AND_SEND_TO_TESTING, parse_websites_and_send_messages, TESTING_CHANNEL_ID)
    elif main_menu_action == PARSE_AND_SEND_TO_MAIN:
        run_after_confirm_screen(PARSE_AND_SEND_TO_MAIN, parse_websites_and_send_messages, TESTING_CHANNEL_ID)
    elif main_menu_action == CREATE_FILES:
        run_after_confirm_screen(CREATE_FILES, create_files)
    elif main_menu_action == CREATE_JSON:
        run_after_confirm_screen(CREATE_JSON, write_events_to_json)
    elif main_menu_action == POST_TO_TESTING:
        run_after_confirm_screen(POST_TO_TESTING, send_messages_from_files, TESTING_CHANNEL_ID)
    elif main_menu_action == POST_TO_MAIN:
        run_after_confirm_screen(POST_TO_TESTING, send_messages_from_files, MAIN_CHANNEL_ID)
    elif main_menu_action == PRINT_CONFIG:
        print_config()
        print()
    elif main_menu_action == DELETE_FILES:
        run_after_confirm_screen(DELETE_FILES, delete_all_files_with_messages)
    elif main_menu_action == EDIT_CONFIG:
        edit_config_screen()

print("Bye!")
