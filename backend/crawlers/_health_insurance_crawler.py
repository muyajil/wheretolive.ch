import codecs
import json
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from retry import retry

from ..models import Town


# WebsiteCrawler
class HealthInsuranceCrawler:
    def __init__(self, db_session):
        self.base_url = "https://www.priminfo.admin.ch/de/praemien"
        self.locations = self.get_locations()
        self.ranges = {
            "age_groups": [(0, 18), (19, 25), (26, 80)],
            "franchise": {
                "adult": [300, 500, 1000, 1500, 2000, 2500],
                "child": [0, 100, 200, 300, 400, 500, 600],
            },
        }
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_session = db_session

    def get_locations(self):
        url = self.base_url + "/locations"
        text = requests.get(url).text
        json_text = codecs.decode(codecs.encode(text[12:]))
        locations = json.loads(json_text)
        return locations

    def compose_url(self, location_id, birth_year, franchise):
        url_suffix = f"?location_id={location_id}"
        url_suffix += f"&yob%5B0%5D={birth_year}"
        url_suffix += f"&franchise%5B0%5D={franchise}"
        url_suffix += "&coverage%5B0%5D=1"
        url_suffix += "&models%5B%5D=base&models%5B%5D=ham&models%5B%5D=hmo&models%5B%5D=div&display=savings"

        return self.base_url + url_suffix

    @property
    def items(self):
        zip_codes = self.db_session.query(Town.zip_code).distinct()
        for (zip_code,) in zip_codes:
            if str(zip_code) not in self.locations["index"]:
                self.logger.warn(f"Zip Code {zip_code} not found in locations")
                continue
            location_id = self.locations["index"][str(zip_code)][0]
            for min_age, max_age in self.ranges["age_groups"]:
                if min_age == 0:
                    franchise_range = self.ranges["franchise"]["child"]
                else:
                    franchise_range = self.ranges["franchise"]["adult"]
                for franchise in franchise_range:
                    min_birth_year = datetime.now().year - min_age
                    yield {
                        "min_birth_year": min_birth_year,
                        "max_birth_year": datetime.now().year - max_age,
                        "zip_code": zip_code,
                        "franchise": franchise,
                        "url": self.compose_url(location_id, min_birth_year, franchise),
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
            rows = self.get_rows_from_url(item["url"])
            for row in rows[3:]:
                texts = row.find_all("th")
                numbers = row.find_all("td")
                try:
                    yield {
                        "name": texts[0].a.string,
                        "url": texts[0].a["href"],
                        "model": texts[1].string.strip().replace("\xad", ""),
                        "rate": float(numbers[0].string),
                        "zip_code": item["zip_code"],
                        "franchise": item["franchise"],
                        "min_birth_year": item["min_birth_year"],
                        "max_birth_year": item["max_birth_year"],
                    }
                except (AttributeError, ValueError):
                    continue
