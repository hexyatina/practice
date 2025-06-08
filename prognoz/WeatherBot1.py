import logging
from telegram import Update 
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler 
import today_weather_api, five_days_forecast, tomorrow_weather_api

BOT_TOKEN = '7340946921:AAFZrqPGOe5gKcnUP1aXDgUjZT4hGQAMklA'    #api for telegram bot from botfather

#for todays weather
temp = today_weather_api.weather["current_temp"] 
max_temp = today_weather_api.weather["max_temp"]
is_it_raining = today_weather_api.weather["it_is_raining"]
feels_like = today_weather_api.weather["feels_like"]
humidity = today_weather_api.weather["humidity"]
uv = today_weather_api.weather["uv"]

#for tomorrows weather
temp_3 = tomorrow_weather_api.tomorrow_weather_3[0]["avg_temp"]  #average temperature for tomorrow
max_temp_3 = tomorrow_weather_api.tomorrow_weather_3[0]["max_temp"]  #maximum temperature for tomorrow
is_it_raining_3 = tomorrow_weather_api.tomorrow_weather_3[0]["it_is_raining"]  #if it is raining tomorrow
feels_like_3 = tomorrow_weather_api.tomorrow_weather_3[0]["avg_temp"]  #feels like temperature for tomorrow
humidity_3 = tomorrow_weather_api.tomorrow_weather_3[0]["humidity"]  #humidity for tomorrow
uv_3 = tomorrow_weather_api.tomorrow_weather_3[0]["uv"]  #UV index for tomorrow


#for next five days weather
temp_2 = five_days_forecast.five_day_weather_2[0]["avg_temp"]  
max_temp_2 = five_days_forecast.five_day_weather_2[0]["max_temp"] 
is_it_raining_2 = five_days_forecast.five_day_weather_2[0]["it_is_raining"]  
feels_like_2 = five_days_forecast.five_day_weather_2[0]["avg_temp"] 
humidity_2 = five_days_forecast.five_day_weather_2[0]["humidity"]  
uv_2 = five_days_forecast.five_day_weather_2[0]["uv"] 
date = five_days_forecast.five_day_weather_2[0]["date"] 

#logging everything to see that everything goes smoothly and changed it to INFO for basically logging everything that is happening
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',          #basically logs to see if something gone wrong
    level=logging.INFO
)
#simple Telegram bot that provides weather updates
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):        #first message that user gets when he starts the bot
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the most trusted weather bot in the world, type /todays_weather to get the most accurate prediction ever")
    
async def todays_weather(update: Update, context: ContextTypes.DEFAULT_TYPE): #def for todays weather using data from today_weather_api.py
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Today's temperature in Kyiv is: {temp}°C. But it feels like {feels_like}°C. "
                                  f"Max temperature is {max_temp}°C, humidity is {humidity}%, UV index is {uv} and the risk of rain is {'high' if is_it_raining>51 else 'low'}.")
    
async def tomorrows_weather(update: Update, context: ContextTypes.DEFAULT_TYPE): #def for tomorrows weather using data from tomorrow_weather_api.py
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tomorrow's temperature in Kyiv will be: {temp_3}°C. But it will feel like {feels_like_3}°C. "
                                  f"Max temperature is {max_temp_3}°C, humidity is {humidity_3}%, UV index is {uv_3} and the risk of rain is {'high' if is_it_raining_3>51 else 'low'}.")

async def next_five_days_weather(update: Update, context: ContextTypes.DEFAULT_TYPE): #def for next five days weather using data from five_days_forecast.py
    message = "That's the weather that will be in five days:\n\n"
    for day in five_days_forecast.five_day_weather_2:
        date = day.get("date")
        temp_2 = day.get("avg_temp")
        max_temp_2 = day.get("max_temp", "Невідомо")
        feels_like_2 = day.get("avg_temp", "Невідомо")
        humidity_2 = day.get("humidity", "Невідомо")
        uv_2 = day.get("uv", "Невідомо")
        is_it_raining_2 = "high" if day.get("it_is_raining", 0) > 51 else "low"
        message += (
            f"{date}: Average temperature for that day will be: {temp_2}°C, \n"
            f"Feels like: {feels_like_2}°C, \n"
            f"Highest temperature possible: {max_temp_2}°C, \n"
            f"Humidity on that day will be: {humidity_2}%, \n"
            f"UV: {uv_2}, \n"
            f"Possibility of rain: {is_it_raining_2}\n"
            f"\n"
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def next_week_weather(update: Update, context: ContextTypes.DEFAULT_TYPE): #def for next week weather, but for now it is just a placeholder
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Next week is hot as hell!! Stay home and eat your cold ice-cream")


if __name__ == '__main__': #main thing that runs evething that were written above
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    #registering the command handlers
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    weather_today_handler = CommandHandler('todays_weather', todays_weather)
    application.add_handler(weather_today_handler)
    
    weather_tomorrow_handler = CommandHandler('tomorrows_weather', tomorrows_weather)
    application.add_handler(weather_tomorrow_handler)
    
    weather_next_five_days_handler = CommandHandler('next_five_days_weather', next_five_days_weather)
    application.add_handler(weather_next_five_days_handler)
    
    weather_next_week_handler = CommandHandler('next_week_weather', next_week_weather)
    application.add_handler(weather_next_week_handler)
    application.run_polling()