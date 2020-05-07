import logging
import os

from flask import Blueprint

from ...aggregators import SBBConnectionAggregator
from ...models import SBBConnection
from ...utils import BatchedDBInserter
from ...webapp.extensions import db

bp = Blueprint("data_processing.sbb_connections", __name__, cli_group=None)


@bp.cli.command("compute_sbb_connections")
def run_job():
    SBBConnection.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    inserter = BatchedDBInserter(logger, db.session, batch_size=50000)

    logger.debug("Starting process...")
    aggregator = SBBConnectionAggregator(db.session)

    logger.debug("Getting SBBConnections...")
    sbb_connections = map(lambda x: SBBConnection(**x), aggregator.aggregate())
    logger.debug("Inserting connections into database...")
    inserter.insert(sbb_connections)
