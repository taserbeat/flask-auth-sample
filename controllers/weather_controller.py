from flask import Blueprint, Response, jsonify, request

from core.auth import ISimpleTokenAuthorizer
from services.weather_service import IWeatherService


weather_api = Blueprint("weather", __name__, url_prefix="/weather")


@weather_api.route("", methods=["GET"])
def get_weather(authorizer: ISimpleTokenAuthorizer, weather_service: IWeatherService):
    token = request.headers.get("Authorization")
    user = authorizer.authorize(token)
    if user is None:
        return Response(status=403)

    weather = weather_service.create_weather()

    response = {
        "temperature": weather.temperature,
        "forecast": weather.forecast,
    }

    return jsonify(response)


@weather_api.route("/", defaults={"path": "/"}, strict_slashes=False)
@weather_api.route("/<path:path>")
def error_404(path: str) -> Response:
    return Response(status=404)
