from ..crawlers import GmapsCommuteCrawler
from ..models import Route
from ..database import get_session, init_db, drop_table
import logging
import os
from datetime import datetime

session = get_session()
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
crawler = GmapsCommuteCrawler(os.environ.get('MAPS_API_KEY'))

logger.debug('Getting Commute Times...')
commute_times = crawler.crawl()

logger.debug('Inserting Commute Times into database...')
start = datetime.now()
start_batch = datetime.now()

for commute_time in commute_times:
    print(commute_time)
    exit()