import logging
from ..models import (
    SBBConnection,
    Town,
    SBBTransfer,
    Commute,
    SBBStation,
    SBBCalendar,
    SBBTrip,
)
from datetime import time, date, timedelta, datetime


class CommuteTimeAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.in_connection = dict()
        self.earliest_arrival = dict()
        self.__connections_list = []

    def init_transfer_map(self):
        self.transfer_map = dict()
        transfers = self.db_session.query(SBBTransfer)
        for transfer in transfers:
            if transfer.from_stop_id not in self.transfer_map:
                self.transfer_map[transfer.from_stop_id] = dict()
            self.transfer_map[transfer.from_stop_id][
                transfer.to_stop_id
            ] = transfer.min_transfer_time

    def get_true_stop_id(self, stop_id, parent_stop_id="missing"):
        if parent_stop_id == "missing":
            parent_stop_id = (
                self.db_session.query(SBBStation).get(stop_id).parent_station
            )
        return parent_stop_id if parent_stop_id else stop_id

    def is_transfer_origin_possible(self, connection):
        true_stop_id = self.get_true_stop_id(
            connection.from_stop_id, connection.from_stop_parent_id
        )

        if true_stop_id not in self.earliest_arrival:
            # Never arrived at this station
            return False
        else:
            if true_stop_id not in self.in_connection:
                # This happens in the case of the first connection leaving at the source station
                return True
            prev_connection = self.in_connection[true_stop_id]
            if (
                prev_connection.to_stop_id not in self.transfer_map
                or connection.from_stop_id
                not in self.transfer_map[prev_connection.to_stop_id]
            ):
                # No transfer condition on these two connections
                if prev_connection.trip_id == connection.trip_id:
                    return prev_connection.arrival_time <= connection.departure_time
                return prev_connection.arrival_time < connection.departure_time

            else:
                # Transfer condition must be satisfied
                min_transfer_time = self.transfer_map[prev_connection.to_stop_id][
                    connection.from_stop_id
                ]
                return (
                    datetime.combine(date.min, prev_connection.arrival_time)
                    + timedelta(seconds=min_transfer_time)
                ).time() <= connection.departure_time

    def is_transfer_dest_possible(self, connection):
        true_stop_id = self.get_true_stop_id(
            connection.to_stop_id, connection.to_stop_parent_id
        )

        if true_stop_id not in self.earliest_arrival:
            # First connection that leads to this stop
            return True
        else:
            # We choose this connection if we arrive earlier
            return connection.arrival_time < self.earliest_arrival[true_stop_id]

    def init_connections(self):
        sbb_connections = (
            self.db_session.query(SBBConnection)
            .join(SBBTrip, SBBTrip.trip_id == SBBConnection.trip_id)
            .join(SBBCalendar, SBBCalendar.service_id == SBBTrip.service_id)
            .filter(SBBConnection.departs_next_day.is_(False))
            .filter(SBBConnection.arrival_time <= time(12, 0, 0))
            .filter(SBBConnection.departure_time >= time(6, 0, 0))
            .filter(SBBCalendar.monday.is_(True))
            .order_by(SBBConnection.departure_time, SBBConnection.trip_id)
            .yield_per(10000)
        )

        self.__connections_list = [x for x in sbb_connections]

    @property
    def connections(self):
        if not self.__connections_list:
            self.init_connections()
        return self.__connections_list

    def compute_csa(self, arrival_stop_id):
        # For the commute we are not interested in connections arriving after lunchtime
        earliest = time(12, 0, 0)

        for c in self.connections:

            if self.is_transfer_origin_possible(c) and self.is_transfer_dest_possible(
                c
            ):
                true_to_stop_id = self.get_true_stop_id(
                    c.to_stop_id, c.to_stop_parent_id
                )

                self.earliest_arrival[true_to_stop_id] = c.arrival_time
                self.in_connection[true_to_stop_id] = c

                # Arrival stop id should always be a parent stop id
                if (
                    c.to_stop_id == arrival_stop_id
                    or c.to_stop_parent_id == arrival_stop_id
                ):
                    earliest = min(earliest, c.arrival_time)

            elif c.arrival_time > earliest:
                return

    def get_route(self, departure_stop_id, arrival_stop_id):
        route = []
        if arrival_stop_id not in self.in_connection:
            return route

        last_true_stop_id = arrival_stop_id

        while last_true_stop_id != departure_stop_id:
            last_connection = self.in_connection[last_true_stop_id]
            route.append(last_connection)
            last_true_stop_id = self.get_true_stop_id(
                last_connection.from_stop_id, last_connection.from_stop_parent_id
            )

        return route

    def compute_journey(self, source_town, target_town, departure_time, station_type):
        self.in_connection = dict()
        self.earliest_arrival = dict()

        if station_type == "closest":
            true_source_stop_id = self.get_true_stop_id(source_town.closest_station_id)
            true_target_stop_id = self.get_true_stop_id(target_town.closest_station_id)
        else:
            true_source_stop_id = self.get_true_stop_id(
                source_town.closest_train_station_id
            )
            true_target_stop_id = self.get_true_stop_id(
                target_town.closest_train_station_id
            )
        if true_source_stop_id == true_target_stop_id:
            return {"time": 0.0, "changes": 0}
        self.earliest_arrival[true_source_stop_id] = departure_time
        self.compute_csa(true_target_stop_id)
        route = self.get_route(true_source_stop_id, true_target_stop_id)
        if len(route) == 0:
            return {"time": None, "changes": None}
        trip_ids = map(lambda x: x.trip_id, route)
        return {
            "time": (
                datetime.combine(date.min, route[0].arrival_time)
                - datetime.combine(date.min, route[-1].departure_time)
            ).seconds,
            "changes": len(set(trip_ids)) - 1,
        }

    def aggregate(self):
        self.init_transfer_map()
        commutes = (
            self.db_session.query(Commute)
            .order_by(Commute.source_town_id)
            .yield_per(100000)
        )
        for commute in commutes:
            source_town = self.db_session.query(Town).get(commute.source_town_id)
            target_town = self.db_session.query(Town).get(commute.target_town_id)
            for station_type in ["closest", "closest_train"]:
                journey = self.compute_journey(
                    source_town, target_town, time(6, 0, 0), station_type,
                )
                if station_type == "closest":
                    commute.commute_closest_station_time = journey["time"]
                    commute.commute_closest_station_changes = journey["changes"]
                else:
                    commute.commute_closest_train_station_time = journey["time"]
                    commute.commute_closest_train_station_changes = journey["changes"]

            yield commute
