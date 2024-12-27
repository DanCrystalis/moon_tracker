import swisseph as swe
import datetime

# Set up Swiss Ephemeris
swe.set_ephe_path('semo_18')  # Adjust to your ephemeris file location

# Define the degree we want the Moon to reach
target_degree = 234.3  # Replace with your desired degree

start_date = datetime.datetime.utcnow()
jd_start = swe.julday(
    start_date.year,
    start_date.month,
    start_date.day,
    start_date.hour + start_date.minute / 60.0,
    swe.GREG_CAL,
)

# Use mooncross_ut to find the exact crossing
try:
    jd_crossing = swe.mooncross_ut(target_degree, jd_start, swe.FLG_SWIEPH)

    # Convert the Julian Day to a calendar date and time
    result_date = swe.revjul(jd_crossing, swe.GREG_CAL)

    # Parse the result_date to extract hours, minutes, and seconds
    year, month, day, hour = result_date
    hour_int = int(hour)
    minute = int((hour - hour_int) * 60)
    second = int(((hour - hour_int) * 60 - minute) * 60)

    print(
        f"The Moon will reach {target_degree}° on {year}-{month:02}-{day:02} "
        f"at {hour_int:02}:{minute:02}:{second:02} UTC."
    )

except swe.Error as e:
    print(f"An error occurred: {e}")
