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
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
if os.path.exists(libdir):
    sys.path.append(libdir)

from lib.TP_lib import epd2in13_V2

logging.basicConfig(level=logging.INFO)


class EpaperDisplay:
    """Class to manage e-paper display for calendar and authentication."""
    
    def __init__(self):
        """Initialize the e-paper display."""
        self.epd = epd2in13_V2.EPD_2IN13_V2()
        self.fontdir = fontdir
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)
        # Initialize event drawing state
        self.event_column = 0
        self.event_y = 0
        logging.info("E-paper display initialized")
    
    def _load_fonts(self):
        """Load fonts for display."""
        try:
            font_large = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 24)
            font_medium = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 18)
            font_small = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 14)
            font_tiny = ImageFont.truetype(os.path.join(self.fontdir, 'Font.ttc'), 12)
        except Exception as e:
            logging.warning(f"Could not load TrueType fonts, using default: {e}")
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
        
        return font_large, font_medium, font_small, font_tiny
    
    def draw_event(self, draw, time_str, summary, font_tiny, font_small):
        """
        Draw a single event at the current position.
        
        Args:
            draw: ImageDraw object
            time_str: Time string for the event
            summary: Event summary text
            font_tiny: Font for time
            font_small: Font for summary
        """
        x_positions = [5, 125]
        x_pos = x_positions[self.event_column]
        draw.text((x_pos, self.event_y), time_str, font=font_tiny, fill=0)
        draw.text((x_pos + 25, self.event_y), summary, font=font_small, fill=0)
        
        # Update position for next event
        self.event_column = (self.event_column + 1) % 2
        if self.event_column == 0:
            self.event_y += 20
    
    def display_auth_code(self, verification_url, user_code):
        """
        Display authentication challenge code on e-paper.
        
        Args:
            verification_url: URL for user to visit (e.g., 'google.com/device')
            user_code: Authentication code to enter
        """
        try:
            # Create a new image with white background
            image = Image.new('1', (self.epd.width, self.epd.height), 255)
            draw = ImageDraw.Draw(image)
            
            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()
            
            # Draw text on the image
            y_position = 10
            draw.text((10, y_position), "Google Auth", font=font_large, fill=0)
            y_position += 35
            
            draw.text((10, y_position), "Required", font=font_large, fill=0)
            y_position += 40
            
            draw.text((10, y_position), "Visit:", font=font_medium, fill=0)
            y_position += 25
            
            draw.text((10, y_position), verification_url, font=font_small, fill=0)
            y_position += 25
            
            draw.text((10, y_position), "Enter code:", font=font_medium, fill=0)
            y_position += 25
            
            draw.text((10, y_position), user_code, font=font_large, fill=0)
            
            # Rotate image upside down
            image = image.rotate(180)
            
            # Display on e-paper
            self.epd.displayPartBaseImage(self.epd.getbuffer(image))
            logging.info(f"Auth code displayed: {user_code}")
            
        except Exception as e:
            logging.error(f"Error displaying auth code: {e}")
            raise
    
    def _draw_events(self, draw, events_list, font_small, font_tiny):
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
            draw.text((5, self.event_y), "No events today", font=font_small, fill=0)
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
                if len(summary) > 12:
                    summary = summary[:12] + "~"
                
                # Draw event
                self.draw_event(draw, time_str, summary, font_tiny, font_small)
                
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
            image = Image.new('1', (self.epd.width, self.epd.height), 255)
            draw = ImageDraw.Draw(image)
            
            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()
            
            # Draw title
            y_position = 5
            draw.text((5, y_position), "Today's Events", font=font_medium, fill=0)
            y_position += 30
            
            # Draw a line
            draw.line([(5, y_position), (self.epd.width - 5, y_position)], fill=0, width=1)
            y_position += 5
            
            # Reset event drawing position
            self.event_column = 0
            self.event_y = y_position
            
            # Draw events
            count = self._draw_events(draw, events_list, font_small, font_tiny)
            
            # Rotate image upside down
            image = image.rotate(180)
            
            # Display on e-paper
            self.epd.displayPartBaseImage(self.epd.getbuffer(image))
            logging.info(f"Displayed {count if events_list else 0} events")
            
        except Exception as e:
            logging.error(f"Error displaying calendar events: {e}")
            raise
    
    def sleep(self):
        """Put the display to sleep mode."""
        self.epd.sleep()
        logging.info("Display put to sleep")
    
    def cleanup(self):
        """Cleanup and exit display."""
        self.epd.Dev_exit()
        logging.info("Display cleanup complete")
