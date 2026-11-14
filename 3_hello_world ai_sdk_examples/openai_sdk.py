from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI


load_dotenv(Path(__file__).with_name(".env"))

client = OpenAI()

print("Sending request to OpenAI (gpt-4o-mini)...")

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Hey There"}
        ],
    )
    print("\nResult:")
    print(response.choices[0].message.content)
except APIError as e:
    print(f"\nOpenAI API Error: {e.message} (Status: {e.status_code})")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
