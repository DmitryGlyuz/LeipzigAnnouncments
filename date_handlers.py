from datetime import datetime, timedelta

from config_handlers import load_config, set_config_property


def get_start_date(config: dict) -> datetime.date:
    start_date_in_config = config["start_date"]
    return datetime.strptime(start_date_in_config, "%Y-%m-%d").date()


def get_shifted_date(current_date, days: int) -> datetime.date:
    return current_date + timedelta(days=days)


def get_final_date(config: dict) -> datetime.date:
    start_date = get_start_date(config)
    days_limit = config["days_limit"]
    return get_shifted_date(start_date, days_limit)


def set_start_date_from_date_object(date: datetime.date):
    date_string = date.strftime("%Y-%m-%d")
    set_config_property('start_date', date_string)


def move_start_date_in_config_week_forward() -> None:
    config = load_config()
    start_date = get_start_date(config)
    new_date = get_shifted_date(start_date, 7)
    set_start_date_from_date_object(new_date)


def get_closest_monday_to_date(date: datetime.date):
    origin_weekday = date.weekday()
    days_to_add = (7 - origin_weekday) % 7
    return get_shifted_date(date, days_to_add)


def set_start_date_to_closest_monday():
    closest_monday = get_closest_monday_to_date(datetime.now().date())
    set_start_date_from_date_object(closest_monday)
