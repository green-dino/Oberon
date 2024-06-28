import streamlit as st
import requests
from datetime import datetime, timedelta

API_KEY = 'your_openweathermap_api_key'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

st.title("Weather Forecast")

# Get today's date
today = datetime.now().strftime('%Y-%m-%d')

# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

# Function to fetch weather data
def get_weather(city_name, date):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'dt': date,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Input field for city name
city_name = st.text_input("Enter your city name:")

# Buttons to fetch weather for today and tomorrow
if st.button("Show Today's Weather"):
    weather_today = get_weather(city_name, today)
    if weather_today:
        st.write(f"Weather for {today}:")
        st.write(f"Temperature: {weather_today['main']['temp']} K")
        st.write(f"Humidity: {weather_today['main']['humidity']}%")
        st.write(f"Description: {weather_today['weather'][0]['description']}")
    else:
        st.write("Unable to fetch weather data for today.")

if st.button("Show Tomorrow's Weather"):
    weather_tomorrow = get_weather(city_name, tomorrow)
    if weather_tomorrow:
        st.write(f"Weather for {tomorrow}:")
        st.write(f"Temperature: {weather_tomorrow['main']['temp']} K")
        st.write(f"Humidity: {weather_tomorrow['main']['humidity']}%")
        st.write(f"Description: {weather_tomorrow['weather'][0]['description']}")
    else:
        st.write("Unable to fetch weather data for tomorrow.")
