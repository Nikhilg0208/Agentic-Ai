import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError


load_dotenv(Path(__file__).with_name(".env"))

client = genai.Client()

entry_time = datetime.now()
start_perf = time.perf_counter()

print(f"Entry Timestamp: {entry_time.strftime('%H:%M:%S.%f')[:-3]}")
print("Sending request to Gemini (gemini-3.6-flash)...")

try:
    response = client.interactions.create(
        model="gemini-3.6-flash",
        input="Hey There",
    )
    exit_time = datetime.now()
    elapsed = time.perf_counter() - start_perf

    print(f"Exit Timestamp : {exit_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Time Taken     : {elapsed:.2f} seconds")
    print("\nResult:")
    print(response.output_text)
except APIError as e:
    exit_time = datetime.now()
    elapsed = time.perf_counter() - start_perf
    print(f"Exit Timestamp : {exit_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Time Taken     : {elapsed:.2f} seconds")
    print(f"\nGemini API Error: {e}")
except Exception as e:
    exit_time = datetime.now()
    elapsed = time.perf_counter() - start_perf
    print(f"Exit Timestamp : {exit_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Time Taken     : {elapsed:.2f} seconds")
    print(f"\nAn unexpected error occurred: {e}")
