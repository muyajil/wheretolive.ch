import logging
import os

from flask import Blueprint

from ...crawlers.shopping import AldiStoreCrawler
from ...extensions import db
from ...utils import BatchedDBCommitter

bp = Blueprint("enrichtment.aldi", __name__, cli_group=None)


@bp.cli.command("import_aldi_stores")
def run_job():
    logger = logging.getLogger(os.path.basename(__file__))

    committer = BatchedDBCommitter(logger, db.session, batch_size=10)

    logger.debug("Starting process...")
    crawler = AldiStoreCrawler(db.session)

    logger.debug("Computing routes...")
    towns = crawler.crawl()
    logger.debug("Committing Aldi Store availability information to database...")
    committer.commit(towns)
