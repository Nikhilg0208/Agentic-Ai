import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI


load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

entry_time = datetime.now()
start_perf = time.perf_counter()

print(f"Entry Timestamp: {entry_time.strftime('%H:%M:%S.%f')[:-3]}")
print("Sending request to Gemini via OpenAI SDK (gemini-3.8-flash)...")

try:
    response = client.chat.completions.create(
        model="gemini-3.8-flash",
        messages=[
            {"role": "user", "content": "Hey there"}
        ],
    )
    exit_time = datetime.now()
    elapsed = time.perf_counter() - start_perf

    print(f"Exit Timestamp : {exit_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Time Taken     : {elapsed:.2f} seconds")
    print("\nResult:")
    print(response.choices[0].message.content)
except APIError as e:
    exit_time = datetime.now()
    elapsed = time.perf_counter() - start_perf
    print(f"Exit Timestamp : {exit_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Time Taken     : {elapsed:.2f} seconds")
    print(f"\nAPI Error: {e.message} (Status: {e.status_code})")
except Exception as e:
    exit_time = datetime.now()
    elapsed = time.perf_counter() - start_perf
    print(f"Exit Timestamp : {exit_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Time Taken     : {elapsed:.2f} seconds")
    print(f"\nAn unexpected error occurred: {e}")
