from datetime import datetime
from cli_functions import run_after_confirm_screen
from config_handlers import load_config, save_config
from messages_builder import create_files_screen
from events_combinator import create_json_screen
from telegram_sender import send_messages_screen
import re
import os


config = load_config()
LPZG_CHANNEL_ID = config['channel_id']
TESTING_CHANNEL_ID = config['testing_channel_id']

HORIZONTAL_LINE = '_' * 50


def print_config():
    print(f"""Current configuration:
    Read events from JSON: {config["read_events_from_json"]}
    Start date: {config["start_date"]}
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


READING_FROM_JSON = "Reading data from JSON"
START_DATE = "Start date"
DAYS_LIMIT = "Days limit"
BACK = "Go back"
ON = "On"
OFF = "Off"


def turn_on_reading_data_from_json():
    config["read_events_from_json"] = True


def turn_off_reading_data_from_json():
    config["read_events_from_json"] = False


def change_setting(message, change_setting_func, *args):
    run_after_confirm_screen(message, change_setting_func, *args, show_starting=False)
    save_config(config)


def edit_reading_from_json_screen():
    print_caption(f"Edit: {READING_FROM_JSON}")
    available_options = (ON, OFF, BACK)
    chosen_option = choose_item_screen(available_options, "Available options:")
    if chosen_option == ON:
        change_setting(f"turn on: {READING_FROM_JSON}", turn_on_reading_data_from_json)
    elif chosen_option == OFF:
        change_setting(f"turn off: {READING_FROM_JSON}", turn_off_reading_data_from_json)
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


def change_start_date(new_date: str):
    config["start_date"] = new_date


def edit_start_date_screen():
    while True:
        user_input = input("Input the new start date in YYYY-MM-DD format or press Enter to go back: ").strip()
        if not user_input:
            return
        elif not valid_date(user_input):
            print_error("Wrong date format")
        else:
            change_setting(f"change start date to {user_input}", change_start_date, user_input)
            return


def change_days_limit(days_limit: int):
    config["days_limit"] = days_limit


def edit_days_limit_screen():
    while True:
        user_input = input("Input the new days limit format or press Enter to go back: ").strip()
        if not user_input:
            return
        elif not re.fullmatch(r"\d+", user_input) or int(user_input) < 1:
            print_error("Days limit value should be a positive integer number ")
        else:
            change_setting(f"change days limit to {user_input}", change_days_limit, int(user_input))
            return


def edit_config_screen():
    while True:
        print_caption_and_config("Editing configuration")
        config_items = (READING_FROM_JSON, START_DATE, DAYS_LIMIT, BACK)
        item_to_edit = choose_item_screen(config_items, "Available config items:")
        if item_to_edit == READING_FROM_JSON:
            edit_reading_from_json_screen()
        elif item_to_edit == START_DATE:
            edit_start_date_screen()
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


CREATE_FILES = "Create files with announcements"
CREATE_JSON = "Create JSON file with announcements"
POST_TO_TESTING = "Post announcements to TESTING channel"
POST_TO_LPZG = "Post announcements to LPZG channel"
PRINT_CONFIG = "Print configuration"
EDIT_CONFIG = "Edit configuration"
DELETE_FILES = "Delete files with texts for Telegram posts"
EXIT = "Exit"
main_menu_actions = (
    CREATE_FILES, CREATE_JSON, POST_TO_TESTING, POST_TO_LPZG, PRINT_CONFIG, DELETE_FILES, EDIT_CONFIG, EXIT)

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
    elif main_menu_action == CREATE_FILES:
        create_files_screen()
    elif main_menu_action == CREATE_JSON:
        create_json_screen()
    elif main_menu_action == POST_TO_TESTING:
        send_messages_screen(TESTING_CHANNEL_ID)
    elif main_menu_action == POST_TO_LPZG:
        send_messages_screen(LPZG_CHANNEL_ID)
    elif main_menu_action == PRINT_CONFIG:
        print_config()
        print()
    elif main_menu_action == DELETE_FILES:
        run_after_confirm_screen(DELETE_FILES, delete_all_files_with_messages)
    elif main_menu_action == EDIT_CONFIG:
        edit_config_screen()

print("Bye!")
