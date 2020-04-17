from ...models import TaxRatePredicted
from ...aggregators import TaxRateAggregator
from ...database import get_session, init_db, drop_table
from ...utils import BatchedDBInserter
import logging
import os


session = get_session()
drop_table(TaxRatePredicted.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

inserter = BatchedDBInserter(logger, session, batch_size=50000)

logger.debug("Starting process...")
aggregator = TaxRateAggregator(session)

logger.debug("Getting TaxRatePredicted...")
tax_rates_predicted = map(lambda x: TaxRatePredicted(**x), aggregator.aggregate())
logger.debug("Inserting tax rates into database...")
inserter.insert(tax_rates_predicted)

session.remove()
