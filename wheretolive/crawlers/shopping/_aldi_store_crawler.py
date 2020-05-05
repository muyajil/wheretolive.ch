from ...models import Town
import logging
import requests
from bs4 import BeautifulSoup
import time
from retry import retry


class AldiStoreCrawler:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__store_locations = None

    def init_store_locations(self):
        url = (
            "https://spatial.virtualearth.net/REST/v1/data/7d24986af4ad4548bb34f034b067d207/"
            + "Filialdaten-CH/Filialdaten-CH?"
            + "$filter=Adresstyp%20Eq%201&$top=5000&$format=json&$skip=0"
            + "&key=AijRQid01hkLFxKFV7vcRwCWv1oPyY5w6XIWJ-LdxHXxwfH7UUG46Z7dMknbj_rL"
        )

        stores = requests.get(url).json()["d"]["results"]

        self.__store_locations = list(
            map(lambda x: {"lat": x["Latitude"], "long": x["Longitude"]}, stores)
        )

    @property
    def store_locations(self):
        if self.__store_locations is None:
            self.init_store_locations()
        return self.__store_locations

    @retry(requests.exceptions.ConnectionError, delay=1, backoff=2, tries=5)
    def get_closest_store_distance(self, zip_code):
        time.sleep(1)
        r = requests.get(
            f"https://www.yellowmap.de/Presentation/AldiSued/de-CH/ResultList?SingleSlotGeo={zip_code}"
        ).json()
        soup = BeautifulSoup(r["Container"], features="lxml")
        try:
            return float(
                soup.find_all("span", {"class": "resultItem-Distance"})[0]
                .string.strip()
                .strip(" km")
            )
        except IndexError:
            return 1000

    def crawl(self):
        towns = self.db_session.query(Town)
        for town in towns:
            distance = self.get_closest_store_distance(town.zip_code)
            if distance <= 5:
                town.aldi = True
            yield town
