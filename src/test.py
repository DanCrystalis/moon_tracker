from skyfield.api import load
from skyfield.framelib import ecliptic_frame

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

def get_zodiac_sign(degree):
    for zodiac in zodiac_signs:
        if zodiac["start"] <= degree <= zodiac["end"]:
            return zodiac["sign"]
    return "Unknown"

def generate_moon_data():
    eph = load('de421.bsp')
    earth = eph['earth']
    moon = eph['moon']
    ts = load.timescale()
    now = ts.now()
    moon_data_list = []

    for day in range(30):
        current_time = now + day   # loop for for the next 30 days
        moon_apparent = moon.at(current_time).observe(earth).apparent()
        moon_ecliptic = moon_apparent.frame_latlon(ecliptic_frame)
        longitude = moon_ecliptic[1].degrees 

        zodiac_sign = get_zodiac_sign(longitude)
        degree_in_sign = longitude % 30

        moon_data = {
            "date": current_time.utc_iso(),
            "longitude": round(longitude, 2),
            "zodiac_sign": zodiac_sign,
            "degree": round(degree_in_sign, 2),
        }

        moon_data_list.append(moon_data)
        print(f"{moon_data['date']}: {moon_data['longitude']}°, {moon_data['zodiac_sign']} {moon_data['degree']}°")

    return moon_data_list

