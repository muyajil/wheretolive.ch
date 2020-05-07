import logging
import os

from flask import Blueprint

from ...crawlers import TaxRateCrawler
from ...models import TaxRate
from ...utils import BatchedDBInserter
from ...webapp.extensions import db

bp = Blueprint("initial_import.tax_rates", __name__, cli_group=None)


@bp.cli.command("import_tax_rates")
def run_job():
    TaxRate.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    inserter = BatchedDBInserter(logger, db.session, batch_size=50000)

    logger.debug("Starting process...")
    crawler = TaxRateCrawler()

    logger.debug("Getting Tax Rates...")
    tax_rates = map(lambda x: TaxRate(**x), crawler.crawl())
    logger.debug("Inserting tax rates into database...")
    inserter.insert(tax_rates)
