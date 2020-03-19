from ..models import Route
from ..aggregators import RouteAggregator
from ..database import get_session, init_db, drop_table
import logging
import os
from datetime import datetime

session = get_session()
drop_table(Route.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
aggregator = RouteAggregator(session)

logger.debug('Mapping Switzerland...')
routes = aggregator.aggregate()

logger.debug('Inserting routes into database')
start = datetime.now()
start_batch = datetime.now()
for idx, route in enumerate(routes):
    route = Route(**route)
    session.add(route)
    if idx % 50000 == 0 and idx > 0:
        now = datetime.now()
        logger.info(
            f'Routes aggregated: {idx}\tBatch Time elapsed: {now-start_batch}\tTotal Time elapsed: {now-start}')
        session.commit()
        start_batch = now
session.commit()
session.remove()
