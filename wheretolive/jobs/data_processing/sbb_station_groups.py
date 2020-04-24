from ...aggregators import SBBStationGroupAggregator
from ...database import get_session, init_db, drop_table
from ...utils import BatchedDBInserter
from ...models import SBBStationGroup
import logging
import os


session = get_session()
drop_table(SBBStationGroup.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, session, batch_size=125)

logger.debug("Starting process...")
aggregator = SBBStationGroupAggregator(session)

logger.debug("Computing routes...")
sbb_station_groups = map(lambda x: SBBStationGroup(**x), aggregator.aggregate())
logger.debug("Inserting SBB station groups to database...")
inserter.insert(sbb_station_groups)

session.remove()
