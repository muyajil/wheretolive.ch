from ...aggregators import SBBStationGroupAggregator
from ...utils import BatchedDBInserter
from ...models import SBBStationGroup
from ...webapp.app import db
import logging
import os


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
