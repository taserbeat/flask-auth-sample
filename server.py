from flask import Flask
from logging import Logger

from core.application import AppBuilder
from core.initialize import IAppInitializer
from core.setting import AppSettings

app = Flask(__name__)


@app.route("/", defaults={"path": "/"}, methods=["GET"])
@app.route("/<path:path>")
def index(path):
    return "this is index\n"


if __name__ == "__main__":
    service = AppBuilder.build(app=app).get_service()

    app_settings = service.injector.get(AppSettings)
    logger = service.injector.get(Logger)
    app_initializer = service.injector.get(IAppInitializer)

    try:
        app_initializer.initialize()
    except Exception as e:
        logger.error(f"failed initialize : {e}")
        raise e

    try:
        app.run(host=app_settings.url, port=app_settings.listen_port, debug=True)
    except Exception as e:
        logger.error(f"application error : {e}")
        raise e

    exit(0)
