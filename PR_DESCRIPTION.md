# Add interactive fortune cookie app with consent boundaries

## Summary

This PR introduces a playful, educational fortune cookie app for the e-paper display that teaches about consent and boundaries through interactive touch-based interactions in Polish.

## Features

- **200+ Funny Polish Fortune Cookies**: Humorous, lighthearted messages
- **Consent & Boundaries Education**: Interactive touch feedback teaching personal space respect
- **Touch Cooldown System**: 15-second cooldown between allowed touches
- **Boundary Messages**: Special messages when touched too soon
- **Interactive Prompts**: "Można dotykać ;-)" appears after 10-30 seconds when ready
- **QR Code Integration**: Every screen displays a QR code linking to https://maciejjankowski.com/qr/
- **Touch Debouncing**: 1-second minimum between processing touch events (prevents avalanche triggering)
- **Landscape Display**: Rotated 90° clockwise for optimal viewing

## Files Added

- `fortune_app.py` - Main application with touch handling and display logic (350+ lines)
- `fortune_messages.py` - 200+ fortune cookies and 30 boundary messages
- `FORTUNE_APP_README.md` - Complete documentation

## Files Modified

- `requirements.txt` - Added `qrcode==8.0` dependency

## Technical Details

- Display rotated 90° clockwise (270° rotation) for landscape orientation
- Images created at 250x122 pixels (swapped dimensions)
- Touch debouncing prevents rapid-fire cascade events
- QR codes generated at 50x50 pixels in bottom-right corner
- Supports both regular fortunes and boundary-respecting educational messages
- Touch controller: GT1151 with debouncing
- E-paper display: Waveshare 2.13" V2

## Educational Purpose

Uses humor and technology to teach:
- **Consent**: Touch requires permission and timing
- **Boundaries**: Everyone has the right to personal space
- **Respect**: Waiting for the right moment shows care
- **Communication**: Clear signals about when interaction is welcome

## Usage

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
python3 fortune_app.py
```

## Commits

1. **Add interactive fortune cookie app with consent boundaries** (2c7b601)
   - Created fortune_app.py with touch handling
   - Created fortune_messages.py with 200+ fortunes
   - Created FORTUNE_APP_README.md documentation

2. **Add QR code to fortune cookie app displays** (468c323)
   - Added QR code generation using qrcode library
   - QR codes appear on all screens (fortune, prompt, warning)
   - Updated requirements.txt with qrcode dependency

3. **Rotate display 90° clockwise and fix touch avalanche triggering** (190e017)
   - Rotated display to landscape orientation
   - Added touch debouncing (1.0s minimum)
   - Fixed rapid-fire touch cascade issue
   - Updated all coordinate calculations

## Test Plan

- [ ] Install dependencies (`pip3 install -r requirements.txt`)
- [ ] Run fortune app (`python3 fortune_app.py`)
- [ ] Verify display appears in landscape orientation (90° clockwise)
- [ ] Test touch interaction - should show new fortune
- [ ] Test touch within 15s - should show boundary message
- [ ] Verify QR code appears in bottom-right corner
- [ ] Verify touch debouncing - rapid touches should be ignored
- [ ] Wait 10-30s after cooldown - should see "Można dotykać ;-)" prompt
- [ ] Scan QR code - should direct to https://maciejjankowski.com/qr/

## Screenshots

The app displays:
- Fortune cookie messages with QR code
- "Nie dotykaj mnie!" warning when touched too soon
- Boundary-respecting educational messages
- "Można dotykać ;-)" invitation when ready

## Notes

This app provides a unique, playful way to teach consent and boundaries using physical computing. The touch-based interaction creates a tangible experience of the importance of timing, permission, and respecting personal space.
