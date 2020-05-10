import logging
import os

from flask import Blueprint

from ...aggregators import TaxRateEffectAggregator
from ...extensions import db
from ...models import TaxRateEffect
from ...utils import BatchedDBInserter

bp = Blueprint("data_processing.tax_rate_effects", __name__, cli_group=None)


@bp.cli.command("compute_tax_rate_effects")
def run_job():
    TaxRateEffect.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    inserter = BatchedDBInserter(logger, db.session, batch_size=50000)

    logger.debug("Starting process...")
    aggregator = TaxRateEffectAggregator(db.session)

    logger.debug("Getting TaxRateEffects...")
    tax_rate_effects = map(lambda x: TaxRateEffect(**x), aggregator.aggregate())
    logger.debug("Inserting tax rates into database...")
    inserter.insert(tax_rate_effects)
