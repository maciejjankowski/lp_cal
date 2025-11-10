#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Soluna Display Module
Displays current moon phase and time until sunset on e-paper.
"""
from sun import get_sunset, get_sunrise
from moon import get_current_moon_phase


def calculate_time_until_sunset(sunset_datetime):
    """Calculate and format time remaining until sunset, or until next sunrise if sunset passed."""
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    time_difference = sunset_datetime - now
    
    if time_difference.total_seconds() <= 0:
        # Sunset passed, get time to next sunrise (tomorrow)
        sunrise_datetime = get_sunrise((now + timedelta(days=1)).date())
        return f"^ {sunrise_datetime.hour}:{sunrise_datetime.minute}"
    
    hours = int(time_difference.total_seconds() // 3600)
    minutes = int((time_difference.total_seconds() % 3600) // 60)
    return f"v {hours}:{minutes}"


if __name__ == "__main__":
    moon_phase = get_current_moon_phase()
    sunset_time = get_sunset()
    time_to_sunset = calculate_time_until_sunset(sunset_time)

    print(f"Moon Phase: {moon_phase}")
    print(f"Time to Sunset: {time_to_sunset}")