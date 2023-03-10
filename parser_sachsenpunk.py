from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import requests
import re


URL = "https://sachsenpunk.de/dates/"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')

entry_content = soup.find('div', {"class" : "entry-content"})
p_tags = entry_content.find_all('p')
events = defaultdict(list)
current_year = datetime.now().year

for p in p_tags:
    if re.match(r"\d+\.\d+\.", p.text):
        date_str = p.text[:6] + str(current_year)
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        events_date = str(date_obj.date())
        current_events = p.find_next('p').text.split("\n")
        for event in current_events:
            if "Leipzig" in event:
                event_str = event.lstrip("Leipzig – ")
                events[events_date].append(event_str)
