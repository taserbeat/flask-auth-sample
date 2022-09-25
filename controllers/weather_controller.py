from flask import Blueprint, Response, jsonify

from core import auth
from services.weather_service import IWeatherService


weather_api = Blueprint("weather", __name__, url_prefix="/weather")


@weather_api.route("/sts", methods=["GET"])
@auth.simple_token_required
def get_weather_by_sts(weather_service: IWeatherService, **kwargs):
    weather = weather_service.create_weather()
    response = {
        "temperature": weather.temperature,
        "forecast": weather.forecast,
    }

    return jsonify(response)


@weather_api.route("/jwt", methods=["GET"])
@auth.jwt_token_required
def get_weather_by_jwt(weather_service: IWeatherService, **kwargs):
    # username: str = kwargs.get("username")  # you can get the user's identifier like this
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
