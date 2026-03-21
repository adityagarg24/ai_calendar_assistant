"""
Google Calendar API client for fetching daily meetings
"""

import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE, TIMEZONE


class CalendarClient:
    def __init__(self):
        self.service = None
        self.timezone = pytz.timezone(TIMEZONE)
    
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Check if token.json exists (saved credentials)
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(CREDENTIALS_FILE):
                    print(f"❌ Error: {CREDENTIALS_FILE} not found!")
                    print("Please download your Google Calendar API credentials and save as 'credentials.json'")
                    print("Instructions: https://developers.google.com/calendar/api/quickstart/python")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            print("✅ Successfully connected to Google Calendar!")
            return True
        except HttpError as error:
            print(f"❌ An error occurred: {error}")
            return False
    
    def get_todays_events(self):
        """Fetch today's calendar events"""
        if not self.service:
            print("❌ Not authenticated. Please run authenticate() first.")
            return []
        
        try:
            # Get today's date range
            now = datetime.now(self.timezone)
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Convert to UTC for API call
            start_time = start_of_day.astimezone(pytz.UTC).isoformat()
            end_time = end_of_day.astimezone(pytz.UTC).isoformat()
            
            print(f"📅 Fetching events for {now.strftime('%B %d, %Y')}...")
            
            # Call the Calendar API
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                print("📭 No events found for today.")
                return []
            
            print(f"📋 Found {len(events)} events for today.")
            return self._process_events(events)
            
        except HttpError as error:
            print(f"❌ An error occurred while fetching events: {error}")
            return []
    
    def _process_events(self, events):
        """Process raw events into a cleaner format"""
        processed_events = []
        
        for event in events:
            # Skip all-day events without specific times
            if 'dateTime' not in event.get('start', {}):
                continue
            
            # Extract event details
            event_data = {
                'id': event.get('id', ''),
                'summary': event.get('summary', 'No Title'),
                'description': event.get('description', ''),
                'start_time': self._parse_datetime(event['start'].get('dateTime')),
                'end_time': self._parse_datetime(event['end'].get('dateTime')),
                'location': event.get('location', ''),
                'attendees': len(event.get('attendees', [])),
                'recurring': 'recurringEventId' in event,
                'created': self._parse_datetime(event.get('created')),
                'updated': self._parse_datetime(event.get('updated'))
            }
            
            processed_events.append(event_data)
        
        return processed_events
    
    def _parse_datetime(self, datetime_str):
        """Parse datetime string to local timezone"""
        if not datetime_str:
            return None
        
        try:
            # Parse the datetime string
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            # Convert to local timezone
            return dt.astimezone(self.timezone)
        except Exception as e:
            print(f"Warning: Could not parse datetime {datetime_str}: {e}")
            return None


def test_calendar_connection():
    """Test function to verify calendar connection works"""
    print("🧪 Testing Google Calendar connection...")
    
    client = CalendarClient()
    
    if client.authenticate():
        events = client.get_todays_events()
        
        if events:
            print(f"\n📋 Sample event:")
            event = events[0]
            print(f"  Title: {event['summary']}")
            print(f"  Time: {event['start_time'].strftime('%I:%M %p')} - {event['end_time'].strftime('%I:%M %p')}")
            print(f"  Recurring: {'Yes' if event['recurring'] else 'No'}")
            print(f"  Has Description: {'Yes' if event['description'] else 'No'}")
        
        return True
    else:
        return False


if __name__ == "__main__":
    test_calendar_connection()