import json
import os
from pathlib import Path
import urllib.parse
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
import requests

# Load API key from .env
load_dotenv(Path(__file__).with_name(".env"))

# Initialize OpenAI client
client = OpenAI()


# -------------------------------------------------------------
# 1. Define the Pydantic Schema for Structured Output
# -------------------------------------------------------------
class WeatherReport(BaseModel):
    city: str = Field(description="The name of the city")
    temperature_c: float = Field(description="Current temperature in Celsius as a number, e.g. 24.5")
    temperature_f: float = Field(description="Current temperature in Fahrenheit as a number, e.g. 76.1")
    condition: str = Field(description="Current weather condition (e.g. Clear, Sunny, Rainy, Smoky Haze)")
    humidity: str = Field(description="Humidity percentage (e.g. '60%')")
    wind_speed: str = Field(description="Wind speed (e.g. '5 km/h')")
    clothing_advice: list[str] = Field(description="List of specific clothing or accessory recommendations")
    carry_umbrella: bool = Field(description="True if rain or snow is likely, False otherwise")
    travel_tip: str = Field(description="Practical tip for outdoor activities or commuting today")


# -------------------------------------------------------------
# 2. Define the Weather Tool
# -------------------------------------------------------------
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

SYSTEM_RULES = """
You are WeatherAI, an intelligent and friendly Weather & Travel Advisor.

### OPERATIONAL RULES:
1. SCOPE: You only answer questions related to weather, climate, travel conditions, and packing/clothing advice. If the user asks about unrelated topics (e.g. general coding, recipes, trivia, politics), politely decline and remind them to ask about weather.
2. LIVE ACCURACY: Always use the `get_weather` tool when asked about current weather in any city. NEVER guess, assume, or fabricate live temperature numbers.
3. STRUCTURED DATA: When returning weather details, you MUST strictly adhere to the WeatherReport schema with accurate numbers and booleans.
4. ERROR HANDLING: If the `get_weather` tool returns an error or fails to find a location, clearly state that live data is currently unavailable for that place.
"""

print("=" * 55)
print("     Weather AI Assistant (with Pydantic & Tools)   ")
print("=" * 55)
print("Ask any weather question directly!")
print("Example: 'What is the weather in Agra?'")
print("Type 'exit' to stop.\n")

# [Chat Memory: keep messages outside the loop]
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
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "get_weather":
                    args = json.loads(tool_call.function.arguments)
                    city_arg = args.get("city", "")
                    print(f"[Tool Calling] Fetching live weather for: {city_arg}...")

                    weather_data = get_weather(city_arg)
                    print(f"[Tool Result] {weather_data}")

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(weather_data),
                        }
                    )

            # Step 3: Parse response with Pydantic!
            print("\nParsing response with Pydantic...")
            parse_response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=messages,
                response_format=WeatherReport,  # <-- Enforces WeatherReport Pydantic schema!
            )

            # Get the validated Pydantic object
            report: WeatherReport = parse_response.choices[0].message.parsed

            # Display structured Pydantic data
            print("\n" + "=" * 55)
            print(f"📍 City         : {report.city}")
            print(f"🌡️  Temperature  : {report.temperature_c}°C / {report.temperature_f}°F")
            print(f"☁️  Condition    : {report.condition}")
            print(f"💧 Humidity     : {report.humidity} | 💨 Wind: {report.wind_speed}")
            print(f"☔ Carry Umbrella: {'YES (Rain/Snow likely)' if report.carry_umbrella else 'NO'}")
            print("👕 What to Wear :")
            for item in report.clothing_advice:
                print(f"   • {item}")
            print(f"💡 Travel Tip   : {report.travel_tip}")
            print("=" * 55)

            # Save the JSON representation in conversation history for memory
            messages.append({"role": "assistant", "content": report.model_dump_json()})

        else:
            # If no tools were called (e.g. conversational question or off-topic decline)
            print(f"\nAI: {response_message.content}")
            messages.append(response_message)

        print("-" * 55 + "\n")

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"\nError: {e}\n")
