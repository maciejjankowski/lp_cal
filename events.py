from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


import json

def get_todays_calendar_events(credentials_file='token.json'):
    """Fetches today's events from the Google Calendar API.

    Args:
        credentials_file: Path to the file containing your OAuth2 credentials.

    Returns:
        A list of dictionaries, each containing:
            - startTime: Start time of the event (datetime object).
            - endTime: End time of the event (datetime object).
            - colorId: ID of the event's color.
    """

    # Load credentials from file (assumes you've already authorized)
    creds = Credentials.from_authorized_user_file(credentials_file)

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Define the start and end times for today
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day, now.hour).isoformat() + 'Z'
    today_end = (datetime(now.year, now.month, now.day) + timedelta(days=1)).isoformat() + 'Z'

    # Fetch events for today
    events_result = service.events().list(calendarId='primary', timeMin=today_start,
                                        timeMax=today_end, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Extract relevant data and return as a list of dictionaries
    today_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        start_hour = int(start.split('T')[1].split(':')[0])
        end_hour = int(end.split('T')[1].split(':')[0])
        
        for hour in range(end_hour - start_hour + 1):
            event_data = {
                'summary': event.get('summary', None),
                'start_hour': start_hour + hour,
                'end_hour': end_hour,
                'start': start,
                'end': end,
                'color_id': event.get('colorId', None)
                # 'color': to_lp_color(event.get('colorId', None))  # Handle events without color
            }
            # print(event_data)
            today_events.append(event_data)

    return today_events


# For testing and to display the returned event data in an organized format:
if __name__ == '__main__':
    # with open("credentials.json", "r") as file:
    #     credentials_json_data = json.load(file)
    todays_events = get_todays_calendar_events() # credentials_json_data
    if not todays_events:
        print("No events found for today.")
    else:
        for event in todays_events:
            print(event)
