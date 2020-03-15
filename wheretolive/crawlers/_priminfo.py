from datetime import datetime
from ..country import SwitzerlandInfo


class PriminfoCrawler():

    def __init__(self):
        pass

    @property
    def base_url(self):
        return "https://www.priminfo.admin.ch/de/praemien"

    @property
    def ranges(self):
        return {
            "birth_year":  [x for x in range(datetime.now().year - 80, datetime.now().year)],
        }

    def compose_url(self, ranges):
        pass

    def crawl(self):
        pass
