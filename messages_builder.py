from datetime import datetime
from parsers import get_all_events
from itertools import chain


CALENDAR_SYMBOL = '🗓'
BULLET_SYMBOL = '🔹'
URL_SYMBOL = '🔗'
LOCATION_SYMBOL = '📍 '


def make_hyperlink(url, resource_name, symbol=URL_SYMBOL):
    return f"{symbol}<a href=\"{url}\">{resource_name}</a>"


def make_strings_for_planlos(events: list[dict]) -> list[str]:
    output_strings = []
    for event in events:
        place = event['place']
        if place:
            place_text = f"\n{LOCATION_SYMBOL}{place}"
        else:
            place_text = ""
        output_strings.append(f"""\
{BULLET_SYMBOL} <b>{event['time']}:</b>
{event['name']}{place_text}
{make_hyperlink(event['URL'], 'event link')}\n\n""")
    return output_strings


def make_strings_for_sachsen_punk(events: list[str]) -> list[str]:
    return [f"{BULLET_SYMBOL} {event}\n\n" for event in events]


def make_strings_for_songkick(events: list[dict]) -> list[str]:
    output_strings = []
    for event in events:
        output_strings.append(f'{BULLET_SYMBOL} ')
        if event['time']:
            output_strings.append(f"<b>{event['time']}:</b> ")
        output_strings.append(f"{event['name']}\n")
        if event['venue_URL']:
            venue_url = event["venue_URL"]
            venue_name = event["venue_name"]
            output_strings.append(f'{make_hyperlink(venue_url, venue_name, LOCATION_SYMBOL)}   ')
        event_url = event['URL']
        output_strings.append(f" {make_hyperlink(event_url, ' event link')}\n\n")
    return output_strings


def messages_generator():
    all_events = get_all_events()
    planlos_events, sachsenpunk_events, songkick_events = all_events.values()
    all_dates = list(set(chain(planlos_events, sachsenpunk_events, songkick_events)))
    all_dates.sort()
    events_dicts_handlers = {
        "🏴 Planlos Leipzig": (planlos_events, make_strings_for_planlos),
        "🤘 Sachsen Punk": (sachsenpunk_events, make_strings_for_sachsen_punk),
        "🎵 Songkick": (songkick_events, make_strings_for_songkick)
    }
    for date in all_dates:
        all_strings = []
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date_str = date_obj.strftime("%A, %B %d, %Y")
        all_strings.append(f"{CALENDAR_SYMBOL} {date_str}\n\n")

        for name, (events_dict, handler) in events_dicts_handlers.items():
            if date in events_dict:
                all_strings.append(f"<b>{name}</b>\n")
                all_strings += handler(events_dict[date])
                all_strings.append("\n")
        message_text = ''.join(all_strings)
        yield date, message_text


def create_files():
    dates_and_messages = messages_generator()
    for date, message in dates_and_messages:
        with open(f"tg_messages/{date}", 'w', encoding='UTF-8') as f:
            f.write(message)
