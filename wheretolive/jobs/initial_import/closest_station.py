from ...aggregators import ClosestStationAggregator
from ...utils import BatchedDBCommitter
from ...database import get_session
import logging
import os


session = get_session()
logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, session, batch_size=100)

logger.debug("Starting process...")
aggregator = ClosestStationAggregator(session)

logger.debug("Finding closest stations...")
towns = aggregator.aggregate()

logger.debug("Committing changes to database...")
committer.commit(towns)

session.remove()
