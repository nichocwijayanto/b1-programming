import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
# ----------------------------------------------
# EUROPEAN CAPITALS (Coordinates)
# ----------------------------------------------
EU_CAPITALS = [
    {"city": "Vienna", "country": "Austria", "lat": 48.2082, "lon": 16.3738},
    {"city": "Brussels", "country": "Belgium", "lat": 50.8503, "lon": 4.3517},
    {"city": "Sofia", "country": "Bulgaria", "lat": 42.6977, "lon": 23.3219},
    {"city": "Zagreb", "country": "Croatia", "lat": 45.8150, "lon": 15.9819},
    {"city": "Nicosia", "country": "Cyprus", "lat": 35.1856, "lon": 33.3823},
    {"city": "Prague", "country": "Czechia", "lat": 50.0755, "lon": 14.4378},
    {"city": "Copenhagen", "country": "Denmark", "lat": 55.6761, "lon": 12.5683},
    {"city": "Tallinn", "country": "Estonia", "lat": 59.4370, "lon": 24.7536},
    {"city": "Helsinki", "country": "Finland", "lat": 60.1695, "lon": 24.9354},
    {"city": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"city": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050},
    {"city": "Athens", "country": "Greece", "lat": 37.9838, "lon": 23.7275},
    {"city": "Budapest", "country": "Hungary", "lat": 47.4979, "lon": 19.0402},
    {"city": "Dublin", "country": "Ireland", "lat": 53.3498, "lon": -6.2603},
    {"city": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964},
    {"city": "Riga", "country": "Latvia", "lat": 56.9496, "lon": 24.1052},
    {"city": "Vilnius", "country": "Lithuania", "lat": 54.6872, "lon": 25.2797},
    {"city": "Luxembourg", "country": "Luxembourg", "lat": 49.6116, "lon": 6.1319},
    {"city": "Valletta", "country": "Malta", "lat": 35.8989, "lon": 14.5146},
    {"city": "Amsterdam", "country": "Netherlands", "lat": 52.3676, "lon": 4.9041},
    {"city": "Warsaw", "country": "Poland", "lat": 52.2297, "lon": 21.0122},
    {"city": "Lisbon", "country": "Portugal", "lat": 38.7223, "lon": -9.1393},
    {"city": "Bucharest", "country": "Romania", "lat": 44.4268, "lon": 26.1025},
    {"city": "Bratislava", "country": "Slovakia", "lat": 48.1486, "lon": 17.1077},
    {"city": "Ljubljana", "country": "Slovenia", "lat": 46.0569, "lon": 14.5058},
    {"city": "Madrid", "country": "Spain", "lat": 40.4168, "lon": -3.7038},
    {"city": "Stockholm", "country": "Sweden", "lat": 59.3293, "lon": 18.0686}
]
# ----------------------------------------------
# WEATHER CODE MAPPING
# ----------------------------------------------
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle (light)",
    53: "Drizzle (moderate)",
    55: "Drizzle (dense)",
    56: "Freezing Drizzle (light)",
    57: "Freezing Drizzle (dense)",
    61: "Rain (slight)",
    63: "Rain (moderate)",
    65: "Rain (heavy)",
    66: "Freezing Rain (light)",
    67: "Freezing Rain (heavy)",
    71: "Snow fall (slight)",
    73: "Snow fall (moderate)",
    75: "Snow fall (heavy)",
    77: "Snow grains",
    80: "Rain showers (slight)",
    81: "Rain showers (moderate)",
    82: "Rain showers (violent)",
    85: "Snow showers (slight)",
    86: "Snow showers (heavy)",
    95: "Thunderstorm",
    96: "Thunderstorm (slight hail)",
    97: "Thunderstorm (heavy hail)"
}
# ----------------------------------------------
# FETCH WEATHER DATA
# ----------------------------------------------
def fetch_weather_data(lat: float, lon: float) -> Optional[Dict]:
#Fetch weather data from Open-Meteo.
    url = "https://api.open-meteo.com/v1/forecast"
    today = datetime.now().strftime("%Y-%m-%d")
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,precipitation_probability,weathercode",
        "temperature_unit": "celsius",
        "windspeed_unit": "kmh",
        "timezone": "auto",
        "start_date": today,
        "end_date": today
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Timeout: ({lat}, {lon})")
    except requests.exceptions.RequestException as e:
        print(f"Request error for ({lat}, {lon}): {e}")
    except json.JSONDecodeError:
        print("JSON parsing failed.")
    return None
# ----------------------------------------------
# PROCESS WEATHER DATA
# ----------------------------------------------

def process_weather_data(data: Dict, city: str, country: str) -> Optional[Dict]:
#"""Convert raw weather API result into structured data."""
    try:
        cw = data.get("current_weather", {})

        current_weather = {
        "temperature": cw.get("temperature"),
        "windspeed": cw.get("windspeed"),
        "weathercode": cw.get("weathercode"),
        "condition": WEATHER_CODES.get(cw.get("weathercode")),
        "time": cw.get("time"),
        }

        hourly = data.get("hourly", {})

        forecast = []

        if all(k in hourly for k in ("time", "temperature_2m", "precipitation_probability", "weathercode")):
            for i in range(len(hourly["time"])):
                forecast.append({
                    "time": hourly["time"][i],
                    "temperature": hourly["temperature_2m"][i],
                    "precipitation_probability": hourly["precipitation_probability"][i],
                    "weathercode": hourly["weathercode"][i],
                    "condition": WEATHER_CODES.get(hourly["weathercode"][i]),
                })
        return {
            "city": city,
            "country": country,
            "coordinates": {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            },
            "current_weather": current_weather,
            "hourly_forecast": forecast,
        }
    except Exception as e:
        print(f"Processing error for {city}, {country}: {e}")
    return None

# ----------------------------------------------
# COLLECT WEATHER DATA FOR ALL CAPITALS
# ----------------------------------------------
def collect_eu_weather_data(delay_seconds: int = 1) -> Dict:
    weather_data = {}
    print("\n--- Collecting Weather for EU Capitals ---")

    for i, cap in enumerate(EU_CAPITALS):
        city = cap["city"]
        country = cap["country"]
        print(f"> Fetching: {city} ({i+1}/{len(EU_CAPITALS)})")
        raw = fetch_weather_data(cap["lat"], cap["lon"])

    if raw:
        processed = process_weather_data(raw, city, country)
        if processed:
            weather_data[city] = processed
            print(f" 7 Success: {city}")
        else:
            print(f" Processing failed: {city}")
    else:
        print(f" Request failed: {city}")
        
    if i < len(EU_CAPITALS) - 1:
        time.sleep(delay_seconds)
    return weather_data
# ----------------------------------------------
# SAVE TO JSON
# ----------------------------------------------
def save_to_json(data: Dict, filename: str) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\nSaved {len(data)} records ³ {filename}")
    except IOError as e:
        print(f"File write error: {e}")

# ----------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------
def main():
    print("#############################################")
    print("# EUROPEAN CAPITAL WEATHER REPORT TOOL #")
    print("#############################################\n")
    all_data = collect_eu_weather_data()
    output_file = "eu_weather_report.json"
    save_to_json(all_data, output_file)
    if not all_data:
        print("\nNo data collected.")
        return
    
    temps = [
        d["current_weather"]["temperature"]
        for d in all_data.values()
        if d["current_weather"]["temperature"] is not None
    ]
    
    if temps:
        avg = sum(temps) / len(temps)
        hottest = max(all_data.values(), key=lambda x: x["current_weather"]["temperature"])
        coldest = min(all_data.values(), key=lambda x: x["current_weather"]["temperature"])
        print("\n--- Summary ---")
        print(f"Average temperature: {avg:.2f}°C")
        print(f"Hottest: {hottest['city']} ({hottest['current_weather']['temperature']}°C)")
        print(f"Coldest: {coldest['city']} ({coldest['current_weather']['temperature']}°C)")
    else:
        print("No temperature data available.")
    if __name__ == "__main__":
        main()