"""
main.py
--------
The entry point of the app. Run this file to start the program.

This file is just the "menu" — it asks the user what they want to do
and calls out to weather_api.py and analysis.py to actually do it.
"""

import pandas as pd

from weather_api import get_weather, save_weather_data, load_weather_data
from analysis import analyze_weather_data, display_analysis


def display_weather(data):
    """Nicely print a single weather lookup result to the terminal."""
    print("\n" + "=" * 40)
    print(f"Weather in {data['city']}, {data['country']}")
    print("=" * 40)
    print(f"Temperature       : {data['temperature']} °C")
    print(f"Feels like        : {data['feels_like']} °C")
    print(f"Min temperature   : {data['min_temperature']} °C")
    print(f"Max temperature   : {data['max_temperature']} °C")
    print(f"Humidity          : {data['humidity']} %")
    print(f"Pressure          : {data['pressure']} hPa")
    print(f"Wind speed        : {data['wind_speed']} m/s")
    print(f"Condition         : {data['weather_condition']}")
    print(f"Description       : {data['weather_description']}")
    print("=" * 40)


def show_history_table():
    """Show the saved weather history as a table using Pandas."""
    df = load_weather_data()
    if df.empty:
        print("\n📭 No weather history saved yet.")
        return

    print("\n🗂  Weather History (most recent 10 records)")
    # to_string keeps the table from getting truncated in the terminal
    print(df.tail(10).to_string(index=False))


def lookup_city_flow():
    city = input("\nEnter city name: ").strip()
    if not city:
        print("❌ City name can't be empty.")
        return

    data = get_weather(city)
    if data is None:
        # get_weather() already printed a helpful error message
        return

    display_weather(data)
    save_weather_data(data)
    print(f"\n✅ Saved this lookup to data/weather_history.csv")


def analyze_flow():
    df = load_weather_data()
    stats = analyze_weather_data(df)
    display_analysis(stats)


def main():
    print("🌤️  Welcome to the Weather API Project (Python + NumPy + Pandas)")

    while True:
        print("\nWhat would you like to do?")
        print("1. Look up weather for a city")
        print("2. View saved weather history")
        print("3. Analyze weather history")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            lookup_city_flow()
        elif choice == "2":
            show_history_table()
        elif choice == "3":
            analyze_flow()
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
