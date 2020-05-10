import logging
import os

from flask import Blueprint

from ...aggregators import SBBStationGroupAggregator
from ...extensions import db
from ...models import SBBStationGroup
from ...utils import BatchedDBInserter

bp = Blueprint("data_processing.sbb_station_groups", __name__, cli_group=None)


@bp.cli.command("compute_sbb_station_groups")
def run_job():
    SBBStationGroup.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    inserter = BatchedDBInserter(logger, db.session, batch_size=125)

    logger.debug("Starting process...")
    aggregator = SBBStationGroupAggregator(db.session)

    logger.debug("Computing routes...")
    sbb_station_groups = map(lambda x: SBBStationGroup(**x), aggregator.aggregate())
    logger.debug("Inserting SBB station groups to database...")
    inserter.insert(sbb_station_groups)
