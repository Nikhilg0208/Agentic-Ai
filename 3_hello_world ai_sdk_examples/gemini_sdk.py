from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv(Path(__file__).with_name(".env"))

client = genai.Client()

response = client.interactions.create(
    model="gemini-3.6-flash",
    input="Hey There",
)

print(response.output_text)
