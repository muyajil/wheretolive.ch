from datetime import datetime
import requests
import codecs
from ..models import Town
from ..database import get_session
import json
from bs4 import BeautifulSoup
import logging
import time
from retry import retry


# WebsiteCrawler
class HealthInsuranceCrawler():

    def __init__(self):
        self.base_url = "https://www.priminfo.admin.ch/de/praemien"
        self.locations = self.get_locations()
        self.ranges = {
            "birth_year":  [x for x in range(datetime.now().year - 80, datetime.now().year)],
            "franchise": {
                "adult": [300, 500, 1000, 1500, 2000, 2500],
                "child": [0, 100, 200, 300, 400, 500, 600]  # Until and including 18 years
            }
        }
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_locations(self):
        url = self.base_url + '/locations'
        text = requests.get(url).text
        json_text = codecs.decode(codecs.encode(text[12:]))
        locations = json.loads(json_text)
        return locations

    def compose_url(self, location_id, birth_year, franchise):
        url_suffix = f'?location_id={location_id}'
        url_suffix += f'&yob%5B0%5D={birth_year}'
        url_suffix += f'&franchise%5B0%5D={franchise}'
        url_suffix += '&coverage%5B0%5D=1'
        url_suffix += '&models%5B%5D=base&models%5B%5D=ham&models%5B%5D=hmo&models%5B%5D=div&display=savings'

        return self.base_url + url_suffix

    @property
    def items(self):
        zip_codes = get_session().query(Town.zip_code).distinct()
        for zip_code, in zip_codes:
            location_id = self.locations['index'][str(zip_code)][0]
            for birth_year in self.ranges['birth_year']:
                if datetime.now().year - birth_year > 18:
                    franchise_range = self.ranges['franchise']['adult']
                else:
                    franchise_range = self.ranges['franchise']['child']
                for franchise in franchise_range:

                    yield {
                        'birth_year': birth_year,
                        'zip_code': zip_code,
                        'franchise': franchise,
                        'url': self.compose_url(location_id, birth_year, franchise)
                    }

    @retry(requests.exceptions.ConnectionError, delay=1, backoff=2)
    def get_rows_from_url(self, url):
        content = requests.get(url).text
        soup = BeautifulSoup(content, features="lxml")
        rows = soup.find_all("tr")
        return rows

    def crawl(self):
        for item in self.items:
            self.logger.debug(f'Requesting url: {item["url"]}')
            rows = self.get_rows_from_url(item['url'])
            for row in rows[3:]:
                texts = row.find_all("th")
                numbers = row.find_all("td")
                try:
                    yield {
                        'name': texts[0].a.string,
                        'url': texts[0].a['href'],
                        'model': texts[1].string.strip().replace('\xad', ''),
                        'rate': float(numbers[0].string),
                        'zip_code': item['zip_code'],
                        'franchise': item['franchise'],
                        'birth_year': item['birth_year']
                    }
                except (AttributeError, ValueError):
                    continue
