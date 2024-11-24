#from js import console, localStorage
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
import json

#def generate_moon_data():

# Zodiac signs with degree ranges 
zodiac_signs = [
    {"sign": "Aries", "start": 0, "end": 29},
    {"sign": "Taurus", "start": 30, "end": 59},
    {"sign": "Gemini", "start": 60, "end": 89},
    {"sign": "Cancer", "start": 90, "end": 119},
    {"sign": "Leo", "start": 120, "end": 149},
    {"sign": "Virgo", "start": 150, "end": 179},
    {"sign": "Libra", "start": 180, "end": 209},
    {"sign": "Scorpio", "start": 210, "end": 239},
    {"sign": "Sagittarius", "start": 240, "end": 269},
    {"sign": "Capricorn", "start": 270, "end": 299},
    {"sign": "Aquarius", "start": 300, "end": 329},
    {"sign": "Pisces", "start": 330, "end": 359},
]


# Helper function to determine zodiac sign
def get_zodiac_sign(degree):
    for zodiac in zodiac_signs:
        if zodiac["start"] <= degree <= zodiac["end"]:
            return zodiac["sign"]
    return "Unknown"

# Load ephemeris data
eph = load('de421.bsp')
earth = eph['earth']
moon = eph['moon']

# Load the current time
ts = load.timescale()
now = ts.now()

# Step 1: Calculate the Moon's position relative to the Earth
# Skyfield automatically accounts for Earth-Moon barycenter dynamics
moon_apparent = moon.at(now).observe(earth).apparent()

# Step 2: Transform the Moon's position into the ecliptic frame
moon_ecliptic = moon_apparent.frame_latlon(ecliptic_frame)

# Step 3: Extract the ecliptic longitude and normalize to 0–360°
longitude = moon_ecliptic[1].degrees % 360  # Normalize longitude to 0-360°

# Calculate zodiac sign and degree within the sign
zodiac_sign = get_zodiac_sign(longitude-180)
degree_in_sign = longitude % 30

# Output results
moon_data = {
    "longitude": round(longitude, 2),
    "zodiac_sign": zodiac_sign,
    "degree": round(degree_in_sign, 2),
}

# Save to JSON file
with open("moon_data.json", "w") as f:
    json.dump(moon_data, f, indent=4)

# print("Moon Data:", moon_data)
#localStorage.setItem("moon_data", str(moon_data))
#console.log("Moon data saved to localStorage:", moon_data)

#generate_moon_data()