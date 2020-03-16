import requests
import zipfile
import shutil
import csv
import math
import logging
import os


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

    def get_towns(self):
        self.download_data()
        self.extract_csv()
        with open(self.csv_path, encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=self.csv_delimiter)
            for item in reader:
                yield {
                    'name': item['Ortschaftsname'],
                    'zip': item['PLZ'],
                    'lang': item['Sprache'],
                    'state': item['Kantonskürzel'],
                    'bfs_nr': item['BFS-Nr'],
                    'x': float(item['E']),
                    'y': float(item['N'])
                }

    def merge_zip_codes(self):
        towns = self.get_towns()
        self.logger.debug('Merging Zip Codes...')
        self.towns_by_zip = dict()
        for town in towns:
            cur_zip = town['zip']
            if cur_zip in self.towns_by_zip:
                prev_n = len(self.towns_by_zip[cur_zip]['names'])
                prev_x = self.towns_by_zip[cur_zip]['x']
                prev_y = self.towns_by_zip[cur_zip]['y']
                self.towns_by_zip[cur_zip]['names'].append(town['name'])
                self.towns_by_zip[cur_zip]['x'] = (prev_n * prev_x + town['x']) / (prev_n + 1)
                self.towns_by_zip[cur_zip]['y'] = (prev_n * prev_y + town['y']) / (prev_n + 1)
            else:
                self.towns_by_zip[cur_zip] = dict()
                self.towns_by_zip[cur_zip]['names'] = [town['name']]
                self.towns_by_zip[cur_zip]['x'] = town['x']
                self.towns_by_zip[cur_zip]['y'] = town['y']
            self.towns_by_zip[cur_zip]['lang'] = town['lang']
            self.towns_by_zip[cur_zip]['state'] = town['state']
            self.towns_by_zip[cur_zip]['bfs_nr'] = town['bfs_nr']

    def crawl(self):
        self.merge_zip_codes()
        return self.towns_by_zip
