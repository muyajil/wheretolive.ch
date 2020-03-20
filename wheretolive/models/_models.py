from ..database import base
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey, Float, Time
from sqlalchemy.types import ARRAY


class Town(base):
    __tablename__ = 'town'
    id = Column(Integer, primary_key=True)
    zip_code = Column(Integer)
    bfs_nr = Column(Integer)
    name = Column(String)
    lat = Column(Float)
    long = Column(Float)
    lang = Column(String)
    state = Column(String)


class TaxRate(base):
    __tablename__ = 'tax_rate'
    profile = Column(String, primary_key=True)
    bfs_nr = Column(Integer, primary_key=True)
    min_income = Column(Integer, primary_key=True)
    max_income = Column(Integer, primary_key=True)
    rate = Column(Float)


class Commute(base):
    __tablename__ = 'commute'
    source_town_id = Column(Integer, primary_key=True)
    target_town_id = Column(Integer, primary_key=True)
    distance = Column(Float)
    car_commute_time = Column(Float)
    public_commute_time = Column(Float)
    public_commute_switches = Column(Integer)


class HealthInsurance(base):
    __tablename__ = 'health_insurance'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    name_capitalized = Column(String)
    url = Column(String)


class HealthInsuranceRate(base):
    __tablename__ = 'health_insurance_rate'
    health_insurance_id = Column(Integer, primary_key=True)
    zip_code = Column(Integer, primary_key=True)
    birth_year = Column(Integer, primary_key=True)
    franchise = Column(Integer, primary_key=True)
    model = Column(String, primary_key=True)
    rate = Column(Float)


class Accomodation(base):
    __tablename__ = 'accomodation'
    comparis_id = Column(Integer, primary_key=True)
    zip_code = Column(Integer)
    town_name = Column(String)
    street_name = Column(String)
    house_number = Column(String)
    rooms = Column(Float)
    area = Column(Float)
    price = Column(Float)
    image_url = Column(String)
    is_rent = Column(Boolean)
    found_date = Column(DateTime)
    property_type_id = Column(Integer)
    property_type = Column(String)


class SBBStation(base):
    __tablename__ = 'sbb_station'
    id = Column(String, primary_key=True)
    name = Column(String)
    lat = Column(Float)
    long = Column(Float)
    parent_station = Column(String)


class SBBStopTime(base):
    __tablename__ = 'sbb_stop_time'
    trip_id = Column(String, primary_key=True)
    station_id = Column(String, primary_key=True)
    stop_sequence = Column(Integer, primary_key=True)
    arrival_time = Column(Time)
    arrives_next_day = Column(Boolean)
    departure_time = Column(Time)
    departs_next_day = Column(Boolean)


class SBBTrip(base):
    __tablename__ = 'sbb_trip'
    trip_id = Column(String, primary_key=True)
    route_id = Column(String)
    service_id = Column(String)


class SBBRoute(base):
    __tablename__ = 'sbb_route'
    route_id = Column(String, primary_key=True)
    route_desc = Column(String)


class SBBCalendar(base):
    __tablename__ = 'sbb_calendar'
    service_id = Column(String, primary_key=True)
    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)


class SBBTransfers(base):
    __tablename__ = 'sbb_transfers'
    from_stop_id = Column(String, primary_key=True)
    to_stop_id = Column(String, primary_key=True)
    min_transfer_time = Column(Integer)
