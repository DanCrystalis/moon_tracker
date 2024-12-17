import swisseph as swe
import json
from datetime import datetime

# Set the path to the Swiss Ephemeris data files
swe.set_ephe_path('semo_18')



# Calculate Julian Day
reference_time = datetime.utcnow()

jd = swe.julday(
        reference_time.year,
        reference_time.month,
        reference_time.day,
        reference_time.hour + reference_time.minute / 60,
    )
moon_position, _ = swe.calc_ut(jd, swe.MOON)
longitude = moon_position[0]

# Set the Ayanamsha to N.C. Lahiri
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Calculate planetary positions and houses
planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
planet_positions = {}
planet_houses = {}
for i, planet in enumerate(planets):
    xx, ret = swe.calc_ut(jd, i, swe.FLG_SPEED)  # Include velocities in the output
    planet_positions[planet] = xx[0]  # Longitude of the planet

    print(f"{planet_positions}")