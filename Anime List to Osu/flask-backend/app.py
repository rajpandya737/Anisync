from flask import Flask, render_template, request, jsonify
from data_processing import convertor
import os
from dotenv import load_dotenv

load_dotenv
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@app.route("/")
def things():
    return render_template("index.html", token="Flask+React")


@app.route("/process", methods=["POST"])
def process_form():
    if request.method == "POST":
        username = request.form["username"]
        anime_list = jsonify(convertor(username))
        print(anime_list)
        return anime_list



if __name__ == "__main__":
    app.run(debug=True, port=5000)