import requests
import io
import os
import json
from dotenv import dotenv_values

from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv('.\.env')

Weather_API_key = os.environ.get("Weather_API_key")

## select Relevant fields for weather APIs

def get_weather_city(location):
    response = requests.get("http://api.weatherapi.com/v1/current.json?key="+Weather_API_key+"&q="+location)
    if response.status_code == 200:
        data = response.json()
        data_to_use = {}
        data_to_use['location'] = data['location']["name"]
        data_to_use['localtime'] = data['location']["localtime"]
        data_to_use['temperature'] = data['current']['temp_c']
        data_to_use['is_day'] = data['current']['is_day']
        data_to_use['weather_condition'] = data['current']['condition']['text']
        data_to_use['wind_mph'] = data['current']['wind_mph']
        data_to_use['wind_kph'] = data['current']['wind_kph']
        data_to_use['humidity'] = data['current']['humidity']
        data_to_use['feels_like_temperature'] = data['current']['feelslike_c']
        data_to_use['cloud_cover'] = data['current']['cloud']
        data_to_use['visibility'] = data['current']['vis_km']
        resp = json.dumps(data_to_use)
    else:
        resp = "No such city!"

    return resp