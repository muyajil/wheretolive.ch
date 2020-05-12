import json

from flask import Blueprint, jsonify, request
from plotly.utils import PlotlyJSONEncoder

from ..services import TaxService

tax_calculator_bp = Blueprint("tax_calculator", __name__, template_folder="templates")


@tax_calculator_bp.route("/", methods=["POST"])
def show():
    service = TaxService()
    target_town_bfs_nr, target_town_taxes, figure_data = service.calculate_taxes(
        **request.get_json()
    )
    return jsonify(
        {
            "target_town_bfs_nr": target_town_bfs_nr,
            "target_town_taxes": target_town_taxes,
            "figure_data": json.dumps(figure_data, cls=PlotlyJSONEncoder),
        }
    )
