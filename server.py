from flask import Flask

app = Flask(__name__)


@app.route("/", defaults={"path": "/"}, methods=["GET"])
@app.route("/<path:path>")
def index(path):
    return "this is index\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    exit(0)
