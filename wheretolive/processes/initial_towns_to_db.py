from ..models import Town
from ..database import get_session, init_db, drop_table
from ..crawlers import TownsCrawler
import logging
import os
from datetime import datetime

session = get_session()
drop_table(Town.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug("Starting process...")
crawler = TownsCrawler()

logger.debug("Getting towns...")
towns = crawler.crawl()

logger.debug("Inserting towns into database...")
start = datetime.now()
for idx, town in enumerate(towns):

    if (
        session.query(Town)
        .filter_by(zip_code=town["zip_code"], name=town["name"], bfs_nr=town["bfs_nr"])
        .one_or_none()
        is None
    ):
        town = Town(**town)
        session.add(town)

now = datetime.now()
logger.info(f"Towns crawled: {idx}\tTotal Time elapsed: {now-start}")

session.commit()
session.remove()
