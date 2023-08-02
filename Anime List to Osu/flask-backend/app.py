from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    make_response,
    session
)
from data_processing import convertor
import os
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)
app.secret_key = "hello"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        session["user"] = user
        session["anime_info"] = convertor(user, 0, 30)
        return redirect(url_for("user"))
    return render_template("home.html")

@app.route("/view-maps", methods=["GET", "POST"])  # Include the 'username' parameter in the route
def user():
    if request.method == "POST":
        user = request.form["user"]
        session["user"] = user
        session["anime_info"] = convertor(user, 0, 30)
        return redirect(url_for("user"))
    
    if "user" in session:
        user = session["user"]
        anime = session["anime_info"]
        #print(user, anime)
        return render_template("list.html", anime_info=anime)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
