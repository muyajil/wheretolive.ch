from ...crawlers.shopping import AldiStoreCrawler
from ...database import get_session
from ...utils import BatchedDBCommitter
import logging
import os


session = get_session()
logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, session, batch_size=10)

logger.debug("Starting process...")
crawler = AldiStoreCrawler(session)

logger.debug("Computing routes...")
towns = crawler.crawl()
logger.debug("Committing Aldi Store availability information to database...")
committer.commit(towns)

session.remove()
