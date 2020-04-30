import logging
from ..models import SBBTransfer, SBBStationGroup
import pandas as pd
import os
import psycopg2 as pg
import json
from subprocess import Popen
import time


class TrainCommuteAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.commutes_by_stations = dict()
        self.db_conn = pg.connect(os.environ.get("DB_CONN"))

    def export_transfer_map(self):
        transfer_map = dict()
        transfers = self.db_session.query(SBBTransfer)
        for transfer in transfers:
            if transfer.from_stop_id not in transfer_map:
                transfer_map[transfer.from_stop_id] = dict()
            transfer_map[transfer.from_stop_id][
                transfer.to_stop_id
            ] = transfer.min_transfer_time
        json.dump(transfer_map, open("/tmp/transfer_map.json", "w"))
        self.logger.info("Transfer Map exported")

    def export_sbb_station_groups(self):
        station_groups_map = dict()
        station_groups = self.db_session.query(SBBStationGroup)
        for station_group in station_groups:
            station_groups_map[station_group.sbb_station_id] = dict()
            for station_id, walking_time in zip(
                station_group.sbb_station_group, station_group.walking_times
            ):
                station_groups_map[station_group.sbb_station_id][
                    station_id
                ] = walking_time

        json.dump(station_groups_map, open("/tmp/station_groups.json", "w"))
        self.logger.info("SBB Station Groups exported")

    def export_connections(self):
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
                sbb_connection.departure_time >= '06:00:00' and
                sbb_calendar.monday
            order by sbb_connection.departure_time, sbb_connection.trip_id
        """

        connections_df = pd.read_sql(sql, self.db_conn)
        connections_df["arrival_time"] = connections_df["arrival_time"].map(
            lambda t: (t.hour * 60 + t.minute) * 60 + t.second
        )
        connections_df["departure_time"] = connections_df["departure_time"].map(
            lambda t: (t.hour * 60 + t.minute) * 60 + t.second
        )
        connections_df.to_csv("/tmp/connections.csv", index=False, header=False)
        del connections_df
        self.logger.info("Connections exported")

    def export_commutes(self):
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
            t_sbb_station.id as target_station_id
        from commute
        join town as s_town on s_town.id = source_town_id
        join town as t_town on t_town.id = target_town_id
        join sbb_station as s_sbb_station on s_sbb_station.id = s_town.closest_train_station_id
        join sbb_station as t_sbb_station on t_sbb_station.id = t_town.closest_train_station_id
        """

        sqls = [sql_1, sql_2]
        commute_types = ["closest_station", "closest_train"]
        commutes = []
        for sql, commute_type in zip(sqls, commute_types):
            cursor = self.db_conn.cursor()
            cursor.execute(sql)
            for c in cursor:
                commute_id, source, target = c
                if source in self.commutes_by_stations:
                    if target in self.commutes_by_stations[source]:
                        self.commutes_by_stations[source][target].append(commute_id)
                        continue

                if source not in self.commutes_by_stations:
                    self.commutes_by_stations[source] = dict()
                self.commutes_by_stations[source][target] = [commute_id]
                commutes.append((source, target, commute_type))
            cursor.close()

        commutes_df = pd.DataFrame(
            commutes,
            columns=["source_station_id", "target_station_id", "commute_type"],
        )

        commutes_df.to_csv("/tmp/commutes.csv", index=False, header=False)
        del commutes_df
        del commutes
        self.logger.info("Commutes exported")

    @property
    def output_lines(self):
        while not os.path.exists("/tmp/train_commutes.csv"):
            time.sleep(2)
        f = open("/tmp/train_commutes.csv")
        finished = False
        prev_chunk = ""
        while not finished:
            chunk = prev_chunk + f.read(4096)
            if chunk == "":
                time.sleep(5)
                continue
            for line in chunk.split("\n"):
                if line == "done":
                    finished = True
                    break
                else:
                    splits = list(filter(lambda x: x != "", line.split(",")))
                    if len(splits) < 5:
                        prev_chunk = line
                    else:
                        yield splits

    def aggregate(self):
        self.export_transfer_map()
        self.export_sbb_station_groups()
        self.export_connections()
        self.export_commutes()

        if os.path.exists("/tmp/train_commutes.csv"):
            os.remove("/tmp/train_commutes.csv")
        _ = Popen(["./csa/csa"])

        for row in self.output_lines:
            source, target, commute_type, time_sec, changes = row
            for commute_id in self.commutes_by_stations[source][target]:
                yield {
                    "commute_id": commute_id,
                    "commute_type": commute_type,
                    "time": None if int(time_sec) < 0 else int(time_sec),
                    "changes": None if int(changes) < 0 else int(changes),
                }
