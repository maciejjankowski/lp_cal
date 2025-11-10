import os
from datetime import date
from dotenv import load_dotenv
from suntime import Sun

load_dotenv()

lat_str = os.getenv('LATITUDE')
if lat_str is None:
    raise ValueError("LATITUDE not set in .env")
LATITUDE = float(lat_str)

lon_str = os.getenv('LONGITUDE')
if lon_str is None:
    raise ValueError("LONGITUDE not set in .env")
LONGITUDE = float(lon_str)

def get_sunrise(target_date=None):
    if target_date is None:
        target_date = date.today()
    sun = Sun(LATITUDE, LONGITUDE)
    return sun.get_sunrise_time(target_date)

def get_sunset(target_date=None):
    if target_date is None:
        target_date = date.today()
    sun = Sun(LATITUDE, LONGITUDE)
    return sun.get_sunset_time(target_date)