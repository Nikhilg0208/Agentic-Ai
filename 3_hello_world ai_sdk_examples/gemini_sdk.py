from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError


load_dotenv(Path(__file__).with_name(".env"))

client = genai.Client()

print("Sending request to Gemini (gemini-3.6-flash)...")

try:
    response = client.interactions.create(
        model="gemini-3.6-flash",
        input="Hey There",
    )
    print("\nResult:")
    print(response.output_text)
except APIError as e:
    print(f"\nGemini API Error: {e}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
