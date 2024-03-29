import logging
from statistics import mean

from ._accomodation_service import AccomodationService
from ._commute_service import CommuteService
from ._health_insurance_service import HealthInsuranceService
from ._tax_service import TaxService
from ._town_service import TownService


class SearchService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.commute_service = CommuteService()
        self.tax_service = TaxService()
        self.accomodation_service = AccomodationService()
        self.health_insurance_service = HealthInsuranceService()
        self.town_service = TownService()

    def get_towns_in_range(self, commute_info):
        towns_by_id = {}
        zip_to_id = {}
        bfs_nr_to_id = {}
        towns_in_range = self.commute_service.get_towns_in_range(commute_info)

        for town in towns_in_range:
            towns_by_id[town["sourceTownId"]] = town

            if town["sourceTownZip"] in zip_to_id:
                zip_to_id[town["sourceTownZip"]].append(town["sourceTownId"])
            else:
                zip_to_id[town["sourceTownZip"]] = [town["sourceTownId"]]

            if town["sourceTownBFSNr"] in bfs_nr_to_id:
                bfs_nr_to_id[town["sourceTownBFSNr"]].append(town["sourceTownId"])
            else:
                bfs_nr_to_id[town["sourceTownBFSNr"]] = [town["sourceTownId"]]

        return towns_by_id, zip_to_id, bfs_nr_to_id

    def get_towns_from_zips(self, zip_codes):
        towns = self.town_service.get_towns_from_zips(zip_codes)

        towns_by_id = {}
        zip_to_id = {}
        bfs_nr_to_id = {}

        for town in towns:
            towns_by_id[town["id"]] = town
            if town["zipCode"] in zip_to_id:
                zip_to_id[town["zipCode"]].append(town["id"])
            else:
                zip_to_id[town["zipCode"]] = [town["id"]]

            if town["bfsNr"] in bfs_nr_to_id:
                bfs_nr_to_id[town["bfsNr"]].append(town["id"])
            else:
                bfs_nr_to_id[town["bfsNr"]] = [town["id"]]

        return towns_by_id, zip_to_id, bfs_nr_to_id

    def get_average_home_cost_and_update(
        self, accomodation_info, towns_by_id, zip_to_id
    ):
        relevant_zip_codes = set(
            map(lambda x: towns_by_id[x]["sourceTownZip"], towns_by_id)
        )

        average_home_cost = self.accomodation_service.get_average_home_cost(
            relevant_zip_codes, accomodation_info
        )

        for zip_code in average_home_cost:
            for town_id in zip_to_id[zip_code]:
                towns_by_id[town_id]["yearlyCostHome"] = int(
                    average_home_cost[zip_code]
                )

        return towns_by_id

    def get_average_health_cost_and_update(
        self, health_info, towns_by_id, zip_to_id, zip_key
    ):
        relevant_zip_codes = set(map(lambda x: towns_by_id[x][zip_key], towns_by_id))

        average_health_cost = self.health_insurance_service.get_health_insurance_cost(
            relevant_zip_codes, health_info
        )

        for zip_code in average_health_cost:
            for town_id in zip_to_id[zip_code]:
                towns_by_id[town_id]["yearlyCostHealth"] = int(
                    average_health_cost[zip_code]
                )

        return towns_by_id

    def get_average_taxes_and_update(self, tax_info, towns_by_id, bfs_nr_key, name_key):
        relevant_bfs_nrs = set(map(lambda x: towns_by_id[x][bfs_nr_key], towns_by_id))
        relevant_names = set(map(lambda x: towns_by_id[x][name_key], towns_by_id))
        taxes_by_bfs_nr_and_name = self.tax_service.get_taxes_by_bfs_nr_and_name(
            tax_info, bfs_nrs=relevant_bfs_nrs, names=relevant_names
        )

        town_ids = list(towns_by_id.keys())
        for town_id in town_ids:
            bfs_nr = towns_by_id[town_id][bfs_nr_key]
            name = towns_by_id[town_id][name_key]
            if bfs_nr in taxes_by_bfs_nr_and_name:
                towns_by_id[town_id]["yearlyCostTaxes"] = taxes_by_bfs_nr_and_name[
                    bfs_nr
                ]
            elif name in taxes_by_bfs_nr_and_name:
                towns_by_id[town_id]["yearlyCostTaxes"] = taxes_by_bfs_nr_and_name[name]
            else:
                self.logger.debug(
                    f"Could not find taxes for town: Id: {town_id}, Name: {name}, BFS Nr: {bfs_nr}"
                )

        return towns_by_id

    def get_shopping_info_and_update(self, towns_by_id):
        town_ids = list(towns_by_id.keys())
        towns = self.town_service.get_shopping_info(town_ids=town_ids)
        for town in towns:
            towns_by_id[town["id"]]["migros"] = True if town["migros"] else False
            towns_by_id[town["id"]]["coop"] = True if town["coop"] else False
            towns_by_id[town["id"]]["lidl"] = True if town["lidl"] else False
            towns_by_id[town["id"]]["aldi"] = True if town["aldi"] else False

        return towns_by_id

    def search_towns(self, commute_info, tax_info, health_info, accomodation_info):

        towns_by_id, zip_to_id, bfs_nr_to_id = self.get_towns_in_range(commute_info)

        towns_by_id = self.get_average_home_cost_and_update(
            accomodation_info, towns_by_id, zip_to_id
        )

        towns_by_id = self.get_average_health_cost_and_update(
            health_info, towns_by_id, zip_to_id, "sourceTownZip"
        )

        towns_by_id = self.get_average_taxes_and_update(
            tax_info, towns_by_id, "sourceTownBFSNr", "sourceTownName"
        )

        towns_by_id = self.get_shopping_info_and_update(towns_by_id)

        town_ids = list(towns_by_id.keys())
        for town_id in town_ids:
            if len(towns_by_id[town_id]) < 12:
                towns_by_id.pop(town_id)

        for town_id in towns_by_id:
            towns_by_id[town_id]["yearlyCostTotal"] = (
                towns_by_id[town_id]["yearlyCostHealth"]
                + towns_by_id[town_id]["yearlyCostTaxes"]
                + towns_by_id[town_id]["yearlyCostHome"]
            )
            towns_by_id[town_id]["monthlyCostTotal"] = (
                towns_by_id[town_id]["yearlyCostTotal"] // 12
            )
            towns_by_id[town_id]["monthlyCostHealth"] = (
                towns_by_id[town_id]["yearlyCostHealth"] // 12
            )
            towns_by_id[town_id]["monthlyCostTaxes"] = (
                towns_by_id[town_id]["yearlyCostTaxes"] // 12
            )
            towns_by_id[town_id]["monthlyCostHome"] = (
                towns_by_id[town_id]["yearlyCostHome"] // 12
            )

        return sorted(towns_by_id.values(), key=lambda x: x["yearlyCostTotal"])

    def search_accomodations(self, zip_codes, tax_info, health_info, accomodation_info):
        accomodations = self.accomodation_service.get_accomodations(accomodation_info)

        towns_by_id, zip_to_id, bfs_nr_to_id = self.get_towns_from_zips(zip_codes)

        towns_by_id = self.get_average_health_cost_and_update(
            health_info, towns_by_id, zip_to_id, "zipCode"
        )

        towns_by_id = self.get_average_taxes_and_update(
            tax_info, towns_by_id, "bfsNr", "name"
        )

        accomodations_augmented = []

        for accomodation in accomodations:
            town_ids = zip_to_id[accomodation["zipCode"]]
            accomodation["monthlyCostTaxes"] = mean(
                map(lambda x: int(towns_by_id[x]["yearlyCostTaxes"]) / 12), town_ids
            )
            accomodation["monthlyCostHealth"] = mean(
                map(lambda x: int(towns_by_id[x]["yearlyCostHealth"]) / 12), town_ids
            )

            accomodations_augmented.append(accomodation)

        return accomodations_augmented
