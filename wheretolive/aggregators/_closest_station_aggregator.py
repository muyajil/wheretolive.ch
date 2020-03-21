import logging
from ..models import Town, SBBStation
from ..utils.math import get_distance
from datetime import datetime


class ClosestStationAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def aggregate(self):
        towns = self.db_session.query(Town)
        start = datetime.now()
        start_batch = datetime.now()
        for idx, town in enumerate(towns):
            closest_station_id = None
            closest_station_distance = None
            closest_train_station_id = None
            closest_train_station_distance = None
            stations = self.db_session.query(SBBStation).filter(
                SBBStation.station_type.in_(["train", "bus_tram"])
            )
            for station in stations:
                self.logger.debug(f"Checking town {town.name} against {station.name}")
                distance = get_distance(town.lat, town.long, station.lat, station.long)
                if station.station_type == "train":
                    if (
                        closest_train_station_distance is None
                        or distance < closest_train_station_distance
                    ):
                        closest_train_station_id = station.id
                        closest_train_station_distance = distance
                if (
                    closest_station_distance is None
                    or distance < closest_station_distance
                ):
                    closest_station_id = station.id
                    closest_station_distance = distance

            town.closest_station_id = closest_station_id
            town.closest_train_station_id = closest_train_station_id
            self.db_session.commit()

            if idx % 100 == 0 and idx > 0:
                now = datetime.now()
                logline = f"Finished towns: {idx}\t"
                logline += f"Batch Time elapsed: {now-start_batch}\t"
                logline += f"Total Time elapsed: {now-start}"
                start_batch = now
                self.logger.info(logline)
