import logging
import os

from flask import Blueprint

from ...aggregators import TrainCommuteAggregator
from ...extensions import db
from ...models import TrainCommute
from ...utils import BatchedDBInserter

bp = Blueprint("data_processing.train_commutes", __name__, cli_group=None)


@bp.cli.command("compute_train_commutes")
def run_job():
    TrainCommute.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    inserter = BatchedDBInserter(logger, db.session, batch_size=400)

    logger.debug("Starting process...")
    aggregator = TrainCommuteAggregator(db.session)

    logger.debug("Computing routes...")
    commutes = map(lambda x: TrainCommute(**x), aggregator.aggregate())
    logger.debug("Inserting train commutes to database...")
    inserter.insert(commutes)
