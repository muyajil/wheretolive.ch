from flask import Blueprint, jsonify, request

from ..services import SearchService

search_bp = Blueprint("search", __name__)


@search_bp.route("/", methods=["POST"])
def show():
    service = SearchService()
    request_json = request.get_data()
    search_result = service.search(request_json)
    return jsonify(search_result)
