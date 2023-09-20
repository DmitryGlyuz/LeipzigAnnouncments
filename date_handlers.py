from config_handlers import load_config, set_config_property, InvalidConfigError
from datetime import datetime, timedelta
import re


config = load_config()


def get_start_date() -> datetime.date:
    start_date_in_config = config["start_date"]
    return (datetime.strptime(start_date_in_config, "%Y-%m-%d") if start_date_in_config else datetime.now()).date()


def get_shifted_date(current_date, days: int) -> datetime.date:
    return current_date + timedelta(days=days)


def get_final_date() -> datetime.date:
    start_date = get_start_date()
    days_limit = config["days_limit"]
    return get_shifted_date(start_date, days_limit)


def move_start_date_in_config_week_forward() -> None:
    start_date = get_start_date()
    new_date = get_shifted_date(start_date, 7)
    new_date_string = new_date.strftime("%Y-%m-%d")
    set_config_property('start_date', new_date_string)


