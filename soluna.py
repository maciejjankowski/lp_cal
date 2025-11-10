#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Soluna Display Module
Displays current moon phase and time until sunset on e-paper.
"""
import os
from datetime import datetime
from sun import get_sunset, get_sunrise
from moon import get_current_moon_phase
from epaper_display import EpaperDisplay


def calculate_time_until_sunset(sunset_datetime):
    """Calculate and format time remaining until sunset, or until next sunrise if sunset passed."""
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    time_difference = sunset_datetime - now
    
    if time_difference.total_seconds() <= 0:
        # Sunset passed, get time to next sunrise (tomorrow)
        sunrise_datetime = get_sunrise((now + timedelta(days=1)).date())
        time_to_sunrise = sunrise_datetime - now
        hours = int(time_to_sunrise.total_seconds() // 3600)
        minutes = int((time_to_sunrise.total_seconds() % 3600) // 60)
        return f"^ {hours}:{minutes}"
    
    hours = int(time_difference.total_seconds() // 3600)
    minutes = int((time_difference.total_seconds() % 3600) // 60)
    return f"v {hours}:{minutes}"


def display_soluna_information():
    """Retrieve soluna data and display on e-paper."""
    display = EpaperDisplay(clear_screen=False)
    display.display_soluna(moon_phase, time_to_sunset)
    display.sleep()
    display.cleanup()

moon_phase = get_current_moon_phase()
sunset_time = get_sunset()
time_to_sunset = calculate_time_until_sunset(sunset_time)

if __name__ == "__main__":
    display_soluna_information()
    # print(f"Moon Phase: {moon_phase}")
    # print(f"Time to Sunset: {time_to_sunset}")