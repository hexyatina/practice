import requests

city = "Kyiv"
api_key = "e3e0a0a855824b928f190351250806"
base = "http://api.weatherapi.com/v1"

def fetch_weather(city, days=1):
    fc_url = f"{base}/forecast.json?key={api_key}&q={city}&days={days}"
    fc_3 = requests.get(fc_url).json()
    return fc_3

forecast_3 = fetch_weather(city)

def process_data(fc_3):
    forecasts_3 = []

    forecast_list_3 = fc_3["forecast"]["forecastday"]
    for forecast_day_3 in forecast_list_3:
        temp_3 = forecast_day_3["day"]["avgtemp_c"]
        min_temp_3 = forecast_day_3["day"]["mintemp_c"]
        max_temp_3 = forecast_day_3["day"]["maxtemp_c"]
        humidity_3 = forecast_day_3["day"]["avghumidity"]
        it_is_raining_3 = int(forecast_day_3["day"].get("daily_chance_of_rain", 0)) > 30
        uv_3 = forecast_day_3["day"]["uv"]
        date_3 = forecast_day_3["date"]

        warnings_3, advice_3 = [], []

        if max_temp_3 > 30:
            warnings_3.append("Warning! Extremely hot.")
            advice_3.append("Cover your head, drink plenty of water, and wear SPF.")
        if it_is_raining_3:
            warnings_3.append("Chance of rain.")
            advice_3.append("Take an umbrella.")
        if uv_3 >= 8:
            warnings_3.append("High UV expected.")
            advice_3.append("Wear sunglasses and sunscreen.")

        forecasts_3.append({
            "date": date_3,
            "avg_temp": temp_3,
            "min_temp": min_temp_3,
            "max_temp": max_temp_3,
            "humidity": humidity_3,
            "uv": uv_3,
            "it_is_raining": it_is_raining_3,
            "warnings": warnings_3,
            "advice": advice_3
        })

    return forecasts_3

tomorrow_weather_3 = process_data(forecast_3)

if __name__ == "__main__":
    print(tomorrow_weather_3)
