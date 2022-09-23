from flask import Blueprint, Response, jsonify

from services.weather_service import IWeatherService


weather_api = Blueprint("weather", __name__, url_prefix="/weather")


@weather_api.route("", methods=["GET"])
def get_weather(weather_service: IWeatherService):
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
