import asyncio
from keys.authentications import get_access_token, TENANT_ID, meeting_link_url, credentials
from keys.authentications import SCOPES as scopes

from msgraph import GraphServiceClient
from msgraph.generated.users.item.online_meetings.online_meetings_request_builder import OnlineMeetingsRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration

async def main():
    access_token = get_access_token()
    graph_client = GraphServiceClient(credentials, scopes)

    query_params = OnlineMeetingsRequestBuilder.OnlineMeetingsRequestBuilderGetQueryParameters(
        filter=f"JoinWebUrl eq '{meeting_link_url}'"
    )

    request_configuration = RequestConfiguration(
        query_parameters=query_params,
    )

    result = await graph_client.me.online_meetings.get(request_configuration=request_configuration)

    if result.status_code == 200:
        print("Successfully joined the meeting.")
    else:
        print(f"Failed to join the meeting. Status code: {result.status_code}, Response: {result.json()}")

if __name__ == "__main__":
    asyncio.run(main())


# # Define the meeting link URL as a variable
# access_token = get_access_token()

# join_meeting_url = "https://graph.microsoft.com/v1.0/communications/calls"

# join_meeting_payload = {
#     "mediaConfig": {
#         "@odata.type": "microsoft.graph.serviceHostedMediaConfig"
#     },
#     "chatInfo": {
#         "@odata.type": "microsoft.graph.chatInfo",
#         "threadId": None  # Optional, if not available you can set it to None or remove it
#     },
#     "meetingInfo": {
#         "@odata.type": "microsoft.graph.organizerMeetingInfo",
#         "joinUrl": meeting_link_url  # Use the meeting link URL variable here
#     },
#     "tenantId": TENANT_ID  # Replace with your tenant ID
# }

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }

# response = requests.post(join_meeting_url, json=join_meeting_payload, headers=headers)

# if response.status_code == 201:
#     print("Successfully joined the meeting.")
# else:
#     print(f"Failed to join the meeting. Status code: {response.status_code}, Response: {response.json()}")
