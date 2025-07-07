from googleapiclient.discovery import build
from google.oauth2 import service_account
from dateutil import parser
from datetime import datetime
import pytz


SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "service_account.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
calendar_service = build("calendar", "v3", credentials=credentials)

CALENDAR_ID = "53d6de6148ad1dab08516998768b304daa4ed8154450e6f31f0f46efa9e1d212@group.calendar.google.com"  

user_states = {}

def create_event(summary, start_time, end_time):
    """Create Google Calendar event and return link."""
    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
        "description": f"Auto-created event: {summary}",
    }
    created_event = calendar_service.events().insert(
        calendarId=CALENDAR_ID, body=event).execute()
    return created_event.get("htmlLink", "No link available")

def get_next_question(user_id, user_message):
    """
    Handles conversation flow and stores responses.
    """
    if user_id not in user_states:
    
        user_states[user_id] = {"step": 0, "data": {}}
        return "📅 What is the title of the event?"

    state = user_states[user_id]

    if state["step"] == 0:
        state["data"]["title"] = user_message
        state["step"] += 1
        return "📆 What date is the event? (e.g., 2025-07-19 or July 19)"

    elif state["step"] == 1:
        try:
            
            date_obj = parser.parse(user_message, fuzzy=True)
            state["data"]["date"] = date_obj.strftime("%Y-%m-%d")
            state["step"] += 1
            return " What time does it start? (e.g., 11:30 am or 15:30)"
        except Exception:
            return " Invalid date. Try again (e.g., 2025-07-19 or July 19)."

    elif state["step"] == 2:
        try:
        
            date_time_str = f"{state['data']['date']} {user_message}"
            start_dt = parser.parse(date_time_str, fuzzy=True)
            state["data"]["start_time"] = start_dt.isoformat()
            state["step"] += 1
            return " What time does it end? (e.g., 12:30 pm or 16:30)"
        except Exception:
            return "Invalid time. Try again (e.g., 11:30 am or 15:30)."

    elif state["step"] == 3:
        try:
            
            date_time_str = f"{state['data']['date']} {user_message}"
            end_dt = parser.parse(date_time_str, fuzzy=True)
            state["data"]["end_time"] = end_dt.isoformat()

        
            link = create_event(
                state['data']['title'],
                state['data']['start_time'],
                state['data']['end_time']
            )

            user_states.pop(user_id) 
            return f"✅ Event created! [View on Calendar]({link})"
        except Exception:
            return " Invalid end time. Try again (e.g., 12:30 pm or 16:30)."

    else:
        user_states.pop(user_id)
        return " Something went wrong. Start over."
