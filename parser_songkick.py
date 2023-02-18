from bs4 import BeautifulSoup
from datetime import datetime
import requests
import locale
from collections import defaultdict

locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

URL = "https://www.songkick.com/metro-areas/28528-germany-leipzig"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
event_elements = soup.find_all('li', {"class": "event-listings-element"})

events = defaultdict(list)


def get_full_url(ending: str) -> str:
    return "https://www.songkick.com" + ending


for event_element in event_elements:
    event = {}
    time_tag = event_element.find("time")
    datetime_property = time_tag['datetime']
    if len(datetime_property) == 10:
        datetime_obj = datetime.strptime(datetime_property, "%Y-%m-%d")
        time_str = None
    else:
        datetime_obj = datetime.strptime(datetime_property, "%Y-%m-%dT%H:%M:%S%z")
        time_str = datetime_obj.strftime("%H:%M")
    date_str = str(datetime_obj.date())
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

