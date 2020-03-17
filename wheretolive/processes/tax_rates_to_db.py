from ..crawlers import TaxRateCrawler
from ..models import TaxRate
from ..database import get_session, init_db, drop_table
import logging
import os

session = get_session()
drop_table(TaxRate.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
crawler = TaxRateCrawler()

logger.debug('Getting Tax Rates...')
tax_rates = crawler.crawl()

logger.debug('Inserting tax rates into database...')
for tax_rate in tax_rates:
    tax_rate = TaxRate(**tax_rate)
    session.add(tax_rate)
session.commit()
session.remove()
