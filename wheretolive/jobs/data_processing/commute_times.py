from ...aggregators import CommuteTimeAggregator
from ...database import get_session, init_db, drop_table
from ...utils import BatchedDBInserter
from ...models import TrainCommute
import logging
import os


session = get_session()
drop_table(TrainCommute.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, session, batch_size=10)

logger.debug("Starting process...")
aggregator = CommuteTimeAggregator(session)

logger.debug("Computing routes...")
commutes = map(lambda x: TrainCommute(**x), aggregator.aggregate())
logger.debug("Inserting train commutes to database...")
inserter.insert(commutes)

session.remove()
