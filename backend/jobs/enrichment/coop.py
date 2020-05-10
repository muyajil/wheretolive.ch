import logging
import os

from flask import Blueprint

from ...crawlers.shopping import CoopStoreCrawler
from ...extensions import db
from ...utils import BatchedDBCommitter

bp = Blueprint("enrichment.coop", __name__, cli_group=None)


@bp.cli.command("import_coop_stores")
def run_job():
    logger = logging.getLogger(os.path.basename(__file__))

    committer = BatchedDBCommitter(logger, db.session, batch_size=500)

    logger.debug("Starting process...")
    crawler = CoopStoreCrawler(db.session)

    logger.debug("Computing routes...")
    towns = crawler.crawl()
    logger.debug("Committing Coop Store availability information to database...")
    committer.commit(towns)
