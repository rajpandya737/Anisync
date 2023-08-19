from flask import Flask, request, render_template, redirect, url_for, session
import dotenv
import os
from data_processing import convertor
from config import HOST, PORT, DEBUG, ENV, START, END

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "instance", ".env")
dotenv.load_dotenv(dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    SECRET_KEY = "Local Host Secret Key"
app = Flask(__name__)
app.secret_key = SECRET_KEY

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
        print(user)
        return render_template("list.html", anime_info=anime, user=user)
    return redirect(url_for("search"))


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
