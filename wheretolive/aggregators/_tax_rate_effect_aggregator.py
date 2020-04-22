import pandas as pd
import numpy as np
import logging
import os


class TaxRateEffectAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__model = None
        self.__tax_rates = None
        self.__sql = """
                    select
                        bfs_nr_state.state,
                        s.bfs_nr,
                        s.min_income,
                        s.max_income,
                        s.rate as s_rate,
                        m0c.rate as m0c_rate,
                        m2c.rate as m2c_rate,
                        m2c2s.rate as m2c2s_rate from
                    (select * from tax_rate
                    where profile = 'single') as s
                    join
                    (select * from tax_rate
                    where profile = 'married_no_children') as m0c
                    on m0c.bfs_nr = s.bfs_nr and m0c.min_income = s.min_income and m0c.max_income = s.max_income
                    join
                    (select * from tax_rate
                    where profile = 'married_2_children') as m2c
                    on m2c.bfs_nr = s.bfs_nr and m2c.min_income = s.min_income and m2c.max_income = s.max_income
                    join
                    (select * from tax_rate
                    where profile = 'married_2_children_2_salaries') as m2c2s
                    on m2c2s.bfs_nr = s.bfs_nr and m2c2s.min_income = s.min_income and m2c2s.max_income = s.max_income
                    join
                    (select distinct bfs_nr, state from town) as bfs_nr_state
                    on bfs_nr_state.bfs_nr = s.bfs_nr
                    order by s.bfs_nr, s.min_income
                    """

    def init_tax_rates(self):
        self.__tax_rates = pd.read_sql(self.__sql, os.environ.get("DB_CONN"))

    def aggregate(self):
        df = pd.read_sql(self.__sql, os.environ.get("DB_CONN"))
        df["2c_effect"] = df["m2c_rate"] - df["m0c_rate"]
        df["m_effect"] = df["m0c_rate"] - df["s_rate"]
        df["2s_effect"] = df["m2c2s_rate"] - df["m2c_rate"]

        df_effects = df.groupby(by=["min_income", "state"]).agg(
            {
                "2c_effect": [np.mean, np.std, np.var],
                "m_effect": [np.mean, np.std, np.var],
                "2s_effect": [np.mean, np.std, np.var],
            }
        )

        effects = set(df_effects.columns.get_level_values(0))

        states = set(df_effects.index.get_level_values(1))
        incomes = set(df_effects.index.get_level_values(0))
        for effect in effects:
            for state in states:
                for min_income in incomes:
                    df.loc[
                        (df.min_income == min_income) & (df.state == state),
                        effect + "_est",
                    ] = df_effects[effect]["mean"][min_income][state]

        for row in df.to_dict("records"):
            yield {
                "bfs_nr": row["bfs_nr"],
                "min_income": row["min_income"],
                "max_income": row["max_income"],
                "child_effect": row["2c_effect_est"] / 2,
                "married_effect": row["m_effect_est"],
                "double_salary_effect": row["2s_effect_est"],
            }
