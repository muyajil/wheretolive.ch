from ..crawlers import TaxRateCrawler
from ..json_savers import FileJsonSaver
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
mapper = TaxRateCrawler()
logger.debug('Getting Tax Rates...')
tax_rates_by_bfs_nr = mapper.crawl()
logger.debug('Saving tax_rates_by_bfs_nr...')
saver = FileJsonSaver()
saver.save('/home/muy/repositories/wheretolive.ch/tax_rates_by_bfs_nr.json', tax_rates_by_bfs_nr)