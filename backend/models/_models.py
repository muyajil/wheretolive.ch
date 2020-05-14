from sqlalchemy import ARRAY

from ..extensions import db


class Town(db.Model):
    __tablename__ = "town"
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.Integer)
    bfs_nr = db.Column(db.Integer)
    name = db.Column(db.String)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    lang = db.Column(db.String)
    state = db.Column(db.String)
    closest_station_id = db.Column(db.String)
    closest_train_station_id = db.Column(db.String)
    migros = db.Column(db.Boolean)
    coop = db.Column(db.Boolean)
    lidl = db.Column(db.Boolean)
    aldi = db.Column(db.Boolean)


class TaxRate(db.Model):
    __tablename__ = "tax_rate"
    profile = db.Column(db.String, primary_key=True)
    bfs_nr = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, primary_key=True)
    state = db.Column(db.String, primary_key=True)
    min_income = db.Column(db.Integer, primary_key=True)
    max_income = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float)


class TaxRateEffect(db.Model):
    __tablename__ = "tax_rate_effect"
    bfs_nr = db.Column(db.Integer, primary_key=True)
    min_income = db.Column(db.Integer, primary_key=True)
    max_income = db.Column(db.Integer, primary_key=True)
    child_effect = db.Column(db.Float, primary_key=True)
    married_effect = db.Column(db.Float, primary_key=True)
    double_salary_effect = db.Column(db.Float, primary_key=True)


class Commute(db.Model):
    __tablename__ = "commute"
    id = db.Column(db.Integer, primary_key=True)
    source_town_id = db.Column(db.Integer)
    target_town_id = db.Column(db.Integer)
    distance = db.Column(db.Float)


class TrainCommute(db.Model):
    __tablename__ = "train_commute"
    commute_id = db.Column(db.Integer, primary_key=True)
    commute_type = db.Column(db.String, primary_key=True)
    time = db.Column(db.Integer)
    changes = db.Column(db.Integer)


class HealthInsurance(db.Model):
    __tablename__ = "health_insurance"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    name_capitalized = db.Column(db.String)
    url = db.Column(db.String)


class HealthInsuranceRate(db.Model):
    __tablename__ = "health_insurance_rate"
    health_insurance_id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.Integer, primary_key=True)
    min_birth_year = db.Column(db.Integer, primary_key=True)
    max_birth_year = db.Column(db.Integer, primary_key=True)
    franchise = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, primary_key=True)
    rate = db.Column(db.Float)


class Accomodation(db.Model):
    __tablename__ = "accomodation"
    comparis_id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean)
    zip_code = db.Column(db.Integer)
    town_name = db.Column(db.String)
    street_name = db.Column(db.String)
    house_number = db.Column(db.String)
    rooms = db.Column(db.Float)
    area = db.Column(db.Float)
    price = db.Column(db.Float)
    image_url = db.Column(db.String)
    is_rent = db.Column(db.Boolean)
    last_seen = db.Column(db.DateTime)
    property_type_id = db.Column(db.Integer)
    property_type = db.Column(db.String)
    original_publisher = db.Column(db.String)
    max_upload = db.Column(db.Integer)
    max_download = db.Column(db.Integer)
    ftth_available = db.Column(db.Boolean)


class SBBStation(db.Model):
    __tablename__ = "sbb_station"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    parent_station = db.Column(db.String)
    station_type = db.Column(db.String)


class SBBStationGroup(db.Model):
    __tablename__ = "sbb_station_group"
    sbb_station_id = db.Column(db.String, primary_key=True)
    sbb_station_group = db.Column(ARRAY(db.String))
    walking_times = db.Column(ARRAY(db.Integer))


class SBBStopTime(db.Model):
    __tablename__ = "sbb_stop_time"
    trip_id = db.Column(db.String, primary_key=True)
    station_id = db.Column(db.String, primary_key=True)
    stop_sequence = db.Column(db.Integer, primary_key=True)
    arrival_time = db.Column(db.Time)
    arrives_next_day = db.Column(db.Boolean)
    departure_time = db.Column(db.Time)
    departs_next_day = db.Column(db.Boolean)


class SBBTrip(db.Model):
    __tablename__ = "sbb_trip"
    trip_id = db.Column(db.String, primary_key=True)
    route_id = db.Column(db.String)
    service_id = db.Column(db.String)


class SBBRoute(db.Model):
    __tablename__ = "sbb_route"
    route_id = db.Column(db.String, primary_key=True)
    route_desc = db.Column(db.String)


class SBBCalendar(db.Model):
    __tablename__ = "sbb_calendar"
    service_id = db.Column(db.String, primary_key=True)
    monday = db.Column(db.Boolean)
    tuesday = db.Column(db.Boolean)
    wednesday = db.Column(db.Boolean)
    thursday = db.Column(db.Boolean)
    friday = db.Column(db.Boolean)
    saturday = db.Column(db.Boolean)
    sunday = db.Column(db.Boolean)


class SBBTransfer(db.Model):
    __tablename__ = "sbb_transfer"
    from_stop_id = db.Column(db.String, primary_key=True)
    to_stop_id = db.Column(db.String, primary_key=True)
    min_transfer_time = db.Column(db.Integer)


class SBBConnection(db.Model):
    __tablename__ = "sbb_connection"
    trip_id = db.Column(db.String, primary_key=True)
    from_stop_id = db.Column(db.String, primary_key=True)
    exact_from_stop_id = db.Column(db.String)
    departure_time = db.Column(db.Time, primary_key=True)
    departs_next_day = db.Column(db.Boolean, primary_key=True)
    to_stop_id = db.Column(db.String, primary_key=True)
    exact_to_stop_id = db.Column(db.String)
    arrival_time = db.Column(db.Time, primary_key=True)
    arrives_next_day = db.Column(db.Boolean, primary_key=True)
    sequence_nr = db.Column(db.Integer, primary_key=True)


class ClosestStationCommute(db.Model):
    __tablename__ = "agg_closest_station_commute"
    source_town_id = db.Column(db.Integer, primary_key=True)
    source_zip_code = db.Column(db.Integer)
    source_town_name = db.Column(db.String)
    source_town_bfs_nr = db.Column(db.Integer)
    target_town_id = db.Column(db.Integer, primary_key=True)
    target_zip_code = db.Column(db.Integer)
    time = db.Column(db.Integer)
    changes = db.Column(db.Integer)


class ClosestTrainCommute(db.Model):
    __tablename__ = "agg_closest_train_commute"
    source_town_id = db.Column(db.Integer, primary_key=True)
    source_zip_code = db.Column(db.Integer)
    source_town_name = db.Column(db.String)
    source_town_bfs_nr = db.Column(db.Integer)
    target_town_id = db.Column(db.Integer, primary_key=True)
    target_zip_code = db.Column(db.Integer)
    time = db.Column(db.Integer)
    changes = db.Column(db.Integer)
