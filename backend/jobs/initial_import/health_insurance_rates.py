import logging
import os
from datetime import datetime

from flask import Blueprint

from ...crawlers import HealthInsuranceCrawler
from ...extensions import db
from ...models import HealthInsurance, HealthInsuranceRate

bp = Blueprint("initial_import.health_insurance_rates", __name__, cli_group=None)


@bp.cli.command("import_health_insurance_rates")
def run_job():
    HealthInsurance.__table__.drop(db.engine)
    HealthInsuranceRate.__table__.drop(db.engine)
    db.create_all()
    logger = logging.getLogger(os.path.basename(__file__))

    logger.debug("Starting process...")
    crawler = HealthInsuranceCrawler(db.session)
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
            db.session.query(HealthInsurance.id)
            .filter_by(name=health_insurace.name)
            .one_or_none()
        )

        if health_insurance_id is None:
            db.session.add(health_insurace)
            db.session.flush()
            health_insurance_id = health_insurace.id
        else:
            (health_insurance_id,) = health_insurance_id

        health_insurance_rate = HealthInsuranceRate(
            health_insurance_id=health_insurance_id,
            zip_code=health_insurance_rate["zip_code"],
            min_birth_year=health_insurance_rate["min_birth_year"],
            max_birth_year=health_insurance_rate["max_birth_year"],
            franchise=health_insurance_rate["franchise"],
            model=health_insurance_rate["model"],
            rate=health_insurance_rate["rate"],
        )

        db.session.add(health_insurance_rate)

        if idx % 5000 == 0 and idx > 0:
            now = datetime.now()
            logger.info(
                f"Health Insurance Rates crawled: {idx}\t"
                + f"Batch Time elapsed: {now-start_batch}\t"
                + f"Total Time elapsed: {now-start}"
            )
            db.session.commit()
            start_batch = now

    now = datetime.now()
    logger.info(
        f"Health Insurance Rates crawled: {idx}\t"
        + f"Batch Time elapsed: {now-start_batch}\t"
        + f"Total Time elapsed: {now-start}"
    )

    db.session.commit()
