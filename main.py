#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Main entry point for e-paper calendar display.
Minimal orchestration of auth, events, and display modules.
"""
import events
import auth
from epaper_display import EpaperDisplay


def main():
    """Display calendar events on e-paper with automatic authentication."""
    display = None
    
    try:
        # Initialize e-paper display
        display = EpaperDisplay()
        
        # Handle authentication (will display auth code on e-paper if needed)
        creds = auth.get_credentials(display)
        
        # Get today's calendar events
        events_list = events.get_todays_calendar_events()
        
        # Display events on e-paper
        display.display_calendar_events(events_list)
        
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
