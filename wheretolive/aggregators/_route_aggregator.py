import json
import logging
import math
from ..models import Town
from ..database import get_session


class RouteAggregator():

    def __init__(self, db_session):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_session = db_session
        self.routes = dict()

    def aggregate(self):
        source_towns = self.db_session.query(Town)
        for source_town in source_towns:
            target_towns = self.db_session.query(Town)
            for target_town in target_towns:
                distance = math.sqrt(
                    (target_town.x - source_town.x)**2 +
                    (target_town.y - source_town.y)**2
                )
                if distance == 0.0:
                    continue
                yield {
                    "source_town": source_town.zip_code,
                    "target_town": target_town.zip_code,
                    "distance": distance
                }
