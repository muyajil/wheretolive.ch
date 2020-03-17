from ..models import Town
from ..database import get_session, init_db, drop_table
from ..crawlers import TownsCrawler
import logging
import os

session = get_session()
drop_table(Town.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
crawler = TownsCrawler()

logger.debug('Getting towns...')
towns_by_zip = crawler.crawl()

logger.debug('Inserting towns into database...')
for zip_code in towns_by_zip:
    town = Town(**towns_by_zip[zip_code])
    session.add(town)
session.commit()
session.remove()
