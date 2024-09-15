# Weather Insights App

A basic Weather Insights App that uses the OpenWeatherMap API and Streamlit for the frontend.

## Objectives

The aim of this project is to:
* Familiarize myself with fetching APIs.
* Manipulate JSON/CSV files for handling data using libraries such as Matplotlib and Pandas.
* Understand and use Streamlit to develop a basic frontend.
* Implement a simple integration of backend and frontend (full-stack development).
* Implement MySQL and Python integration

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/omavashia2005/weather-insights-app.git
2. Install the required packages (streamlit, pandas, matplotlib, json, csv, datetime, timezone)
3. Enter this bash command on your terminal:
   ```bash
   streamlit run weather.py

## Current Features

* Display weather data for a user-specified city.
* Generate unique emojis based on temperature (e.g., sunny, cloudy, windy).
* Show the "feels like" temperature.
* Switch between temperature units (Fahrenheit, Celsius, Kelvin).
* Display local time
* Added a "Suggest activities" button

## Future Additions

Coming soon:
* Plotting the temperature range for the day using Matplotlib.
   * Will use another API to fetch weather data from the previous and next weeks, store it in a database, and plot using matplotlib 
* Suggesting outdoor activities based on temperature.
   * Work on customized suggestions depending on time
* Generate emoji depending on time of day
* Try to make the map prettier using [prettymap]([url](https://prettymapp.streamlit.app)) GitHub repo

