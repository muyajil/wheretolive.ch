import requests
import json
from datetime import datetime
import logging
import zipfile
import csv


class SBBTimetableCrawler():

    def __init__(self):
        self.base_url = 'https://opendata.swiss/api/3/action/package_show?id=fahrplanentwurf-2020-gtfs'
        self.zip_path = '/tmp/timetable.zip'
        self.extraction_path = '/tmp/timetable/'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.downloaded = False

    @property
    def data_url(self):
        metadata = json.loads(requests.get(self.base_url).text)

        resources = sorted(
            metadata['result']['resources'],
            key=lambda x: datetime.strptime(x['created'], "%Y-%m-%dT%H:%M:%S.%f"))

        return resources[-1]['download_url']

    def download_data(self):
        self.logger.debug('Downloading data...')
        r = requests.get(self.data_url, stream=True)
        with open(self.zip_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)

    def extract_data(self):
        self.download_data()
        with zipfile.ZipFile(self.zip_path, 'r') as f:
            f.extractall(self.extraction_path)
        self.downloaded = True

    def get_rows_from_export(self, filename):
        if not self.downloaded:
            self.extract_data()
        path = self.extraction_path + filename
        with open(path, 'r') as f:
            next(f)
            for line in csv.reader(f):
                yield line

    def check_if_next_day(self, time):
        splits = time.split(':')
        next_day = False
        if int(splits[0]) > 23:
            splits[0] = str(int(splits[0]) - 24)
            next_day = True
            datetime.strptime(':'.join(splits), "%H:%M:%S").time()
        return datetime.strptime(':'.join(splits), "%H:%M:%S").time(), next_day

    def crawl_stops(self):
        for line in self.get_rows_from_export('stops.txt'):
            yield {
                "id": line[0],
                "name": line[1],
                "lat": float(line[2]),
                "long": float(line[3]),
                "parent_station": line[5] if line[5] != '' else None
            }

    def crawl_stop_times(self):
        for line in self.get_rows_from_export('stop_times.txt'):
            arrival_time, arrives_next_day = self.check_if_next_day(line[1])
            departure_time, departs_next_day = self.check_if_next_day(line[2])
            yield {
                "trip_id": line[0],
                "station_id": line[3],
                "arrival_time": arrival_time,
                "arrives_next_day": arrives_next_day,
                "departure_time": departure_time,
                "departs_next_day": departs_next_day,
                "stop_sequence": int(line[4])
            }

    def crawl_trips(self):
        for line in self.get_rows_from_export('trips.txt'):
            yield {
                "trip_id": line[2],
                "route_id": line[0],
                "service_id": line[1]
            }

    def crawl_routes(self):
        for line in self.get_rows_from_export('routes.txt'):
            yield {
                "route_id": line[0],
                "route_desc": line[4]
            }

    def crawl_calendar(self):
        for line in self.get_rows_from_export('calendar.txt'):
            yield {
                "service_id": line[0],
                "monday": line[1] == "1",
                "tuesday": line[2] == "1",
                "wednesday": line[3] == "1",
                "thursday": line[4] == "1",
                "friday": line[5] == "1",
                "saturday": line[6] == "1",
                "sunday": line[7] == "1"
            }

    def crawl_transfers(self):
        for line in self.get_rows_from_export('transfers.txt'):
            yield {
                "from_stop_id": line[0],
                "to_stop_id": line[1],
                "min_transfer_time": line[3]
            }
