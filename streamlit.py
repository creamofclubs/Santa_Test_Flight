
import streamlit as st
st.set_page_config(layout="wide")
from generate import *
from getweather import get_weather_SL
import config
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#st.set_page_config(layout="wide", initial_sidebar_state='expanded')


def get_hourly(weather):
    data = []
    for hour in weather['hourly']:
        hour_data = {
            'date' : config.get_date_only(hour['dt']),
            'hour' : config.get_time_only(hour['dt'])[:2],
            'temp': round(hour['temp']),
            'cloudcover': hour['clouds'],
            'gendescription': hour['weather'][0]['description']
        }
        data.append(hour_data)
    return pd.DataFrame(data)



#image = Image.open('santas Test flight.jpg')

st.image('santas Test flight.jpg', caption='Merry Christmas')

# Add instuctions

with st.expander("Instuctions"):
    st.write("""
        :santa: :santa: Well Ho ho ho, Santa has started to test his raindeer. :santa: :santa:
        Enter your postcode or location in the searchbar.

        Once entered, you will get a list of when santa will next fly over you.
        
        apart from the time dates. It will also show you where to look in the sky.

        if you have a smart phone, open up the **compass**.


        **StartDeg, MaxDeg, EndDeg:** are the degrees from a compass, from start middle and end.\n
        **startEl, MaxEl,endEl:** Are the degrees in of height. from 0 = horizon, 90 = direct over your head.\n
        **StartTime, ApexTime, EndTime:** Are the starting times\n
        **mag**: Is brighness :sunglasses: -2 is the brightest\n 
        **Duration**: Is the total length in seconds\n
        **Temp, cloudcover,gendescription** Are the estimated weather condtions\n
    """)
    st.image("https://www.stockvault.net/data/2016/05/20/199020/preview16.jpg")

#Sidebar
try:
    location = st.text_input('Enter Location')
    
    # Generate location
    df= get_sat_info(location)

    maxrows = df[0].shape[0]
    lat = df[1]
    lon = df[2]
    weather = get_weather_SL(lat,lon)
    hourlyweather = get_hourly(weather)
    maxresults = st.slider('How many rows',1,maxrows,10)

# # Main page
    st.title(f'Santa Tracker for {location}')
    st.write("Current Weather")
    
    # Todays Weather
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label='Temp',value = str(weather['current']['temp']) + ' °C')
    with col2:
        st.metric(label='Cloud Cover',value = str(weather['current']['clouds'])+ '%')
    with col3:
        st.metric(label='Sunrise',value = config.get_time_only(weather['current']['sunrise']))
    with col4:
        st.metric(label='Sunset',value = config.get_time_only(weather['current']['sunset']))
    with col5:
        icon = weather['current']['weather'][0]['icon']
        st.image(f'http://openweathermap.org/img/wn/{icon}@2x.png')
    
    df = df[0].drop(['Date_ran','location'], axis=1)
    df['hour'] = df['StartTime'].str[:2]
    hourlyweather['hours'] = hourlyweather['hour'].astype(str)

    #forces column to string before merge
    df.StartDates = df.StartDates.astype(str)
    df.hour = df.hour.astype(str)
    hourlyweather.hours = hourlyweather.hours.astype(str)
    hourlyweather.date = hourlyweather.date.astype(str)
    
    joined = pd.merge(df, hourlyweather, how='left', left_on=['StartDates','hour'], right_on =['date','hours'])
    joined.drop(['date','hour_x','hour_y','hours'],axis=1, inplace=True)
    # Renaming columns for a festive display
    joined.rename(columns={
        'StartDates': 'Date 🎄',
        'StartTime': 'Santa\'s Arrival Time 🎅',
        'StartDeg': 'Starting Direction 🌌',
        'startEl': 'Starting Elevation 🎁',
        'ApexTime': 'Sleigh Highest 🎅',
        'MaxDeg': 'Max Direction',
        'maxEl': 'Max Elevation 🎆',
        'EndTime': 'Departure Time 🎉',
        'EndDeg': 'Departure Direction 🎄',
        'endEl': 'End Elevation 🎁',
        'mag': 'Santa Brightness ⭐️',
        'duration': 'Flight Duration 🎄',
        'temp': 'Temperature 🎄',
        'cloudcover': 'Cloud Cover 🌨️',
        'genderdescription': 'Sky Conditions ❄️'
    }, inplace=True)
    
    st.subheader(f'🎅Santas next test flights.🎅')
    st.caption('Watch the skies for the next magical pass!')
    #st.dataframe(joined.head(maxresults).style.set_precision(2),use_container_width=True)
    st.dataframe(joined.head(maxresults))
    arcdf = joined[['Starting Direction 🌌','Starting Elevation 🎁','Max Direction','Max Elevation 🎆','Departure Direction 🎄','End Elevation 🎁']].head(maxresults)
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    for i, row in arcdf.head().iterrows():
        # Convert directions to radians
        theta_start = np.deg2rad(row["Starting Direction 🌌"])
        theta_max = np.deg2rad(row["Max Direction"])
        theta_end = np.deg2rad(row["Departure Direction 🎄"])
        
        # Radii for elevations
        radii_start = row["Starting Elevation 🎁"]
        radii_max = row["Max Elevation 🎆"]
        radii_end = row["End Elevation 🎁"]
        
        # Generate points for the arc including the peak
        theta = np.linspace(theta_start,theta_max, theta_end, 100)
        radii = np.interp(theta, [theta_start, theta_max, theta_end], [radii_start, radii_max, radii_end])
        #radii = np.interp(theta, [theta_start, theta_end], [radii_start,  radii_end])
        
        # Plot the arc
        ax.plot(theta, radii, label=f'Flight {i+1}', linewidth=2)

    ax.set_title("Santa's Path Across the Sky", va='bottom')
    ax.set_rmax(1)  # Set maximum radius for clarity in elevation representation
    plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    st.pyplot(plt.gcf())

  
except Exception as e: 

    st.title('Please enter a location')
    



