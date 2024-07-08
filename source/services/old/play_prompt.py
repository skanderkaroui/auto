# play_prompt.py
from msgraph import GraphServiceClient
from msgraph.generated.communications.calls.item.play_prompt.play_prompt_post_request_body import PlayPromptPostRequestBody
from msgraph.generated.models.media_prompt import MediaPrompt
from msgraph.generated.models.media_info import MediaInfo
from keys.authentications import get_access_token
from source.azure_integration.join_meeting import call_id

# Initialize the GraphServiceClient with your credentials
access_token = get_access_token()
credentials = {
    'access_token': access_token
}
graph_client = GraphServiceClient(credentials, scopes=["https://graph.microsoft.com/.default"])

# Create the request body
request_body = PlayPromptPostRequestBody(
    client_context="d45324c1-fcb5-430a-902c-f20af696537c",
    prompts= MediaPrompt(
    odata_type="#microsoft.graph.mediaPrompt",
    media_info=MediaInfo(
        odata_type="#microsoft.graph.mediaInfo",
        uri="https://cdn.contoso.com/beep.wav",
        resource_id="1D6DE2D4-CD51-4309-8DAA-70768651088E"
    ),
),
)

# Call the API to play the prompt
result = graph_client.communications.calls.by_call_id(call_id).play_prompt.post(request_body)

print(result)  # This will show the response from the API
