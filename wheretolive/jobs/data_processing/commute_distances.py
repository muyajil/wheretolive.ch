from ...models import Commute
from ...aggregators import CommuteAggregator
from ...utils import BatchedDBInserter
from ...webapp.app import db
import logging
import os


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
