from sqlalchemy.sql import func

from ..models import Accomodation


class AccomodationService:
    def __init__(self):
        self.mortgage_rate = 0.01
        self.loan_percentage = 0.8
        self.maintenance_cost = 0.01

    def compute_yearly_cost_home(self, is_rent, price):
        if is_rent:
            return price * 12
        else:
            return (
                self.mortgage_rate * self.loan_percentage + self.maintenance_cost
            ) * price

    def get_average_home_cost(self, relevant_zip_codes, max_rooms, min_rooms):
        average_prices = (
            Accomodation.query.with_entities(
                Accomodation.zip_code,
                Accomodation.is_rent,
                func.avg(Accomodation.price),
                func.count(Accomodation.price),
            )
            .filter(Accomodation.zip_code.in_(relevant_zip_codes))
            .filter(Accomodation.rooms >= min_rooms)
            .filter(Accomodation.rooms <= max_rooms)
            .filter(
                ~Accomodation.property_type_id.in_(
                    [5, 8, 9, 10, 23, 24, 25, 26, 27, 28]
                )
            )
            .filter(Accomodation.price > 0)
            .group_by(Accomodation.zip_code, Accomodation.is_rent)
            .order_by(Accomodation.zip_code)
        )
        average_home_cost = {}
        cur_zip = ""
        weighted_sum = 0
        total_obs = 0
        for average_price in average_prices:
            if average_price[0] != cur_zip:
                if cur_zip != "":
                    average_home_cost[cur_zip] = weighted_sum / total_obs
                weighted_sum = 0
                total_obs = 0
                cur_zip = average_price[0]
            weighted_sum += (
                self.compute_yearly_cost_home(average_price[1], average_price[2])
                * average_price[3]
            )
            total_obs += average_price[3]

        return average_home_cost