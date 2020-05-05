from ...crawlers import FTTHCrawler
from ...database import get_session
from ...utils import BatchedDBCommitter
import logging
import os


session = get_session()
logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, session, batch_size=400)

logger.debug("Starting process...")
crawler = FTTHCrawler(session)

logger.debug("Computing routes...")
accomodations = crawler.crawl()
logger.debug("Committing FTTH information to database...")
committer.commit(accomodations)

session.remove()
