import logging
import math
from ..models import Town


class RouteAggregator():

    def __init__(self, db_session):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_session = db_session
        self.routes = dict()

    def get_distance(self, source_town, target_town):
        s_lat = math.radians(source_town.lat)
        s_long = math.radians(source_town.long)
        t_lat = math.radians(target_town.lat)
        t_long = math.radians(target_town.long)
        a = ((1 - math.cos(t_lat-s_lat))/2
             + math.cos(s_lat) * math.cos(t_lat) * (1-math.cos(t_long-s_long))/2)
        return 12742 * math.asin(math.sqrt(a))

    def aggregate(self):
        source_towns = self.db_session.query(Town)
        for source_town in source_towns:
            target_towns = self.db_session.query(Town)
            for target_town in target_towns:
                if source_town.id == target_town.id:
                    continue

                yield {
                    "source_town_id": source_town.id,
                    "target_town_id": target_town.id,
                    "distance": self.get_distance(source_town, target_town)
                }
