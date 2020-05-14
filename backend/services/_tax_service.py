import numpy as np

from ..models import TaxRate, TaxRateEffect, Town
from ..utils.math import add_thousands_sep


class TaxService:
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

    def get_taxes(self, married, double_salary, num_children, income, bfs_nrs=None):
        base_profile, children_diff = self.get_tax_base_profile(
            married, double_salary, num_children
        )

        tax_rates = (
            TaxRate.query.with_entities(
                TaxRate.bfs_nr, TaxRate.name, TaxRate.rate, TaxRateEffect.child_effect
            )
            .join(TaxRateEffect, TaxRateEffect.bfs_nr == TaxRate.bfs_nr)
            .filter(TaxRate.min_income <= income)
            .filter(TaxRate.max_income > income)
            .filter(TaxRateEffect.min_income <= income)
            .filter(TaxRateEffect.max_income > income)
            .filter(TaxRate.profile == base_profile)
        )

        if bfs_nrs:
            tax_rates = tax_rates.filter(TaxRate.bfs_nr.in_(bfs_nrs))

        taxes = {}

        for tax_rate in tax_rates:
            tax_amount = max(
                int(((tax_rate[2] + children_diff * tax_rate[3]) / 100) * income), 0.0
            )
            taxes[tax_rate[0]] = tax_amount
            taxes[tax_rate[1]] = tax_amount
        return taxes

    def get_histogram_bins(self, all_taxes):
        max_taxes = max(all_taxes.values())
        if max_taxes <= 100:
            bin_width = 10
        elif max_taxes <= 5000:
            bin_width = 100
        elif max_taxes <= 10000:
            bin_width = 500
        elif max_taxes <= 25000:
            bin_width = 1000
        elif max_taxes <= 50000:
            bin_width = 2500
        elif max_taxes <= 100000:
            bin_width = 5000
        else:
            bin_width = 10000

        right_edge = ((max_taxes // bin_width) + 1) * bin_width
        return list(range(0, right_edge, bin_width))

    def calculate_taxes(
        self,
        married,
        double_salary,
        num_children,
        income,
        target_town_id,
        target_town_name,
    ):
        if not married:
            double_salary = False
        all_taxes = self.get_taxes(married, double_salary, num_children, income)
        target_bfs_nr = Town.query.get(target_town_id).bfs_nr

        try:
            target_town_taxes = all_taxes[target_bfs_nr]
        except KeyError:
            try:
                target_town_taxes = all_taxes[target_town_name]
            except KeyError:
                target_town_taxes = None

        histogram_bins = self.get_histogram_bins(all_taxes)

        counts, bins = np.histogram(list(all_taxes.values()), bins=histogram_bins)
        data = []
        target_town_idx = None

        for idx, (lower, upper, count) in enumerate(zip(bins[:-1], bins[1:], counts)):
            data.append(
                {
                    "range": add_thousands_sep(str(int(lower)))
                    + "-"
                    + add_thousands_sep(str(int(upper))),
                    "count": int(count),
                }
            )

            if lower <= target_town_taxes and upper >= target_town_taxes:
                target_town_idx = idx

        return target_town_taxes, target_town_idx, data
