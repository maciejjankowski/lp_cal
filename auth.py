import os.path
import time
import requests
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from epaper_display import EpaperDisplay

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_credentials(display=None):
    """
    Get valid Google Calendar credentials.
    If credentials are invalid/expired, display auth code on e-paper and authenticate.
    
    Args:
        display: Optional EpaperDisplay instance to show auth code
    
    Returns:
        Credentials object
    """
    creds = None
    token_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lp_cal', 'token.json')
    # Check if token.json exists
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            print(f"Error loading token.json: {e}")
            creds = None
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired token...")
                creds.refresh(Request())
            else:
                print("Starting device authentication flow...")
                
                # Load client secrets
                with open("credentials.json", "r") as f:
                    client_config = json.load(f)
                
                client_id = client_config["installed"]["client_id"]
                client_secret = client_config["installed"]["client_secret"]
                
                # Request device code
                device_code_response = requests.post("https://oauth2.googleapis.com/device/code", data={
                    "client_id": client_id,
                    "scope": " ".join(SCOPES)
                })
                device_code_data = device_code_response.json()
                
                verification_url = device_code_data['verification_url']
                user_code = device_code_data['user_code']
                
                print(f"Please go to {verification_url} and enter code: {user_code}")
                
                # Display on e-paper if display provided
                if display:
                    display.display_auth_code(verification_url, user_code)
                
                # Poll for token
                while True:
                    token_response = requests.post("https://oauth2.googleapis.com/token", data={
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "device_code": device_code_data["device_code"],
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                    })
                    token_data = token_response.json()
                    
                    if "access_token" in token_data:
                        creds = Credentials(
                            token=token_data["access_token"],
                            refresh_token=token_data.get("refresh_token"),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=client_id,
                            client_secret=client_secret,
                            scopes=SCOPES
                        )
                        print("Authentication successful!")
                        break
                    elif token_data.get("error") == "authorization_pending":
                        time.sleep(device_code_data["interval"])
                    else:
                        raise Exception(f"Authorization failed: {token_data}")
            
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            
        except Exception as e:
            print(f"Authentication error: {e}")
            raise
    
    return creds


def main():
    """Standalone authentication script."""
    display = None
    
    try:
        display = EpaperDisplay()
        creds = get_credentials(display)
        print("Authentication completed successfully!")
        
    except KeyboardInterrupt:
        print("\nAuthentication cancelled by user")
    except Exception as e:
        print(f"Error during authentication: {e}")
        raise
    finally:
        if display:
            display.sleep()
            display.cleanup()


if __name__ == "__main__":
    main()