"""
weather_api.py
---------------
Handles everything related to talking to the OpenWeatherMap API:
- Fetching live weather data for a given city
- Saving that data into our CSV history file
- Loading the CSV history back in as a Pandas DataFrame

This file is intentionally kept separate from main.py so the
"talking to the internet / files" logic stays isolated from the
"talking to the user" logic.
"""

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Where we keep our history of past lookups
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "weather_history.csv")

# Columns for our history CSV, in the exact order we want them saved
CSV_COLUMNS = [
    "date", "time", "city", "country",
    "temperature", "feels_like", "min_temperature", "max_temperature",
    "humidity", "pressure", "wind_speed", "weather_condition",
]


def get_weather(city):
    """
    Fetch current weather for `city` from OpenWeatherMap.

    Returns a dictionary of clean, ready-to-use weather data on success,
    or None if something went wrong (city not found, bad key, no internet, etc).
    """
    if not API_KEY:
        print("\n❌ No API key found. Please add OPENWEATHER_API_KEY to your .env file.")
        return None

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # gives us Celsius instead of Kelvin
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        print("\n❌ Network error: could not reach the weather service. Check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("\n❌ The request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Something went wrong while making the request: {e}")
        return None

    # Handle specific HTTP status codes with friendly messages
    if response.status_code == 401:
        print("\n❌ Invalid API key. Double-check the key in your .env file.")
        return None
    if response.status_code == 404:
        print(f"\n❌ City '{city}' not found. Please check the spelling and try again.")
        return None
    if response.status_code != 200:
        print(f"\n❌ API error (status code {response.status_code}). Please try again later.")
        return None

    try:
        raw = response.json()
        weather_data = {
            "city": raw["name"],
            "country": raw["sys"]["country"],
            "temperature": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "min_temperature": raw["main"]["temp_min"],
            "max_temperature": raw["main"]["temp_max"],
            "humidity": raw["main"]["humidity"],
            "pressure": raw["main"]["pressure"],
            "wind_speed": raw["wind"]["speed"],
            "weather_condition": raw["weather"][0]["main"],
            "weather_description": raw["weather"][0]["description"],
        }
        return weather_data
    except (KeyError, IndexError) as e:
        print(f"\n❌ Unexpected response format from the API (missing field: {e}).")
        return None


def save_weather_data(data):
    """
    Append one weather record to our CSV history file.
    Creates the file (with headers) if it doesn't exist yet.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    now = datetime.now()
    record = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "city": data["city"],
        "country": data["country"],
        "temperature": data["temperature"],
        "feels_like": data["feels_like"],
        "min_temperature": data["min_temperature"],
        "max_temperature": data["max_temperature"],
        "humidity": data["humidity"],
        "pressure": data["pressure"],
        "wind_speed": data["wind_speed"],
        "weather_condition": data["weather_condition"],
    }

    df_new = pd.DataFrame([record], columns=CSV_COLUMNS)

    file_exists = os.path.isfile(CSV_FILE)
    # mode="a" appends; we only write the header row the first time
    df_new.to_csv(CSV_FILE, mode="a", header=not file_exists, index=False)


def load_weather_data():
    """
    Load the full weather history CSV into a Pandas DataFrame.
    Returns an empty DataFrame (with the right columns) if the file
    doesn't exist yet, so callers never have to special-case "no data".
    """
    if not os.path.isfile(CSV_FILE):
        return pd.DataFrame(columns=CSV_COLUMNS)

    try:
        df = pd.read_csv(CSV_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=CSV_COLUMNS)

    # Basic cleaning: drop rows that are missing critical numeric fields
    numeric_cols = ["temperature", "feels_like", "min_temperature",
                     "max_temperature", "humidity", "pressure", "wind_speed"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["temperature"])
    return df
