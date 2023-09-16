import requests
import io
import os
import json
from dotenv import dotenv_values
import pandas as pd
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv('.\.env')

Weather_API_key = os.environ.get("Weather_API_key")

## select Relevant fields for weather APIs

def get_weather_API(location):
    print(location)
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


def num_compare(x, wr):
    if x.name=="weather_condition":
      return x.dropna()[x.dropna().apply(lambda a: wr[x.name].lower() in a)]
    else:
      return x.dropna()[pd.eval(str(wr[x.name])+" "+x.dropna().astype(str))]



## Outfit recommendation logic based on temprature, humidity, weather_condition, wind speed KPH, cloud cover  

def get_outfit_recomendation(weather_response):
    outfit_logic = pd.read_excel("outfit_logic.xlsx")

    if type(weather_response)== str:
        weather_response = weather_response.split("=")[-1].strip() 
        weather_response = json.loads(weather_response)

    
    outfit_logic = outfit_logic.set_index("outfit")
    outfit_logic = outfit_logic.apply(lambda x : num_compare(x,weather_response))
    return outfit_logic.index.tolist()

## activity recommendation logic based on weather conditions

def get_activity_recomendation(weather_response):
    if type(weather_response)== str:
        weather_response = weather_response.split("=")[-1].strip() 
        weather_response = json.loads(weather_response)

    if (weather_response["weather_condition"] in ["cloudy","rain", "thunder"]):
        return "suggest an indoor activities"
    
    else:
        return "suggest an outdoor activities"

