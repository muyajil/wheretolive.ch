import logging

from ._accomodation_service import AccomodationService
from ._commute_service import CommuteService
from ._health_insurance_service import HealthInsuranceService
from ._tax_service import TaxService


class TownsAnalysisService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.commute_service = CommuteService()
        self.tax_service = TaxService()
        self.accomodation_service = AccomodationService()
        self.health_insurance_service = HealthInsuranceService()

    def analyze(self, search_profile):
        town_stats = {}
        zip_to_id = {}
        bfs_nr_to_id = {}
        relevant_towns = self.commute_service.get_towns_in_range(
            search_profile["workplace_zip_code"],
            search_profile["commute_type"],
            search_profile["max_commute_h"],
        )

        for relevant_town in relevant_towns:
            town_stats[relevant_town[0]] = {
                "zip_code": relevant_town[1],
                "name": relevant_town[2],
                "bfs_nr": relevant_town[3],
            }
            if relevant_town[1] in zip_to_id:
                zip_to_id[relevant_town[1]].append(relevant_town[0])
            else:
                zip_to_id[relevant_town[1]] = [relevant_town[0]]

            if relevant_town[3] in bfs_nr_to_id:
                bfs_nr_to_id[relevant_town[3]].append(relevant_town[0])
            else:
                bfs_nr_to_id[relevant_town[3]] = [relevant_town[0]]

        relevant_zip_codes = set(map(lambda x: town_stats[x]["zip_code"], town_stats))

        average_home_cost = self.accomodation_service.get_average_home_cost(
            relevant_zip_codes, search_profile["max_rooms"], search_profile["min_rooms"]
        )

        for zip_code in average_home_cost:
            for town_id in zip_to_id[zip_code]:
                town_stats[town_id]["yearly_cost_home"] = average_home_cost[zip_code]

        health_insurance_cost = self.health_insurance_service.get_health_insurance_cost(
            search_profile["people"], relevant_zip_codes
        )

        for zip_code in health_insurance_cost:
            for town_id in zip_to_id[zip_code]:
                town_stats[town_id]["yearly_cost_health"] = health_insurance_cost[
                    zip_code
                ]

        relevant_bfs_nrs = set(map(lambda x: town_stats[x]["bfs_nr"], town_stats))

        taxes = self.tax_service.get_taxes(
            search_profile["married"],
            search_profile["double_salary"],
            search_profile["num_children"],
            search_profile["income"],
            relevant_bfs_nrs,
        )

        for bfs_nr in taxes:
            for town_id in bfs_nr_to_id[bfs_nr]:
                town_stats[town_id]["yearly_cost_taxes"] = taxes[bfs_nr]

        return town_stats
