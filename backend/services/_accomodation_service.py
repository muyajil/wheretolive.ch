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

    def get_average_home_cost(self, relevant_zip_codes, accomodation_info):
        average_prices = (
            Accomodation.query.with_entities(
                Accomodation.zip_code,
                Accomodation.is_rent,
                func.avg(Accomodation.price),
                func.count(Accomodation.price),
            )
            .filter(Accomodation.zip_code.in_(relevant_zip_codes))
            .filter(
                ~Accomodation.property_type_id.in_(
                    [5, 8, 9, 10, 23, 24, 25, 26, 27, 28]
                )
            )
            .filter(Accomodation.price > 0)
            .filter(Accomodation.is_rent.is_(accomodation_info["isRent"]))
        )

        if accomodation_info["minRooms"] is not None:
            average_prices = average_prices.filter(
                Accomodation.rooms >= accomodation_info["minRooms"]
            )

        if accomodation_info["maxRooms"] is not None:
            average_prices = average_prices.filter(
                Accomodation.rooms <= accomodation_info["maxRooms"]
            )

        if accomodation_info["minArea"] is not None:
            average_prices = average_prices.filter(
                Accomodation.area >= accomodation_info["minArea"]
            )

        if accomodation_info["maxArea"] is not None:
            average_prices = average_prices.filter(
                Accomodation.rooms <= accomodation_info["maxArea"]
            )

        average_prices = average_prices.group_by(
            Accomodation.zip_code, Accomodation.is_rent
        ).order_by(Accomodation.zip_code)
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

        average_home_cost[cur_zip] = weighted_sum / total_obs

        return average_home_cost

    def get_accomodations(self, accomodation_info):
        accomodations = (
            Accomodation.query.filter(
                Accomodation.zip_code.in_(accomodation_info["zipCodes"])
            )
            .filter(Accomodation.is_rent.is_(accomodation_info["isRent"]))
            .filter(Accomodation.is_active.is_(True))
            .filter(
                ~Accomodation.property_type.in_([5, 8, 9, 10, 23, 24, 25, 26, 27, 28])
            )
        )

        if accomodation_info["minRooms"] is not None:
            accomodations = accomodations.filter(
                Accomodation.rooms >= accomodation_info["minRooms"]
            )

        if accomodation_info["maxRooms"] is not None:
            accomodations = accomodations.filter(
                Accomodation.rooms <= accomodation_info["maxRooms"]
            )

        if accomodation_info["minArea"] is not None:
            accomodations = accomodations.filter(
                Accomodation.area >= accomodation_info["minArea"]
            )

        if accomodation_info["maxArea"] is not None:
            accomodations = accomodations.filter(
                Accomodation.rooms <= accomodation_info["maxArea"]
            )

        accomodations = [
            {
                "zipCode": x.zip_code,
                "rooms": x.rooms,
                "area": x.area,
                "originalLink": "https://www.comparis.ch/immobilien/marktplatz/details/show/"
                + x.comparis_id,
                "imageUrl": x.image_url,
                "price": x.price,
                "ftthAvailable": x.ftth_available,
                "maxUpload": x.max_upload,
                "maxDownload": x.max_download,
                "lastSeen": x.last_seen,
                "townName": x.town_name,
                "streetName": x.street_name,
                "houseNumber": x.house_number,
            }
            for x in accomodations
        ]
