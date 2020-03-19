import googlemaps
import logging
from ..models import Route
from ..database import get_session
from datetime import datetime
from retry import retry


class GmapsCommuteCrawler():

    def __init__(self, api_key):
        self.client = googlemaps.Client(api_key)
        self.departure_time = datetime.now().replace(
            hour=8, minute=0, second=0, microsecond=0)
        if self.departure_time.isoweekday() in [6,7]:
            self.departure_time += datetime.timedelta(days=8 - self.departure_time.isoweekday())
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ranges = {
            "mode": ['DRIVING', 'TRANSIT']
        }

    def get_directions_data(self, origin, destination, mode):
        try:
            directions_results = self.client.directions(
                origin=origin,
                destination=destination,
                mode=mode,
                departure_time=self.departure_time)

            leg = directions_results[0]['legs'][0]
            return leg
        except:
            return None

    def get_time_in_vehicle(self, leg, mode):
        relevant_steps = filter(lambda x: x['travel_mode'] == mode, leg['steps'])
        durations = map(lambda x: x['duration']['value'], relevant_steps)
        return sum(durations)

    def get_number_of_vehicles(self, leg, mode):
        relevant_steps = filter(lambda x: x['travel_mode'] == mode, leg['steps'])
        return len(list(relevant_steps))

    @property
    def items(self):
        routes = get_session().query(Route)
        for route in routes:
            for mode in self.ranges['mode']:
                yield {
                    "origin": route.source_town_zip_code,
                    "destination": route.target_town_zip_code,
                    "mode": mode
                }

    def crawl(self):
        for item in self.items:
            leg = self.get_directions_data(**item)
            if leg is None:
                continue

            yield {
                "origin_zip_code": item['origin'],
                "destination_zip_code": item['destination'],
                "mode": item['mode'],
                "total_seconds": self.get_time_in_vehicle(leg, item['mode']),
                "num_vehicles": self.get_number_of_vehicles(leg, item['mode'])
            }
