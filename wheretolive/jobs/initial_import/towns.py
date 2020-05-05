from ...models import Town
from ...crawlers import TownsCrawler
from ...webapp.app import db
import logging
import os
from datetime import datetime

Town.__table__.drop(db.engine)
db.create_all()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug("Starting process...")
crawler = TownsCrawler()

logger.debug("Getting towns...")
towns = crawler.crawl()

logger.debug("Inserting towns into database...")
start = datetime.now()
for idx, town in enumerate(towns):

    if (
        db.session.query(Town)
        .filter_by(zip_code=town["zip_code"], name=town["name"], bfs_nr=town["bfs_nr"])
        .one_or_none()
        is None
    ):
        town = Town(**town)
        db.session.add(town)

now = datetime.now()
logger.info(f"Towns crawled: {idx}\tTotal Time elapsed: {now-start}")

db.session.commit()
