import os
from datetime import date
from dotenv import load_dotenv
from astral import LocationInfo
from astral.sun import sun

load_dotenv()

lat_str = os.getenv('LATITUDE')
if lat_str is None:
    raise ValueError("LATITUDE not set in .env")
LATITUDE = float(lat_str)

lon_str = os.getenv('LONGITUDE')
if lon_str is None:
    raise ValueError("LONGITUDE not set in .env")
LONGITUDE = float(lon_str)

loc = LocationInfo('Ełk', 'Poland', latitude=LATITUDE, longitude=LONGITUDE)

def get_sunrise(target_date=None):
    if target_date is None:
        target_date = date.today()
    s = sun(loc.observer, target_date)
    return s['sunrise']

def get_sunset(target_date=None):
    if target_date is None:
        target_date = date.today()
    s = sun(loc.observer, target_date)
    return s['sunset']