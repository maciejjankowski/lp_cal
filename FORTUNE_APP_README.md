# Fortune Cookie App - Ciasteczko z Wróżbą

An interactive e-paper app that teaches about consent and boundaries through playful fortune cookies in Polish.

## Features

- **200+ Funny Polish Fortune Cookies**: Humorous and lighthearted messages to brighten your day
- **Consent & Boundaries Education**: Teaches about personal space and respecting boundaries through interactive touch feedback
- **Touch Cooldown System**: 15-second cooldown period between touches
- **Boundary Messages**: Special messages when touched too soon, teaching about consent
- **Interactive Prompts**: Shows "Można dotykać ;-)" after 10-30 seconds when ready to be touched again
- **QR Code**: Every screen displays a QR code in the bottom-right corner linking to https://maciejjankowski.com/qr/

## How It Works

1. **Initial Display**: Shows a random fortune cookie message
2. **Touch Interaction**: Tap the screen to get a new fortune
3. **Too Soon?**: If you touch within 15 seconds, you'll see messages like:
   - "Nie dotykaj mnie!" (Don't touch me!)
   - "Może najpierw powiesz jak masz na imię, zanim zaczniesz mnie dotykać" (Maybe tell me your name before touching me)
   - Plus a boundary-respecting fortune cookie
4. **Ready Prompt**: After 10-30 seconds, displays "Można dotykać ;-)" to invite interaction

## Installation

First, install the required dependencies:

```bash
pip3 install -r requirements.txt
```

This will install the `qrcode` library and other required packages.

## Running the App

```bash
cd /home/user/lp_cal
python3 fortune_app.py
```

Or make it executable and run directly:
```bash
chmod +x fortune_app.py
./fortune_app.py
```

## Files

- `fortune_app.py` - Main application with touch handling and display logic
- `fortune_messages.py` - Contains 200+ fortune cookies and boundary messages
  - `REGULAR_FORTUNES` - 200+ funny fortune cookies
  - `BOUNDARY_FORTUNES` - 30 messages about respecting boundaries
  - `get_touch_too_soon_message()` - Warning messages for early touches

## Educational Purpose

This app uses humor and interactive technology to teach important concepts:
- **Consent**: Touch requires permission and timing
- **Boundaries**: Everyone has the right to personal space
- **Respect**: Waiting for the right moment shows care
- **Communication**: Clear signals about when interaction is welcome

## Technical Details

- **Display**: Waveshare e-Paper 2.13" V2 (rotated 90 degrees clockwise for landscape orientation)
- **Touch Controller**: GT1151 with debouncing (1 second minimum between touch events)
- **Cooldown**: 15 seconds between allowed touches
- **Touch Debounce**: 1.0 second minimum between processing touch events (prevents avalanche triggering)
- **Prompt Delay**: Random 10-30 seconds before showing "ready" message
- **Font Support**: TrueType fonts with fallback to default
- **QR Code**: Generated using qrcode library, 50x50 pixels, linking to https://maciejjankowski.com/qr/
- **Dependencies**: Requires `qrcode` package (see requirements.txt)
- **Display Rotation**: Images created at 250x122 pixels, rotated 270 degrees for proper orientation

## Customization

You can easily customize:
- Cooldown period: Change `self.touch_cooldown` in `FortuneApp.__init__()` (default: 15 seconds)
- Touch debounce time: Change `self.touch_debounce` in `FortuneApp.__init__()` (default: 1.0 second)
- Prompt timing: Modify the `random.uniform(10, 30)` range
- Add more fortunes: Add to lists in `fortune_messages.py`
- Messages: Edit existing messages in `fortune_messages.py`
- QR Code URL: Change the URL in `_generate_qr_code()` calls throughout `fortune_app.py`
- QR Code size: Modify the `size` parameter in `_generate_qr_code()` calls
- Display rotation: Change the `rotate()` angle (currently 270 degrees for 90° clockwise)

## License

Part of the lp_cal project.
