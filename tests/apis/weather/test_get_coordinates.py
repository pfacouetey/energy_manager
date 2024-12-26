import os
import pytest

from src.energy_manager.apis.weather.get_coordinates import get_coordinates

TOL_FLOAT = 1e-06


@pytest.mark.parametrize(
    "city_name, openweathermap_api_key, expected_city_coordinates",
    [
        ("paris", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 48.8588897, "lon": 2.3200410217200766}),
        ("Toulouse      ", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 43.6044622, "lon": 1.4442469}),
        ("Montpellier", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 43.6112422, "lon": 3.8767337}),
        ("STRASBOURG", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 48.584614, "lon": 7.7507127}),
        ("Nice", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 43.7009358, "lon": 7.2683912}),
        ("Lyon", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 45.7578137, "lon": 4.8320114}),
        ("Now is the day", os.getenv("OPEN_WEATHER_API_KEY"), None),
    ]
)

def test_get_coordinates(city_name, openweathermap_api_key, expected_city_coordinates):
    """
    Test the functionality of the `get_coordinates` function by comparing the actual
    coordinates retrieved for a city name with the expected coordinates. The test
    evaluates various scenarios, including exact matches for city coordinates,
    handling of trimmed or capitalized city names, and cases where no coordinate is
    expected for an invalid input.

    Args:
        city_name (str): The name of the city for which the coordinates are being
            retrieved. This can include valid city names, trimmed white-spaces, or
            invalid names.
        openweathermap_api_key (str): API key required for authenticating with the
            OpenWeatherMap API. The key must be valid for requesting data.
        expected_city_coordinates (dict or None): Expected coordinates of the city
            in the format {"lat": float, "lon": float}. This is None for invalid or
            unrecognized city names.
    """
    actual_city_coordinates = get_coordinates(
        city_name=city_name,
        openweathermap_api_key=openweathermap_api_key
    )

    if expected_city_coordinates is None:
        assert actual_city_coordinates is None
    else:
        assert actual_city_coordinates is not None
        assert actual_city_coordinates["lat"] == pytest.approx(expected_city_coordinates["lat"], abs=TOL_FLOAT)
        assert actual_city_coordinates["lon"] == pytest.approx(expected_city_coordinates["lon"], abs=TOL_FLOAT)
