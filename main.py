#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Main entry point for e-paper calendar display.
Minimal orchestration of auth, events, and display modules.
"""
import os
import events
import auth
from epaper_display import EpaperDisplay
import soluna

def main():
    """Display calendar events on e-paper with automatic authentication."""
    display = None
    
    try:
        # Initialize e-paper display
        display = EpaperDisplay()
        
        # Handle authentication (will display auth code on e-paper if needed)
        creds = auth.get_credentials(display)
        
        # Get today's calendar events
        token_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lp_cal', 'token.json')
        events_list = events.get_todays_calendar_events(token_file)

        # Display events on e-paper
        display.display_calendar_events(events_list)
        moon_phase = soluna.get_current_moon_phase()
        sunset_time = soluna.get_sunset()
        time_to_sunset = soluna.calculate_time_until_sunset(sunset_time)
        display.display_soluna(moon_phase, time_to_sunset)
        # Put display to sleep
        display.sleep()
        
    except KeyboardInterrupt:
        print("Interrupted by user")
        if display:
            display.sleep()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        if display:
            display.sleep()
    finally:
        if display:
            display.cleanup()


if __name__ == "__main__":
    main()
