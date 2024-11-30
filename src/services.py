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

gates_date = [
    {
        "name": "Gate 1",
        "sign": "Scorpio",
        "center": "Identity",
        "degrees": {"start": 223.15, "end": 228.523},
    },
    {
        "name": "Gate 2",
        "sign": "Taurus",
        "center": "Identity",
        "degrees": {"start": 43.15, "end": 48.523},
    },
    {
        "name": "Gate 3",
        "sign": "Aries/Taurus",
        "center": "Sacral",
        "degrees": {"start": 26.223, "end": 32},
    },
    {
        "name": "Gate 4",
        "sign": "Leo",
        "center": "Ajna",
        "degrees": {"start": 138.523, "end": 144.3},
    },
    {
        "name": "Gate 5",
        "sign": "Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 251.223, "end": 257},
    },
    {
        "name": "Gate 6",
        "sign": "Virgo",
        "center": "Solar Plexus",
        "degrees": {"start": 172.373, "end": 178.15},
    },
    {
        "name": "Gate 7",
        "sign": "Leo",
        "center": "Identity",
        "degrees": {"start": 133.15, "end": 138.523},
    },
    {
        "name": "Gate 8",
        "sign": "Taurus/Gemini",
        "center": "Throat",
        "degrees": {"start": 54.3, "end": 60.073},
    },
    {
        "name": "Gate 9",
        "sign": "Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 245.45, "end": 251.223},
    },
    {
        "name": "Gate 10",
        "sign": "Sagittarius/Capricorn",
        "center": "Identity",
        "degrees": {"start": 268.15, "end": 273.523},
    },
    {
        "name": "Gate 11",
        "sign": "Sagittarius",
        "center": "Ajna",
        "degrees": {"start": 262.373, "end": 268.15},
    },
    {
        "name": "Gate 12",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 82.373, "end": 88.15},
    },
    {
        "name": "Gate 13",
        "sign": "Aquarius",
        "center": "Identity",
        "degrees": {"start": 313.15, "end": 318.523},
    },
    {
        "name": "Gate 14",
        "sign": "Scorpio/Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 234.3, "end": 240.073},
    },
    {
        "name": "Gate 15",
        "sign": "Gemini/Cancer",
        "center": "Identity",
        "degrees": {"start": 88.15, "end": 93.523},
    },
    {
        "name": "Gate 16",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 65.45, "end": 71.223},
    },
    {
        "name": "Gate 17",
        "sign": "Aries",
        "center": "Ajna",
        "degrees": {"start": 3.523, "end": 9.3},
    },
    {
        "name": "Gate 18",
        "sign": "Libra",
        "center": "Spleen",
        "degrees": {"start": 183.523, "end": 189.3},
    },
    {
        "name": "Gate 19",
        "sign": "Aquarius",
        "center": "Root",
        "degrees": {"start": 307.373, "end": 313.15},
    },
    {
        "name": "Gate 20",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 60.073, "end": 65.45},
    },
    {
        "name": "Gate 21",
        "sign": "Aries",
        "center": "Heart",
        "degrees": {"start": 9.3, "end": 15.073},
    },
    {
        "name": "Gate 22",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 347, "end": 352.373},
    },
    {
        "name": "Gate 23",
        "sign": "Taurus",
        "center": "Throat",
        "degrees": {"start": 48.523, "end": 54.3},
    },
    {
        "name": "Gate 24",
        "sign": "Taurus",
        "center": "Ajna",
        "degrees": {"start": 37.373, "end": 43.15},
    },
    {
        "name": "Gate 25",
        "sign": "Aries/Pisces",
        "center": "Identity",
        "degrees": {"start": 28.15, "end": 333.523},
    },
    {
        "name": "Gate 26",
        "sign": "Sagittarius",
        "center": "Heart",
        "degrees": {"start": 257, "end": 262.373},
    },
    {
        "name": "Gate 27",
        "sign": "Taurus",
        "center": "Sacral",
        "degrees": {"start": 32, "end": 37.373},
    },
    {
        "name": "Gate 28",
        "sign": "Scorpio",
        "center": "Spleen",
        "degrees": {"start": 212, "end": 217.373},
    },
    {
        "name": "Gate 29",
        "sign": "Leo/Virgo",
        "center": "Sacral",
        "degrees": {"start": 144.3, "end": 150.073},
    },
    {
        "name": "Gate 30",
        "sign": "Aquarius/Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 324.3, "end": 330.073},
    },
    {
        "name": "Gate 31",
        "sign": "Leo",
        "center": "Throat",
        "degrees": {"start": 122, "end": 127.373},
    },
    {
        "name": "Gate 32",
        "sign": "Libra",
        "center": "Spleen",
        "degrees": {"start": 200.45, "end": 206.223},
    },
    {
        "name": "Gate 33",
        "sign": "Leo",
        "center": "Throat",
        "degrees": {"start": 127.373, "end": 133.15},
    },
    {
        "name": "Gate 34",
        "sign": "Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 240.073, "end": 245.45},
    },
    {
        "name": "Gate 35",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 71.223, "end": 77},
    },
    {
        "name": "Gate 36",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 352.373, "end": 358.15},
    },
    {
        "name": "Gate 37",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 335.45, "end": 341.223},
    },
    {
        "name": "Gate 38",
        "sign": "Cancer",
        "center": "Root",
        "degrees": {"start": 99.3, "end": 105.073},
    },
    {
        "name": "Gate 39",
        "sign": "Cancer",
        "center": "Root",
        "degrees": {"start": 99.3, "end": 105.073},
    },
    {
        "name": "Gate 40",
        "sign": "Virgo",
        "center": "Heart",
        "degrees": {"start": 155.45, "end": 161.223},
    },
    {
        "name": "Gate 41",
        "sign": "Aquarius",
        "center": "Root",
        "degrees": {"start": 302, "end": 307.373},
    },
    {
        "name": "Gate 42",
        "sign": "Aries",
        "center": "Sacral",
        "degrees": {"start": 20.45, "end": 26.223},
    },
    {
        "name": "Gate 43",
        "sign": "Scorpio",
        "center": "Ajna",
        "degrees": {"start": 228.523, "end": 234.3},
    },
    {
        "name": "Gate 44",
        "sign": "Scorpio",
        "center": "Spleen",
        "degrees": {"start": 217.373, "end": 223.15},
    },
    {
        "name": "Gate 45",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 77, "end": 82.373},
    },
    {
        "name": "Gate 46",
        "sign": "Libra/Virgo",
        "center": "Identity",
        "degrees": {"start": 208.15, "end": 153.523},
    },
    {
        "name": "Gate 47",
        "sign": "Virgo",
        "center": "Ajna",
        "degrees": {"start": 167, "end": 172.373},
    },
    {
        "name": "Gate 48",
        "sign": "Libra",
        "center": "Spleen",
        "degrees": {"start": 189.3, "end": 195.073},
    },
    {
        "name": "Gate 49",
        "sign": "Aquarius",
        "center": "Solar Plexus",
        "degrees": {"start": 318.523, "end": 324.3},
    },
    {
        "name": "Gate 50",
        "sign": "Libra/Scorpio",
        "center": "Spleen",
        "degrees": {"start": 206.223, "end": 212},
    },
    {
        "name": "Gate 51",
        "sign": "Aries",
        "center": "Heart",
        "degrees": {"start": 15.073, "end": 20.45},
    },
    {
        "name": "Gate 52",
        "sign": "Cancer",
        "center": "Root",
        "degrees": {"start": 93.523, "end": 99.3},
    },
    {
        "name": "Gate 53",
        "sign": "Cancer",
        "center": "Root",
        "degrees": {"start": 105.073, "end": 110.45},
    },
    {
        "name": "Gate 54",
        "sign": "Capricorn",
        "center": "Root",
        "degrees": {"start": 285.073, "end": 290.45},
    },
    {
        "name": "Gate 55",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 330.073, "end": 335.45},
    },
    {
        "name": "Gate 56",
        "sign": "Cancer/Leo",
        "center": "Throat",
        "degrees": {"start": 116.223, "end": 122},
    },
    {
        "name": "Gate 57",
        "sign": "Virgo",
        "center": "Spleen",
        "degrees": {"start": 165.073, "end": 170.45},
    },
    {
        "name": "Gate 58",
        "sign": "Capricorn",
        "center": "Root",
        "degrees": {"start": 273.523, "end": 279.3},
    },
    {
        "name": "Gate 59",
        "sign": "Gemini",
        "center": "Sacral",
        "degrees": {"start": 60.073, "end": 65.45},
    },
    {
        "name": "Gate 60",
        "sign": "Capricorn/Aquarius",
        "center": "Root",
        "degrees": {"start": 296.223, "end": 302},
    },
    {
        "name": "Gate 61",
        "sign": "Capricorn",
        "center": "Head",
        "degrees": {"start": 290.45, "end": 296.223},
    },
    {
        "name": "Gate 62",
        "sign": "Cancer",
        "center": "Throat",
        "degrees": {"start": 110.45, "end": 116.223},
    },
    {
        "name": "Gate 63",
        "sign": "Pisces",
        "center": "Head",
        "degrees": {"start": 341.223, "end": 347},
    },
    {
        "name": "Gate 64",
        "sign": "Virgo",
        "center": "Head",
        "degrees": {"start": 161.223, "end": 167},
    },
]


def get_zodiac_sign(degree):
    for zodiac in zodiac_signs:
        if zodiac["start"] <= degree <= zodiac["end"]:
            return zodiac["sign"]
    return "Unknown"


def generate_moon_data():
    eph = load("de421.bsp")
    earth = eph["earth"]
    moon = eph["moon"]
    ts = load.timescale()
  # Get the current local time and time zone
    local_time = datetime.now()  # System's local time
    local_timezone = ZoneInfo(local_time.astimezone().tzinfo.key)  # Automatically get system time zone
    
    # Convert local time to UTC
    localized_time = local_time.replace(tzinfo=local_timezone)  # Localize time to system's timezone
    utc_time = localized_time.astimezone(ZoneInfo("UTC"))  # Convert to UTC
    
    # Create a Skyfield Time object
    skyfield_time = ts.utc(
        utc_time.year, utc_time.month, utc_time.day,
        utc_time.hour, utc_time.minute, utc_time.second
    )
    
    # Calculate moon data
    moon_apparent = moon.at(skyfield_time).observe(earth).apparent()
    moon_ecliptic = moon_apparent.frame_latlon(ecliptic_frame)
    longitude = moon_ecliptic[1].degrees
    zodiac_sign = get_zodiac_sign(longitude)
    degree_in_sign = longitude % 30

    moon_data = {
        "date": now.utc_iso(),
        "longitude": round(longitude, 2),
        "zodiac_sign": zodiac_sign,
        "degree": round(degree_in_sign, 2),
    }

    return moon_data
