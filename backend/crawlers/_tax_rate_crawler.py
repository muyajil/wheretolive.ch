import logging
from datetime import datetime

import pandas as pd
import requests


# FileCrawler
class TaxRateCrawler:
    def __init__(self):
        self.base_url = (
            "https://www.estv.admin.ch/dam/estv/de/dokumente/allgemein"
            + "/Dokumentation/Zahlen_fakten/Steuerstatistiken/steuerbelastung/"
        )
        self.xlsx_path = "/tmp/data.xlsx"
        self.code_mapping = {
            "Ledig": "single",
            "VOK": "married_no_children",
            "VMK": "married_2_children",
            "DOPMK": "married_2_children_2_salaries",
            "REN": "retired",
        }
        self.income_brackets = [
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
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def data_url(self):
        year = datetime.now().year
        month = datetime.now().month
        latest_year = year - 2 if month < 10 else year - 1
        return (
            self.base_url
            + f"{latest_year}/SB-NP-alle-Gden_{latest_year}.xlsx.download.xlsx/SB-NP-alle-Gden_{latest_year}.xlsx"
        )

    def download_data(self):
        self.logger.debug("Downloading data...")
        r = requests.get(self.data_url, stream=True)
        with open(self.xlsx_path, "wb") as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)

    def crawl(self):
        self.download_data()
        self.logger.debug("Extracting tax rates...")
        sheet_names = ["Ledig", "VOK", "VMK", "DOPMK", "REN"]

        for sheet_name in sheet_names:
            profile = self.code_mapping[sheet_name]
            df = pd.read_excel("/tmp/data.xlsx", sheet_name=sheet_name).dropna()
            for index, row in df.iterrows():
                if index < 5:
                    continue

                row = list(row)
                bfs_nr = row[1]
                if sheet_name == "REN":
                    rates = rates = zip(
                        self.income_brackets[3:-1], self.income_brackets[4:], row[3:]
                    )
                else:
                    rates = zip(
                        self.income_brackets[:-1], self.income_brackets[1:], row[3:]
                    )
                for rate in rates:
                    yield {
                        "bfs_nr": bfs_nr,
                        "profile": profile,
                        "min_income": rate[0],
                        "max_income": rate[1],
                        "rate": rate[2],
                    }
