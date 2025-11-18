#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Fortune Cookie App with Touch Boundaries
An interactive e-paper app teaching consent and boundaries through fortune cookies
"""
import sys
import os
import time
import logging
import random
from PIL import Image, ImageDraw, ImageFont
import qrcode

# Add library paths
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lp_cal', 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lp_cal', 'pic')
if os.path.exists(libdir) and os.path.exists(fontdir):
    sys.path.append(libdir)
    sys.path.append(fontdir)

from lib.TP_lib import epd2in13_V2
from lib.TP_lib import gt1151
import fortune_messages

logging.basicConfig(level=logging.INFO)


class FortuneApp:
    """Interactive fortune cookie app with consent boundaries."""

    def __init__(self):
        """Initialize the fortune cookie app."""
        self.epd = epd2in13_V2.EPD_2IN13_V2()
        self.gt = gt1151.GT1151()
        self.fontdir = fontdir

        # Touch state tracking
        self.last_touch_time = 0
        self.touch_cooldown = 15  # seconds before can touch again
        self.can_touch_prompt_shown = False
        self.next_prompt_time = 0
        self.last_touch_processed = 0  # Track last processed touch to prevent avalanche
        self.touch_debounce = 1.0  # Minimum seconds between processing touches
        self.is_processing_touch = False  # Flag to prevent concurrent touch processing

        # Initialize display
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)

        # Initialize touch controller
        self.gt.GT_Init()
        self.GT_Dev = gt1151.GT_Development()
        self.GT_Old = gt1151.GT_Development()

        logging.info("Fortune cookie app initialized")

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

    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width."""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def _generate_qr_code(self, url, size=60):
        """
        Generate a QR code image for the given URL.

        Args:
            url: The URL to encode in the QR code
            size: Size of the QR code in pixels

        Returns:
            PIL Image object containing the QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        # Resize to desired size
        qr_img = qr_img.resize((size, size), Image.NEAREST)

        return qr_img

    def display_fortune(self, message, is_boundary_message=False):
        """
        Display a fortune cookie message on the e-paper screen.

        Args:
            message: The fortune cookie message to display
            is_boundary_message: Whether this is a boundary-related message
        """
        try:
            # Create image (swapped dimensions for 90-degree rotation)
            image = Image.new('1', (self.epd.height, self.epd.width), 255)
            draw = ImageDraw.Draw(image)

            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()

            # Draw title
            y_position = 10
            title = "🥠 CIASTECZKO Z WRÓŻBĄ" if not is_boundary_message else "⚠️ GRANICE"
            draw.text((5, y_position), title, font=font_medium, fill=0)
            y_position += 30

            # Draw separator line (image width is now self.epd.height)
            draw.line([(5, y_position), (self.epd.height - 5, y_position)], fill=0, width=1)
            y_position += 10

            # Wrap and draw fortune message (image width is now self.epd.height)
            wrapped_lines = self._wrap_text(message, font_small, self.epd.height - 20)
            for line in wrapped_lines:
                draw.text((10, y_position), line, font=font_small, fill=0)
                y_position += 18

            # Draw footer separator (image height is now self.epd.width)
            y_position = self.epd.width - 35
            draw.line([(5, y_position), (self.epd.height - 5, y_position)], fill=0, width=1)
            y_position += 8

            # Draw footer message
            if is_boundary_message:
                footer = "Szacunek = Podstawa"
            else:
                footer = "Dotknij dla nowej wróżby"
            draw.text((10, y_position), footer, font=font_tiny, fill=0)

            # Generate and paste QR code in bottom right corner
            qr_code = self._generate_qr_code("https://maciejjankowski.com/qr/", size=50)
            qr_x = self.epd.height - 55  # 5px margin from right (image width is self.epd.height)
            qr_y = self.epd.width - 55  # 5px margin from bottom (image height is self.epd.width)
            image.paste(qr_code, (qr_x, qr_y))

            # Display on e-paper (rotate 90 degrees clockwise = -90 or 270 degrees)
            image = image.rotate(270, expand=False)
            self.epd.displayPartBaseImage(self.epd.getbuffer(image))

            logging.info(f"Displayed fortune: {message[:50]}...")

        except Exception as e:
            logging.error(f"Error displaying fortune: {e}")
            raise

    def display_touch_prompt(self):
        """Display 'Można dotykać ;-)' prompt."""
        try:
            # Create image (swapped dimensions for 90-degree rotation)
            image = Image.new('1', (self.epd.height, self.epd.width), 255)
            draw = ImageDraw.Draw(image)

            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()

            # Draw centered message
            message = "Można dotykać ;-)"
            bbox = font_large.getbbox(message)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (self.epd.height - text_width) // 2  # Image width is self.epd.height
            y = (self.epd.width - text_height) // 2  # Image height is self.epd.width

            draw.text((x, y), message, font=font_large, fill=0)

            # Generate and paste QR code in bottom right corner
            qr_code = self._generate_qr_code("https://maciejjankowski.com/qr/", size=50)
            qr_x = self.epd.height - 55  # 5px margin from right (image width is self.epd.height)
            qr_y = self.epd.width - 55  # 5px margin from bottom (image height is self.epd.width)
            image.paste(qr_code, (qr_x, qr_y))

            # Display on e-paper (rotate 90 degrees clockwise = -90 or 270 degrees)
            image = image.rotate(270, expand=False)
            self.epd.displayPartBaseImage(self.epd.getbuffer(image))

            self.can_touch_prompt_shown = True
            logging.info("Displayed 'Można dotykać' prompt")

        except Exception as e:
            logging.error(f"Error displaying touch prompt: {e}")

    def display_too_soon_message(self):
        """Display 'touched too soon' warning with boundary fortune."""
        try:
            # Get warning message
            warning = fortune_messages.get_touch_too_soon_message()

            # Create image (swapped dimensions for 90-degree rotation)
            image = Image.new('1', (self.epd.height, self.epd.width), 255)
            draw = ImageDraw.Draw(image)

            # Load fonts
            font_large, font_medium, font_small, font_tiny = self._load_fonts()

            # Draw warning in large text
            y_position = 20
            wrapped_warning = self._wrap_text(warning, font_large, self.epd.height - 20)  # Image width is self.epd.height
            for line in wrapped_warning:
                bbox = font_large.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (self.epd.height - text_width) // 2  # Image width is self.epd.height
                draw.text((x, y_position), line, font=font_large, fill=0)
                y_position += 30

            y_position += 20

            # Draw separator
            draw.line([(10, y_position), (self.epd.height - 10, y_position)], fill=0, width=2)  # Image width is self.epd.height
            y_position += 15

            # Draw boundary fortune
            boundary_fortune = fortune_messages.get_boundary_fortune()
            wrapped_fortune = self._wrap_text(boundary_fortune, font_small, self.epd.height - 20)  # Image width is self.epd.height
            for line in wrapped_fortune:
                draw.text((10, y_position), line, font=font_small, fill=0)
                y_position += 18

            # Generate and paste QR code in bottom right corner
            qr_code = self._generate_qr_code("https://maciejjankowski.com/qr/", size=50)
            qr_x = self.epd.height - 55  # 5px margin from right (image width is self.epd.height)
            qr_y = self.epd.width - 55  # 5px margin from bottom (image height is self.epd.width)
            image.paste(qr_code, (qr_x, qr_y))

            # Display on e-paper (rotate 90 degrees clockwise = -90 or 270 degrees)
            image = image.rotate(270, expand=False)
            self.epd.displayPartBaseImage(self.epd.getbuffer(image))

            logging.info(f"Displayed 'too soon' message: {warning}")

        except Exception as e:
            logging.error(f"Error displaying too soon message: {e}")

    def handle_touch(self):
        """Handle touch event with cooldown logic and debouncing."""
        current_time = time.time()
        time_since_last_processed = current_time - self.last_touch_processed

        # Debounce: Ignore touches that are too close together (prevent avalanche)
        if time_since_last_processed < self.touch_debounce:
            logging.debug(f"Touch debounced: {time_since_last_processed:.2f}s < {self.touch_debounce}s")
            return

        # Prevent concurrent touch processing
        if self.is_processing_touch:
            logging.debug("Touch ignored - already processing another touch")
            return

        self.is_processing_touch = True
        self.last_touch_processed = current_time

        try:
            time_since_last_touch = current_time - self.last_touch_time

            # Check if touch is allowed
            if time_since_last_touch < self.touch_cooldown:
                logging.info(f"Touch too soon! {time_since_last_touch:.1f}s < {self.touch_cooldown}s")
                self.display_too_soon_message()
                # Reset cooldown timer
                self.last_touch_time = current_time
                # Set next prompt time (10-30 seconds from now)
                self.next_prompt_time = current_time + random.uniform(10, 30)
                self.can_touch_prompt_shown = False
            else:
                logging.info("Touch accepted - showing new fortune")
                # Show new fortune
                fortune = fortune_messages.get_random_fortune()
                self.display_fortune(fortune)
                # Update last touch time
                self.last_touch_time = current_time
                # Set next prompt time (10-30 seconds from now)
                self.next_prompt_time = current_time + random.uniform(10, 30)
                self.can_touch_prompt_shown = False
        finally:
            self.is_processing_touch = False

    def check_touch(self):
        """Check for touch events."""
        try:
            # Check touch interrupt pin
            if self.gt.digital_read(self.gt.INT) == 0:
                self.GT_Dev.Touch = 1
            else:
                self.GT_Dev.Touch = 0

            # Scan for touch
            self.gt.GT_Scan(self.GT_Dev, self.GT_Old)

            # If touch detected, handle it
            if self.GT_Dev.TouchpointFlag:
                self.GT_Dev.TouchpointFlag = 0
                self.handle_touch()

        except Exception as e:
            logging.error(f"Error checking touch: {e}")

    def run(self):
        """Main app loop."""
        try:
            # Display initial fortune
            initial_fortune = fortune_messages.get_random_fortune()
            self.display_fortune(initial_fortune)
            self.last_touch_time = time.time()
            self.next_prompt_time = self.last_touch_time + random.uniform(10, 30)

            logging.info("Fortune app running... Press Ctrl+C to exit")

            # Main loop
            while True:
                # Check for touch events
                self.check_touch()

                # Check if it's time to show "Można dotykać" prompt
                current_time = time.time()
                if (not self.can_touch_prompt_shown and
                    current_time >= self.next_prompt_time and
                    current_time - self.last_touch_time >= self.touch_cooldown):
                    self.display_touch_prompt()

                # Small delay to avoid excessive CPU usage
                time.sleep(0.1)

        except KeyboardInterrupt:
            logging.info("App interrupted by user")
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup and exit."""
        try:
            self.epd.sleep()
            self.epd.Dev_exit()
            logging.info("Fortune app cleanup complete")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")


def main():
    """Main entry point."""
    app = FortuneApp()
    app.run()


if __name__ == "__main__":
    main()
