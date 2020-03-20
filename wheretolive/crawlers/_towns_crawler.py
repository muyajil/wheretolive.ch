import requests
import zipfile
import shutil
import csv
import logging


# FileCrawler
class TownsCrawler:
    def __init__(self):
        self.base_url = "https://data.geo.admin.ch/ch.swisstopo-vd.ortschaftenverzeichnis_plz/PLZO_CSV_LV03.zip"
        self.zip_path = "/tmp/data.zip"
        self.csv_path = "/tmp/data.csv"
        self.csv_delimiter = ";"
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def data_url(self):
        return self.base_url

    def download_data(self):
        self.logger.debug("Downloading data...")
        r = requests.get(self.data_url, stream=True)
        with open(self.zip_path, "wb") as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)

    def extract_csv(self):
        self.logger.debug("Extracting CV...")
        zip_file = zipfile.ZipFile(self.zip_path)
        source_file_name = zip_file.namelist()[0]
        source = zip_file.open(source_file_name)
        target = open(self.csv_path, "wb")
        with source, target:
            shutil.copyfileobj(source, target)

    def get_latitude(self, east, north):
        # Axiliary values (% Bern)
        y_aux = (east - 600000) / 1000000
        x_aux = (north - 200000) / 1000000
        lat = (
            16.9023892
            + (3.238272 * x_aux)
            - (0.270978 * y_aux ** 2)
            - (0.002528 * x_aux ** 2)
            - (0.0447 * y_aux ** 2 * x_aux)
            - (0.0140 * x_aux ** 3)
        )

        # Unit 10000" to 1" and convert seconds to degrees (dec)
        lat = (lat * 100) / 36
        return lat

    def get_longitude(self, east, north):
        # Axiliary values (% Bern)
        y_aux = (east - 600000) / 1000000
        x_aux = (north - 200000) / 1000000
        lng = (
            2.6779094
            + (4.728982 * y_aux)
            + (0.791484 * y_aux * x_aux)
            + (0.1306 * y_aux * x_aux ** 2)
            - (0.0436 * y_aux ** 3)
        )

        # Unit 10000" to 1" and convert seconds to degrees (dec)
        lng = (lng * 100) / 36
        return lng

    def crawl(self):
        self.download_data()
        self.extract_csv()
        with open(self.csv_path, encoding="latin-1") as f:
            reader = csv.DictReader(f, delimiter=self.csv_delimiter)
            for item in reader:
                if item["Kantonskürzel"] == "LI":
                    # Skip Lichtenstein
                    continue
                yield {
                    "name": item["Ortschaftsname"],
                    "zip_code": int(item["PLZ"]),
                    "lang": item["Sprache"],
                    "state": item["Kantonskürzel"],
                    "bfs_nr": int(item["BFS-Nr"]),
                    "lat": self.get_latitude(float(item["E"]), float(item["N"])),
                    "long": self.get_longitude(float(item["E"]), float(item["N"])),
                }
