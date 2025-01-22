import statistics
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import streamlit as st
from datetime import datetime, timedelta
import seaborn as sns

# Current weather API settings, basic front end details

st.title("Weather Insights App")
City = st.text_input("Enter City")
st.header(" Pick a unit of temperature 🌡")
unit = st.radio("Units: ", ["Fahrenheit", "Celsius", "Kelvin"])

# Change path name here
# ****************************************************************************************************************
API_path = 'ENTER PATH NAME'
# ****************************************************************************************************************

# API key
apiKey = open(API_path, 'r').read()



# Historical Weather API settings (testing)
# ******************************************Change path name here*************************************************
hist_API_path = 'ENTER PATH'
# ****************************************************************************************************************

# Historical data API Key
histApiKey = open(hist_API_path, 'r').read()

# Fetching historical weather data

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

    forecast_data = extract_data(data)

    # error checking
    if response.status_code == 200:
        return response.json(), forecast_data

    else:
        print("City not found")
        return None

# extracting historical weather data
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

    return forecast_data
    # list_to_df(forecast_data)


# Fetching weather data
def get_weather(city, apiKey):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = base_url + "appid=" + apiKey + "&q=" + city

    response = requests.get(url)
    data = response.json()

    with open('resp.json', 'w') as f:
        json.dump(data, f, indent=4)

    if response.status_code == 200:
        return response.json()

    else:
        st.error("City not found")
        return None

# Temperature convert
def k_f(temp):
    C = temp - 273.15

    return str(int((C * (9/5) + 32))) + " °F"

def k_c(temp):
    return str(int(temp - 273.15)) + " °C"


# Helper function to return the correct emoji
def get_weather_emoji(temp):
        if temp >= 38:
            return "☀️️"
        elif 38 > temp > 25:
            return "⛅"
        elif 10 < temp <= 25:
            return "💨"
        else:
            return "❄️"

def error_catcher():
    st.error("City not found")
    return None;

if not City:
    error_catcher()


path = '/resp.json'

weather_data = get_weather(City, apiKey)
def daylight_hrs():
    with open("resp.json", 'r') as f:
        json_data = json.load(f)

    df1 = pd.json_normalize(json_data)
    df_csv = df1.to_csv("resp.csv", index=False)
    df = pd.read_csv('resp.csv')
    df = df.drop(columns=['weather'])
    df = df.drop(columns=['base'])

    df['sunrise_time'] = df['sys.sunrise'].apply(lambda x: str(datetime.utcfromtimestamp(x)))
    df['sunset_time'] = df['sys.sunset'].apply(lambda x: str(datetime.utcfromtimestamp(x)))

    df[['sunrise_date', 'sunrise_time']] = df['sunrise_time'].str.split(' ', expand=True)
    df[['sunset_date', 'sunset_time']] = df['sunset_time'].str.split(' ', expand=True)
    df = df.drop(columns=['sunset_date'])
    df = df.drop(columns=['sunrise_date'])

    df['hrs'] = df['sys.sunset'] - df['sys.sunrise']
    df['daylight_time'] = df['hrs'].apply(lambda x: str(datetime.utcfromtimestamp(x)))
    df[['daylight_date', 'daylight_hours']] = df['daylight_time'].str.split(' ', expand=True)
    df = df.drop(columns=['daylight_time'])
    df = df.drop(columns=['daylight_date'])
    df = df.drop(columns=['hrs'])
    df = df.drop(columns=['sys.type'])

    daylight_hours = df['daylight_hours'].to_string()

    return daylight_hours[1:]

def Pearson_Corr_Coeff():
    df = pd.read_csv('resp.csv')
    df['pearson_ratio'] = df['visibility'] / df['main.humidity']

    sns.pairplot(df[['visibility', 'main.humidity', 'pearson_ratio']])
    plt.suptitle('Pairplot: Visibility, Humidity, and Pearson Ratio', y=1.02)

    st.pyplot(plt)


# gets local time
local_time = datetime.utcnow() + timedelta(seconds=weather_data['timezone'])
st.header("Local Time :clock4:")
st.subheader(local_time.strftime('%H:%M'))
st.header("Daylight Hours :sunrise:")
st.subheader(daylight_hrs())
st.header("Pearson Visibility Ratio :eyes:")
Pearson_Corr_Coeff()

if weather_data:

    temperature = weather_data['main']['temp']
    temperature_to_c = temperature - 273.15
    temperature_to_f = temperature_to_c * (9 / 5) + 32

    def unitChanger(unit, temp):

        if unit == "Fahrenheit":
            temp = k_f(temp)

        elif unit == "Celsius":
            temp = k_c(temp)

        else:
            temp = str(int(temp)) + " K"

        return temp

    emoji = ""
    emoji = get_weather_emoji(temperature_to_c)

    # weather
    st.header("☁️ WEATHER ☁️")
    st.subheader(f":blue-background[Temperature in  {City}]")
    temp = unitChanger(unit, temperature)
    st.subheader(temp + "\t" + emoji)

    # map
    feels_like = weather_data['main']['feels_like']


    if int(feels_like - 273) != temperature_to_c:
        emoji = get_weather_emoji(int(feels_like - 273))

    st.subheader(f":red-background[Feels Like]")

    st.subheader(unitChanger(unit, feels_like) + "\t" + emoji)
    df = pd.DataFrame(
        {
            "col1": weather_data['main']['temp_min'],
            "col2": np.random.randn(1000) / 50 + -122.4,
            "col3": weather_data['coord']['lat'],
            "col4": weather_data['coord']['lon']
        }
    )

    st.subheader("Where is this? :earth_africa:")
    st.map(df, latitude="col3", longitude="col4")


    # # Making historical data API call
    # _, forcast_Data = hist_data(City, "metric", histApiKey)


    st.subheader("Over the next 15 days:")

    high_Temp = st.button("Highest Temperature")

    if(high_Temp):
        max_temp = -500

        for i in range(0, len(forcast_Data)):
            max_temp = max(max_temp, forcast_Data[i]['temp_max'])

        st.write(max_temp)

    low_Temp = st.button("Lowest Temperature")

    if (low_Temp):
        min_temp = 1000

        for i in range(0, len(forcast_Data)):
            min_temp = min(min_temp, forcast_Data[i]['temp_min'])

        st.write(min_temp)

    avg_Feels_Like = st.button("Average Feels Like Temperature")

    if (avg_Feels_Like):
        avg_temp = 1000
        sum = 0
        for i in range(0, len(forcast_Data)):
            sum += forcast_Data[i]['feels_like']

        st.write(sum // len(forcast_Data))
