from ..crawlers import TaxRateCrawler
from ..models import TaxRate
from ..database import get_session, init_db, drop_table
from ..utils import BatchedDBInserter
import logging
import os


session = get_session()
drop_table(TaxRate.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, session)

logger.debug("Starting process...")
crawler = TaxRateCrawler()

logger.debug("Getting Tax Rates...")
tax_rates = map(lambda x: TaxRate(**x), crawler.crawl())
logger.debug("Inserting tax rates into database...")
inserter.insert(tax_rates)

session.remove()
