# join_meeting.py
import requests
from keys.authentications import get_access_token

access_token = get_access_token()

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

join_meeting_url = "https://graph.microsoft.com/v1.0/communications/calls"
join_meeting_payload = {
    # Your payload to join the meeting, which includes the meeting URL and other details
}

response = requests.post(join_meeting_url, headers=headers, json=join_meeting_payload)
if response.status_code == 201:
    call_id = response.json()["id"]
    print(f"Call ID: {call_id}")
else:
    print(f"Error: {response.status_code}, {response.json()}")
