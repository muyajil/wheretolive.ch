import logging

from ...models import ClosestStationCommute, ClosestTrainCommute


class TownsAnalysisService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_relevant_zip_codes(self, search_profile):
        max_commute_secs = int(float(search_profile["max_commute_h"]) * 3600)
        if search_profile["commute_type"] == "closest_station":
            source_zips = (
                ClosestStationCommute.query.with_entities(
                    ClosestStationCommute.source_zip_code
                )
                .filter_by(target_zip_code=search_profile["workplace_zip_code"])
                .filter(ClosestStationCommute.time <= max_commute_secs)
            )
            return [x for x, in source_zips]
        else:
            source_zips = (
                ClosestTrainCommute.query.with_entities(
                    ClosestTrainCommute.source_zip_code
                )
                .filter_by(target_zip_code=search_profile["workplace_zip_code"])
                .filter(ClosestStationCommute.time <= max_commute_secs)
            )
            return [x for x, in source_zips]

    def analyze(self, search_profile):
        return self.get_relevant_zip_codes(search_profile)
