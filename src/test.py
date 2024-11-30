from skyfield.api import load
from skyfield.framelib import ecliptic_frame

zodiac_signs = [
    {"sign": "Aries", "start": 0, "end": 29.9999},
    {"sign": "Taurus", "start": 30, "end": 59.9999},
    {"sign": "Gemini", "start": 60, "end": 89.9999},
    {"sign": "Cancer", "start": 90, "end": 119.9999},
    {"sign": "Leo", "start": 120, "end": 149.9999},
    {"sign": "Virgo", "start": 150, "end": 179.9999},
    {"sign": "Libra", "start": 180, "end": 209.9999},
    {"sign": "Scorpio", "start": 210, "end": 239.9999},
    {"sign": "Sagittarius", "start": 240, "end": 269.9999},
    {"sign": "Capricorn", "start": 270, "end": 299.9999},
    {"sign": "Aquarius", "start": 300, "end": 329.9999},
    {"sign": "Pisces", "start": 330, "end": 359.9999},
]


def get_zodiac_sign(degree):
    for zodiac in zodiac_signs:
        # Debugging to check each range
        print(f"Checking {degree} against {zodiac['sign']} ({zodiac['start']}° - {zodiac['end']}°)")
        if zodiac["start"] <= degree <= zodiac["end"]:
            return zodiac["sign"]
    print(f"No zodiac sign found for {degree}")  # Debugging "Unknown"
    return "Unknown"


def generate_moon_data2():
    eph = load("de421.bsp")  # Load ephemeris data
    earth = eph["earth"]  # Earth reference
    moon = eph["moon"]  # Moon reference
    ts = load.timescale()  # Load timescale
    now = ts.now()  # Current time
    moon_data_list = []  # Store moon data for 30 days

    print("Starting moon data generation...\n")  # Debug log

    for day in range(30):  # Loop for the next 30 days
        current_time = now + day  # Calculate time for each day
        moon_apparent = moon.at(current_time).observe(earth).apparent()
        moon_ecliptic = moon_apparent.frame_latlon(ecliptic_frame)
        
        # Normalize and adjust longitude
        longitude = moon_ecliptic[1].degrees  # Original longitude calculation
        longitude = (longitude + 360 - 180) % 360  # Correct for 180-degree offset
        
        zodiac_sign = get_zodiac_sign(longitude)
        degree_in_sign = longitude % 30

        moon_data = {
            "date": current_time.utc_iso(),
            "longitude": round(longitude, 2),
            "zodiac_sign": zodiac_sign,
            "degree": round(degree_in_sign, 2),
        }

        # Append to list and log the details to the terminal
        moon_data_list.append(moon_data)
        print(f"Date: {moon_data['date']}")
        print(f"Longitude: {moon_data['longitude']}°")
        print(f"Zodiac Sign: {moon_data['zodiac_sign']}")
        print(f"Degree in Sign: {moon_data['degree']}°\n")

    print("Moon data generation completed.")
    print("Generated Moon Data List:")
    print(moon_data_list) 

    return moon_data_list


if __name__ == "__main__":
    generate_moon_data2()
