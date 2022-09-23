from flask import Blueprint, Response
from logging import Logger

from controllers.healthcheck_controller import healthcheck_api

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/", defaults={"path": "/"}, strict_slashes=False)
@api.route("/<path:path>")
def error_404(path: str, logger: Logger) -> Response:
    log = "path: '/{0}/{1}' is 404 not found.".format(api.name, path.lstrip("/"))
    logger.error(log)
    return Response(status=404)


api.register_blueprint(healthcheck_api)
