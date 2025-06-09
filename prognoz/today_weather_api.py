import requests
import os
from dotenv import load_dotenv

load_dotenv()


city = "Kyiv"
api_key = os.getenv("WEATHERTOKEN")
base = "http://api.weatherapi.com/v1"

def fetch_weather(city):    # Fetching weather from the site api.weatherapi.com with error handling
    try:
        curr_url = f"{base}/current.json?key={api_key}&q={city}"
        curr_resp = requests.get(curr_url)
        curr_resp.raise_for_status()
        curr = curr_resp.json()
    except Exception as e:
        print(f"Error fetching current weather: {e}")
        curr = {}

    try:
        fc_url = f"{base}/forecast.json?key={api_key}&q={city}&days=2"
        fc_resp = requests.get(fc_url)
        fc_resp.raise_for_status()
        fc = fc_resp.json()
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        fc = {}

    return curr, fc

current, forecast = fetch_weather(city)

def process_data(curr, fc):   #Processing data that we got from the site
    c = curr["current"]
    forecast_day = fc["forecast"]["forecastday"][0]["day"]
    wind = c["wind_kph"]
    temp = c["temp_c"]
    min_temp = forecast_day["mintemp_c"]
    max_temp = forecast_day["maxtemp_c"]
    humidity = c["humidity"]
    it_is_raining = forecast.get("daily_chance_of_rain", 0) > 0
    feels_like = forecast_day.get("feelslike_c", c["temp_c"])
    uv = c["uv"]

    warnings, advice = [], []

    if temp > 30:   #checking the probabilities of different conditions
        warnings.append("Warning! Extremely hot!")
        advice.append("Don't forget to cover your head, drink plenty of water, and use SPF.")
    if it_is_raining:
        warnings.append("It is raining outside.")
        advice.append("Don't forget your umbrella!")
    if uv >= 8:
        warnings.append("High UV!")
        advice.append("Wear your sunglasses.")

    return {    #checking if the data sends correctly
        "current_temp": temp,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "humidity": humidity,
        "uv": uv,
        "it_is_raining": it_is_raining,
        "feels_like": feels_like,
        "wind": wind,
        "warnings": warnings,
        "advice": advice
    }

weather = process_data(current, forecast)   #processing the data and storing it in a variable

if __name__ == "__main__":
    print(weather)  #showcasing what data we got