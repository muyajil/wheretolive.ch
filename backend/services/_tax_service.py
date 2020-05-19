import logging

from ..models import TaxRate, TaxRateEffect
from ._town_service import TownService


class TaxService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.town_service = TownService()

    def get_tax_base_profile(self, married, double_salary, num_children):
        if married:
            if double_salary:
                base_profile = "married_2_children_2_salaries"
                included_children = 2
            else:
                if num_children > 0:
                    base_profile = "married_2_children"
                    included_children = 2
                else:
                    base_profile = "married_0_children"
                    included_children = 0
        else:
            base_profile = "single"
            included_children = 0

        if included_children != num_children:
            children_diff = num_children - included_children
        else:
            children_diff = 0

        return base_profile, children_diff

    def get_all_taxes(self, tax_info, target_town_id=None):
        return self.get_taxes(tax_info, target_town_id=target_town_id)

    def get_taxes(self, tax_info, target_town_id=None, bfs_nrs=[], names=[]):
        base_profile, children_diff = self.get_tax_base_profile(
            tax_info["married"], tax_info["doubleSalary"], tax_info["numChildren"]
        )

        tax_rates = (
            TaxRate.query.with_entities(
                TaxRate.bfs_nr, TaxRate.name, TaxRate.rate, TaxRateEffect.child_effect
            )
            .join(TaxRateEffect, TaxRateEffect.bfs_nr == TaxRate.bfs_nr)
            .filter(TaxRate.min_income <= tax_info["income"])
            .filter(TaxRate.max_income > tax_info["income"])
            .filter(TaxRateEffect.min_income <= tax_info["income"])
            .filter(TaxRateEffect.max_income > tax_info["income"])
            .filter(TaxRate.profile == base_profile)
        )

        if bfs_nrs and names:
            tax_rates = tax_rates.filter(
                TaxRate.bfs_nr.in_(bfs_nrs) or TaxRate.name.in_(names)
            )

        taxes = {}

        for tax_rate in tax_rates:
            bfs_nr, name, rate, child_effect = tax_rate
            tax_amount = max(
                int(((rate + children_diff * child_effect) / 100) * tax_info["income"]),
                0.0,
            )
            taxes[bfs_nr] = tax_amount
            taxes[name] = tax_amount
        taxes_mapped = self.map_to_town_ids(taxes, target_town_id, bfs_nrs, names)
        self.logger.info(f"Completed Tax Calculation for: {tax_info}")
        return taxes_mapped

    def map_to_town_ids(self, taxes, target_town_id=None, bfs_nrs=[], names=[]):
        taxes_mapped = []
        target_town_tax_amount = 0
        towns = self.town_service.get_towns(bfs_nrs, names)
        for town in towns:
            town_id, name, bfs_nr = town

            if bfs_nr in taxes:
                tax_amount = taxes[bfs_nr]

            elif name in taxes:
                tax_amount = taxes[name]
            else:
                self.logger.warn(
                    f"Could not find taxes for town: Id: {town_id}, Name: {name}, BFS Nr: {bfs_nr}"
                )
                continue

            if town_id == target_town_id:
                target_town_tax_amount = tax_amount
            taxes_mapped.append({"id": town_id, "taxAmount": tax_amount})

        return taxes_mapped, target_town_tax_amount
