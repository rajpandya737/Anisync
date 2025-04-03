from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    session,
    make_response,
)
import defusedxml.ElementTree as ET
import logging
from data_processing import convertor
from config import HOST, PORT, DEBUG, START, END, SECRET_KEY, SESSION_LIFETIME


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["PERMANENT_SESSION_LIFETIME"] = SESSION_LIFETIME

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)


# Home and Search page routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user = request.form["user"]
        session["user"] = user
        return redirect(url_for("user"))
    return render_template("search.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        user = request.form["user"]
        session["user"] = user
        return redirect(url_for("user"))
    return render_template("search.html")


# About page route
@app.route("/about")
def about():
    return render_template("about.html")


# View maps page route, redirect if session is not set
@app.route(
    "/view-maps", methods=["GET", "POST"]
)  # Include the 'username' parameter in the route
def user():
    if request.method == "POST":
        user = request.form["user"]
        session["user"] = user
        return redirect(url_for("user"))

    if "user" in session:
        user = session["user"]
        anime = convertor(user, START, END)
        app.logger.debug(user)
        return render_template("list.html", anime_info=anime, user=user)
    return redirect(url_for("search"))


@app.errorhandler(404)
# 404 error page route
def not_found_error(error):
    return (
        render_template(
            "error.html",
            error_code=404,
            error_description="Page not found",
        ),
        404,
    )


@app.errorhandler(Exception)
# 500 error page route
def global_error_handler(error):
    return (
        render_template(
            "error.html", error_code=500, error_description="Something went wrong"
        ),
        500,
    )


@app.route("/sitemap.xml")
def sitemap():
    base_url = "https://anisync.live"

    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    urls = ["/", "/search", "/about"]
    for url in urls:
        loc = ET.SubElement(root, "url")
        ET.SubElement(loc, "loc").text = base_url + url

    xml_string = ET.tostring(root, encoding="utf-8")
    response = make_response(xml_string)
    response.headers["Content-Type"] = "application/xml"

    return response



if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
