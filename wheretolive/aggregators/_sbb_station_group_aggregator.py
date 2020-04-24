import logging
from ..utils.math import get_distance
from ..models import SBBStation
import numpy as np


class SBBStationGroupAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def aggregate(self):
        relevant_stations = np.array(
            [
                (x.id, x.lat, x.long)
                for x in self.db_session.query(
                    SBBStation.id, SBBStation.lat, SBBStation.long
                ).filter(SBBStation.parent_station.is_(None))
            ],
            np.dtype("object,float,float"),
        )
        for source_station in relevant_stations:
            sbb_station_group = []
            target_stations = relevant_stations
            for target_station in target_stations:
                if source_station[0] == target_station[0]:
                    continue
                distance = get_distance(
                    source_station[1],
                    source_station[2],
                    target_station[1],
                    target_station[2],
                )

                if distance <= 0.1:
                    sbb_station_group.append(target_station[0])

            if len(sbb_station_group) > 0:
                yield {
                    "sbb_station_id": source_station[0],
                    "sbb_station_group": sbb_station_group,
                }
