import logging
import os

from flask import Blueprint

from ...aggregators import CommuteAggregator
from ...extensions import db
from ...models import Commute
from ...utils import BatchedDBInserter

bp = Blueprint("data_processing.commute_distances", __name__, cli_group=None)


@bp.cli.command("compute_commute_distances")
def run_job():
    Commute.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    inserter = BatchedDBInserter(logger, db.session, batch_size=50000)

    logger.debug("Starting process...")
    aggregator = CommuteAggregator(db.session)

    logger.debug("Mapping Switzerland...")
    commutes = map(lambda x: Commute(**x), aggregator.aggregate())
    logger.debug("Inserting routes into database")
    inserter.insert(commutes)
