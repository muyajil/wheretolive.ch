from ...models import TaxRateEffect
from ...aggregators import TaxRateEffectAggregator
from ...utils import BatchedDBInserter
from ...webapp.app import db
import logging
import os


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
