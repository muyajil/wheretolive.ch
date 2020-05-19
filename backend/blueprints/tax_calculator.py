from flask import Blueprint, jsonify, request

from ..services import TaxService

tax_calculator_bp = Blueprint("tax_calculator", __name__)


@tax_calculator_bp.route("/", methods=["POST"])
def show():
    tax_service = TaxService()
    request_json = request.get_json()
    tax_info = {
        "married": bool(request_json["married"]),
        "doubleSalary": bool(request_json["doubleSalary"]),
        "numChildren": int(request_json["numChildren"]),
        "income": int(request_json["income"]),
        "targetTown": request_json["targetTown"]["label"],
    }
    taxes, target_town_tax_amount = tax_service.get_all_taxes(
        tax_info, target_town_id=int(request_json["targetTown"]["id"])
    )
    return jsonify({"taxData": taxes, "targetTownTaxAmount": target_town_tax_amount})
