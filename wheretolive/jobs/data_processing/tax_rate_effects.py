from ...models import TaxRateEffect
from ...aggregators import TaxRateEffectAggregator
from ...database import get_session, init_db, drop_table
from ...utils import BatchedDBInserter
import logging
import os


session = get_session()
drop_table(TaxRateEffect.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, session, batch_size=50000)

logger.debug("Starting process...")
aggregator = TaxRateEffectAggregator(session)

logger.debug("Getting TaxRateEffects...")
tax_rate_effects = map(lambda x: TaxRateEffect(**x), aggregator.aggregate())
logger.debug("Inserting tax rates into database...")
inserter.insert(tax_rate_effects)

session.remove()
