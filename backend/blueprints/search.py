from flask import Blueprint, jsonify, request

from ..services import SearchService

search_bp = Blueprint("search", __name__)


def get_info_blocks_from_request(request_json):
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
        if "minRooms" in request_json and request_json["minRooms"] != ""
        else None,
        "maxRooms": float(request_json["maxRooms"])
        if "maxRooms" in request_json and request_json["maxRooms"] != ""
        else None,
        "minArea": int(float(request_json["minArea"]))
        if "minArea" in request_json and request_json["minArea"] != ""
        else None,
        "maxArea": int(float(request_json["maxArea"]))
        if "maxArea" in request_json and request_json["maxArea"] != ""
        else None,
        "isRent": request_json["offerType"] == "Rent",
    }

    return commute_info, tax_info, health_info, accomodation_info


@search_bp.route("/towns", methods=["POST"])
def search_towns():
    service = SearchService()
    request_json = request.get_json()

    (
        commute_info,
        tax_info,
        health_info,
        accomodation_info,
    ) = get_info_blocks_from_request(request_json)

    search_result = service.search_towns(
        commute_info, tax_info, health_info, accomodation_info
    )
    return jsonify(search_result)


@search_bp.route("/towns", methods=["POST"])
def search_accomodations():
    service = SearchService()
    request_json = request.get_json()

    _, tax_info, health_info, accomodation_info = get_info_blocks_from_request(
        request_json
    )
    zip_codes = request_json["zipCodes"]

    search_result = service.search_accomodations(
        zip_codes, tax_info, health_info, accomodation_info
    )

    return jsonify(search_result)
