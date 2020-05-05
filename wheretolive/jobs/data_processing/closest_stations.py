from ...aggregators import ClosestStationAggregator
from ...utils import BatchedDBCommitter
from ...webapp.app import db
import logging
import os


logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, db.session, batch_size=100)

logger.debug("Starting process...")
aggregator = ClosestStationAggregator(db.session)

logger.debug("Finding closest stations...")
towns = aggregator.aggregate()

logger.debug("Committing changes to database...")
committer.commit(towns)
