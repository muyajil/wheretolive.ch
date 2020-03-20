from ..models import Commute
from ..aggregators import CommuteAggregator
from ..database import get_session, init_db, drop_table
from ..utils import BatchedDBInserter
import logging
import os


session = get_session()
drop_table(Commute.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, session, batch_size=50000)

logger.debug("Starting process...")
aggregator = CommuteAggregator(session)

logger.debug("Mapping Switzerland...")
commutes = map(lambda x: Commute(**x), aggregator.aggregate())
logger.debug("Inserting routes into database")
inserter.insert(commutes)

session.remove()
