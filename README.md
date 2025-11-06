# E-Paper Calendar Display

This application displays your Google Calendar events on an e-Paper display with authentication support.

## Features

- **Device Authentication Flow**: When credentials are missing or expired, the authentication code is displayed directly on the e-Paper display
- **Calendar Event Display**: Shows today's calendar events with times and summaries
- **PIL-based Rendering**: All display output uses PIL (Python Imaging Library) for consistent rendering
- **Modular Design**: Separate module (`epaper_display.py`) handles all e-paper display operations
- **Automatic Token Refresh**: Handles expired tokens automatically

## Project Structure

```
lp_cal/
├── main.py              # Main entry point - displays calendar events
├── auth.py              # Authentication module - handles login & displays auth code
├── events.py            # Calendar events fetching
├── epaper_display.py    # E-paper display module using TP_lib
├── credentials.json     # Google OAuth credentials (you provide)
├── token.json           # Stored auth token (auto-generated)
└── requirements.txt     # Python dependencies
```

## Setup

### 1. Install Dependencies

```bash
cd /Users/mj/code/pap/Touch_e-Paper_HAT/python/lp_cal
pip install -r requirements.txt
```

### 2. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop App)
5. Download the credentials and save as `credentials.json` in this directory

### 3. Run the Application

Simply run the main script - it will handle authentication automatically:

```bash
python main.py
```

**What happens:**
- If you have valid credentials (`token.json`), it displays calendar events immediately
- If credentials are missing or expired, it displays the authentication code on the e-paper screen
- You visit the URL on another device and enter the code
- Once authenticated, it displays your calendar events

No need to run separate scripts - everything is handled automatically!

## How It Works

### Single Entry Point

Just run `python main.py` - it automatically handles everything:

1. **Initialize e-paper display**
2. **Check authentication:**
   - If `token.json` exists and is valid → proceed to display events
   - If token is expired but refreshable → refresh automatically  
   - If no valid token → display auth code on e-paper screen
3. **Fetch calendar events** using `events.py`
4. **Display events** using `epaper_display.py`

### Authentication Flow

When authentication is needed:
- Requests device code from Google OAuth
- **Displays verification URL and auth code on e-paper screen**
- You visit the URL on another device and enter the code
- Polls for token completion
- Saves `token.json` for future use

### Display Features

- **Auth Screen**: Shows Google auth URL and code prominently
- **Calendar Screen**: Lists today's events with times and titles
- **PIL Rendering**: All display uses PIL with proper fonts
- **TP_lib Integration**: Uses Waveshare e-paper library for hardware control

## Display Layout

### Authentication Screen
```
Google Auth
Required

Visit:
google.com/device

Enter code:
XXXX-XXXX
```

### Calendar Events Screen
```
Today's Events
─────────────────
09:00  Team Meeting
10:30  Code Review
13:00  Lunch Break
15:00  Project Plan...
```

## Troubleshooting

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### E-Paper Display Not Working
- Check hardware connections
- Ensure SPI is enabled on Raspberry Pi: `sudo raspi-config`
- Verify the display model matches (2.13" V2)

### Authentication Fails
- Delete `token.json` and try again
- Verify `credentials.json` is valid
- Check internet connection

## Notes

- The e-Paper display is refreshed with a full update for authentication screen
- Calendar events use the same display method for consistency
- The display goes to sleep mode after updating to save power
- Events are truncated to fit on the small screen (max 6 events, 15 chars per title)
- All e-paper operations are isolated in `epaper_display.py` module

## Files

- `main.py` - **Main entry point** - handles authentication and displays calendar events
- `auth.py` - Standalone authentication script (optional - main.py handles this automatically)
- `events.py` - Google Calendar API event fetching
- `epaper_display.py` - E-paper display module using TP_lib
- `credentials.json` - Google OAuth client credentials (you provide)
- `token.json` - Stored authentication token (auto-generated)
- `requirements.txt` - Python dependencies

