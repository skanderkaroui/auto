# play_prompt.py
from msgraph import GraphServiceClient
from msgraph.generated.communications.calls.item.play_prompt.play_prompt_post_request_body import PlayPromptPostRequestBody
from msgraph.generated.models.media_prompt import MediaPrompt
from msgraph.generated.models.media_info import MediaInfo
from keys.authentications import get_access_token

# Initialize the GraphServiceClient with your credentials
access_token = get_access_token()
credentials = {
    'access_token': access_token
}
graph_client = GraphServiceClient(credentials, scopes=["https://graph.microsoft.com/.default"])

# Define the media prompt
media_prompt = MediaPrompt(
    odata_type="#microsoft.graph.mediaPrompt",
    media_info=MediaInfo(
        odata_type="#microsoft.graph.mediaInfo",
        uri="https://cdn.contoso.com/beep.wav",
        resource_id="1D6DE2D4-CD51-4309-8DAA-70768651088E"
    )
)

# Create the request body
request_body = PlayPromptPostRequestBody(
    client_context="d45324c1-fcb5-430a-902c-f20af696537c",
    prompts=[media_prompt]
)

# Call the API to play the prompt
call_id = "your-call-id"  # Replace with the actual call ID obtained in join_meeting.py
result = graph_client.communications.calls.by_call_id(call_id).play_prompt.post(request_body)

print(result)  # This will show the response from the API
