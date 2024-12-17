import swisseph as swe 
from datetime import datetime, timedelta, timezone 
import DateTime
import pytz
from decimal import Decimal

zodiac_signs = [
    {"sign": "Aries", "start": 0, "end": 30},
    {"sign": "Taurus", "start": 30, "end": 60},
    {"sign": "Gemini", "start": 60, "end": 90},
    {"sign": "Cancer", "start": 90, "end": 120},
    {"sign": "Leo", "start": 120, "end": 150},
    {"sign": "Virgo", "start": 150, "end": 180},
    {"sign": "Libra", "start": 180, "end": 210},
    {"sign": "Scorpio", "start": 210, "end": 240},
    {"sign": "Sagittarius", "start": 240, "end": 270},
    {"sign": "Capricorn", "start": 270, "end": 300},
    {"sign": "Aquarius", "start": 300, "end": 330},
    {"sign": "Pisces", "start": 330, "end": 360},
]

gates_data = [
    {
        "name": "Gate 17",
        "sign": "Aries",
        "center": "Ajna",
        "degrees": {"start": 3.523, "end": 9.3},
    },
    {
        "name": "Gate 21",
        "sign": "Aries",
        "center": "Heart",
        "degrees": {"start": 9.3, "end": 15.073},
    },
    {
        "name": "Gate 51",
        "sign": "Aries",
        "center": "Heart",
        "degrees": {"start": 15.073, "end": 20.45},
    },
    {
        "name": "Gate 42",
        "sign": "Aries",
        "center": "Sacral",
        "degrees": {"start": 20.45, "end": 26.223},
    },
    {
        "name": "Gate 3",
        "sign": "Aries/Taurus",
        "center": "Sacral",
        "degrees": {"start": 26.223, "end": 32},
    },
    {
        "name": "Gate 27",
        "sign": "Taurus",
        "center": "Sacral",
        "degrees": {"start": 32, "end": 37.373},
    },
    {
        "name": "Gate 24",
        "sign": "Taurus",
        "center": "Ajna",
        "degrees": {"start": 37.373, "end": 43.15},
    },
    {
        "name": "Gate 2",
        "sign": "Taurus",
        "center": "Identity",
        "degrees": {"start": 43.15, "end": 48.523},
    },
    {
        "name": "Gate 23",
        "sign": "Taurus",
        "center": "Throat",
        "degrees": {"start": 48.523, "end": 54.3},
    },
    {
        "name": "Gate 8",
        "sign": "Taurus/Gemini",
        "center": "Throat",
        "degrees": {"start": 54.3, "end": 60.073},
    },
    {
        "name": "Gate 20",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 60.073, "end": 65.45},
    },
    {
        "name": "Gate 59",
        "sign": "Gemini",
        "center": "Sacral",
        "degrees": {"start": 60.073, "end": 65.45},
    },
    {
        "name": "Gate 16",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 65.45, "end": 71.223},
    },
    {
        "name": "Gate 35",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 71.223, "end": 77},
    },
    {
        "name": "Gate 45",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 77, "end": 82.373},
    },
    {
        "name": "Gate 12",
        "sign": "Gemini",
        "center": "Throat",
        "degrees": {"start": 82.373, "end": 88.15},
    },
    {
        "name": "Gate 15",
        "sign": "Gemini/Cancer",
        "center": "Identity",
        "degrees": {"start": 88.15, "end": 93.523},
    },
    {
        "name": "Gate 52",
        "sign": "Cancer",
        "center": "Root",
        "degrees": {"start": 93.523, "end": 99.3},
    },
    {
        "name": "Gate 39",
        "sign": "Cancer",
        "center": "Root",
        "degrees": {"start": 99.3, "end": 105.073},
    },
    {
        "name": "Gate 53",
        "sign": "Cancer",
        "center": "Root",
        "degrees": {"start": 105.073, "end": 110.45},
    },
    {
        "name": "Gate 62",
        "sign": "Cancer",
        "center": "Throat",
        "degrees": {"start": 110.45, "end": 116.223},
    },
    {
        "name": "Gate 56",
        "sign": "Cancer/Leo",
        "center": "Throat",
        "degrees": {"start": 116.223, "end": 122},
    },
    {
        "name": "Gate 31",
        "sign": "Leo",
        "center": "Throat",
        "degrees": {"start": 122, "end": 127.373},
    },
    {
        "name": "Gate 33",
        "sign": "Leo",
        "center": "Throat",
        "degrees": {"start": 127.373, "end": 133.15},
    },
    {
        "name": "Gate 7",
        "sign": "Leo",
        "center": "Identity",
        "degrees": {"start": 133.15, "end": 138.523},
    },
    {
        "name": "Gate 4",
        "sign": "Leo",
        "center": "Ajna",
        "degrees": {"start": 138.523, "end": 144.3},
    },
    {
        "name": "Gate 29",
        "sign": "Leo/Virgo",
        "center": "Sacral",
        "degrees": {"start": 144.3, "end": 150.073},
    },
    {
        "name": "Gate 40",
        "sign": "Virgo",
        "center": "Heart",
        "degrees": {"start": 155.45, "end": 161.223},
    },
    {
        "name": "Gate 64",
        "sign": "Virgo",
        "center": "Head",
        "degrees": {"start": 161.223, "end": 167},
    },
    {
        "name": "Gate 57",
        "sign": "Virgo",
        "center": "Spleen",
        "degrees": {"start": 165.073, "end": 170.45},
    },
    {
        "name": "Gate 47",
        "sign": "Virgo",
        "center": "Ajna",
        "degrees": {"start": 167, "end": 172.373},
    },
    {
        "name": "Gate 6",
        "sign": "Virgo",
        "center": "Solar Plexus",
        "degrees": {"start": 172.373, "end": 178.15},
    },
    {
        "name": "Gate 18",
        "sign": "Libra",
        "center": "Spleen",
        "degrees": {"start": 183.523, "end": 189.3},
    },
    {
        "name": "Gate 48",
        "sign": "Libra",
        "center": "Spleen",
        "degrees": {"start": 189.3, "end": 195.073},
    },
    {
        "name": "Gate 32",
        "sign": "Libra",
        "center": "Spleen",
        "degrees": {"start": 200.45, "end": 206.223},
    },
    {
        "name": "Gate 50",
        "sign": "Libra/Scorpio",
        "center": "Spleen",
        "degrees": {"start": 206.223, "end": 212},
    },
    {
        "name": "Gate 46",
        "sign": "Libra/Virgo",
        "center": "Identity",
        "degrees": {"start": 208.15, "end": 153.523},
    },
    {
        "name": "Gate 28",
        "sign": "Scorpio",
        "center": "Spleen",
        "degrees": {"start": 212, "end": 217.373},
    },
    {
        "name": "Gate 44",
        "sign": "Scorpio",
        "center": "Spleen",
        "degrees": {"start": 217.373, "end": 223.15},
    },
    {
        "name": "Gate 1",
        "sign": "Scorpio",
        "center": "Identity",
        "degrees": {"start": 223.15, "end": 228.523},
    },
    {
        "name": "Gate 43",
        "sign": "Scorpio",
        "center": "Ajna",
        "degrees": {"start": 228.523, "end": 234.3},
    },
    {
        "name": "Gate 14",
        "sign": "Scorpio/Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 234.3, "end": 240.073},
    },
    {
        "name": "Gate 34",
        "sign": "Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 240.073, "end": 245.45},
    },
    {
        "name": "Gate 9",
        "sign": "Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 245.45, "end": 251.223},
    },
    {
        "name": "Gate 5",
        "sign": "Sagittarius",
        "center": "Sacral",
        "degrees": {"start": 251.223, "end": 257},
    },
    {
        "name": "Gate 26",
        "sign": "Sagittarius",
        "center": "Heart",
        "degrees": {"start": 257, "end": 262.373},
    },
    {
        "name": "Gate 11",
        "sign": "Sagittarius",
        "center": "Ajna",
        "degrees": {"start": 262.373, "end": 268.15},
    },
    {
        "name": "Gate 10",
        "sign": "Sagittarius/Capricorn",
        "center": "Identity",
        "degrees": {"start": 268.15, "end": 273.523},
    },
    {
        "name": "Gate 58",
        "sign": "Capricorn",
        "center": "Root",
        "degrees": {"start": 273.523, "end": 279.3},
    },
        {
        "name": "Gate 38",
        "sign": "Capricorn",
        "center": "Root",
        "degrees": {"start": 279.3, "end": 285.073},
    },
    {
        "name": "Gate 54",
        "sign": "Capricorn",
        "center": "Root",
        "degrees": {"start": 285.073, "end": 290.45},
    },
    {
        "name": "Gate 61",
        "sign": "Capricorn",
        "center": "Head",
        "degrees": {"start": 290.45, "end": 296.223},
    },
    {
        "name": "Gate 60",
        "sign": "Capricorn/Aquarius",
        "center": "Root",
        "degrees": {"start": 296.223, "end": 302},
    },
    {
        "name": "Gate 41",
        "sign": "Aquarius",
        "center": "Root",
        "degrees": {"start": 302, "end": 307.373},
    },
    {
        "name": "Gate 19",
        "sign": "Aquarius",
        "center": "Root",
        "degrees": {"start": 307.373, "end": 313.15},
    },
    {
        "name": "Gate 13",
        "sign": "Aquarius",
        "center": "Identity",
        "degrees": {"start": 313.15, "end": 318.523},
    },
    {
        "name": "Gate 49",
        "sign": "Aquarius",
        "center": "Solar Plexus",
        "degrees": {"start": 318.523, "end": 324.3},
    },
    {
        "name": "Gate 30",
        "sign": "Aquarius/Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 324.3, "end": 330.073},
    },
    {
        "name": "Gate 55",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 330.073, "end": 335.45},
    },
    {
        "name": "Gate 37",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 335.45, "end": 341.223},
    },
    {
        "name": "Gate 63",
        "sign": "Pisces",
        "center": "Head",
        "degrees": {"start": 341.223, "end": 347},
    },
    {
        "name": "Gate 22",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 347, "end": 352.373},
    },
    {
        "name": "Gate 36",
        "sign": "Pisces",
        "center": "Solar Plexus",
        "degrees": {"start": 352.373, "end": 358.15},
    },
        {
        "name": "Gate 25",
        "sign": "Aries/Pisces",
        "center": "Identity",
        "degrees": {"start": 358.15, "end": 3.523},
    },
]

def get_zodiac_sign(degree):
    for zodiac in zodiac_signs:
        if zodiac["start"] <= degree <= zodiac["end"]:
            return zodiac["sign"]
    return "Aries"

def get_gate(degree):
    for gt in gates_data:
        try:
            start = gt["degrees"]["start"]
            end = gt["degrees"]["end"]

            print(f"Checking degree {degree} against gate '{gt['name']}' range ({start} - {end})")

            if start <= degree <= end:
                print(f"Match found: {gt['name']}")
                return gt["name"]
        except KeyError as e:
            print(f"KeyError: {e} in {gt}") 
        except TypeError as e:
            print(f"TypeError: {e} in {gt}")  
    print(f"No match found for degree {degree}.")
    return "unknown"

def next_gate_change(longitude, reference_time=None, step_minutes=1):
    if reference_time is None:
        reference_time = datetime.utcnow().replace(second=0, microsecond=0)

    # Calculate the Julian Day (JD) from the reference time
    jd = swe.julday(
        reference_time.year,
        reference_time.month,
        reference_time.day,
        reference_time.hour + reference_time.minute / 60
    )

    # Sort gates_data by start degree
    #sorted_gates = sorted(gates_data, key=lambda g: g["degrees"]["start"])

    # Determine the current gate
    current_gate = get_gate(longitude)
    
    current_gate_info = next(g for g in gates_data if g["name"] == current_gate)
    current_start_degree = current_gate_info["degrees"]["start"]
    
    next_gate = next(
        (g for g in gates_data if g["degrees"]["start"] > current_start_degree),
        gates_data[0]  # Wrap around to the first gate if no higher start degree exists
    )
    target_degree = next_gate["degrees"]["start"]

    # Increment time until the moon's longitude matches the next gate's start degree
    while True:
        moon_position, _ = swe.calc_ut(jd, swe.MOON)
        current_longitude = moon_position[0]

        # Check if we've reached the target degree (start of the next gate)
        if current_longitude >= target_degree:
            transition_time = swe.revjul(jd)
            year, month, day = map(int, transition_time[:3])
            hour = int(transition_time[3])
            minute = int((transition_time[3] - hour) * 60)
            second = int((((transition_time[3] - hour) * 60) - minute) * 60)

            transition_datetime = datetime(year, month, day, hour, minute, second)
            return transition_datetime, next_gate["name"]

        # Increment Julian Day by the step size
        jd += step_minutes / (24 * 60)  # Convert minutes to fraction of a day

def next_ten_gate_changes(reference_time=None, step_minutes=1):
    if reference_time is None:
        reference_time = datetime.utcnow().replace(second=0, microsecond=0)

    # Calculate the Julian Day (JD) from the reference time
    jd = swe.julday(
        reference_time.year,
        reference_time.month,
        reference_time.day,
        reference_time.hour + reference_time.minute / 60
    )

    # Get the current gate based on longitude
    moon_position, _ = swe.calc_ut(jd, swe.MOON)
    current_longitude = moon_position[0]
    current_gate = next(
        g for g in gates_data if g["degrees"]["start"] <= current_longitude < g["degrees"]["end"]
    )

    # Prepare results list
    results = []
    current_index = gates_data.index(current_gate)

    # Find the next 10 gates sequentially
    for i in range(10):
        next_index = (current_index + i + 1) % len(gates_data)  # Ensure wrap-around
        next_gate = gates_data[next_index]
        target_degree = next_gate["degrees"]["start"]

        # Increment time until the moon's longitude matches the next gate's start degree
        while True:
            moon_position, _ = swe.calc_ut(jd, swe.MOON)
            current_longitude = moon_position[0]

            # Check if the moon's longitude has reached or exceeded the target degree
            if current_longitude >= target_degree:
                transition_time = swe.revjul(jd)
                year, month, day = map(int, transition_time[:3])
                hour = int(transition_time[3])
                minute = int((transition_time[3] - hour) * 60)
                second = int((((transition_time[3] - hour) * 60) - minute) * 60)
                microsecond = int(((((transition_time[3] - hour) * 60) - minute) * 60 - second) * 1e6)

                transition_datetime = datetime(year, month, day, hour, minute, second, microsecond)
                results.append((transition_datetime.isoformat(), next_gate["name"]))

                # Break to calculate the next gate
                jd += step_minutes / (24 * 60)  # Increment for next iteration
                break

            # Increment Julian Day by the step size
            jd += step_minutes / (24 * 60)

    return results

def generate_moon_data():
    now = datetime.utcnow()
    
    jd = swe.julday(
        now.year,
        now.month,
        now.day,
        now.hour + now.minute / 60 + now.second / 3600,
    )

    moon_position, _ = swe.calc_ut(jd, swe.MOON)
    longitude = moon_position[0]

    zodiac_sign = get_zodiac_sign(longitude)
    degree_in_sign = longitude % 30

    gate = get_gate(longitude)
    
    next_change_time, next_gate = next_gate_change(longitude, now)
    next_ten_gates = next_ten_gate_changes()
    moon_data = {
        "date": now.isoformat(),
        "longitude": round(longitude, 6),
        "zodiac_sign": zodiac_sign,
        "degree": round(degree_in_sign, 2),
        "gate": gate,
        "next_gate_change_time": next_change_time.isoformat(),
        "next_gate": next_gate,
        "next_10_gates": next_ten_gates,
    }

    print(f"Moon Data: {moon_data}")
    return moon_data

if __name__ == "__main__":
    generate_moon_data()
