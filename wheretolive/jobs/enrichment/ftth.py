from ...crawlers import FTTHCrawler
from ...utils import BatchedDBCommitter
from ...webapp.app import db
import logging
import os


logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, db.session, batch_size=10)

logger.debug("Starting process...")
crawler = FTTHCrawler(db.session)

logger.debug("Computing routes...")
accomodations = crawler.crawl()
logger.debug("Committing FTTH information to database...")
committer.commit(accomodations)
