import logging
import os
from datetime import datetime

from flask import Blueprint

from ...crawlers import AccomodationsCrawler
from ...extensions import db
from ...models import Accomodation

bp = Blueprint("updates.accomodations", __name__, cli_group=None)


@bp.cli.command("update_accomodations")
def run_job():
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    logger.debug("Starting process...")
    crawler = AccomodationsCrawler(db.session)

    logger.debug("Getting Accomodations...")
    accomodations = crawler.crawl()

    logger.debug("Inserting Accomodations into database...")
    start = datetime.now()
    start_batch = datetime.now()

    # Insert or Update active listings
    for idx, accomodation in enumerate(accomodations):
        acc = (
            db.session.query(Accomodation)
            .filter_by(comparis_id=accomodation["comparis_id"])
            .one_or_none()
        )
        if acc is None:
            accomodation = Accomodation(**accomodation)
            db.session.add(accomodation)
        else:
            for k, v in accomodation.items():
                setattr(acc, k, v)
        if idx % 10 == 0 and idx > 0:
            now = datetime.now()
            logger.info(
                f"Listings crawled: {idx}\tBatch Time elapsed: {now-start_batch}\tTotal Time elapsed: {now-start}"
            )
            db.session.commit()
            start_batch = now
    now = datetime.now()
    logger.info(
        f"Listings crawled: {idx}\tBatch Time elapsed: {now-start_batch}\tTotal Time elapsed: {now-start}"
    )
    db.session.commit()

    # Update listings that are not active anymore
    old_listings = (
        db.session.query(Accomodation)
        .filter(Accomodation.last_seen < start)
        .filter(Accomodation.is_active.is_(True))
    )
    for old_listing in old_listings:
        old_listing.is_active = False
    db.session.commit()
    logger.info(f"Marked {old_listings.count()} listings as not active anymore")
