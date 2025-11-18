# Fortune Cookie Web App for Kindle Paperwhite

A web-based fortune cookie app optimized for Kindle Paperwhite 7th generation's experimental web browser. This interactive app teaches about consent and boundaries through playful fortune cookies in Polish.

## Features

- **229 Funny Polish Fortune Cookies**: Humorous and lighthearted messages to brighten your day
- **Consent & Boundaries Education**: Teaches about personal space and respecting boundaries through interactive touch feedback
- **15-Second Cooldown System**: Prevents interaction fatigue and teaches patience
- **Boundary Messages**: Special warning messages when tapped too soon, teaching about consent
- **Interactive Prompts**: Shows "Można dotykać ;-)" after 10-30 seconds when ready for interaction
- **QR Code**: Displays a QR code linking to https://maciejjankowski.com/qr/
- **E-ink Optimized**: High contrast, no animations, perfect for e-paper displays
- **Touch-Friendly**: Large buttons and simple interface designed for touchscreen use
- **Standalone File**: Single HTML file - no internet connection required after download

## How to Use on Kindle Paperwhite

### Installation

1. **Download the file**: Transfer `fortune_cookie_kindle.html` to your Kindle using:
   - USB cable (drag and drop to Documents folder)
   - Send to Kindle email
   - Download directly on Kindle if you have the URL

2. **Open in Browser**:
   - On your Kindle, go to Menu → Experimental Browser
   - Navigate to the file location or enter the file path
   - Alternatively, use "Go to URL" and enter: `file:///mnt/us/documents/fortune_cookie_kindle.html`

3. **Bookmark it**: Add the page to your browser bookmarks for easy access

### How It Works

1. **Initial Display**: Shows a random fortune cookie message
2. **Touch Interaction**: Tap the "Losuj Wróżbę" button or anywhere on the screen to get a new fortune
3. **Too Soon?**: If you touch within 15 seconds, you'll see warning messages like:
   - "Nie dotykaj mnie!" (Don't touch me!)
   - "Może najpierw powiesz jak masz na imię, zanim zaczniesz mnie dotykać" (Maybe tell me your name before touching me)
   - Plus a boundary-respecting fortune cookie
4. **Cooldown Timer**: Shows countdown of seconds until you can tap again
5. **Ready Prompt**: After 10-30 seconds, displays "Można dotykać ;-)" to invite interaction

## Educational Purpose

This app uses humor and interactive technology to teach important concepts:
- **Consent**: Touch requires permission and timing
- **Boundaries**: Everyone has the right to personal space
- **Respect**: Waiting for the right moment shows care
- **Communication**: Clear signals about when interaction is welcome
- **Patience**: Good things come to those who wait

## Technical Details

### Kindle Paperwhite 7th Gen Specifications
- **Display**: 6" E Ink Carta, 758 x 1024 pixels, 300 ppi
- **Browser**: Webkit-based experimental browser
- **Touch**: Capacitive touchscreen

### App Specifications
- **File Type**: Single HTML file with inline CSS and JavaScript
- **Size**: ~35KB (lightweight for quick loading)
- **Compatibility**: Works with older JavaScript (ES5) for browser compatibility
- **Offline**: Fully functional without internet connection
- **Storage**: Uses browser's localStorage for persistent state (if available)

### Optimization for E-ink
- High contrast black and white design
- No animations or transitions
- Large, touch-friendly buttons
- Simple, clean layout
- Serif fonts for better e-ink readability
- Minimal page refreshes

## Customization

To customize the app, open `fortune_cookie_kindle.html` in a text editor and modify:

- **Cooldown period**: Change `touchCooldown = 15000` (value in milliseconds)
- **Prompt timing**: Modify `var delay = 10000 + Math.random() * 20000` (10-30 seconds)
- **Add more fortunes**: Add to `REGULAR_FORTUNES` array
- **Add boundary messages**: Add to `BOUNDARY_FORTUNES` array
- **Warning messages**: Add to `TOO_SOON_MESSAGES` array
- **QR Code URL**: Change the QR code data URL in the HTML
- **Colors**: Modify CSS color values (keep high contrast for e-ink)
- **Font sizes**: Adjust font-size values in CSS

## Comparison with Python Version

This web app is based on the Python e-paper display app but adapted for web browsers:

| Feature | Python App | Web App |
|---------|-----------|---------|
| Platform | Raspberry Pi + e-Paper HAT | Kindle Browser |
| Display | Waveshare 2.13" V2 | Kindle 6" Screen |
| Touch | GT1151 Controller | Browser Touch Events |
| Installation | Python + Libraries | Single HTML File |
| Portability | Hardware-specific | Any web browser |
| Fortunes | 229 messages | 229 messages (same) |
| Cooldown | 15 seconds | 15 seconds |
| QR Code | Generated dynamically | Embedded SVG |

## Troubleshooting

### App doesn't load
- Ensure the file is in the Documents folder
- Try refreshing the browser
- Check the file path is correct

### Touch doesn't work
- Make sure JavaScript is enabled in browser settings
- Try the physical button instead of screen tap
- Restart the Kindle browser

### Display looks wrong
- The app is optimized for portrait mode
- Some formatting may vary on different Kindle models
- Try zooming in/out if needed

### QR Code doesn't scan
- E-ink displays have limited resolution
- Try increasing brightness
- Scan from a closer distance

## Files

- `fortune_cookie_kindle.html` - Main web app (standalone, fully functional)
- `KINDLE_FORTUNE_APP_README.md` - This documentation
- `fortune_app.py` - Original Python version for e-paper displays
- `fortune_messages.py` - Message database used by Python version

## Related Projects

- **Python E-Paper Version**: See `FORTUNE_APP_README.md` for the hardware version
- **Source Code**: Original Python implementation in `fortune_app.py`

## License

Part of the lp_cal project.

## Contributing

To add new fortunes or improve the app:
1. Edit the message arrays in the `<script>` section
2. Test on your Kindle
3. Submit your improvements

## Privacy

This app:
- Runs entirely locally on your device
- Does not collect or transmit any data
- Does not require internet connection after loading
- Does not use cookies or tracking

## Credits

Created as a web adaptation of the Python fortune cookie app for e-paper displays. All messages are in Polish and designed to be humorous while teaching about consent and boundaries.

---

**Enjoy your fortune cookies and remember: consent and boundaries matter! 🥠**
