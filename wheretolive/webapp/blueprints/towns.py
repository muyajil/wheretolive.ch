from flask import Blueprint, jsonify, request

from ..services import TownsAnalysisService

towns_bp = Blueprint("towns", __name__, template_folder="templates")


@towns_bp.route("/", methods=["POST"])
def show():
    service = TownsAnalysisService()
    analysis = service.analyze(request.get_json())
    return jsonify(analysis)
