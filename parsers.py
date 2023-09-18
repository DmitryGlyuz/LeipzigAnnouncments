from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from collections import defaultdict
from config_handlers import load_config
import requests
import locale
import re


config = load_config()

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

PLANLOS_URL = "https://www.planlos-leipzig.org/"
SACHSENPUNK_URL = "https://sachsenpunk.de/dates/"
SONGKICK_URL = "https://www.songkick.com/metro-areas/28528-germany-leipzig"

start_date_in_config = config["start_date"]
days_limit = config["days_limit"]

start_date = (datetime.strptime(start_date_in_config, "%Y-%m-%d") if start_date_in_config else datetime.now()).date()
final_date = start_date + timedelta(days=days_limit)


def add_spaces(string: str) -> str:
    result = string
    pattern = r'([a-zA-ZÄÃ¤ÖÜäöüß-]+)(\d{2}\.)|(\d{1,2}:\d{2})(\d{2}.\d{2}.\d{4})'
    if re.search(pattern, string):
        result = re.sub(pattern, r'\1\3 \2\4', string)
    return result


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def get_planlos_events():
    soup = get_soup(PLANLOS_URL)
    entry_content = soup.find('div', {"class": "entry-content"})
    headers = entry_content.find_all('h3')
    events = defaultdict(list)

    for header in headers:
        current_date = datetime.strptime(header.text, "%a, %d. %B %Y").date()
        if current_date < start_date:
            continue
        if current_date >= final_date:
            break

        event_date = str(current_date)
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
    return events


def get_sachsenpunk_events():
    soup = get_soup(SACHSENPUNK_URL)
    entry_content = soup.find('div', {"class": "entry-content"})
    p_tags = entry_content.find_all('p')
    events = defaultdict(list)
    current_year = datetime.now().year
    previous_month = 0
    year = current_year

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
    return events


def get_songkick_events():
    soup = get_soup(SONGKICK_URL)
    event_elements = soup.find_all('li', {"class": "event-listings-element"})
    events = defaultdict(list)

    def get_full_url(ending: str) -> str:
        return "https://www.songkick.com" + ending

    for event_element in event_elements:
        event = {}
        time_tag = event_element.find("time")
        datetime_property = time_tag['datetime']
        if len(datetime_property) == 10:
            current_datetime = datetime.strptime(datetime_property, "%Y-%m-%d")
            time_str = None
        else:
            current_datetime = datetime.strptime(datetime_property, "%Y-%m-%dT%H:%M:%S%z")
            time_str = current_datetime.strftime("%H:%M")

        current_date = current_datetime.date()
        if current_date < start_date:
            continue
        if current_date >= final_date:
            break

        date_str = str(current_datetime.date())
        events[date_str].append(event)
        event['time'] = time_str

        div_artist = event_element.find('div', {"class": "artists-venue-location-wrapper"})
        event_link = div_artist.find('a', {"class": "event-link"})
        venue_link = div_artist.find('a', {"class": "venue-link"})
        event_name = div_artist.strong.text
        event_url = get_full_url(event_link['href'])
        event['name'] = event_name
        event['URL'] = event_url
        venue_name = None
        venue_url = None

        if venue_link:
            venue_url = get_full_url(venue_link['href'])
            venue_name = venue_link.text
        event['venue_name'] = venue_name
        event['venue_URL'] = venue_url
    return events