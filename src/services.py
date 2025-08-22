import swisseph as swe
from datetime import datetime
import math
import json
import os

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


def load_gates_data():
    """Load gates data from JSON file"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gates_file_path = os.path.join(script_dir, "gates.json")

        with open(gates_file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: gates.json not found at {gates_file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing gates.json: {e}")
        return []
    except Exception as e:
        print(f"Error loading gates data: {e}")
        return []


# Load gates data from JSON file
gates_data = load_gates_data()


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

            if start <= degree <= end:
                return gt["name"]
        except KeyError as e:
            pass
        except TypeError as e:
            pass
    return "unknown"


def next_gate_changes(count=32, reference_time=None):
    # Clamp count to safe bounds
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 32
    count = max(1, min(128, count))

    if reference_time is None:
        reference_time = datetime.utcnow().replace(microsecond=0)

    jd_start = swe.julday(
        reference_time.year,
        reference_time.month,
        reference_time.day,
        reference_time.hour + reference_time.minute / 60 + reference_time.second / 3600,
    )

    # Get current moon position and gate
    moon_position, _ = swe.calc_ut(jd_start, swe.MOON)
    current_longitude = moon_position[0]

    # Find current gate
    current_gate = None
    for gate in gates_data:
        if gate["degrees"]["start"] <= current_longitude < gate["degrees"]["end"]:
            current_gate = gate
            break

    if not current_gate:
        return []

    results = []
    current_index = gates_data.index(current_gate)

    # Calculate the next `count` gate changes
    for i in range(count):
        next_index = (current_index + i + 1) % len(gates_data)
        next_gate = gates_data[next_index]
        target_degree = next_gate["degrees"]["start"]

        # Find the exact transition time
        transition_jd = find_moon_degree_simple(jd_start, target_degree)

        if transition_jd:
            # Convert Julian Day back to datetime
            transition_time = swe.revjul(transition_jd)
            year, month, day = map(int, transition_time[:3])
            hours, minutes, seconds = decimal_to_hms(transition_time[3])
            transition_datetime = datetime(year, month, day, hours, minutes, seconds)

            results.append((transition_datetime.isoformat(), next_gate["name"]))

            # Update start time for next iteration
            jd_start = transition_jd + 0.001  # Small increment to avoid finding same transition

    return results


def find_moon_degree_simple(start_jd, target_degree):
    """
    Find when the Moon reaches a specific degree using simple binary search.

    Args:
        start_jd: Starting Julian Day
        target_degree: Target lunar longitude in degrees

    Returns:
        Julian Day of the transition, or None if not found
    """
    # Normalize target degree
    target_degree = target_degree % 360

    # Get current position
    moon_position, _ = swe.calc_ut(start_jd, swe.MOON)
    current_longitude = moon_position[0] % 360

    # If we're already at the target, return start time
    if abs(current_longitude - target_degree) < 0.001:
        return start_jd

    # Estimate time to reach target (moon moves ~13.2 degrees per day)
    degrees_to_travel = (target_degree - current_longitude) % 360
    estimated_days = degrees_to_travel / 13.2

    # Set search bounds
    jd_low = start_jd
    jd_high = start_jd + min(estimated_days * 2, 30)  # Max 30 days

    # Binary search
    for _ in range(20):  # Max 20 iterations
        jd_mid = (jd_low + jd_high) / 2

        moon_position, _ = swe.calc_ut(jd_mid, swe.MOON)
        mid_longitude = moon_position[0] % 360

        # Calculate shortest angular distance
        diff = (mid_longitude - target_degree + 180) % 360 - 180

        if abs(diff) < 0.001:  # Within 3.6 seconds of arc
            return jd_mid

        if diff > 0:
            jd_high = jd_mid
        else:
            jd_low = jd_mid

        # Check if search bounds are too close
        if jd_high - jd_low < 0.0001:  # About 8.6 seconds
            return jd_mid

    return None


def decimal_to_hms(decimal_hours):
    # Convert decimal hours to total whole seconds using floor to avoid 60-second rollovers
    total_seconds = int(decimal_hours * 3600)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds


def convert_to_dms(degrees):
    d = int(degrees)

    remaining = abs(degrees - d)
    minutes = int(remaining * 60)

    return f"{d}°{minutes}"


def calculate_moon_phase(longitude):
    """Calculate moon phase based on lunar longitude"""
    # Moon phases based on longitude:
    # 0° = New Moon, 90° = First Quarter, 180° = Full Moon, 270° = Last Quarter
    if 0 <= longitude < 45:
        return "Waxing Crescent"
    elif 45 <= longitude < 90:
        return "1st Quarter"
    elif 90 <= longitude < 135:
        return "Waxing Gibbous"
    elif 135 <= longitude < 180:
        return "Full Moon"
    elif 180 <= longitude < 225:
        return "Waning Gibbous"
    elif 225 <= longitude < 270:
        return "3rd Quarter"
    elif 270 <= longitude < 315:
        return "Waning Crescent"
    else:
        return "Dark Moon"


def generate_moon_data(count=32):
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
    dms = convert_to_dms(degree_in_sign)

    gate = get_gate(longitude)

    next_gates = next_gate_changes(count=count)

    # Calculate moon phase as fallback
    moon_phase = calculate_moon_phase(longitude)
    illumination = abs(math.sin(math.radians(longitude)))

    moon_data = {
        "date": now.isoformat(),
        "longitude": round(longitude, 6),
        "zodiac_sign": zodiac_sign,
        "degree": dms,
        "gate": gate,
        "next_gates": next_gates,
        "moon_phase": moon_phase,
        "illumination": round(illumination, 3),
    }

    print(f"Moon Data: {moon_data}")
    return moon_data


if __name__ == "__main__":
    generate_moon_data()
