import json

from flask import Blueprint, jsonify, request
from plotly.utils import PlotlyJSONEncoder

from ..services import TownsAnalysisService

towns_bp = Blueprint("towns", __name__, template_folder="templates")


@towns_bp.route("/", methods=["POST"])
def show():
    service = TownsAnalysisService()
    analysis, figure_data = service.analyze(request.get_json())
    return jsonify(
        {
            "analysis": analysis,
            "figure_data": json.dumps(figure_data, cls=PlotlyJSONEncoder),
        }
    )
