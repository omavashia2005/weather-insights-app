# Weather Insights App

A Weather App that uses the OpenWeatherMap and Visual Crossing APIs and Streamlit for the frontend.

## Objectives

The aim of this project is to:
* Familiarize myself with fetching APIs.
* Manipulate JSON/CSV files for handling data using libraries such as ``Matplotlib`` and ``Pandas``.
* Implementing feature engineering 
* Understand and use ``Streamlit`` to develop a basic frontend.
* Implement a simple integration of backend and frontend (full-stack development).
* Implement ``MySQL`` and Python integration

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/omavashia2005/weather-insights-app.git
2. Install the required packages (streamlit, pandas, matplotlib, json, csv, datetime, timezone)
3. Get an OpenWeatherMap API key
4. Enter this ``bash`` command on your terminal:
   ```bash
   streamlit run weather.py

## Current Features

* Display weather data for a user-specified city.
* Displaying total number of daylight hours
* Correlation between visibility and humidity
* Generate unique emojis based on temperature (e.g., sunny, cloudy, windy).
* Show the "feels like" temperature.
* Switch between temperature units (Fahrenheit, Celsius, Kelvin).
* Display local time
* Display weather data from the next 15 days for a user-specified city.

## Future Additions

Coming soon:
* Plotting the temperature range for the day using Matplotlib.
   * Use API to fetch weather data from the previous and next weeks, store it in a database, and plot using matplotlib 
* Suggesting outdoor activities based on temperature.
   * Work on customized suggestions depending on time
* Generate emoji depending on time of day
* Make the map prettier using [prettymap](https://prettymapp.streamlit.app) GitHub repo

## Additional Folders
   * **Learning** : Folder documenting new concepts I had to learn for this project. For now, that was using the ``sqlite3`` library.
   * **Resources** : Folder containing all the resources I used for testing. Currently, it contains the "resp.json" file that holds sample test data to avoid making multiple API calls while adding new features. 
