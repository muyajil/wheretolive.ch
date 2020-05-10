import logging

import requests

from ...models import Town
from ...utils.math import get_distance


class CoopStoreCrawler:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__store_locations = None

    def init_store_locations(self):
        url = (
            "https://www.coop.ch/de/unternehmen/standorte-und-oeffnungszeiten.getvstlist.json?"
            + "lat=10&lng=10&start=1&end=5000&filterFormat=retail"
        )

        stores = requests.get(url).json()["vstList"]

        self.__store_locations = list(map(lambda x: x["geoKoordinaten"], stores))

    @property
    def store_locations(self):
        if self.__store_locations is None:
            self.init_store_locations()
        return self.__store_locations

    def crawl(self):
        towns = self.db_session.query(Town)
        for town in towns:
            for store_location in self.store_locations:
                if (
                    get_distance(
                        town.lat,
                        town.long,
                        store_location["latitude"],
                        store_location["longitude"],
                    )
                    <= 5
                ):
                    town.coop = True
                    break
            yield town
