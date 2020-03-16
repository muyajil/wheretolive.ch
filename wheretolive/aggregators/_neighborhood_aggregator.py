import json
import logging
import math


class NeighborhoodAggregator():

    def __init__(self, towns_by_zip_path):
        self.towns_by_zip = json.load(open(towns_by_zip_path))
        self.logger = logging.getLogger(self.__class__.__name__)

    def compute_neighborhoods(self):
        self.neighborhoods = dict()
        self.logger.debug('Computing Neighborhoods...')
        for base_zip in self.towns_by_zip:
            neighborhoods = []
            for candidate_zip in self.towns_by_zip:
                cand = self.towns_by_zip[candidate_zip]
                base = self.towns_by_zip[base_zip]

                dist = math.sqrt((cand['x'] - base['x'])**2 + (cand['y'] - base['y'])**2)
                if dist == 0.0:
                    continue
                neighborhoods.append({'zip': candidate_zip, 'dist': dist})
            self.neighborhoods[base_zip] = sorted(neighborhoods, key=lambda x: x['dist'])

    def aggregate(self):
        self.compute_neighborhoods()
        return self.neighborhoods
