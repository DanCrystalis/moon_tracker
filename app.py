from flask import Flask, send_from_directory
from src.services import generate_moon_data
#from src.services import generate_sun_data

app = Flask(__name__, static_folder="src/assets")

# Route to serve the main HTML file
@app.route("/")
def serve_index():
    return send_from_directory("src/assets", "index.html")

# API route to fetch moon data
@app.route("/data")
def get_data():
    return generate_moon_data()

#@app.route("/data_sun")
#def get_data_sun():
    #return generate_sun_data()

# Route to serve static assets (JS, CSS, etc.)
@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory("src/assets", filename)
