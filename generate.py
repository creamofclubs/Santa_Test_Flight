from config import *
from geopy.geocoders import Nominatim
import pandas as pd
import requests as r
import streamlit as st
import time

fld = './data/'

geolocator = Nominatim(user_agent=APPNAME)

# returns the elevation from lat, long, based on open elevation data
@st.cache
def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
    res = r.get(query).json()  # json object, various ways you can extract value
    # one approach is to use pandas json functionality:
    elevation = pd.json_normalize(res, 'results')['elevation'].values[0]
    return elevation

# returns latitude, londitude, Alttude, and address from geolocator
@st.cache
def get_location(place):
    """Gets the location information from the Geo Api then gets the elevation information.
    Paremeters: require as place or location"""
    location = geolocator.geocode(place)
    lat = location.latitude
    lon = location.longitude
    address = location.address
    alt = get_elevation(lat,lon)
    return lat,lon,alt,address

# processes the satilate passing information and while convertiing the unix times to datetime
@st.cache
def process_file(d):
    passes = d['passes']
    df = pd.DataFrame(passes)
    df['startUTC'] = pd.to_datetime(df['startUTC'],unit='s')
    df['endUTC'] = pd.to_datetime(df['endUTC'],unit='s')
    df['startVisibility'] = pd.to_datetime(df['startVisibility'],unit='s')
    df['maxUTC'] = pd.to_datetime(df['maxUTC'],unit='s')
    df['location'] = d['location']
    ##rename cols
    df = df.rename(columns={'startAz' : 'StartDeg','maxAz' : 'MaxDeg','endAz' : 'EndDeg'})
    ## Modify datetime colums
    df['Date_ran'] = pd.to_datetime('today')
    df['Date_ran'] = df['Date_ran'].dt.date
    df['StartDates'] = df['startUTC'].dt.date
    df['StartTime'] = df['startUTC'].dt.time.astype(str)
    df['ApexTime'] = df['maxUTC'].dt.time.astype(str)
    df['EndTime'] = df['endUTC'].dt.time.astype(str)
    df = df[['Date_ran','StartDates','StartTime','StartDeg','startEl', 'ApexTime','MaxDeg','maxEl','EndTime','EndDeg' ,'endEl', 'mag', 'duration', 'location']]
    df = df.round(2)
    return df

# generate the satilite information
@st.cache(suppress_st_warning=True)
def get_sat_info(place = "Castleford"):
    st.snow()
    getloc = get_location(place)
    lat = getloc[0]
    lon = getloc[1]
    alt = getloc[2]
    URL = (f'https://api.n2yo.com/rest/v1/satellite/visualpasses/{SATID}/{lat}/{lon}/{alt}/24/60/&apiKey={API_KEY}')
    data  = r.get(URL).json()
    data['location'] = place
    df = process_file(data)
    return df,lat,lon
