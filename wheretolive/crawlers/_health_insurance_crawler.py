from datetime import datetime
import requests
import codecs
from ..json_savers import FileJsonSaver
from .. import Switzerland
import json


# WebsiteCrawler
class HealthInsuranceCrawler():

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        self.locations = self.get_locations()
        self.health_insurance_rates_by_zip = dict()
        self.country = Switzerland(towns_by_zip_path='/home/repositories/wheretolive.ch/towns_by_zip.json')
        self.ranges = {
            "birth_year":  [x for x in range(datetime.now().year - 80, datetime.now().year)],
            "franchise": {
                "adult": [300, 500, 1000, 1500, 2000, 2500],
                "child": [0, 100, 200, 300, 400, 500, 600]  # Until and including 18 years
            },
            "zip_codes": self.country.zip_codes
        }
        self.base_url = "https://www.priminfo.admin.ch/de/praemien"

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
        url_suffix += '&models%5B%5D=base&models%5B%5D=ham&models%5B%5D=hmo&models%5B%5D=div'

        return self.base_url + url_suffix

    @property
    def urls(self):
        for zip_code in self.ranges['zip_codes']:
            location_id = self.locations[zip_code][0]
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

    def crawl(self):
        for url in self.urls:
            pass
