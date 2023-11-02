from flask import Flask, current_app, request, jsonify
import libraries.milestone_1 as m1
import libraries.milestone_2 as m2

app = Flask(__name__, static_folder="/")

# the youtube playlist url to the 60 minutes interview playlist
app.config[
    "YT_URL"
] = "https://www.youtube.com/playlist?list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL"
app.config["SITE_DIR"] = "web/"


@app.errorhandler(404)
def page_not_found(e):
    return current_app.send_static_file(app.config["SITE_DIR"] + "/html/404.html"), 404


@app.route("/")
def index():
    return current_app.send_static_file(app.config["SITE_DIR"] + "/html/index.html")


@app.route("/api/<arg>")
def api(arg):
    if arg == "check":
        return "OK"
    elif arg == "milestone1":
        try:
            m1.main(app)
            return "OK"
        except Exception as e:
            return str(e)
    elif arg == "milestone2":
        try:
            m2.main(app)
            return "OK"
        except Exception as e:
            return str(e)
    else:
        return "Invalid argument"


if __name__ == "__main__":
    app.run()
