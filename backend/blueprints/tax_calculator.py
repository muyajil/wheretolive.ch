import json

from flask import Blueprint, jsonify, request
from plotly.utils import PlotlyJSONEncoder

from ..services import TaxService

tax_calculator_bp = Blueprint("tax_calculator", __name__, template_folder="templates")


@tax_calculator_bp.route("/", methods=["POST"])
def show():
    service = TaxService()
    request_json = request.get_json()
    target_town_taxes, figure_data = service.calculate_taxes(
        married=bool(request_json["married"]),
        double_salary=bool(request_json["doubleSalary"]),
        num_children=int(request_json["numChildren"]),
        income=int(request_json["income"]),
        target_town_id=int(request_json["targetTown"]["id"]),
    )
    return jsonify(
        {
            "target_town_taxes": target_town_taxes,
            "figure_data": json.dumps(figure_data, cls=PlotlyJSONEncoder),
        }
    )
