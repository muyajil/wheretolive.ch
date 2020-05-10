import logging

from ..models import Town
from ..utils.math import get_distance


class CommuteAggregator:
    def __init__(self, db_session):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_session = db_session
        self.routes = dict()

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
                    "distance": get_distance(
                        source_town.lat,
                        source_town.long,
                        target_town.lat,
                        target_town.long,
                    ),
                }
