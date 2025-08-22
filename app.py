from flask import Flask, send_from_directory, jsonify, request
from src.services import generate_moon_data
import requests
#from src.services import generate_sun_data

app = Flask(__name__, static_folder="src/assets")

# Route to serve the main HTML file
@app.route("/")
def serve_index():
    return send_from_directory("src/assets", "index.html")

# API route to fetch moon data
@app.route("/data")
def get_data():
    # Read optional count parameter and clamp between 1 and 128, default 32
    try:
        count = int(request.args.get("count", 32))
    except (TypeError, ValueError):
        count = 32
    count = max(1, min(128, count))
    return generate_moon_data(count=count)

# Proxy route for moon phases API to avoid certificate issues
@app.route("/moonphases")
def get_moon_phases():
    try:
        import time
        unix_time = int(time.time())
        response = requests.get(f"https://api.farmsense.net/v1/moonphases/?d={unix_time}", 
                              verify=False,  # Disable SSL verification to bypass certificate issues
                              timeout=5)  # Reduced timeout
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.Timeout:
        print("Timeout fetching moon phases from external API, using fallback")
        # Fallback to calculated moon phase data
        moon_data = generate_moon_data()
        return jsonify([{
            "Error": 0,
            "Phase": moon_data["moon_phase"],
            "Illumination": moon_data["illumination"],
            "Moon": ["Calculated"]
        }])
    except Exception as e:
        print(f"Error fetching moon phases: {e}")
        # Fallback to calculated moon phase data
        moon_data = generate_moon_data()
        return jsonify([{
            "Error": 0,
            "Phase": moon_data["moon_phase"],
            "Illumination": moon_data["illumination"],
            "Moon": ["Calculated"]
        }])

#@app.route("/data_sun")
#def get_data_sun():
    #return generate_sun_data()

# Route to serve static assets (JS, CSS, etc.)
@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory("src/assets", filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
