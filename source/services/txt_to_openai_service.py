import os

from openai import AzureOpenAI


class OpenAIAPI:
    def __init__(self):
        self.azure_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01"
        )
        self.MODEL_NAME = "azure_open_ai"
        self.MAX_TOKENS = 2000

    def response_generation(self, text: str, first_message=True):
        messages = []

        if first_message:
            prompt = (
                "Act as a business meeting assistant named Auto in a dialogue designed to help businesses make better decisions. "
                "Ensure responses are extremely brief and suitable for a conversational tone keep responses under 50 characters"
            )
            messages.append({"role": "system", "content": prompt})

        messages.append({"role": "user", "content": text})

        response = self.azure_client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=messages
        )

        return response.choices[0].message.content

# def test_openai_api():
#     # Initialize the OpenAIAPI instance
#     openai_api = OpenAIAPI()
#
#     # Define a test input text
#     test_input_text = "How can we improve our quarterly sales performance?"
#
#     try:
#         # Call the response_generation method
#         response = openai_api.response_generation(test_input_text)
#
#         # Print the response
#         print("Response from OpenAI API:")
#         print(response)
#     except Exception as e:
#         print(f"Error: {str(e)}")


if __name__ == "__main__":
    # test_openai_api()
    pass
