from flask import jsonify, Blueprint, Response
from datetime import datetime


healthcheck_api = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")


@healthcheck_api.route("", methods=["GET"])
def healthcheck() -> Response:
    """HTTP Health Check
    """

    response = {
        "health": "OK",
        "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(response)


@healthcheck_api.route("/", defaults={"path": "/"}, strict_slashes=False)
@healthcheck_api.route("/<path:path>")
def error_404(path) -> Response:
    return Response(status=404)
