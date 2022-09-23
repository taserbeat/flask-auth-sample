from flask import Blueprint, Response

from controllers.healthcheck_controller import healthcheck_api

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/", defaults={"path": "/"}, strict_slashes=False)
@api.route("/<path:path>")
def error_404(path) -> Response:
    return Response(status=404)


api.register_blueprint(healthcheck_api)
