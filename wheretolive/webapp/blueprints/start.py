import json

from flask import Blueprint, render_template, request
from plotly.utils import PlotlyJSONEncoder

from ..services import TownsAnalysisService

towns_bp = Blueprint("towns", __name__, template_folder="templates")


@towns_bp.route("/", methods=["POST"])
def show():
    service = TownsAnalysisService()
    figure_data = service.analyze(request.get_json())
    graphJSON = json.dumps(figure_data, cls=PlotlyJSONEncoder)
    return render_template("towns_analysis.html.jinja", plot=graphJSON)
