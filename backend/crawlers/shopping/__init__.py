from ._aldi_store_crawler import AldiStoreCrawler
from ._coop_store_crawler import CoopStoreCrawler
from ._lidl_store_crawler import LidlStoreCrawler
from ._migros_store_crawler import MigrosStoreCrawler

__all__ = [
    "MigrosStoreCrawler",
    "CoopStoreCrawler",
    "LidlStoreCrawler",
    "AldiStoreCrawler",
]
