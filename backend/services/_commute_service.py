from ..models import ClosestStationCommute, ClosestTrainCommute


class CommuteService:
    def get_towns_in_range(self, target_zip_code, commute_type, max_commute_h):
        max_commute_secs = int(float(max_commute_h) * 3600)
        if commute_type == "closest_station":
            source_zips = (
                ClosestStationCommute.query.with_entities(
                    ClosestStationCommute.source_town_id,
                    ClosestStationCommute.source_zip_code,
                    ClosestStationCommute.source_town_name,
                    ClosestStationCommute.source_town_bfs_nr,
                )
                .filter_by(target_zip_code=target_zip_code)
                .filter(ClosestStationCommute.time <= max_commute_secs)
            )

        else:
            source_zips = (
                ClosestTrainCommute.query.with_entities(
                    ClosestTrainCommute.source_town_id,
                    ClosestTrainCommute.source_zip_code,
                    ClosestTrainCommute.source_town_name,
                    ClosestTrainCommute.source_town_bfs_nr,
                )
                .filter_by(target_zip_code=target_zip_code)
                .filter(ClosestTrainCommute.time <= max_commute_secs)
            )
        return [x for x in source_zips]
