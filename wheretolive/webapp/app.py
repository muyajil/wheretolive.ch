import os

from flask import Flask
from flask_bootstrap import Bootstrap

from ..jobs.data_processing.closest_stations import bp as closest_stations_job_bp
from ..jobs.data_processing.commute_distances import bp as commute_distances_job_bp
from ..jobs.data_processing.sbb_connections import bp as sbb_connections_job_bp
from ..jobs.data_processing.sbb_station_groups import bp as sbb_station_groups_job_bp
from ..jobs.data_processing.tax_rate_effects import bp as tax_rate_effects_job_bp
from ..jobs.data_processing.train_commutes import bp as train_commutes_job_bp
from ..jobs.enrichment.aldi import bp as aldi_job_bp
from ..jobs.enrichment.coop import bp as coop_job_bp
from ..jobs.enrichment.ftth import bp as ftth_job_bp
from ..jobs.enrichment.lidl import bp as lidl_job_bp
from ..jobs.enrichment.migros import bp as migros_job_bp
from ..jobs.initial_import.health_insurance_rates import bp as health_insurance_job_bp
from ..jobs.initial_import.sbb_timetable import bp as sbb_timetable_job_bp
from ..jobs.initial_import.tax_rates import bp as tax_rates_job_bp
from ..jobs.initial_import.towns import bp as towns_job_bp
from ..jobs.updates.accomodations import bp as accomodations_job_bp
from .blueprints.towns import towns_bp
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_CONN")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    register_extensions(app)
    register_blueprints(app)

    Bootstrap(app)

    return app


def register_blueprints(app):
    app.register_blueprint(towns_bp, url_prefix="/towns")
    app.register_blueprint(accomodations_job_bp)
    app.register_blueprint(health_insurance_job_bp)
    app.register_blueprint(sbb_timetable_job_bp)
    app.register_blueprint(tax_rates_job_bp)
    app.register_blueprint(towns_job_bp)
    app.register_blueprint(closest_stations_job_bp)
    app.register_blueprint(commute_distances_job_bp)
    app.register_blueprint(sbb_connections_job_bp)
    app.register_blueprint(sbb_station_groups_job_bp)
    app.register_blueprint(tax_rate_effects_job_bp)
    app.register_blueprint(train_commutes_job_bp)
    app.register_blueprint(aldi_job_bp)
    app.register_blueprint(coop_job_bp)
    app.register_blueprint(ftth_job_bp)
    app.register_blueprint(lidl_job_bp)
    app.register_blueprint(migros_job_bp)


def register_extensions(app):
    db.init_app(app)
