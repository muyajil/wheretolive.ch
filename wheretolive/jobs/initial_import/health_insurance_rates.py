from ...crawlers import HealthInsuranceCrawler
from ...models import HealthInsurance, HealthInsuranceRate
from ...database import get_session, init_db, drop_table
import logging
import os
from datetime import datetime

session = get_session()
drop_table(HealthInsurance.__table__)
drop_table(HealthInsuranceRate.__table__)
init_db()
logger = logging.getLogger(os.path.basename(__file__))

logger.debug("Starting process...")
crawler = HealthInsuranceCrawler(session)
logger.debug("Getting Health Insurance Rates...")
health_insurance_rates = crawler.crawl()
logger.debug("Inserting Health Insurance Rates into database...")
start = datetime.now()
start_batch = datetime.now()
for idx, health_insurance_rate in enumerate(health_insurance_rates):
    health_insurace = HealthInsurance(
        name=health_insurance_rate["name"].lower(),
        name_capitalized=health_insurance_rate["name"],
        url=health_insurance_rate["url"],
    )

    health_insurance_id = (
        session.query(HealthInsurance.id)
        .filter_by(name=health_insurace.name)
        .one_or_none()
    )

    if health_insurance_id is None:
        session.add(health_insurace)
        session.flush()
        health_insurance_id = health_insurace.id
    else:
        (health_insurance_id,) = health_insurance_id

    health_insurance_rate = HealthInsuranceRate(
        health_insurance_id=health_insurance_id,
        zip_code=health_insurance_rate["zip_code"],
        birth_year=health_insurance_rate["birth_year"],
        franchise=health_insurance_rate["franchise"],
        model=health_insurance_rate["model"],
        rate=health_insurance_rate["rate"],
    )

    session.add(health_insurance_rate)

    if idx % 5000 == 0 and idx > 0:
        now = datetime.now()
        logger.info(
            f"Health Insurance Rates crawled: {idx}\t"
            + f"Batch Time elapsed: {now-start_batch}\t"
            + f"Total Time elapsed: {now-start}"
        )
        session.commit()
        start_batch = now

now = datetime.now()
logger.info(
    f"Health Insurance Rates crawled: {idx}\t"
    + f"Batch Time elapsed: {now-start_batch}\t"
    + f"Total Time elapsed: {now-start}"
)

session.commit()
session.remove()
