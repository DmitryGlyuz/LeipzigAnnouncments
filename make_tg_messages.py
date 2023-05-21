#!/usr/bin/python
from datetime import datetime
import parser_planlos
import parser_sachsenpunk
import parser_songkick
from itertools import chain


planlos_events = parser_planlos.events
sachsenpunk_events = parser_sachsenpunk.events
songkick_events = parser_songkick.events

all_dates = list(set(chain(planlos_events, sachsenpunk_events, songkick_events)))
all_dates.sort()
now = datetime.now().strftime("%A, %B %d, %Y %H:%M")


def make_hyperlink(url, name):
    return f"🔗 <a href=\"{url}\">{name}</a>"


def handle_planlos(events: list[dict]) -> str:
    result = ''
    for event in events:
        result += f"🔹 <b>{event['time']}:</b>\n" \
                f"{event['name']}\n" \
                f"{make_hyperlink(event['URL'], 'event link')}\n\n"
    return result


def handle_sachsen_punk(events: list[str]) -> str:
    result = ''
    for event in events:
        result += f"🔹 {event}\n"
    return result


def handle_songkick(events: list[dict]) -> str:
    result = ''
    for event in events:
        result += '🔹 '
        if event['time']:
            result += f"<b>{event['time']}:</b> "
        result += event['name']
        if event['venue_name']:
            result += f" @ {event['venue_name']} "
        result += "\n" + make_hyperlink(event['URL'], "event link")
        # result += f"[[event link]]({event['URL']})"
        if event['venue_URL']:
            result += '  ' + make_hyperlink(event['venue_URL'], 'venue link') + '\n'
        result += "\n"
    return result


events_dicts_handlers = {
    "🏴 Planlos Leipzig": (planlos_events, handle_planlos),
    "🤘 Sachsen Punk": (sachsenpunk_events, handle_sachsen_punk),
    "🎵 Songkick": (songkick_events, handle_songkick)
}

for date in all_dates:
    text = ""
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    date_str = date_obj.strftime("%A, %B %d, %Y")
    text += f"🗓 {date_str}\n\n"

    for name, (events_dict, handler) in events_dicts_handlers.items():
        if date in events_dict:
            text += f"<b>{name}</b>\n{handler(events_dict[date])}\n"

    with open(f"tg_messages/{date}", 'w', encoding='UTF-8') as f:
        f.write(text)
