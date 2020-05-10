import logging
import os

from flask import Blueprint

from ...crawlers import SBBTimetableCrawler
from ...extensions import db
from ...models import (
    SBBCalendar,
    SBBRoute,
    SBBStation,
    SBBStopTime,
    SBBTransfer,
    SBBTrip,
)
from ...utils import BatchedDBInserter

bp = Blueprint("initial_import.sbb_timetable", __name__, cli_group=None)


@bp.cli.command("import_sbb_timetable")
def run_job():
    SBBStation.__table__.drop(db.engine)
    SBBStopTime.__table__.drop(db.engine)
    SBBTrip.__table__.drop(db.engine)
    SBBRoute.__table__.drop(db.engine)
    SBBCalendar.__table__.drop(db.engine)
    SBBTransfer.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    inserter = BatchedDBInserter(logger, db.session, batch_size=50000)

    logger.debug("Starting process...")
    crawler = SBBTimetableCrawler()

    logger.debug("Getting Stations...")
    stations = map(lambda x: SBBStation(**x), crawler.crawl_stops())
    logger.debug("Inserting Stations into Database...")
    inserter.insert(stations)

    logger.debug("Getting Stop Times...")
    stop_times = map(lambda x: SBBStopTime(**x), crawler.crawl_stop_times())
    logger.debug("Inserting Stop Times into Database...")
    inserter.insert(stop_times)

    logger.debug("Getting Trips...")
    trips = map(lambda x: SBBTrip(**x), crawler.crawl_trips())
    logger.debug("Inserting Trips into Database...")
    inserter.insert(trips)

    logger.debug("Getting Routes...")
    routes = map(lambda x: SBBRoute(**x), crawler.crawl_routes())
    logger.debug("Inserting Routes into Database...")
    inserter.insert(routes)

    logger.debug("Getting Calendar...")
    calendars = map(lambda x: SBBCalendar(**x), crawler.crawl_calendar())
    logger.debug("Inserting Calendar into Database...")
    inserter.insert(calendars)

    logger.debug("Getting Transfers...")
    transfers = map(lambda x: SBBTransfer(**x), crawler.crawl_transfers())
    logger.debug("Inserting Transfers into Database...")
    inserter.insert(transfers)
