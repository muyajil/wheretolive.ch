from ...aggregators import ClosestStationAggregator
from ...database import get_session
import logging
import os


session = get_session()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug("Starting process...")
aggregator = ClosestStationAggregator(session)

logger.debug("Finding closest stations...")
aggregator.aggregate()
