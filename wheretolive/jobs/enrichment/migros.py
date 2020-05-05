from ...crawlers.shopping import MigrosStoreCrawler
from ...webapp.app import db
from ...utils import BatchedDBCommitter
import logging
import os


logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, db.session, batch_size=500)

logger.debug("Starting process...")
crawler = MigrosStoreCrawler(db.session)

logger.debug("Computing routes...")
towns = crawler.crawl()
logger.debug("Committing Migros Store availability information to database...")
committer.commit(towns)
