import os
import pytest

from energy_manager.src.energy_manager.apis.weather.get_coordinates import get_coordinates


@pytest.mark.parametrize(
    "city_name, openweathermap_api_key, city_expected_coordinates",
    [
        ("pariS ", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 48.8588897, "lon": 2.3200410217200766}),
        ("    PARIS", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 48.8588897, "lon": 2.3200410217200766}),
        ("Toulouse      ", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 43.6044622, "lon": 1.4442469}),
        ("Montpellier", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 43.6112422, "lon": 3.8767337}),
        ("Marseille", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 43.2961743, "lon": 5.3699525}),
        ("STRASBOurG", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 48.584614, "lon": 7.7507127}),
        ("BoRDeauX", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 44.841225, "lon": -0.5800364}),
        ("LiLle", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 50.6365654, "lon": 3.0635282}),
        ("Nice", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 43.7009358, "lon": 7.2683912}),
        ("Lyon", os.getenv("OPEN_WEATHER_API_KEY"), {"lat": 45.7578137, "lon": 4.8320114}),
        ("No", os.getenv("OPEN_WEATHER_API_KEY"), None),
    ]
)

def test_get_coordinates(city_name, openweathermap_api_key, city_expected_coordinates):
    """
    Test the get_coordinates function to ensure it returns correct coordinates for known cities.
    """
    # Get coordinates for the specified city using the get_coordinates function
    city_actual_coordinates = get_coordinates(city_name=city_name, openweathermap_api_key=openweathermap_api_key)

    # Assert that actual coordinates match expected coordinates
    assert city_actual_coordinates == city_expected_coordinates, (
        f"Expected {city_expected_coordinates}, but got {city_actual_coordinates}"
    )