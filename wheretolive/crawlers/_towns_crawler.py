import requests
import zipfile
import shutil
import csv
import logging


# FileCrawler
class TownsCrawler():

    def __init__(self):
        self.base_url = 'https://data.geo.admin.ch/ch.swisstopo-vd.ortschaftenverzeichnis_plz/PLZO_CSV_LV03.zip'
        self.zip_path = '/tmp/data.zip'
        self.csv_path = '/tmp/data.csv'
        self.csv_delimiter = ';'
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def data_url(self):
        return self.base_url

    def download_data(self):
        self.logger.debug('Downloading data...')
        r = requests.get(self.data_url, stream=True)
        with open(self.zip_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)

    def extract_csv(self):
        self.logger.debug('Extracting CV...')
        zip_file = zipfile.ZipFile(self.zip_path)
        source_file_name = zip_file.namelist()[0]
        source = zip_file.open(source_file_name)
        target = open(self.csv_path, 'wb')
        with source, target:
            shutil.copyfileobj(source, target)

    def crawl(self):
        self.download_data()
        self.extract_csv()
        with open(self.csv_path, encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=self.csv_delimiter)
            for item in reader:
                yield {
                    'name': item['Ortschaftsname'],
                    'zip_code': int(item['PLZ']),
                    'lang': item['Sprache'],
                    'state': item['Kantonskürzel'],
                    'bfs_nr': int(item['BFS-Nr']),
                    'x': float(item['E']),
                    'y': float(item['N'])
                }
