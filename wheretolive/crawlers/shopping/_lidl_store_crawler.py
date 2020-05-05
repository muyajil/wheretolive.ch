from ...utils.math import get_distance
from ...models import Town
import logging
import requests


class LidlStoreCrawler:
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

    def crawl(self):
        towns = self.db_session.query(Town)
        for town in towns:
            for store_location in self.store_locations:
                if (
                    get_distance(
                        town.lat,
                        town.long,
                        store_location["lat"],
                        store_location["long"],
                    )
                    < 5
                ):
                    town.lidl = True
                    break
            yield town
