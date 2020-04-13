from ..models import TaxRate
from sklearn.svm import SVR
import pandas as pd


class TaxRateAggregator:
    def __init__(self, db_session, logger):
        self.db_session = db_session
        self.logger = logger
        self.__model = None
        self.__tax_rates = None
        self.__sql = """
                    select bfs_nr, profile, min_income, rate from tax_rate
                    order by bfs_nr, profile, min_income
                    """

    def init_model(self):
        self.__model = SVR(1.0, 0.2)

    @property
    def model(self):
        if not self.__model:
            self.init_model()
        return self.__model

    def init_tax_rates(self):
        self.__tax_rates = pd.read_sql(self.__sql, self.db_session)

    @property
    def tax_rates(self):
        if not self.__tax_rates:
            self.init_tax_rates()
        return self.__tax_rates

    @property
    def tax_rates_to_predict(self):
        # TODO: Check that the generated tuples make sense
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
        is_married_range = [True, False]
        bfs_nr_range = [x for x, in self.db_session.query(TaxRate.bfs_nr).distinct()]

        for bfs_nr in bfs_nr_range:
            for num_salaries in num_salaries_range:
                for num_children in num_children_range:
                    for min_salary, max_salary in zip(
                        income_brackets[:-1], income_brackets[1:]
                    ):
                        for is_married in is_married_range:
                            tax_rates_to_predict.append(
                                {
                                    "bfs_nr": bfs_nr,
                                    "num_salaries": num_salaries,
                                    "num_children": num_children,
                                    "min_salary": min_salary,
                                    "max_salary": max_salary,
                                    "is_married": is_married,
                                    "is_exact": False,
                                }
                            )
        return tax_rates_to_predict

    def preprocess_train_data(self, df):
        df["children"] = df["profile"].map(lambda x: 2 if "2_children" in x else 0)
        df["salaries"] = df["profile"].map(lambda x: 2 if "2_salaries" in x else 1)
        df["num_taxed"] = df["profile"].map(lambda x: 2 if "married" in x else 1)
        df = df.drop(["profile"], axis=1)
        # TODO: Shuffle data
        return (
            df[["bfs_nr", "min_income", "children", "salaries", "num_taxed"]],
            df["rate"],
        )

    def train(self, X, y):
        self.model = self.model.fit(X, y)

    def predict(self, X):
        return self.__model.predict(X)

    def aggregate(self):
        # TODO: For each tax rate in the database yield exact tax rate
        X_train, y_train = self.preprocess_train_data(self.tax_rates)
        self.train(X_train, y_train)

        tax_rates_to_predict = pd.DataFrame([x for x in self.tax])
        tax_rates_to_predict["rate"] = self.predict(tax_rates_to_predict)

        # TODO: For each tax rate in the predicted ones yield not exact tax_rate
