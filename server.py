from flask import Flask

from core.application import AppBuilder
from core.setting import AppSettings

app = Flask(__name__)


@app.route("/", defaults={"path": "/"}, methods=["GET"])
@app.route("/<path:path>")
def index(path):
    return "this is index\n"


if __name__ == "__main__":
    service = AppBuilder.build(app=app).get_service()
    app_settings = service.injector.get(AppSettings)
    app.run(host=app_settings.url, port=app_settings.listen_port, debug=True)
    exit(0)
