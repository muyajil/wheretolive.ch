from flask import Blueprint, jsonify, request

from ..services import SearchService

search_bp = Blueprint("search", __name__)


@search_bp.route("/", methods=["POST"])
def show():
    service = SearchService()
    request_json = request.get_json()

    commute_info = {
        "workplaceTownId": int(request_json["selectedTown"]["id"]),
        "maxCommuteSecs": int(request_json["commuteTime"]) * 60,
        "onlyTrainCommute": bool(request_json["onlyTrainCommute"]),
    }

    tax_info = {
        "income": int(request_json["income"]),
        "married": bool(request_json["married"]),
        "doubleSalary": bool(request_json["doubleSalary"]),
        "numChildren": int(request_json["numChildren"]),
    }

    health_info = {
        "people": list(
            map(
                lambda x: {"birthYear": int(x[0]), "franchise": int(x[1])},
                zip(request_json["birthYears"], request_json["franchises"]),
            )
        )
    }

    accomodation_info = {
        "minRooms": float(request_json["minRooms"])
        if "minRooms" in request_json
        else None,
        "maxRooms": float(request_json["maxRooms"])
        if "maxRooms" in request_json
        else None,
        "minArea": int(float(request_json["minArea"]))
        if "minArea" in request_json
        else None,
        "maxArea": int(float(request_json["maxArea"]))
        if "maxArea" in request_json
        else None,
        "isRent": request_json["offerType"] == "Rent",
    }

    search_result = service.search_towns(
        commute_info, tax_info, health_info, accomodation_info
    )
    return jsonify(search_result)
