from openai import OpenAI

client = OpenAI()


response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a business meeting assistant designed to help businesses make better decisions."},
  ],
  prompt= "Give me your opinion about this."
)

