import requests
import re
import logging
from ..models import Town
from ..database import get_session
from bs4 import BeautifulSoup
import json
from datetime import datetime
from retry import retry


class AccomodationsCrawler():

    def __init__(self):
        self.base_url = "https://www.comparis.ch/immobilien/result/list"
        self.logger = logging.getLogger(self.__class__.__name__)

    @retry(requests.exceptions.ConnectionError, delay=1, backoff=2)
    def get_max_pages(self, url):
        content = requests.get(url).text
        pagination_items = re.findall(r"pagination-item-[0-9]+", content)
        if len(pagination_items) == 0:
            return None
        last_page = max(map(lambda x: int(x.split('-')[-1]), pagination_items))
        return last_page

    def compose_url(self, deal_type, zip_code, page=0):
        url_suffix = "?requestobject=%7B"
        url_suffix += f"%22DealType%22%3A{deal_type}%2C"
        url_suffix += "%22SiteId%22%3A0%2C"
        url_suffix += "%22RootPropertyTypes%22%3A%5B%5D%2C"
        url_suffix += "%22PropertyTypes%22%3A%5B%5D%2C"
        url_suffix += "%22RoomsFrom%22%3Anull%2C"
        url_suffix += "%22RoomsTo%22%3Anull%2C"
        url_suffix += "%22FloorSearchType%22%3A0%2C"
        url_suffix += "%22LivingSpaceFrom%22%3Anull%2C"
        url_suffix += "%22LivingSpaceTo%22%3Anull%2C"
        url_suffix += "%22PriceFrom%22%3Anull%2C"
        url_suffix += "%22PriceTo%22%3Anull%2C"
        url_suffix += "%22ComparisPointsMin%22%3A0%2C"
        url_suffix += "%22AdAgeMax%22%3A0%2C"
        url_suffix += "%22AdAgeInHoursMax%22%3Anull%2C"
        url_suffix += "%22Keyword%22%3A%22%22%2C"
        url_suffix += "%22WithImagesOnly%22%3Anull%2C"
        url_suffix += "%22WithPointsOnly%22%3Anull%2C"
        url_suffix += "%22Radius%22%3Anull%2C"
        url_suffix += "%22MinAvailableDate%22%3A%221753-01-01T00%3A00%3A00%22%2C"
        url_suffix += "%22MinChangeDate%22%3A%221753-01-01T00%3A00%3A00%22%2C"
        url_suffix += f"%22LocationSearchString%22%3A%22{zip_code}%22%2C"
        url_suffix += "%22Sort%22%3A%223%22%2C" # Sort by newest
        url_suffix += "%22HasBalcony%22%3Afalse%2C"
        url_suffix += "%22HasTerrace%22%3Afalse%2C"
        url_suffix += "%22HasFireplace%22%3Afalse%2C"
        url_suffix += "%22HasDishwasher%22%3Afalse%2C"
        url_suffix += "%22HasWashingMachine%22%3Afalse%2C"
        url_suffix += "%22HasLift%22%3Afalse%2C"
        url_suffix += "%22HasParking%22%3Afalse%2C"
        url_suffix += "%22PetsAllowed%22%3Afalse%2C"
        url_suffix += "%22MinergieCertified%22%3Afalse%2C"
        url_suffix += "%22WheelchairAccessible%22%3Afalse%2C"
        url_suffix += "%22LowerLeftLatitude%22%3Anull%2C"
        url_suffix += "%22LowerLeftLongitude%22%3Anull%2C"
        url_suffix += "%22UpperRightLatitude%22%3Anull%2C"
        url_suffix += "%22UpperRightLongitude%22%3Anull"
        url_suffix += f"%7D&page={page}"

        return self.base_url + url_suffix

    @property
    def items(self):
        zip_codes = get_session().query(Town.zip_code).distinct()
        for deal_type in [20, 10]:
            for zip_code, in zip_codes:
                url = self.compose_url(deal_type, zip_code)
                last_page = self.get_max_pages(url)
                if last_page is None:
                    continue
                for page in range(last_page + 1):
                    yield {
                        "zip_code": zip_code,
                        "page": page,
                        "url": self.compose_url(deal_type, zip_code, page)
                    }

    @retry(requests.exceptions.ConnectionError, delay=1, backoff=2)
    def get_listings_from_url(self, url):
        content = requests.get(url).text
        soup = BeautifulSoup(content, features='lxml')
        json_text = soup.find_all("script", id="__NEXT_DATA__")[0].string
        return json.loads(json_text)['props']['pageProps']['initialResultData']['resultItems']

    def get_address(self, listing):
        try:
            if len(listing['Address']) == 0:
                return None, None, None
            if len(listing['Address']) == 1:
                _, town_name = listing['Address'][0].split(' ', 1)
                return town_name, None, None
            elif len(listing['Address']) == 2:
                try:
                    splits = listing['Address'][0].split(' ')
                    house_number = int(splits[-1])
                    street_name = ' '.join(splits[:-1])
                except ValueError:
                    house_number = None
                    street_name = listing['Address'][0]

                _, town_name = listing['Address'][1].split(' ', 1)
                return town_name, street_name, house_number
        except:
            self.logger.error(f'Problem with parsing address of listing {listing["AdId"]}')
            return None, None, None

    def get_rooms(self, listing):
        if len(listing['EssentialInformation']) == 0:
            return None
        try:
            if 'zimmer' in listing['EssentialInformation'][0].lower():
                rooms = float(listing['EssentialInformation'][0].split(' ')[0])
            else:
                rooms = None
            return rooms
        except:
            self.logger.error(f'Problem with parsing rooms of listing {listing["AdId"]}')
            return None

    def get_image_url(self, listing):
        if '//' == listing['ImageUrl'][:2]:
            image_url = 'https:' + listing['ImageUrl']
        elif '/immobilien' == listing['ImageUrl'][:11]:
            image_url = 'https://www.comparis.ch' + listing['ImageUrl']
        else:
            image_url = listing['ImageUrl']

        return image_url

    def crawl(self):
        for item in self.items:
            self.logger.debug(f'Requesting url: {item["url"]}')
            listings = self.get_listings_from_url(item['url'])
            for listing in listings:
                town_name, street_name, house_number = self.get_address(listing)

                yield {
                    "comparis_id": listing['AdId'],
                    "zip_code": item['zip_code'],
                    "town_name": town_name,
                    "street_name": street_name,
                    "house_number": house_number,
                    "price": listing['PriceValue'],
                    "area": listing['AreaValue'],
                    "is_rent": listing['DealType'] == 10,
                    "image_url": self.get_image_url(listing),
                    "found_date": datetime.now(),
                    "property_type_id": listing['PropertyTypeId'],
                    "property_type": listing['PropertyTypeText'],
                    "rooms": self.get_rooms(listing)
                }
