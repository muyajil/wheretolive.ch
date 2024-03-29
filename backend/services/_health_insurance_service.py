from datetime import datetime

from sqlalchemy.sql import func

from ..models import HealthInsuranceRate


class HealthInsuranceService:
    def set_max_birth_year(self, person):
        cur_year = datetime.now().year
        if cur_year - person["birthYear"] <= 18:
            person["maxBirthYear"] = cur_year - 18
        elif cur_year - person["birthYear"] <= 25:
            person["maxBirthYear"] = cur_year - 25
        else:
            person["maxBirthYear"] = 1940
        return person

    def get_health_insurance_cost(self, relevant_zip_codes, health_info):
        health_insurance_cost = {}
        people = list(map(lambda x: self.set_max_birth_year(x), health_info["people"]))
        max_birth_years = list(map(lambda x: x["maxBirthYear"], people))
        franchises = set(map(lambda x: x["franchise"], people))
        rates = (
            HealthInsuranceRate.query.with_entities(
                HealthInsuranceRate.zip_code,
                HealthInsuranceRate.max_birth_year,
                HealthInsuranceRate.franchise,
                func.avg(HealthInsuranceRate.rate),
            )
            .filter(HealthInsuranceRate.zip_code.in_(relevant_zip_codes))
            .filter(HealthInsuranceRate.franchise.in_(franchises))
            .filter(HealthInsuranceRate.max_birth_year.in_(max_birth_years))
            .group_by(
                HealthInsuranceRate.zip_code,
                HealthInsuranceRate.max_birth_year,
                HealthInsuranceRate.franchise,
            )
        )
        for rate in rates:
            if rate[0] not in health_insurance_cost:
                health_insurance_cost[rate[0]] = 0
            for person in people:
                if rate[1] == person["maxBirthYear"] and rate[2] == person["franchise"]:
                    health_insurance_cost[rate[0]] += rate[3] * 12

        return health_insurance_cost
