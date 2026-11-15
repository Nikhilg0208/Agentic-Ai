import json
import os
from pathlib import Path
import urllib.parse
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv(Path(__file__).with_name(".env"))

# Initialize OpenAI client
client = OpenAI()


def get_weather(city: str) -> dict:
    """
    Fetch current weather data for a city using a free weather API.
    Uses urllib.parse.quote to safely handle cities with spaces (e.g. 'New York').
    """
    try:
        encoded_city = urllib.parse.quote(city.strip())
        url = f"https://wttr.in/{encoded_city}?format=j1"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        return {
            "city": city.title(),
            "temperature": f"{current['temp_C']}°C",
            "condition": current["weatherDesc"][0]["value"],
            "humidity": f"{current['humidity']}%",
            "wind_speed": f"{current['windspeedKmph']} km/h",
        }
    except Exception as e:
        return {"error": f"Could not fetch weather for '{city}': {e}"}


# Define the Tool schema so the LLM knows how to call get_weather
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get real-time current weather information for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city, e.g. Agra, New York, Tokyo, London.",
                    }
                },
                "required": ["city"],
            },
        },
    }
]

print("=" * 50)
print("     Weather AI Assistant (with Live Tools)   ")
print("=" * 50)
print("Ask any weather question directly! (Follow-up questions supported)")
print("Examples:")
print("  - 'What is the weather in New York?'")
print("  - 'Compare weather in Agra and London'")
print("  - 'What should I wear there?'")
print("Type 'exit' to stop.\n")

SYSTEM_RULES = """
You are WeatherAI, an intelligent and friendly Weather & Travel Advisor.

### OPERATIONAL RULES:
1. SCOPE: You only answer questions related to weather, climate, travel conditions, and packing/clothing advice. If the user asks about unrelated topics (e.g. general coding, recipes, trivia, politics), politely decline and remind them to ask about weather.
2. LIVE ACCURACY: Always use the `get_weather` tool when asked about current weather in any city. NEVER guess, assume, or fabricate live temperature numbers.
3. DUAL UNITS: Always report temperatures in both Celsius and Fahrenheit (e.g., 22°C / 72°F).
4. ERROR HANDLING: If the `get_weather` tool returns an error or fails to find a location, clearly state that live data is currently unavailable for that place and offer typical seasonal climate information instead.
5. CONCISE & STRUCTURED: When reporting weather, provide a crisp response with:
   - 🌡️ **Current Conditions**: Temperature, sky condition, humidity, and wind.
   - 👕 **What to Wear**: Practical clothing or accessory recommendations (e.g., umbrella, sunglasses, jacket).
   - 💡 **Activity/Travel Tip**: A quick practical tip for outdoor plans.
"""

# [Improvement 1: Chat Memory]
# Keep the conversation history list outside the loop so context is remembered!
messages = [
    {
        "role": "system",
        "content": SYSTEM_RULES,
    }
]

while True:
    try:
        user_prompt = input("You: ").strip()

        if not user_prompt:
            continue

        if user_prompt.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        # Append the new user question to the ongoing history
        messages.append({"role": "user", "content": user_prompt})

        print("\nThinking...")

        # Step 1: Send query with tools to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )

        response_message = response.choices[0].message

        # Step 2: Check if AI decided to call any tools
        if response_message.tool_calls:
            # [Improvement 2: Multiple Tool Calls Fix]
            # Append the assistant's tool-call request ONCE before the loop
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "get_weather":
                    args = json.loads(tool_call.function.arguments)
                    city_arg = args.get("city", "")
                    print(f"[Tool Calling] Fetching live weather for: {city_arg}...")

                    # [Improvement 3: Handled spaces in city names]
                    weather_data = get_weather(city_arg)
                    print(f"[Tool Result] {weather_data}")

                    # Provide tool result back to the conversation
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(weather_data),
                        }
                    )

            # [Improvement 4: Streaming Output]
            # Stream the final answer word-by-word like ChatGPT!
            print("\nAI: ", end="", flush=True)
            stream_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
            )

            full_reply = ""
            for chunk in stream_response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                full_reply += content
            print()

            # Save the assistant's final response into conversation memory
            messages.append({"role": "assistant", "content": full_reply})

        else:
            # If no tools were called, print directly and store in memory
            print(f"\nAI: {response_message.content}")
            messages.append(response_message)

        print("-" * 50 + "\n")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"\nError: {e}\n")
