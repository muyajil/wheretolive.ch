import json


class Switzerland():

    def __init__(self,
                 mode='json',
                 towns_by_zip_path=None,
                 neighborhoods_by_zip_path=None,
                 tax_rates_by_bfs_nr_path=None):
        self.mode = mode
        self.towns_by_zip_path = towns_by_zip_path
        self.towns_by_zip = None
        self.neighborhoods_by_zip_path = neighborhoods_by_zip_path
        self.neighborhoods_by_zip = None
        self.tax_rates_by_bfs_nr_path = tax_rates_by_bfs_nr_path
        self.tax_rates_by_bfs_nr = None

    @property
    def zip_codes(self):
        if self.towns_by_zip is None:
            self.towns_by_zip = json.load(open(self.towns_by_zip_path))

        return list(self.towns_by_zip.keys())
