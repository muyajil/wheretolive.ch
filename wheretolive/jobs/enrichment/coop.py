from ...crawlers.shopping import CoopStoreCrawler
from ...utils import BatchedDBCommitter
from ...webapp.app import db
import logging
import os


logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, db.session, batch_size=500)

logger.debug("Starting process...")
crawler = CoopStoreCrawler(db.session)

logger.debug("Computing routes...")
towns = crawler.crawl()
logger.debug("Committing Coop Store availability information to database...")
committer.commit(towns)
