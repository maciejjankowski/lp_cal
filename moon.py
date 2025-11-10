import os
from datetime import date
from dotenv import load_dotenv
from astral import LocationInfo
from astral.moon import moonrise, phase

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

def get_current_moon_phase():
    p = phase(date.today())
    if p < 1.84566:
        return "( )" 
    elif p < 5.53699:
        return " )" # )
    elif p < 9.22831:
        return "o)" # d)
    elif p < 12.91963:
        return "O)" # o)
    elif p < 16.61096:
        return "O" # 
    elif p < 20.30228:
        return "(O" # (O
    elif p < 23.99361:
        return "(o" # (o
    else:
        return "( " # (

def get_moonrise(target_date=None):
    if target_date is None:
        target_date = date.today()
    return moonrise(loc.observer, target_date)