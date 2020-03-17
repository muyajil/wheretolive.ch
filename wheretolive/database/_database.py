from sqlalchemy import create_engine
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine(os.environ.get('DB_CONN'), convert_unicode=True)
session_factory = sessionmaker(bind=engine)
base = declarative_base()


def init_db():
    from ..models import Town, Route, HealthInsuranceRate, HealthInsurance, Accomodation, TaxRate
    base.metadata.create_all(bind=engine)


def get_session():
    return scoped_session(session_factory)


def drop_table(table):
    table.drop(engine)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"
