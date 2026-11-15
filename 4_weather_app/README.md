# 4. Weather App CLI with AI

A terminal-based AI assistant that answers questions about live weather for any city.

---

## Setup Steps

### 1. Create and Activate Virtual Environment
```cmd
cd 4_weather_app
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 3. Configure API Keys
Copy `.env.example` to `.env`:
```cmd
copy .env.example .env
```
Open `.env` and fill in your keys.

---

## Free Weather API Options

Here are two popular, free weather APIs you can use:

1. **[WeatherAPI.com](https://www.weatherapi.com/)** (Free, easy setup)
   - Endpoint: `http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=CITY_NAME`
2. **[OpenWeatherMap](https://openweathermap.org/)** (Free tier available)
   - Endpoint: `https://api.openweathermap.org/data/2.5/weather?q=CITY_NAME&appid=YOUR_KEY&units=metric`
3. **[Open-Meteo](https://open-meteo.com/)** (Free, **NO API KEY needed!**)
   - Great if you want to test immediately without signing up for a key.

---

## Write Your Code
Open `main.py` and implement the TODO sections!
