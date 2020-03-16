import requests
from datetime import datetime
import logging
import pandas as pd


# FileCrawler
class TaxRateCrawler():

    def __init__(self):
        self.base_url = 'https://www.estv.admin.ch/dam/estv/de/dokumente/allgemein/Dokumentation/Zahlen_fakten/Steuerstatistiken/steuerbelastung/'
        self.xlsx_path = '/tmp/data.xlsx'
        self.code_mapping = {
            'Ledig': 'single',
            'VOK': 'married_no_children',
            'VMK': 'married_2_children',
            'DOPMK': 'married_2_children_2_salaries',
            'REN': 'retired'
        }
        self.income_brackets = [12500, 15000, 17500, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 60000, 70000,
                                80000, 90000, 100000, 125000, 150000, 175000, 200000, 250000, 300000, 400000, 500000,
                                1000000]
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tax_rates_by_bfs_num = dict()

    @property
    def data_url(self):
        year = datetime.now().year
        month = datetime.now().month
        latest_year = year - 2 if month < 10 else year - 1
        return self.base_url + f'{latest_year}/SB-NP-alle-Gden_{latest_year}.xlsx.download.xlsx/SB-NP-alle-Gden_{latest_year}.xlsx'

    def download_data(self):
        self.logger.debug('Downloading data...')
        r = requests.get(self.data_url, stream=True)
        with open(self.xlsx_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)

    def extract_data(self):
        self.download_data()
        self.logger.debug('Extracting tax rates...')
        sheet_names = ['Ledig', 'VOK', 'VMK', 'DOPMK', 'REN']

        for sheet_name in sheet_names:
            profile = self.code_mapping[sheet_name]
            self.tax_rates_by_bfs_num[profile] = dict()
            df = pd.read_excel('/tmp/data.xlsx', sheet_name=sheet_name)
            for index, row in df.iterrows():
                if index < 5:
                    continue

                row = list(row)
                bfs_nr = row[1]
                town_name = row[2]
                tax_rates = [{'min_income': x, 'tax_rate': y} for x, y in zip(self.income_brackets, row[3:])]
                self.tax_rates_by_bfs_num[profile][bfs_nr] = dict()
                self.tax_rates_by_bfs_num[profile][bfs_nr]['town_name'] = town_name
                self.tax_rates_by_bfs_num[profile][bfs_nr]['tax_rates'] = tax_rates

    def crawl(self):
        self.extract_data()
        return self.tax_rates_by_bfs_num
