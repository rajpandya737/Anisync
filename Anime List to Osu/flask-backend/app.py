from flask import Flask, request, jsonify, render_template
#from data_processing import convertor
import os
#from dotenv import load_dotenv

#load_dotenv()
app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# if any errors arise, try changing yarn.lock file back to original

@app.route("/")
def home():
    return render_template("index.html", token="Hello Flask+React") # token is used to test if the connection is working


if __name__ == "__main__":
    app.run(debug=True)