from flask import Blueprint, jsonify

from ..services import TownService

towns_bp = Blueprint("towns", __name__)


@towns_bp.route("/typeahead", methods=["GET"])
def get_typeahead_dict():
    service = TownService()
    typeahead_data = service.get_typeahead_data()
    return jsonify(typeahead_data)
