from ...crawlers import TaxRateCrawler
from ...models import TaxRate
from ...webapp.app import db
from ...utils import BatchedDBInserter
import logging
import os


TaxRate.__table__.drop(db.engine)
db.create_all()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, db.session, batch_size=50000)

logger.debug("Starting process...")
crawler = TaxRateCrawler()

logger.debug("Getting Tax Rates...")
tax_rates = map(lambda x: TaxRate(**x), crawler.crawl())
logger.debug("Inserting tax rates into database...")
inserter.insert(tax_rates)
