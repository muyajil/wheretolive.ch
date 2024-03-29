import logging
import time

import requests

from ..models import Accomodation


class FTTHCrawler:
    def __init__(self, db_session):
        self.base_url = "https://api.init7.net/check/address"
        self.db_session = db_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def crawl(self):
        accomodations = (
            self.db_session.query(Accomodation)
            .filter(~Accomodation.house_number.is_(None))
            .filter(~Accomodation.street_name.is_(None))
            .filter(Accomodation.ftth_available.is_(None))
            .filter(Accomodation.street_name != "")
        )
        self.logger.info(
            f"Found {accomodations.count()} listings with missing information"
        )
        for acc in accomodations:
            time.sleep(0.1)
            url = f"{self.base_url}/{acc.zip_code}/{acc.street_name.strip()}/{acc.house_number}"
            try:
                result = requests.get(url).json()
                if "Q03" in map(lambda x: x["code"], result["messages"]):
                    acc.ftth_available = False
                elif result["fiber"]:
                    acc.ftth_available = True
                    acc.max_upload = 1000
                    acc.max_download = 1000
                else:
                    acc.ftth_available = False
                    acc.max_download = result["vdsl_down"] / 1000
                    acc.max_upload = result["vdsl_up"] / 1000
            except:  # noqa: E722
                acc.ftth_available = False
                self.logger.error(
                    f"Problem with getting FTTH Info for accomodation {acc.comparis_id}"
                )
            yield acc
