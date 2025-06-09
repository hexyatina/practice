import requests
import os
from dotenv import load_dotenv

load_dotenv()


city = "Kyiv"
api_key = os.getenv("WEATHERTOKEN")
base = "http://api.weatherapi.com/v1"

def fetch_weather(city, days=5):
    fc_url = f"{base}/forecast.json?key={api_key}&q={city}&days={days}"
    try:
        response = requests.get(fc_url)
        response.raise_for_status()
        fc_2 = response.json()
        return fc_2
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

forecast_2 = fetch_weather(city)

def process_data(fc_2):
    if not fc_2 or "forecast" not in fc_2 or "forecastday" not in fc_2["forecast"]:
        print("Invalid or missing weather data.")
        return []

    forecasts_2 = []

    forecast_list_2 = fc_2["forecast"]["forecastday"]

    for day_data_2 in forecast_list_2:
        try:
            date_2 = day_data_2["date"]
            forecast_day_2 = day_data_2["day"]

            temp_2 = forecast_day_2["avgtemp_c"]
            min_temp_2 = forecast_day_2["mintemp_c"]
            max_temp_2 = forecast_day_2["maxtemp_c"]
            humidity_2 = forecast_day_2["avghumidity"]
            it_is_raining_2 = forecast_day_2.get("daily_chance_of_rain", 0) > 30
            uv_2 = forecast_day_2["uv"]

            warnings_2, advice_2 = [], []

            if max_temp_2 > 30:
                warnings_2.append("Warning! Extremely hot.")
                advice_2.append("Cover your head, drink plenty of water, and wear SPF.")
            if it_is_raining_2:
                warnings_2.append("Chance of rain.")
                advice_2.append("Take an umbrella.")
            if uv_2 >= 8:
                warnings_2.append("High UV expected.")
                advice_2.append("Wear sunglasses and sunscreen.")

            forecasts_2.append({
                "date": date_2,
                "avg_temp": temp_2,
                "min_temp": min_temp_2,
                "max_temp": max_temp_2,
                "humidity": humidity_2,
                "uv": uv_2,
                "it_is_raining": it_is_raining_2,
                "warnings": warnings_2,
                "advice": advice_2
            })
        except (KeyError, TypeError) as e:
            print(f"Error processing day data: {e}")
            continue

    return forecasts_2

five_day_weather_2 = process_data(forecast_2)

if __name__ == "__main__":
    print(five_day_weather_2)