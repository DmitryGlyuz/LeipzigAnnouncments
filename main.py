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
markdown_contents = f"""# Eventkalender
Auf dieser Seite finden Sie Ankündigungen für kommende Veranstaltungen in Leipzig von den folgenden Websites:
- https://www.planlos-leipzig.org/
- https://sachsenpunk.de/
- https://www.songkick.com/

*Letzte Aktualisierung; {now}*
"""

def handle_planlos(_date: str) -> str:
    result = f"### Planlos Leipzig: \n"
    events_list = planlos_events[_date]
    for event in events_list:
        result += f"- **{event['time']}:** {event['name']} | [[event link]]({event['URL']})\n"
    return result


def handle_sachsen_punk(_date: str) -> str:
    result = "### Sachsen Punk:\n"
    for event in sachsenpunk_events[_date]:
        result += f"- {event}\n"
    return result


def handle_songkick(_date: str) -> str:
    result = f"### Songkick: \n"
    events_list = songkick_events[_date]
    for event in events_list:
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


def add_daily_content(_date: str, events_collection, function):
    return function(_date) + "\n" if _date in events_collection else ''


for date in all_dates:
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    date_str = date_obj.strftime("%A, %B %d, %Y")
    markdown_contents += f"## {date_str} \n"

    markdown_contents += add_daily_content(date, planlos_events, handle_planlos)
    markdown_contents += add_daily_content(date, sachsenpunk_events, handle_sachsen_punk)
    markdown_contents += add_daily_content(date, songkick_events, handle_songkick)

with open('events.md', 'w', encoding='UTF-8') as f:
    f.write(markdown_contents)
