from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import requests
import re
import date_range_setter


URL = "https://sachsenpunk.de/dates/"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')

entry_content = soup.find('div', {"class": "entry-content"})
p_tags = entry_content.find_all('p')
events = defaultdict(list)
current_year = datetime.now().year
previous_month = 0
year = current_year

start_date = date_range_setter.start_date
final_date = date_range_setter.final_date

for p in p_tags:
    if re.match(r"\d+\.\d+\.", p.text):
        # Checking if there is announcement for the new year
        current_month = int(p.text[3:5])
        if previous_month and current_month < previous_month:
            year += 1
        previous_month = current_month

        date_str = p.text[:6] + str(year)
        current_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        if current_date < start_date:
            continue
        if current_date >= final_date:
            break

        events_date = str(current_date)
        current_events = p.find_next('p').text.split("\n")
        for event in current_events:
            if "Leipzig" in event:
                event_str = event.lstrip("Leipzig – ")
                events[events_date].append(event_str)
