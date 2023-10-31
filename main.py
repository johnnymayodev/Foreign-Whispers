from flask import Flask, current_app, request

app = Flask(__name__, static_folder="/")
app.config["SITE_DIR"] = "web/"


@app.errorhandler(404)
def page_not_found(e):
    return current_app.send_static_file(app.config["SITE_DIR"] + "/html/404.html"), 404


@app.route("/")
def index():
    return current_app.send_static_file(app.config["SITE_DIR"] + "/html/index.html")


@app.route("/api", methods=["GET"])
def api():
    print(request.args.get("check"))
    if request.args.get("check") == "true":
        return "OK"
    else:
        return "ARGUMENT ERROR"


if __name__ == "__main__":
    app.run()
