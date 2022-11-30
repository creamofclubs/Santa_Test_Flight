import pandas as pd
from config import clean_request
from generate import  get_location as g_loc

import db
database = r"./db/locationData.db"
fld = './data/'
conn = db.create_connection(database)

def get_locations(f):
    #check if location exitits if so get information
    #if location dosent exsits go get add to database and grab info
    x =  g_loc(clean_request(f))
    lat = x[0]
    lon = x[1]
    alt = int(x[2])
    add = x[3]
    data = (f,lat,lon,alt,add)
    print(data)
    db.main(data)
    return data
