import pytest

from energy_manager.src.apis.weather.get_coordinates import get_coordinates


@pytest.mark.parametrize(
    "city_name, city_expected_coordinates",
    [
        ("pariS ", {"lat": 48.8588897, "lon": 2.3200410217200766}),
        ("    PARIS", {"lat": 48.8588897, "lon": 2.3200410217200766}),
        ("Toulouse      ", {"lat": 43.6044622, "lon": 1.4442469}),
        ("Montpellier", {"lat": 43.6112422, "lon": 3.8767337}),
        ("Marseille", {"lat": 43.2961743, "lon": 5.3699525}),
        ("STRASBOurG", {"lat": 48.584614, "lon": 7.7507127}),
        ("BoRDeauX", {"lat": 44.841225, "lon": -0.5800364}),
        ("LiLle", {"lat": 50.6365654, "lon": 3.0635282}),
        ("Nice", {"lat": 43.7009358, "lon": 7.2683912}),
        ("Lyon", {"lat": 45.7578137, "lon": 4.8320114}),
    ]
)

def test_get_coordinates(city_name, city_expected_coordinates):
    """
    Test the get_coordinates function to ensure it returns correct coordinates for known cities.
    """
    # Get coordinates for the specified city using the get_coordinates function
    city_actual_coordinates = get_coordinates(city_name)

    # Assert that actual coordinates match expected coordinates
    assert city_actual_coordinates == city_expected_coordinates, (
        f"Expected {city_expected_coordinates}, but got {city_actual_coordinates}"
    )