from ...aggregators import CommuteTimeAggregator
from ...database import get_session
from ...utils import BatchedDBCommitter
import logging
import os


session = get_session()
logger = logging.getLogger(os.path.basename(__file__))

committer = BatchedDBCommitter(logger, session, batch_size=100)

logger.debug("Starting process...")
aggregator = CommuteTimeAggregator(session)

logger.debug("Computing routes...")
commutes = aggregator.aggregate()

logger.debug("Committing changes to database...")
committer.commit(commutes)

session.remove()
