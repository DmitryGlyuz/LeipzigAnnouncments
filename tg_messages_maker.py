#!/usr/bin/python
import json
from datetime import datetime
import events_combinator
from itertools import chain


all_events = events_combinator.get_events()


planlos_events = all_events["planlos"]
sachsenpunk_events = all_events["sachsenpunk"]
songkick_events = all_events["songkick"]

all_dates = list(set(chain(planlos_events, sachsenpunk_events, songkick_events)))
all_dates.sort()
now = datetime.now().strftime("%A, %B %d, %Y %H:%M")

CALENDAR_SYMBOL = '🗓'
BULLET_SYMBOL = '🔹'
URL_SYMBOL = '🔗'
LOCATION_SYMBOL = '📍 '


def make_hyperlink(url, resource_name, symbol=URL_SYMBOL):
    return f"{symbol}<a href=\"{url}\">{resource_name}</a>"


def make_strings_for_planlos(events: list[dict]) -> list[str]:
    output_strings = []
    for event in events:
        output_strings.append(f"""\
{BULLET_SYMBOL} <b>{event['time']}:</b>
{event['name']}
{make_hyperlink(event['URL'], 'event link')}\n\n""")
    return output_strings


def make_strings_for_sachsen_punk(events: list[str]) -> list[str]:
    output_strings = []
    for event in events:
        output_strings.append(f"{BULLET_SYMBOL} {event}\n\n")
    return output_strings


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

    with open(f"tg_messages/{date}", 'w', encoding='UTF-8') as f:
        text = ''.join(all_strings)
        f.write(text)
