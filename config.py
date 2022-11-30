from datetime import datetime
import random as rn
import secrets, string, re, math
import streamlit as st

def createname(x= 6, y =15):
    """Generates a random list of letters. This list will 
    create a name from between 6 and 15 letters by default, However you can pass in diffrent if required"""
    letters = string.ascii_letters
    name_length = rn.randint(x,y)
    nme = ''
    for i in range(name_length):
        nme += ''.join(secrets.choice(letters))
    return str.lower(nme)
name = createname()

"""The API keys will be loaded directly into Streamlit via the secret section. and will be taken from 
st.secrets["API_KEY"] for example, use keys below for testing only!!!"""

## API available from openweathermap.org.
LOCAL_API = st.secrets["WEATHER_API_KEY"] #!!!! Hide after Dev
## API from https://api.n2yo.com  # NASA
API_KEY = st.secrets["NASA_API_KEY"] #!!!! Hide after Dev
SATID = 25544 # this is the space station ID
URL = (f'https://api.n2yo.com/rest/v1/satellite/visualpasses/{SATID}/41.702/-76.014/0/2/60/&apiKey={API_KEY}')
APPNAME = name # 'santatraker1' #!!!! Hide after Dev

def clean_request(f):
    """ Clean text input by removing all leading, trainling and extras spaces, also forces lowercase, This will be
    used for cleaing up text entry"""
    x = str.lower(f)            # force to lowercase
    x = x.strip()               # remove all leading and trailing spaces
    x = re.sub(' +', ' ', x)    # remove any access extra spaces
    return x

def check_postcode(pc):
    """This will check that the text entered fits with a vaild US zipcode or a UK postcode. Note: The UK postcode
    may have a space"""
    uszipcheck = re.findall(r'^[0-9]{5}(?:-[0-9]{4})?$',pc)
    ukpccheck = re.findall(r'[A-Za-z]{1,2}[0-9R][0-9A-Za-z]?[ ]?[0-9][A-Za-z]{2}', pc)
    if len(uszipcheck) > 0:
        out = True
    elif len(ukpccheck) > 0:
        print(ukpccheck)
        out = True
    else:
        out = False
    return out

############ CONVERTORS #############
#### convert unix timestamp in to timestamp
def get_timestamp(ti):
    date = datetime.fromtimestamp(ti).strftime("%Y-%m-%d %H:%M:%S")
    return date
#### convert unix timestamp in to a Date
def get_date_only(ti):
    date = datetime.fromtimestamp(ti).strftime("%Y-%m-%d")
    return date
#### convert unix timestamp into time
def get_time_only(ts):
    tim = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    return tim

def aqi_oz_pm(o,pm2,pm10):
    """Generates the AQI pollutant_concentration stength"""
    return o + pm2 + pm10

def convertMillis(milisecs):
    """ Converts milliseconds into Days, Hours, Minutes and Seconds. If Day is less than 1 then will obmit the day"""
    millis = int(milisecs)
    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000*60)) % 60
    minutes = int(minutes)
    hours = math.floor((millis/(1000*60*60)) % 24)
    days = math.floor(millis/(1000*60*60*24))
    if days > 0:
        out = f"{days}:{hours}:{minutes}:{seconds}"
    else:
        out = f"{hours}:{minutes}:{seconds}"
    return out



