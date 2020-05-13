import numpy as np
import plotly.graph_objects as go

from ..models import TaxRate, TaxRateEffect, Town


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
                TaxRate.bfs_nr, TaxRate.rate, TaxRateEffect.child_effect
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
            taxes[tax_rate[0]] = max(
                ((tax_rate[1] + children_diff * tax_rate[2]) / 100) * income, 0.0
            )
        return taxes

    def calculate_taxes(
        self, married, double_salary, num_children, income, target_town_id
    ):
        all_taxes = self.get_taxes(married, double_salary, num_children, income)
        target_bfs_nr = Town.query.get(target_town_id).bfs_nr

        colors = ["lightslategray"] * 200

        counts, bins = np.histogram(list(all_taxes.values()), bins=100)
        x = []
        for idx, (lower, upper) in enumerate(zip(bins[:-1], bins[1:])):
            x.append((lower, upper))
            if lower <= all_taxes[target_bfs_nr] and upper >= all_taxes[target_bfs_nr]:
                colors[idx] = "crimson"

        fig = go.Figure(go.Bar(x=x, y=counts, marker_color=colors))

        fig.update_layout(
            title="Taxes", xaxis_title="Tax Amount", yaxis_title="Count",
        )

        return all_taxes[target_bfs_nr], fig
