from ...aggregators import TrainCommuteAggregator
from ...utils import BatchedDBInserter
from ...models import TrainCommute
from ...webapp.app import db
import logging
import os


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
