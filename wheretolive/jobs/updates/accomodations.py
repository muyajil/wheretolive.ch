from ...crawlers import AccomodationsCrawler
from ...models import Accomodation
from ...database import get_session, init_db
import logging
import os
from datetime import datetime

session = get_session()
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug("Starting process...")
crawler = AccomodationsCrawler(session)

logger.debug("Getting Accomodations...")
accomodations = crawler.crawl()

logger.debug("Inserting Accomodations into database...")
start = datetime.now()
start_batch = datetime.now()

# Insert or Update active listings
for idx, accomodation in enumerate(accomodations):
    acc = (
        session.query(Accomodation)
        .filter_by(comparis_id=accomodation["comparis_id"])
        .one_or_none()
    )
    if acc is None:
        accomodation = Accomodation(**accomodation)
        session.add(accomodation)
    else:
        for k, v in accomodation.items():
            setattr(acc, k, v)
    if idx % 10 == 0 and idx > 0:
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

# Update listings that are not active anymore
old_listings = session.query(Accomodation).filter(Accomodation.last_seen < start)
for old_listing in old_listings:
    old_listing.is_active = False
session.commit()
logger.info(f"Marked {old_listings.count()} listings as not active anymore")
session.remove()