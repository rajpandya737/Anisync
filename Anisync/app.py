from flask import Flask, request, render_template, redirect, url_for, session
import dotenv
import os
from data_processing import convertor

dotenv_path = os.path.join(os.path.dirname(__file__), "instance", ".env")
dotenv.load_dotenv(dotenv_path)
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


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


@app.route("/about")
def about():
    return render_template("about.html")


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
        anime = convertor(user, 0, 300)
        print(user)
        return render_template("list.html", anime_info=anime, user=user)
    return redirect(url_for("search"))


if __name__ == "__main__":
    app.run(debug=True)
