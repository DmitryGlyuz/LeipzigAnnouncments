import html5lib
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import requests
import locale
import re

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

URL = "https://www.planlos-leipzig.org/"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
entry_content = soup.find('div', {"class": "entry-content"})
events = defaultdict(list)
headers = entry_content.find_all('h3')


def add_spaces(string: str) -> str:
    result = string
    pattern = r'([a-zA-ZÄÃ¤ÖÜäöüß-]+)(\d{2}\.)|(\d{1,2}:\d{2})(\d{2}.\d{2}.\d{4})'
    if re.search(pattern, string):
        result = re.sub(pattern, r'\1\3 \2\4', string)
    return result


for header in headers:
    date_obj = datetime.strptime(header.text, "%a, %d. %B %Y")
    event_date = str(date_obj.date())
    day_table = header.find_next("table")
    events_rows = day_table.find_all("tr")
    for event_row in events_rows:
        event_cells = event_row.find_all("td")
        time_cell = event_cells[0]
        event_cell = event_cells[1]
        event = {
            "name": event_cell.text.strip(),
            "time": add_spaces(time_cell.text.strip()),
            "URL": event_cell.a.get("href")
        }
        events[event_date].append(event)
