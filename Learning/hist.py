import pandas as pd
import requests
import sqlite3
import csv
import json

def hist_data(city, unit, histApiKey):
    # fetching API
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    url = base_url + city + "?" + "unitGroup=" + unit + "&include=days&&key=" + histApiKey + "&contentType=json"

    # storing JSON
    response = requests.get(url)
    data = response.json()

    # dumping JSON file
    with open('hist.json', 'w') as f:
        json.dump(data, f, indent=4)
    extract_data(data)

    # error checking
    if response.status_code == 200:
        return response.json()

    else:
        print("City not found")
        return None

# stores relevant data from JSON to a list
def extract_data(data):
    forecast_data = []

    for day in data['days']:
        forecast_data.append({
            'date_time': day['datetime'],
            'temp_max': day['tempmax'],
            'temp_min': day['tempmin'],
            'temp': day['temp'],
            'feels_like_max': day['feelslikemax'],
            'feels_like_min': day['feelslikemin'],
            'feels_like': day['feelslike']
        }
        )

    list_to_df(forecast_data)

# converts list to dataframe

def list_to_df(forecast_data):
    df = pd.DataFrame(forecast_data)
    df.to_csv('hist.csv')
    df = pd.read_csv('hist.csv')
    load_to_db(df)

def create_db():
    weather_db = sqlite3.connect("Weather.db")
    cur = weather_db.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS weather_forecast 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT,
                    tempmax REAL,
                    tempmin REAL,
                    temp REAL,
                    feelslikemax REAL,
                    feelslikemin REAL,
                    feelslike REAL
                )
        ''')

    weather_db.commit()
    weather_db.close()

# database testing
def load_to_db(df):
    create_db()

    conn = sqlite3.connect("Weather.db")

    df.to_sql('historical_data', conn, if_exists='append', index=False)

    conn.close()

    print(max_min_temp())

def max_min_temp():
    conn = sqlite3.connect("Weather.db")

    cur = conn.cursor()

    cur.execute('''
            SELECT
                date_time as date_time,
                MAX(temp_max) AS max_temperature,
                MIN(temp_min) AS min_temperature
            FROM 
                historical_data
        ''')

    res = cur.fetchone()

    conn.close()

    if res:
        date_time, max_temp, min_temp = res
        return date_time, max_temp, min_temp
    else:
        return None


def main():
    # ******************************************Change path name here*************************************************
    path = '/Users/omavashia/PycharmProjects/LeetCode/.venv/weather_app/hist_api_key'
    # ****************************************************************************************************************

    histApiKey = open(path, 'r').read()
    unit = "metric"
    city = "Tempe"
    hist_data(city, unit, histApiKey)

if __name__ == "__main__":
    main()