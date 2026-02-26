import requests # to fetch data from the web (like browsing)
import json     # to save data to a file
import time     # to add a delay (specified time) = "API Rate Limiting"
                # Servers don't like being spammed. Delay is necessary between each request, so it doesn't block your IP.

final_weather_data = {}

eu_capitals = [
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

weather_codes = {
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

for place in eu_capitals:
    city_name = place['city']
    lat = place['lat']
    lon = place['lon']

    url = f"https://api.open-meteo.com/v1/forecast"
    query_params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "temperature_2m,precipitation_probability,weathercode",
        "timezone": "UTC" 
    }
    print(f"\nFetching weather for {city_name}...")

    try:
        # sends a request to the server
        response = requests.get(url, params=query_params, timeout=10)
        #checks if the request was successful. if not, this line will "raise" an error (jump to except block).
        response.raise_for_status() 

        # convert the raw data into a Python dictionary
        data = response.json()

        if "error" in data:
            print(f"API Error for {city_name}: {data.get('reason')}")
            continue

        # dictionary of dictionaries, based on city names. 
        #final_weather_data[city_name] = data

        # "current weather" is also a dictionary from the json data.
        current = data["current_weather"]
        # "hourly" is also a dictionary from the json data.
        hourly = data["hourly"]

        # Build the structured entry for cities.
        final_weather_data[city_name] = {
            "country": place["country"],
            "coordinates": {
                "latitude": lat, 
                "longitude": lon
            },
            "current_weather": {
                "temperature": current["temperature"],
                "windspeed": current["windspeed"],
                "weathercode": current["weathercode"],
                "condition": weather_codes.get(current["weathercode"], "Unknown"),
                "time": current["time"]
            },
            "hourly_forecast": [] # This list will hold hourly objects
        }

       #for index in range(len(hourly["time"])): --> 24 h x 7 days = 168 entries (too much)
        for index in range(24):     #just right for 24 entries within a single day. 
            forecast_entry = {
                "time": hourly["time"][index],
                "temperature": hourly["temperature_2m"][index],
                "precipitation_probability": hourly["precipitation_probability"][index],
                "weathercode": hourly["weathercode"][index]
            }
            # hourly_forecast is a list?? from the api? 
            final_weather_data[city_name]["hourly_forecast"].append(forecast_entry)
            
        print(f"Successfully mapped data for {city_name}\n")

    except Exception as e:
        print(f"Could not get data for {city_name}: {e}")

    time.sleep(1.0)

print("\nAll cities processed!\n")

print("\nSaving results to eu_weather_data.json...")

with open("eu_weather_data.json","w") as f:
    # takes the dictionary then translates it into JSON format, and writes data to f. 
    json.dump(final_weather_data, f, indent=4)
    # indent=4 is important for indentation and new lines. . Otherwise, all data would be one giant messy line. 

print("\nLab completed successfully!\n")