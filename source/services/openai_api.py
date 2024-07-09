import os

from openai import AzureOpenAI


class OpenAIAPI:
    def __init__(self):
        self.azure_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01"
        )
        self.MODEL_NAME = "gpt-3.5-turbo"
        self.MAX_TOKENS = 2000

    def text_proofreading(self, text: str):
        chat_client = self.azure_client.get_chat_client("my-gpt-35-turbo-deployment")
        response = chat_client.create_completion(
            model=self.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Act as a business meeting assistant designed to help businesses make better decisions.",
                },
                {"role": "user", "content": text},
            ]
        )
        return response.choices[0]["message"]["content"].strip()
