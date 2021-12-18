import os
from datetime import datetime
import requests
from decouple import config
import telebot


OWT = config('OW_TOKEN')
OWL = config('OW_LOCATION')
TBT = config('TBOT_TOKEN')


print('Weather Bot Working, Enjoy!!')

# send message using the telegram API
bot = telebot.TeleBot(TBT)

@bot.message_handler(commands=['start'])
def send_start(message):
    message_start = """
    Welcome to Weather Bot
    
    To get weather details just type
    '/weather' or '/forecast'.
    
    Have a nice day!!
    """
    bot.send_message(message.chat.id, message_start)

@bot.message_handler(commands=['weather', 'forecast'])
def send_weather(message):
    # send request to API for forecast
    url = f"https://api.openweathermap.org/data/2.5/weather?id={OWL}&appid={OWT}&units=metric"

    data = requests.get(url).json()

    messageTime = datetime.fromtimestamp(data['dt'])
    wmessage = "Hay Pal,\nHere is today's forecast:\n\n"
    wmessage += (f'Time: {messageTime}\n'
                 f"City: {data['name']}\n"
                 f"Description: {data['weather'][0]['description']}\n"
                 f"Temperature: {int(data['main']['temp'])}C\n"
                 f"Feels like: {int(data['main']['feels_like'])}C\n"
                 f"Wind speed: {int(data['wind']['speed'] * 3.6)}Kph\n"
                 )
    bot.send_message(message.chat.id, wmessage)
bot.infinity_polling(timeout=5)
