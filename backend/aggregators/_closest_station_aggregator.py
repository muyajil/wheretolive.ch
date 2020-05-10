import logging

from sqlalchemy import func
from sqlalchemy.sql import label

from ..models import SBBStation, Town
from ..utils.math import get_distance


class ClosestStationAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def aggregate(self):
        towns = self.db_session.query(Town)
        for idx, town in enumerate(towns):
            closest_station = dict()
            closest_train_station = dict()

            num_platforms = (
                self.db_session.query(
                    SBBStation.parent_station,
                    label("num_platforms", func.count(SBBStation.id)),
                ).group_by(SBBStation.parent_station)
            ).subquery()

            stations = (
                self.db_session.query(
                    SBBStation.id,
                    SBBStation.name,
                    SBBStation.lat,
                    SBBStation.long,
                    SBBStation.station_type,
                    num_platforms.c.num_platforms,
                )
                .outerjoin(
                    num_platforms, SBBStation.id == num_platforms.c.parent_station
                )
                .filter(SBBStation.station_type.in_(["train", "bus_tram"]))
            )

            for idx, station in enumerate(stations):
                self.logger.debug(f"Checking town {town.name} against {station.name}")
                distance = get_distance(town.lat, town.long, station.lat, station.long)
                if station.station_type == "train":
                    if (
                        "distance" not in closest_train_station
                        # new station is much closer
                        or (closest_train_station["distance"] - distance > 1.0)
                        # new station is a bit closer, and not significantly less tracks
                        or (
                            0.0 <= closest_train_station["distance"] - distance <= 1.0
                            and closest_train_station["num_platforms"]
                            <= station.num_platforms * 1.5
                        )
                        # new station is a bit farther, but has significantly more tracks
                        or (
                            0.0 <= distance - closest_train_station["distance"] <= 1.0
                            and closest_train_station["num_platforms"] * 1.5
                            < station.num_platforms
                        )
                    ):
                        closest_train_station["id"] = station.id
                        closest_train_station["distance"] = distance
                        closest_train_station["num_platforms"] = station.num_platforms
                if (
                    "distance" not in closest_station
                    or distance < closest_station["distance"]
                ):
                    closest_station["id"] = station.id
                    closest_station["distance"] = distance

            self.logger.debug(f"Checked {idx} stations for town {town.name}")

            town.closest_station_id = closest_station["id"]
            town.closest_train_station_id = closest_train_station["id"]
            yield town
