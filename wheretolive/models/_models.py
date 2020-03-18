from ..database import base
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey, Float
from sqlalchemy.types import ARRAY


class Town(base):
    __tablename__ = 'town'
    zip_code = Column(Integer, primary_key=True)
    bfs_nr = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    lang = Column(String)
    state = Column(String)


class TaxRate(base):
    __tablename__ = 'tax_rate'
    profile = Column(String, primary_key=True)
    bfs_nr = Column(Integer, primary_key=True)
    min_income = Column(Integer, primary_key=True)
    max_income = Column(Integer, primary_key=True)
    rate = Column(Float)


class Route(base):
    __tablename__ = 'route'
    source_town_zip_code = Column(Integer, primary_key=True)
    source_town_bfs_nr = Column(Integer, primary_key=True)
    source_town_name = Column(String, primary_key=True)
    target_town_zip_code = Column(Integer, primary_key=True)
    target_town_bfs_nr = Column(Integer, primary_key=True)
    target_town_name = Column(String, primary_key=True)
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

