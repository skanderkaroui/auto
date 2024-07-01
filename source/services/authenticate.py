import requests
import msal


# Authentication
authority = f"https://login.microsoftonline.com/{tenant_id}"
app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret,
)

scopes = ["https://graph.microsoft.com/.default"]
result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    # Joining the meeting
    join_meeting_url = f"https://graph.microsoft.com/v1.0/me/onlineMeetings/joinMeeting?meetingUrl={meeting_url}"
    headers = {
        "Authorization": f"Bearer {result['access_token']}",
        "Content-Type": "application/json"
    }
    response = requests.post(join_meeting_url, headers=headers)

    if response.status_code == 200:
        print("Successfully joined the meeting")
    else:
        print(f"Failed to join the meeting: {response.status_code} - {response.text}")
else:
    print("Authentication failed")
