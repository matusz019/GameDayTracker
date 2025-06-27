import datetime
import os.path

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from Scraper import get_matches
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def remove_ordinal_suffix(dayStr):
  return re.sub(r'(\d+)(st|nd|rd|th)', r'\1', dayStr)

def create_event(service, match):
  # Clean and parse datetime
  raw_date_time = f"{match['date']} {match['time']}"  # e.g., '2nd Aug 2025 15:00'
  cleaned_date_time = remove_ordinal_suffix(raw_date_time)
  start_dt_naive = datetime.strptime(cleaned_date_time, "%d %b %Y %H:%M")
  
  # Attach timezone info
  start_dt = start_dt_naive.replace(tzinfo=ZoneInfo("Europe/London"))
  end_dt = start_dt + timedelta(minutes=90)
  
  event = {
    "summary": match["summary"],
    "location": match["location"],
    "description": "Match added from Leeds United website",
    "start": {
      "dateTime": start_dt.isoformat(),
      "timeZone": "Europe/London",
    },
    "end": {
      "dateTime": end_dt.isoformat(),
      "timeZone": "Europe/London",
    },
    'reminders':{
      'useDefault': False,
      'overrides':[
        {'method': 'popup', 'minutes' : 1440},
        {'method': 'popup', 'minutes' : 300},
      ]
    }
  }
  
  event = service.events().insert(calendarId="primary", body=event).execute()
  print("Event created:", event.get("htmlLink"))



def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    
    matches= get_matches("https://www.leedsunited.com/en/matches/mens-team/fixtures")
    for match in matches:
      create_event(service, match)
      
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()