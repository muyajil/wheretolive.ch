import logging
import os

from flask import Blueprint

from ...crawlers.shopping import LidlStoreCrawler
from ...extensions import db
from ...utils import BatchedDBCommitter

bp = Blueprint("enrichment.lidl", __name__, cli_group=None)


@bp.cli.command("import_lidl_stores")
def run_job():
    logger = logging.getLogger(os.path.basename(__file__))

    committer = BatchedDBCommitter(logger, db.session, batch_size=500)

    logger.debug("Starting process...")
    crawler = LidlStoreCrawler(db.session)

    logger.debug("Computing routes...")
    towns = crawler.crawl()
    logger.debug("Committing Lidl Store availability information to database...")
    committer.commit(towns)
