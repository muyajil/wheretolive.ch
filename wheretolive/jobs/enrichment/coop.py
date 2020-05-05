from ...crawlers.shopping import CoopStoreCrawler
from ...database import get_session
from ...utils import BatchedDBCommitter
import logging
import os


session = get_session()
logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, session, batch_size=500)

logger.debug("Starting process...")
crawler = CoopStoreCrawler(session)

logger.debug("Computing routes...")
towns = crawler.crawl()
logger.debug("Committing Coop Store availability information to database...")
committer.commit(towns)

session.remove()
