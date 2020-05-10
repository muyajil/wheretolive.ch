import logging

from ..models import SBBStation, SBBStopTime
from ..utils import BatchIterator


class SBBConnectionAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_true_station_id(self, stop_id):
        if stop_id not in self.parent_station_map:
            return stop_id
        return self.parent_station_map[stop_id]

    def init_parent_station_map(self):
        stations = self.db_session.query(
            SBBStation.id, SBBStation.parent_station
        ).filter(SBBStation.parent_station.isnot(None))

        self.parent_station_map = dict(stations)

    def aggregate(self):
        self.init_parent_station_map()
        trip_ids = self.db_session.query(SBBStopTime.trip_id).distinct()
        batch_iterator = BatchIterator(100, trip_ids)

        origin = None
        dest = None
        sequence_nr = 0

        for batch in batch_iterator.batches:
            batch = [x[0] for x in batch]
            stop_times = (
                self.db_session.query(SBBStopTime)
                .filter(SBBStopTime.trip_id.in_(batch))
                .order_by(SBBStopTime.trip_id, SBBStopTime.stop_sequence.asc())
            )

            for stop_time in stop_times:
                origin = dest
                dest = stop_time

                if origin is None or dest is None:
                    continue

                if origin.trip_id != dest.trip_id:
                    sequence_nr = 0
                    continue

                if origin.station_id == dest.station_id:
                    continue

                yield {
                    "trip_id": origin.trip_id,
                    "from_stop_id": self.get_true_station_id(origin.station_id),
                    "exact_from_stop_id": origin.station_id,
                    "departure_time": origin.departure_time,
                    "departs_next_day": origin.departs_next_day,
                    "to_stop_id": self.get_true_station_id(dest.station_id),
                    "exact_to_stop_id": dest.station_id,
                    "arrival_time": dest.arrival_time,
                    "arrives_next_day": dest.arrives_next_day,
                    "sequence_nr": sequence_nr,
                }

                sequence_nr += 1
