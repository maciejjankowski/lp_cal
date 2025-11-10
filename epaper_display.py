#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
E-Paper Display Module
Handles authentication display and calendar event rendering on e-paper display
"""
import sys
import os
import time
import logging
from PIL import Image, ImageDraw, ImageFont

# Add library paths
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'lp_cal', 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lp_cal', 'pic')
if os.path.exists(libdir) and os.path.exists(fontdir):
    sys.path.append(libdir)
    sys.path.append(fontdir)
else:
    logging.warning(f"Library directory not found: {libdir}")
    logging.warning(f"Font directory not found: {fontdir}")

from lib.TP_lib import epd2in13_V2

logging.basicConfig(level=logging.INFO)


class EpaperDisplay:
    """Class to manage e-paper display for calendar and authentication."""
    
    def __init__(self, clear_screen=True):
        """Initialize the e-paper display."""
        self.epd = epd2in13_V2.EPD_2IN13_V2()
        self.fontdir = fontdir
        if clear_screen:
            self.epd.init(self.epd.FULL_UPDATE) 
            self.epd.Clear(0xFF)
        else:
            self.epd.init(self.epd.PART_UPDATE) 

        # Initialize event drawing state
        self.event_column = 0
        self.event_y = 0
        logging.info("E-paper display initialized")
        self.image = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.draw = ImageDraw.Draw(self.image)
    
    def _load_fonts(self):
        """Load fonts for display."""
        try:
            font_large = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 24)
            font_medium = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 16)
            font_small = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 14)
            font_tiny = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 12)
        except Exception as e:
            logging.warning(f"Could not load TrueType fonts, using default: {e}")
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
        
        return font_large, font_medium, font_small, font_tiny

    def draw_event(self, draw, time_str, summary, font_tiny, font_small, font_medium):
        """
        Draw a single event at the current position.
        
        Args:
            draw: ImageDraw object
            time_str: Time string for the event
            summary: Event summary text
            font_tiny: Font for time
            font_small: Font for summary
            font_medium: Font for medium text
        """
        x_positions = [0, 125]
        x_pos = x_positions[self.event_column]
        draw.text((x_pos + 85, self.event_y), time_str, font=font_tiny, fill=0)
        self.event_y += 12
        draw.text((x_pos + 3, self.event_y), summary, font=font_medium, fill=0)
        
        # Update position for next event
        # self.event_column = (self.event_column + 1) % 2
        if self.event_column == 0:
            self.event_y += 25
    
    def display_auth_code(self, verification_url, user_code):
        """
        Display authentication challenge code on e-paper.
        
        Args:
            verification_url: URL for user to visit (e.g., 'google.com/device')
            user_code: Authentication code to enter
        """
        try:
            # Create a new image with white background
            
            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()
            
            # Draw text on the image
            y_position = 10
            self.draw.text((10, y_position), "Google Auth", font=font_large, fill=0)
            y_position += 35

            self.draw.text((10, y_position), "Required", font=font_large, fill=0)
            y_position += 40

            self.draw.text((10, y_position), "Visit:", font=font_medium, fill=0)
            y_position += 25

            self.draw.text((10, y_position), verification_url, font=font_small, fill=0)
            y_position += 25

            self.draw.text((10, y_position), "Enter code:", font=font_medium, fill=0)
            y_position += 25

            self.draw.text((10, y_position), user_code, font=font_large, fill=0)

            # Rotate image upside down
            self.image = self.image.rotate(180)

            # Display on e-paper
            self.epd.displayPartBaseImage(self.epd.getbuffer(self.image))
            logging.info(f"Auth code displayed: {user_code}")
            
        except Exception as e:
            logging.error(f"Error displaying auth code: {e}")
            raise
    
    def _draw_events(self, draw, events_list, font_small, font_tiny, font_medium):
        """
        Draw calendar events on the provided draw object.
        
        Args:
            draw: ImageDraw object
            events_list: List of event dictionaries
            font_small: Font for event summaries
            font_tiny: Font for event times
        """
        count = 0  # Initialize count
        if not events_list:
            self.draw.text((5, self.event_y), "No events today", font=font_small, fill=0)
        else:
            # Display events
            displayed_events = set()
            max_events = 8
            
            for event in events_list:
                # Skip duplicate events
                event_key = f"{event.get('summary', 'No Title')}_{event.get('start')}"
                if event_key in displayed_events or count >= max_events:
                    continue
                displayed_events.add(event_key)
                count += 1
                
                # Extract time
                start_time = event.get('start', '')
                if 'T' in start_time:
                    time_str = start_time.split('T')[1][:5]  # HH:MM
                else:
                    time_str = "All day"
                
                # Event summary
                summary = event.get('summary', 'No Title')
                if len(summary) > 14:
                    summary = summary[:14] + "~"
                
                # Draw event
                self.draw_event(draw, time_str, summary, font_tiny, font_small, font_medium)
                
                if self.event_y > self.epd.height - 20:
                    break
        return count
    
    def display_calendar_events(self, events_list):
        """
        Display calendar events on e-paper.
        
        Args:
            events_list: List of event dictionaries with 'start', 'summary', etc.
        """
        try:
            # Create a new image with white background
            
            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()
            
            y_position = 0
            
            # Reset event drawing position
            self.event_column = 0
            self.event_y = y_position
            
            # Draw events
            count = self._draw_events(self.draw, events_list, font_small, font_tiny, font_medium)
            
            # Rotate image upside down
            self.image = self.image.rotate(180)

            # Display on e-paper
            self.epd.displayPartBaseImage(self.epd.getbuffer(self.image))
            logging.info(f"Displayed {count if events_list else 0} events")
            
        except Exception as e:
            logging.error(f"Error displaying calendar events: {e}")
            raise
    
    def display_soluna(self, moon_phase, time_to_sunset):
        """
        Display moon phase and time to sunset at the bottom of the screen.
        
        Args:
            moon_phase: String describing the current moon phase
            time_to_sunset: String describing time remaining until sunset
        """
        try:
            # Create a new image with white background
            
            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()
            
            # Draw at bottom
            y_position = self.epd.height - 30
            self.draw.text((10, y_position), f"{moon_phase}", font=font_small, fill=0)
            y_position += 15
            self.draw.text((10, y_position), f"(*) {time_to_sunset}", font=font_small, fill=0)

            # Rotate image upside down
            self.image = self.image.rotate(180)
            
            # Display on e-paper
            self.epd.displayPartBaseImage(self.epd.getbuffer(self.image))

        except Exception as e:
            logging.error(f"Error displaying soluna: {e}")
            raise
    
    def sleep(self):
        """Put the display to sleep mode."""
        self.epd.sleep()
        logging.info("Display put to sleep")
    
    def cleanup(self):
        """Cleanup and exit display."""
        self.epd.Dev_exit()
        logging.info("Display cleanup complete")
