import pytest

from energy_manager.src.apis.get_department import get_department


@pytest.mark.parametrize(
    "city_name, city_expected_department",
    [
        ("Nancy", "meurthe-et-moselle"),
        ("NaNcy ", "meurthe-et-moselle"),
        ("Toulouse      ", "haute-garonne"),
        ("PARIS", "paris"),
        ("STRASBOurG", "bas-rhin"),
        ("BoRDeauX", "gironde"),
        ("LiLle", "nord"),
        ("Nice", "alpes-maritimes"),
        ("Lyon", "rhone")
    ]
)

def test_get_department(city_name, city_expected_department):
    """
    Test the get_department function to ensure it returns correct departments for known cities.
    """
    # Get department for the specified city using the function get_department
    city_actual_department = get_department(city_name)

    # Assert that actual department matches expected department
    assert city_actual_department == city_expected_department, (
        f"Expected {city_expected_department}, but got {city_actual_department}"
    )