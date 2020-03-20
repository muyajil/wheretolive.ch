from ..crawlers import AccomodationsCrawler
from ..models import Accomodation
from ..database import get_session, init_db, drop_table
import logging
import os
from datetime import datetime

session = get_session()
drop_table(Accomodation.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug("Starting process...")
crawler = AccomodationsCrawler()

logger.debug("Getting Accomodations...")
accomodations = crawler.crawl()

logger.debug("Inserting Accomodations into database...")
start = datetime.now()
start_batch = datetime.now()

for idx, accomodation in enumerate(accomodations):
    if (
        session.query(Accomodation)
        .filter_by(comparis_id=accomodation["comparis_id"])
        .one_or_none()
        is None
    ):
        accomodation = Accomodation(**accomodation)
        session.add(accomodation)
    if idx % 100 == 0 and idx > 0:
        now = datetime.now()
        logger.info(
            f"Listings crawled: {idx}\tBatch Time elapsed: {now-start_batch}\tTotal Time elapsed: {now-start}"
        )
        session.commit()
        start_batch = now
now = datetime.now()
logger.info(
    f"Listings crawled: {idx}\tBatch Time elapsed: {now-start_batch}\tTotal Time elapsed: {now-start}"
)
session.commit()
session.remove()
