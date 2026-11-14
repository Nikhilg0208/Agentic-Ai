import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI


load_dotenv(Path(__file__).with_name(".env"))

client = OpenAI()

entry_time = datetime.now()
start_perf = time.perf_counter()

print(f"Entry Timestamp: {entry_time.strftime('%H:%M:%S.%f')[:-3]}")
print("Sending request to OpenAI (gpt-4o-mini)...")

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Hey There"}
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
    print(f"\nOpenAI API Error: {e.message} (Status: {e.status_code})")
except Exception as e:
    exit_time = datetime.now()
    elapsed = time.perf_counter() - start_perf
    print(f"Exit Timestamp : {exit_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Time Taken     : {elapsed:.2f} seconds")
    print(f"\nAn unexpected error occurred: {e}")
