"""
analysis.py
------------
All the "crunch the numbers" logic lives here, using NumPy for the
math and Pandas for handling the table of data.

Keeping this separate means main.py just calls one function and
prints whatever comes back — it doesn't need to know how the
numbers were calculated.
"""

import numpy as np


def analyze_weather_data(df):
    """
    Take a Pandas DataFrame of weather history and return a dictionary
    of summary statistics calculated with NumPy.

    Returns None if there isn't enough data to analyze.
    """
    if df is None or df.empty:
        return None

    # Pull each column out as a NumPy array — this is where NumPy
    # actually does the work (mean, min, max, std are all NumPy calls).
    temps = df["temperature"].to_numpy(dtype=float)
    humidity = df["humidity"].to_numpy(dtype=float)
    wind = df["wind_speed"].to_numpy(dtype=float)

    stats = {
        "record_count": int(len(df)),
        "avg_temperature": round(float(np.mean(temps)), 2),
        "max_temperature": round(float(np.max(temps)), 2),
        "min_temperature": round(float(np.min(temps)), 2),
        "temperature_range": round(float(np.max(temps) - np.min(temps)), 2),
        "temperature_std": round(float(np.std(temps)), 2),
        "avg_humidity": round(float(np.mean(humidity)), 2),
        "avg_wind_speed": round(float(np.mean(wind)), 2),
    }
    return stats


def display_analysis(stats):
    """Pretty-print the analysis dictionary produced by analyze_weather_data()."""
    if stats is None:
        print("\n📭 No weather history yet. Look up a few cities first, then come back!")
        return

    print("\n📊 Weather History Analysis")
    print("-" * 40)
    print(f"Records analyzed     : {stats['record_count']}")
    print(f"Average temperature  : {stats['avg_temperature']} °C")
    print(f"Highest temperature  : {stats['max_temperature']} °C")
    print(f"Lowest temperature   : {stats['min_temperature']} °C")
    print(f"Temperature range    : {stats['temperature_range']} °C")
    print(f"Temperature std dev  : {stats['temperature_std']} °C")
    print(f"Average humidity     : {stats['avg_humidity']} %")
    print(f"Average wind speed   : {stats['avg_wind_speed']} m/s")
    print("-" * 40)
