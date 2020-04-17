from ...models import SBBConnection
from ...aggregators import SBBConnectionAggregator
from ...database import get_session, init_db, drop_table
from ...utils import BatchedDBInserter
import logging
import os


session = get_session()
drop_table(SBBConnection.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, session, batch_size=50000)

logger.debug("Starting process...")
aggregator = SBBConnectionAggregator(session)

logger.debug("Getting SBBConnections...")
sbb_connections = map(lambda x: SBBConnection(**x), aggregator.aggregate())
logger.debug("Inserting connections into database...")
inserter.insert(sbb_connections)

session.remove()
