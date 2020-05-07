import logging
import os

from flask import Blueprint

from ...aggregators import ClosestStationAggregator
from ...utils import BatchedDBCommitter
from ...webapp.extensions import db

bp = Blueprint("data_processing.closest_stations", __name__, cli_group=None)


@bp.cli.command("compute_closest_stations")
def run_job():
    logger = logging.getLogger(os.path.basename(__file__))

    committer = BatchedDBCommitter(logger, db.session, batch_size=100)

    logger.debug("Starting process...")
    aggregator = ClosestStationAggregator(db.session)

    logger.debug("Finding closest stations...")
    towns = aggregator.aggregate()

    logger.debug("Committing changes to database...")
    committer.commit(towns)
