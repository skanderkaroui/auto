import openai
from keys.authentications import OPENAI_KEY

openai.api_key = OPENAI_KEY

# Function to get response from OpenAI
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a business meeting assistant designed to help businesses make better decisions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    sample_prompt = "Give me your opinion about this."
    response = get_openai_response(sample_prompt)
    print("AI Response:", response)
