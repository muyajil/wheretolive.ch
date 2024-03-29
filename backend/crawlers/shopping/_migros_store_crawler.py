import logging

import requests

from ...models import Town
from ...utils.math import get_distance


class MigrosStoreCrawler:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__store_locations = None

    def init_store_locations(self):
        url = (
            "https://web-api.migros.ch/widgets/stores?"
            + "key=8ApUDaqeNER3Mest&limit=5000"
            + "&filters%5Bmarkets%5D%5B0%5D%5B%5D=super"
            + "&filters%5Bmarkets%5D%5B0%5D%5B%5D=voi"
            + "&filters%5Bmarkets%5D%5B0%5D%5B%5D=mp"
        )

        stores = requests.get(
            url, headers={"Origin": "https://filialen.migros.ch"},
        ).json()["stores"]

        self.__store_locations = list(map(lambda x: x["location"]["geo"], stores))

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
                        store_location["lat"],
                        store_location["lon"],
                    )
                    <= 5
                ):
                    town.migros = True
                    break
            yield town
