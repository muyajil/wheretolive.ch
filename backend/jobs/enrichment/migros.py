import logging
import os

from flask import Blueprint

from ...crawlers.shopping import MigrosStoreCrawler
from ...extensions import db
from ...utils import BatchedDBCommitter

bp = Blueprint("enrichment.migros", __name__, cli_group=None)


@bp.cli.command("import_migros_stores")
def run_job():
    logger = logging.getLogger(os.path.basename(__file__))

    committer = BatchedDBCommitter(logger, db.session, batch_size=500)

    logger.debug("Starting process...")
    crawler = MigrosStoreCrawler(db.session)

    logger.debug("Computing routes...")
    towns = crawler.crawl()
    logger.debug("Committing Migros Store availability information to database...")
    committer.commit(towns)
