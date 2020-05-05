from ...models import SBBConnection
from ...aggregators import SBBConnectionAggregator
from ...utils import BatchedDBInserter
from ...webapp.app import db
import logging
import os


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
