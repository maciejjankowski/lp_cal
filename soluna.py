#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Soluna Display Module
Displays current moon phase and time until sunset on e-paper.
"""
import os
from datetime import datetime
from sun import get_sunset
from moon import get_current_moon_phase
from epaper_display import EpaperDisplay


def calculate_time_until_sunset(sunset_datetime):
    """Calculate and format time remaining until sunset."""
    now = datetime.now()
    time_difference = sunset_datetime - now
    
    if time_difference.total_seconds() <= 0:
        return "Sunset passed"
    
    hours = int(time_difference.total_seconds() // 3600)
    minutes = int((time_difference.total_seconds() % 3600) // 60)
    return f"{hours}h {minutes}m"


def display_soluna_information():
    """Retrieve soluna data and display on e-paper."""
    moon_phase = get_current_moon_phase()
    sunset_time = get_sunset()
    time_to_sunset = calculate_time_until_sunset(sunset_time)
    
    display = EpaperDisplay()
    display.display_soluna(moon_phase, time_to_sunset)
    display.sleep()
    display.cleanup()


if __name__ == "__main__":
    display_soluna_information()