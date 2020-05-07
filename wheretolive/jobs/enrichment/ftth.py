import logging
import os

from flask import Blueprint

from ...crawlers import FTTHCrawler
from ...utils import BatchedDBCommitter
from ...webapp.extensions import db

bp = Blueprint("enrichment.ftth", __name__, cli_group=None)


@bp.cli.command("update_ftth")
def run_job():
    logger = logging.getLogger(os.path.basename(__file__))

    committer = BatchedDBCommitter(logger, db.session, batch_size=10)

    logger.debug("Starting process...")
    crawler = FTTHCrawler(db.session)

    logger.debug("Computing routes...")
    accomodations = crawler.crawl()
    logger.debug("Committing FTTH information to database...")
    committer.commit(accomodations)
