from flask import Flask
from .services import generate_moon_data

app = Flask(__name__)

@app.route("/")
def get_data():
    return generate_moon_data()