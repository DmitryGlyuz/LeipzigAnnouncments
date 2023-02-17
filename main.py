from datetime import datetime
import parser_planlos
import parser_sachsenpunk


planlos_events = parser_planlos.events
sachsenpunk_events = parser_sachsenpunk.events

all_dates = list(set(tuple(planlos_events) + tuple(sachsenpunk_events)))
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
            markdown_contents += f"- **{event['time']}:** {event['name']} - [[link]]({event['URL']})\n"
        markdown_contents += "\n"

    if date in sachsenpunk_events:
        markdown_contents += "### Sachsen Punk:\n"
        for event in sachsenpunk_events[date]:
            markdown_contents += f"- {event}\n"
        markdown_contents += '\n'

with open("events.md", 'w') as f:
    f.write(markdown_contents)
