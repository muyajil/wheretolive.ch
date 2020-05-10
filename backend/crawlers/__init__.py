from ._accomodations_crawler import AccomodationsCrawler
from ._ftth_crawler import FTTHCrawler
from ._health_insurance_crawler import HealthInsuranceCrawler
from ._sbb_timetable_crawler import SBBTimetableCrawler
from ._tax_rate_crawler import TaxRateCrawler
from ._towns_crawler import TownsCrawler

__all__ = [
    "HealthInsuranceCrawler",
    "TownsCrawler",
    "TaxRateCrawler",
    "AccomodationsCrawler",
    "SBBTimetableCrawler",
    "FTTHCrawler",
]
