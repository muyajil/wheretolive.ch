import logging
from ..models import SBBTransfer, SBBStationGroup
from datetime import time, date, timedelta, datetime
import pandas as pd
import os
import psycopg2 as pg
import numpy as np


class CommuteTimeAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.in_connection = dict()
        self.earliest_arrival = dict()
        self.computed_commutes = dict()
        self.__connections_df = None
        self.db_conn = pg.connect(os.environ.get("DB_CONN"))

    def init_transfer_map(self):
        self.transfer_map = dict()
        transfers = self.db_session.query(SBBTransfer)
        for transfer in transfers:
            if transfer.from_stop_id not in self.transfer_map:
                self.transfer_map[transfer.from_stop_id] = dict()
            self.transfer_map[transfer.from_stop_id][
                transfer.to_stop_id
            ] = transfer.min_transfer_time
        self.logger.info("Transfer Map initialized")

    def init_sbb_station_groups(self):
        self.station_groups = dict()
        station_groups = self.db_session.query(SBBStationGroup)
        for station_group in station_groups:
            self.station_groups[station_group.sbb_station_id] = list(
                zip(station_group.sbb_station_group, station_group.walking_times)
            )

        self.logger.info("SBB Station Groups initialized")

    def is_transfer_origin_possible(self, connection):
        true_stop_id = self.get_conn_attr(connection, "from_stop_id")

        if true_stop_id not in self.earliest_arrival:
            # Never arrived at this station
            return False
        else:
            if true_stop_id not in self.in_connection:
                # This happens in the case of the first connection leaving at the source station
                return True
            prev_connection = self.in_connection[true_stop_id]
            if (
                self.get_conn_attr(prev_connection, "exact_to_stop_id")
                not in self.transfer_map
                or self.get_conn_attr(connection, "exact_from_stop_id")
                not in self.transfer_map[
                    self.get_conn_attr(prev_connection, "exact_to_stop_id")
                ]
            ):
                # No transfer condition on these two connections
                return self.get_conn_attr(
                    prev_connection, "arrival_time"
                ) <= self.get_conn_attr(connection, "departure_time")

            else:
                # Transfer condition must be satisfied
                min_transfer_time = self.transfer_map[
                    self.get_conn_attr(prev_connection, "exact_to_stop_id")
                ][self.get_conn_attr(connection, "exact_from_stop_id")]
                return (
                    datetime.combine(
                        date.min, self.get_conn_attr(prev_connection, "arrival_time")
                    )
                    + timedelta(seconds=min_transfer_time)
                ).time() <= self.get_conn_attr(connection, "departure_time")

    def is_transfer_dest_possible(self, connection):
        true_stop_id = self.get_conn_attr(connection, "to_stop_id")

        if true_stop_id not in self.earliest_arrival:
            # First connection that leads to this stop
            return True
        else:
            # We choose this connection if we arrive earlier
            return (
                self.get_conn_attr(connection, "arrival_time")
                < self.earliest_arrival[true_stop_id]
            )

    def init_connections(self):
        sql = """
            select
                sbb_connection.from_stop_id,
                sbb_connection.exact_from_stop_id,
                sbb_connection.to_stop_id,
                sbb_connection.exact_to_stop_id,
                sbb_connection.departure_time,
                sbb_connection.arrival_time,
                sbb_connection.trip_id
            from sbb_connection
            join sbb_trip on sbb_trip.trip_id = sbb_connection.trip_id
            join sbb_calendar on sbb_calendar.service_id = sbb_trip.service_id
            where
                not sbb_connection.departs_next_day and
                not sbb_connection.arrives_next_day and
                sbb_calendar.monday
            order by sbb_connection.departure_time, sbb_connection.trip_id
        """

        self.__connections_df = pd.read_sql(sql, self.db_conn)
        self.logger.info("Connections initialized")

    @property
    def connections(self):
        if self.__connections_df is None:
            self.init_connections()
        return self.__connections_df

    def load_commutes(self):
        sql_1 = """
            select
            commute.id,
            s_sbb_station.id as source_station_id,
            t_sbb_station.id as target_station_id
        from commute
        join town as s_town on s_town.id = source_town_id
        join town as t_town on t_town.id = target_town_id
        join sbb_station as s_sbb_station on s_sbb_station.id = s_town.closest_station_id
        join sbb_station as t_sbb_station on t_sbb_station.id = t_town.closest_station_id
        """

        sql_2 = """
            select
            commute.id,
            s_sbb_station.id as source_station_id,
            t_sbb_station.id as target_station_id,
        from commute
        join town as s_town on s_town.id = source_town_id
        join town as t_town on t_town.id = target_town_id
        join sbb_station as s_sbb_station on s_sbb_station.id = s_town.closest_train_station_id
        join sbb_station as t_sbb_station on t_sbb_station.id = t_town.closest_train_station_id
        """

        sqls = [sql_1, sql_2]
        commute_types = ["closest_station", "closest_train"]

        for sql, commute_type in zip(sqls, commute_types):
            cursor = self.db_conn.cursor()
            cursor.execute(sql)
            for c in cursor:
                yield c + (commute_type,)
            cursor.close()

    @property
    def train_commutes(self):
        for commute in self.load_commutes():

            yield {
                "commute_id": commute[0],
                "source": commute[1],
                "target": commute[2],
                "type": commute[3],
            }

    def compute_csa(self, arrival_stop_id):
        # For the commute we are not interested in connections arriving after lunchtime
        earliest = time(23, 59, 59)

        for c in self.connections.values:

            if self.is_transfer_origin_possible(c) and self.is_transfer_dest_possible(
                c
            ):
                true_to_stop_id = self.get_conn_attr(c, "to_stop_id")

                self.earliest_arrival[true_to_stop_id] = self.get_conn_attr(
                    c, "arrival_time"
                )
                self.in_connection[true_to_stop_id] = c

                if true_to_stop_id in self.station_groups:
                    for stop_id, walking_time in self.station_groups[true_to_stop_id]:
                        potential_arrival_time = (
                            datetime.combine(
                                date.min, self.get_conn_attr(c, "arrival_time")
                            )
                            + timedelta(seconds=walking_time)
                        ).time()
                        if (
                            stop_id not in self.earliest_arrival
                            or self.earliest_arrival[stop_id] > potential_arrival_time
                        ):
                            self.earliest_arrival[stop_id] = potential_arrival_time
                            self.in_connection[stop_id] = np.array(
                                (
                                    true_to_stop_id,
                                    true_to_stop_id,
                                    stop_id,
                                    stop_id,
                                    self.get_conn_attr(c, "arrival_time"),
                                    self.earliest_arrival[stop_id],
                                    None,
                                )
                            )

                # Arrival stop id should always be a parent stop id
                if arrival_stop_id in self.earliest_arrival:
                    earliest = self.earliest_arrival[arrival_stop_id]

            elif self.get_conn_attr(c, "arrival_time") > earliest:
                return

    def get_route(self, departure_stop_id, arrival_stop_id):
        route = []
        if arrival_stop_id not in self.in_connection:
            return route

        last_true_stop_id = arrival_stop_id

        possible_departure_stop_ids = [departure_stop_id]

        if departure_stop_id in self.station_groups:
            possible_departure_stop_ids += self.station_groups[departure_stop_id]

        while last_true_stop_id not in possible_departure_stop_ids:
            last_connection = self.in_connection[last_true_stop_id]
            route.append(last_connection)
            last_true_stop_id = self.get_conn_attr(last_connection, "from_stop_id")

        return route

    def compute_journey(self, train_commute):
        self.in_connection = dict()
        self.earliest_arrival = dict()

        if train_commute["source"] == train_commute["target"]:
            return {"time": 0, "changes": 0}
        self.earliest_arrival[train_commute["source"]] = time(6, 0, 0)

        # We could also start the journey from a close station to the start station
        if train_commute["source"] in self.station_groups:
            for stop_id, walking_time in self.station_groups[train_commute["source"]]:
                self.earliest_arrival[stop_id] = (
                    datetime.combine(date.min, time(6, 0, 0))
                    + timedelta(seconds=walking_time)
                ).time()

        self.compute_csa(train_commute["target"])
        route = self.get_route(train_commute["source"], train_commute["target"])
        if len(route) == 0:
            return {"time": None, "changes": None}
        trip_ids = filter(
            lambda x: x is not None,
            map(lambda x: self.get_conn_attr(x, "trip_id"), route),
        )
        return {
            "time": (
                datetime.combine(date.min, self.get_conn_attr(route[0], "arrival_time"))
                - datetime.combine(
                    date.min, self.get_conn_attr(route[-1], "departure_time")
                )
            ).seconds,
            "changes": len(set(trip_ids)) - 1,
        }

    def get_conn_attr(self, connection, attr):
        if attr == "from_stop_id":
            return connection[0]
        if attr == "exact_from_stop_id":
            return connection[1]
        if attr == "to_stop_id":
            return connection[2]
        if attr == "exact_to_stop_id":
            return connection[3]
        if attr == "departure_time":
            return connection[4]
        if attr == "arrival_time":
            return connection[5]
        if attr == "trip_id":
            return connection[6]
        raise ValueError(f"Attribute {attr} not supported!")

    def aggregate(self):
        self.init_transfer_map()
        self.init_sbb_station_groups()
        for train_commute in self.train_commutes:

            if train_commute["source"] in self.computed_commutes:
                if (
                    train_commute["target"]
                    in self.computed_commutes[train_commute["source"]]
                ):
                    yield {
                        "commute_id": train_commute["commute_id"],
                        "commute_type": train_commute["type"],
                        "time": self.computed_commutes[train_commute["source"]][
                            train_commute["target"]
                        ]["time"],
                        "changes": self.computed_commutes[train_commute["source"]][
                            train_commute["target"]
                        ]["changes"],
                    }
                    continue

            journey = self.compute_journey(train_commute)
            if train_commute["source"] not in self.computed_commutes:
                self.computed_commutes[train_commute["source"]] = dict()

            if (
                train_commute["target"]
                not in self.computed_commutes[train_commute["source"]]
            ):
                self.computed_commutes[train_commute["source"]][
                    train_commute["target"]
                ] = dict()

            self.computed_commutes[train_commute["source"]][train_commute["target"]][
                "time"
            ] = journey["time"]
            self.computed_commutes[train_commute["source"]][train_commute["target"]][
                "changes"
            ] = journey["changes"]

            yield {
                "commute_id": train_commute["commute_id"],
                "commute_type": train_commute["type"],
                "time": journey["time"],
                "changes": journey["changes"],
            }
