from ..models import TaxRate
from sklearn.svm import SVR
from sklearn.utils import shuffle
import pandas as pd
import logging
import os


class TaxRateAggregator:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__model = None
        self.__tax_rates = None
        self.__sql = """
                    select bfs_nr, profile, min_income, max_income, rate from tax_rate
                    order by bfs_nr, profile, min_income
                    """

    def init_model(self):
        self.__model = SVR()

    @property
    def model(self):
        if not self.__model:
            self.init_model()
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    def init_tax_rates(self):
        self.__tax_rates = pd.read_sql(self.__sql, os.environ.get("DB_CONN"))

    @property
    def tax_rates(self):
        if not self.__tax_rates:
            self.init_tax_rates()
        return self.__tax_rates

    @property
    def tax_rates_to_predict(self):
        tax_rates_to_predict = []
        num_children_range = [1, 2, 3, 4, 5]
        income_brackets = [
            12500,
            15000,
            17500,
            20000,
            25000,
            30000,
            35000,
            40000,
            45000,
            50000,
            60000,
            70000,
            80000,
            90000,
            100000,
            125000,
            150000,
            175000,
            200000,
            250000,
            300000,
            400000,
            500000,
            1000000,
            10000000,
        ]
        num_salaries_range = [1, 2]
        num_taxed_range = [1, 2]
        bfs_nr_range = [x for x, in self.db_session.query(TaxRate.bfs_nr).distinct()]

        for bfs_nr in bfs_nr_range:
            for num_salaries in num_salaries_range:
                for num_children in num_children_range:
                    for min_income, max_income in zip(
                        income_brackets[:-1], income_brackets[1:]
                    ):
                        for num_taxed in num_taxed_range:
                            if (
                                (
                                    num_taxed == 2
                                    and num_children == 2
                                    and num_salaries == 1
                                )
                                or (
                                    num_taxed == 2
                                    and num_children == 0
                                    and num_salaries == 1
                                )
                                or (
                                    num_taxed == 2
                                    and num_children == 2
                                    and num_salaries == 2
                                )
                                or (num_taxed == 1 and num_salaries == 2)
                            ):
                                continue
                            tax_rates_to_predict.append(
                                {
                                    "bfs_nr": bfs_nr,
                                    "num_salaries": num_salaries,
                                    "num_children": num_children,
                                    "min_income": min_income,
                                    "max_income": max_income,
                                    "num_taxed": num_taxed,
                                    "is_exact": False,
                                }
                            )
        return tax_rates_to_predict

    def preprocess_train_data(self, df):
        df["num_children"] = df["profile"].map(lambda x: 2 if "2_children" in x else 0)
        df["num_salaries"] = df["profile"].map(lambda x: 2 if "2_salaries" in x else 1)
        df["num_taxed"] = df["profile"].map(lambda x: 2 if "married" in x else 1)
        df = df.drop(["profile"], axis=1)
        df["is_exact"] = True
        df = shuffle(df)
        return df

    def train(self, X, y):
        self.model = self.model.fit(X, y)

    def predict(self, X):
        return self.__model.predict(X)

    def aggregate(self):
        tax_rates = self.preprocess_train_data(self.tax_rates)
        self.train(tax_rates.drop("rate", axis=1), tax_rates["rate"])

        for tax_rate in tax_rates.to_dict("records"):
            yield tax_rate

        tax_rates_to_predict = pd.DataFrame(self.tax_rates_to_predict)
        tax_rates_to_predict["rate"] = self.predict(tax_rates_to_predict)
        tax_rates_to_predict.loc[tax_rates_to_predict.rate < 0, "rate"] = 0.0

        for tax_rate_predicted in tax_rates_to_predict.to_dict("records"):
            yield tax_rate_predicted
