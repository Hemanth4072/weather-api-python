
# Weather API Project (Python + NumPy + Pandas)

A simple, beginner-friendly app that looks up live weather for any city,
saves every lookup to a history file, and lets you analyze that history
with some basic stats.

## What it does

1. You type in a city name.
2. It fetches live weather from **OpenWeatherMap** (temperature, humidity,
   wind speed, etc.).
3. It prints that weather nicely to your terminal.
4. It saves the result as a new row in `data/weather_history.csv`.
5. Any time you want, you can analyze all your saved history — average
   temperature, hottest/coldest recorded, humidity trends, and more.

## Project structure

```
weather_api_project/
├── main.py              # Run this file — the menu / user interaction
├── weather_api.py        # Talks to the OpenWeatherMap API, saves/loads CSV
├── analysis.py            # NumPy-powered stats on the saved history
├── data/
│   └── weather_history.csv   # Created automatically after your first lookup
├── .env                   # Your real API key goes here (not committed)
├── .env.example            # Template showing what .env should look like
├── requirements.txt
└── README.md
```

## How the Weather API works

The app calls OpenWeatherMap's "Current Weather" endpoint:

```
https://api.openweathermap.org/data/2.5/weather?q=<city>&appid=<your_key>&units=metric
```

It sends your city name and API key, and OpenWeatherMap responds with a
JSON payload containing temperature, humidity, wind, and more. `weather_api.py`
pulls out just the fields we care about and hands back a clean Python dictionary.

If the city doesn't exist, your API key is wrong, or your internet drops,
the app catches that and prints a friendly error instead of crashing.

## Getting an API key

1. Go to https://openweathermap.org/ and create a free account.
2. Once logged in, go to your account's **API keys** tab.
3. Copy the default key (or generate a new one).
4. New keys can take a few minutes to an hour to activate — if you get an
   "invalid API key" error right after signing up, just wait a bit and try again.

## Setting up your `.env` file

1. Copy `.env.example` to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and paste in your real key:
   ```
   OPENWEATHER_API_KEY=paste_your_real_key_here
   ```
3. Never commit your real `.env` file — it's already listed in `.gitignore`.

## Installing dependencies

Make sure you have Python 3 installed, then run:

```bash
pip install -r requirements.txt
```

This installs:
- `requests` — for calling the weather API
- `numpy` — for the number-crunching (averages, min/max, std dev)
- `pandas` — for storing/reading the CSV history as a table
- `python-dotenv` — for loading your API key from `.env`

## Running the project

From inside the `weather_api_project` folder, run:

```bash
python main.py
```

You'll see a menu:

```
🌤️  Welcome to the Weather API Project (Python + NumPy + Pandas)

What would you like to do?
1. Look up weather for a city
2. View saved weather history
3. Analyze weather history
4. Exit
Enter choice (1-4):
```

### Example: looking up a city

```
Enter choice (1-4): 1

Enter city name: Vijayawada

========================================
Weather in Vijayawada, IN
========================================
Temperature       : 33.5 °C
Feels like        : 37.2 °C
Min temperature   : 33.5 °C
Max temperature   : 33.5 °C
Humidity          : 58 %
Pressure          : 1006 hPa
Wind speed        : 3.6 m/s
Condition         : Clouds
Description       : scattered clouds
========================================

✅ Saved this lookup to data/weather_history.csv
```

### Example: analyzing history

```
Enter choice (1-4): 3

📊 Weather History Analysis
----------------------------------------
Records analyzed     : 5
Average temperature  : 31.4 °C
Highest temperature  : 35.2 °C
Lowest temperature   : 27.8 °C
Temperature range    : 7.4 °C
Temperature std dev  : 2.63 °C
Average humidity     : 61.2 %
Average wind speed   : 3.1 m/s
----------------------------------------
```

## Where NumPy is used

NumPy does the actual math in `analysis.py`. Once the Pandas columns are
converted to NumPy arrays, we use:
- `np.mean()` — average temperature, humidity, wind speed
- `np.max()` / `np.min()` — highest/lowest recorded temperature
- `np.std()` — how much the temperature varies (standard deviation)
- Simple subtraction (`max - min`) for the temperature range

## Where Pandas is used

Pandas handles all the "table of data" work:
- **`weather_api.py`** — builds a one-row DataFrame for each lookup and
  appends it to `weather_history.csv` with `to_csv(mode="a")`, and reads
  the whole history back in with `pd.read_csv()`.
- **`main.py`** — uses `df.tail(10).to_string()` to print a clean table
  of your most recent lookups.
- **`analysis.py`** — pulls individual columns out of the DataFrame
  (e.g. `df["temperature"]`) to feed into NumPy.

## A note on beginner-friendliness

Every function does one clear job, there are comments throughout the code
explaining *why* something is done (not just *what*), and errors are
caught and explained in plain language instead of showing scary stack
traces. Feel free to open up `weather_api.py`, `analysis.py`, and
`main.py` and read through them top to bottom — that's the best way to
see how the pieces fit together.
