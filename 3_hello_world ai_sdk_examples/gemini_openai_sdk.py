import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI


load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

print("Sending request to Gemini via OpenAI SDK (gemini-3.8-flash)...")

try:
    response = client.chat.completions.create(
        model="gemini-3.8-flash",
        messages=[
            {"role": "user", "content": "Hey there"}
        ],
    )
    print("\nResult:")
    print(response.choices[0].message.content)
except APIError as e:
    print(f"\nAPI Error: {e.message} (Status: {e.status_code})")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
