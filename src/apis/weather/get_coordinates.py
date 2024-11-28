import os
import requests
from unidecode import unidecode
from typing import Dict, Optional


def get_coordinates(city_name: str) -> Optional[Dict[str, float]]:
    """
    Get coordinates for a given city.

    Args:
        city_name (str): Name of the city.

    Returns:
        Optional[Dict[str, float]]: Dictionary with "lat" and "lon" keys, or None if not found.
    """
    api_key = os.getenv("OPEN_WEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{unidecode(city_name.strip().lower())}",
        "limit": 1,
        "appid": api_key
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        country_code = data[0]["country"] if data else None

        if not country_code:
            print(f"Country code not found for city {city_name}.")
            return None

        if country_code == "FR":
            city_coordinates = {"lat": data[0]["lat"], "lon": data[0]["lon"]}
            return city_coordinates

        else:
            print(f"City {city_name} not found in France. Please, specify a city known in France.")
            return None

    else:
        print(f"Error fetching data: {response.status_code}")
        return None
