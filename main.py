from datetime import datetime
import parser_planlos
import parser_sachsenpunk
import parser_songkick
from itertools import chain


planlos_events = parser_planlos.events
sachsenpunk_events = parser_sachsenpunk.events
songkick_events = parser_songkick.events

# all_dates = list(set(list(planlos_events) + list(sachsenpunk_events)))
all_dates = list(set(chain(planlos_events, sachsenpunk_events, songkick_events)))
all_dates.sort()
now = datetime.now().strftime("%A, %B %d, %Y %H:%M")
markdown_contents = f"# Eventkalender\n" \
     f"*Letzte Aktualisierung; {now}*\n"
for date in all_dates:
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    date_str = date_obj.strftime("%A, %B %d, %Y")
    markdown_contents += f"## {date_str} \n"

    if date in planlos_events:
        markdown_contents += f"### Planlos Leipzig: \n"
        events_list = planlos_events[date]
        for event in events_list:
            markdown_contents += f"- **{event['time']}:** {event['name']} | [[event link]]({event['URL']})\n"
        markdown_contents += "\n"

    if date in sachsenpunk_events:
        markdown_contents += "### Sachsen Punk:\n"
        for event in sachsenpunk_events[date]:
            markdown_contents += f"- {event}\n"
        markdown_contents += '\n'

    if date in songkick_events:
        markdown_contents += f"### Songkick: \n"
        events_list = songkick_events[date]
        for event in events_list:
            markdown_line = '- '
            if event['time']:
                markdown_line += f"**{event['time']}:** "
            markdown_line += event['name']
            if event['venue_name']:
                markdown_line += f" @ {event['venue_name']} "
            markdown_line += f"[[event link]]({event['URL']})"
            if event['venue_URL']:
                markdown_line += f" | [[venue link]]({event['venue_URL']})"
            markdown_contents += markdown_line + "\n"
        markdown_contents += '\n'

with open("events.md", 'w') as f:
    f.write(markdown_contents)
