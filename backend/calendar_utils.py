from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime


SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "service_account.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
calendar_service = build("calendar", "v3", credentials=credentials)


CALENDAR_ID = "53d6de6148ad1dab08516998768b304daa4ed8154450e6f31f0f46efa9e1d212@group.calendar.google.com"


def create_event(summary, start_time, end_time):
    """
    Create a Google Calendar event and return the link.
    """
    event = {
        "summary": summary,  
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "description": f"Auto-created event: {summary}",
    }

    try:
        created_event = calendar_service.events().insert(
            calendarId=CALENDAR_ID,
            body=event
        ).execute()

        print(f"✅ Event created: {created_event.get('htmlLink')}")
        return created_event.get('htmlLink', 'No link available')
    except Exception as e:
        print(f"⚠️ Error creating event: {e}")
        return None
