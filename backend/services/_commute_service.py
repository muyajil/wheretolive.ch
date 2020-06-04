from ..models import ClosestStationCommute, ClosestTrainCommute, Town


class CommuteService:
    def get_towns_in_range(self, commute_info):
        if commute_info["onlyTrainCommute"]:
            source_towns = (
                ClosestTrainCommute.query.with_entities(
                    ClosestTrainCommute.source_town_id,
                    ClosestTrainCommute.source_zip_code,
                    ClosestTrainCommute.source_town_name,
                    ClosestTrainCommute.source_town_bfs_nr,
                    ClosestTrainCommute.time,
                )
                .filter_by(target_town_id=commute_info["workplaceTownId"])
                .filter(ClosestTrainCommute.time <= commute_info["maxCommuteSecs"])
            )

        else:
            source_towns = (
                ClosestStationCommute.query.with_entities(
                    ClosestStationCommute.source_town_id,
                    ClosestStationCommute.source_zip_code,
                    ClosestStationCommute.source_town_name,
                    ClosestStationCommute.source_town_bfs_nr,
                    ClosestStationCommute.time,
                )
                .filter_by(target_town_id=commute_info["workplaceTownId"])
                .filter(ClosestStationCommute.time <= commute_info["maxCommuteSecs"])
            )

        towns_in_range = [
            {
                "sourceTownId": x[0],
                "sourceTownZip": x[1],
                "sourceTownName": x[2],
                "sourceTownBFSNr": x[3],
                "commuteTime": x[4],
            }
            for x in source_towns
        ]

        workplaceTown = Town.query.get(commute_info["workplaceTownId"])

        towns_in_range.append(
            {
                "sourceTownId": workplaceTown.id,
                "sourceTownZip": workplaceTown.zip_code,
                "sourceTownBFSNr": workplaceTown.bfs_nr,
                "sourceTownName": workplaceTown.name,
                "commuteTime": 0,
            }
        )

        return towns_in_range
