import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import streamlit as st
from datetime import datetime, timedelta


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

# API key
apiKey = open('/Users/omavashia/PycharmProjects/LeetCode/.venv/lib/api_key', 'r').read()

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

# Frontend
st.title("Weather Insights App")
City = st.text_input("Enter City")
st.header(" Pick a unit of temperature 🌡 ")
unit = st.radio("Units: ", ["Farenheit🇺🇸", "Celcius🇬🇧", "Kelvin🧠"])
if City:
    path = '/Users/omavashia/PycharmProjects/LeetCode/resp.json'

    # weather_data = json.loads(open(path, 'r').read())

    weather_data = get_weather(City, apiKey)

    # gets local time
    local_time = datetime.utcnow() + timedelta(seconds=weather_data['timezone'])
    st.header("Local Time :clock4:")
    st.subheader(local_time.strftime('%H:%M'))

    if weather_data:
        temperature = weather_data['main']['temp']
        temperature_to_c = temperature - 273.15
        temperature_to_f = temperature_to_c * (9 / 5) + 32

        def unitChanger(unit, temp):
            if unit == "Farenheit🇺🇸":
                temp = k_f(temp)

            elif unit == "Celcius🇬🇧":
                temp = k_c(temp)

            else:
                temp = str(int(temp)) + " K"

            return temp

        emoji = ""
        emoji = get_weather_emoji(temperature_to_c)
        st.header("☁️ WEATHER ☁️")
        st.subheader(f":blue-background[Temperature in  {City}]")
        st.subheader(unitChanger(unit, temperature) + "\t" + emoji)

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

        st.button("Suggest an activity")
