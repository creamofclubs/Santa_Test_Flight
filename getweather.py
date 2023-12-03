from geopy.geocoders import Nominatim
import requests as r
import streamlit as st
import pandas as pd
import time
import config

geolocator = Nominatim(user_agent=config.APPNAME)
api = config.LOCAL_API

@st.cache_data 
def get_weather(place = 'castleford'):
    location = geolocator.geocode(place)
    lat = location.latitude
    lon = location.longitude
    #api = config.API
    weatherurl = (f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid={api}&units=metric')
    weather = r.get(weatherurl).json()
    Currentweather = get_current(weather,location)
    daily = get_dailt_hourly(weather,location)
    
    
    return weather, daily, Currentweather
@st.cache_data 
def get_weather_SL(lat,lon):
    #api = config.API
    weatherurl = (f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid={api}&units=metric')
    weather = r.get(weatherurl).json()
    return weather

def get_current(weather,location):
    Current = weather['current']
    current_data = {
    'datetime' : config.get_timestamp(Current['dt']),
    'sunrise' : config.get_time_only(Current['sunrise']),
    'sunset' : config.get_time_only(Current['sunset']),
    'temp': Current['temp'],
    'feels_like': Current['feels_like'],
    'pressure': Current['pressure'],
    'humidity': Current['humidity'],
    'dew_point': Current['dew_point'],
    'uvindex': Current['uvi'],
    'cloudcover': Current['clouds'],
    'visibility': Current['visibility'],
    'wind_speed': Current['wind_speed'],
    'wind_direction': Current['wind_deg'],
    'genweather': Current['weather'][0]['main'],
    'gendescription': Current['weather'][0]['description']

}
    return current_data


def get_dailt_hourly(weather,location='cas'):
    data = []
    for hour in weather['hourly']:
        hour_data = {
            'datetime' : config.get_timestamp(hour['dt']),
            'temp': hour['temp'],
            'wind_speed': hour['wind_speed'],
            'cloudcover': hour['clouds'],
            'rain_pop' : hour['pop'],
            'gendescription': hour['weather'][0]['description']
        }
        data.append(hour_data)
 
    return data


def get_daily(weather):
    
    for dw in weather['daily']:
        day_data = {
            'datetime' : config.get_timestamp(dw['dt']),
            'sunrise' : config.get_time_only(dw['sunrise']),
            'sunset' : config.get_time_only(dw['sunset']),
            'moonrise' : config.get_time_only(dw['moonrise']),
            'moon_phase' : (dw['moon_phase']),
            'temp': dw['temp'],
            'wind_speed': dw['wind_speed'],
            'cloudcover': dw['clouds'],
            'rain_pop' : dw['pop'],
            'gendescription': dw['weather'][0]['description']
        }
        #print(day_data)
        return day_data
  

def get_weather_icon(weathercode):
    url = 'http://openweathermap.org/img/wn/10d@2x.png'


places = ['castleford']
for place in places:
    try:
        get_weather(place)
        time.sleep(1)
    except Exception as e:
        print(e)
        print(f'Location not found for {place}') 





