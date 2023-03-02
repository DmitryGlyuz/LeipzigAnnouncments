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
markdown_contents = f"# Eventkalender\n" \
                    f"Auf dieser Seite finden Sie Ankündigungen für kommende Veranstaltungen in Leipzig von " \
                    f"den folgenden Websites:\n\n" \
                    f"- https://www.planlos-leipzig.org/ \n" \
                    f"- https://sachsenpunk.de/ \n" \
                    f"- https://www.songkick.com/ \n\n" \
                    f"*Letzte Aktualisierung; {now}*\n"


def handle_planlos(events: list[dict]) -> str:
    result = ''
    for event in events:
        result += f"- **{event['time']}:** {event['name']} | [[event link]]({event['URL']})\n"
    return result


def handle_sachsen_punk(events: list[str]) -> str:
    result = ''
    for event in events:
        result += f"- {event}\n"
    return result


def handle_songkick(events: list[dict]) -> str:
    result = ''
    for event in events:
        result += '- '
        if event['time']:
            result += f"**{event['time']}:** "
        result += event['name']
        if event['venue_name']:
            result += f" @ {event['venue_name']} "
        result += f"[[event link]]({event['URL']})"
        if event['venue_URL']:
            result += f" | [[venue link]]({event['venue_URL']})"
        result += "\n"
    return result


events_dicts_handlers = {
    "Planlos Leipzig": (planlos_events, handle_planlos),
    "Sachsen Punk": (sachsenpunk_events, handle_sachsen_punk),
    "Songkick": (songkick_events, handle_songkick)
}

for date in all_dates:
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    date_str = date_obj.strftime("%A, %B %d, %Y")
    markdown_contents += f"## {date_str} \n"

    for name, (events_dict, handler) in events_dicts_handlers.items():
        if date in events_dict:
            markdown_contents += f"### {name}: \n{handler(events_dict[date])}\n"

with open('events.md', 'w', encoding='UTF-8') as f:
    f.write(markdown_contents)
