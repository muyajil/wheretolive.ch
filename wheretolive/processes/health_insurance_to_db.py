from ..crawlers import HealthInsuranceCrawler
from ..models import HealthInsurance, HealthInsuranceRate
from ..database import get_session, init_db, drop_table
import logging
import os

session = get_session()
drop_table(HealthInsurance.__table__)
drop_table(HealthInsuranceRate.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting process...')
crawler = HealthInsuranceCrawler()
logger.debug('Getting Health Insurance Rates...')
health_insurance_rates = crawler.crawl()
logger.debug('Inserting Health Insurance Rates into database...')
for health_insurance_rate in health_insurance_rates:
    