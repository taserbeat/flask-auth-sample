from flask import Flask

from core.setting import SettingLoader

app = Flask(__name__)


@app.route("/", defaults={"path": "/"}, methods=["GET"])
@app.route("/<path:path>")
def index(path):
    return "this is index\n"


if __name__ == "__main__":
    app_settings = SettingLoader.load_setting().get_setting()
    app.run(host=app_settings.url, port=app_settings.listen_port, debug=True)
    exit(0)
