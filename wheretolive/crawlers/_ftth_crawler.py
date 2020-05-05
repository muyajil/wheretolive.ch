from ..models import Accomodation
import logging
import requests


class FTTHCrawler:
    def __init__(self, db_session):
        self.base_url = "https://api.init7.net/check/address"
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def crawl(self):
        accomodations = self.db_session.query(Accomodation).filter(
            ~Accomodation.house_number.is_(None)
            and ~Accomodation.street_name.is_(None)
            and Accomodation.ftth_available.is_(None)
        )

        for acc in accomodations:
            url = f"{self.base_url}/{acc.zip_code}/{acc.street_name}/{acc.house_number}"
            result = requests.get(url).json
            if result["fiber"]:
                acc.ftth_available = True
                acc.max_upload = 1000
                acc.max_download = 1000
            else:
                acc.ftth_available = False
                acc.max_upload = result["vdsl_down"] / 1000
                acc.max_download = result["vdsl_up"] / 1000
            yield acc
