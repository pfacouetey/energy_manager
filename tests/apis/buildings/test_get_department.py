import pytest

from src_copy.energy_manager.apis.buildings.get_department import get_department


@pytest.mark.parametrize(
    "city_name, expected_city_department",
    [
        ("Nancy", "Meurthe-et-Moselle"),
        ("NaNcy ", "Meurthe-et-Moselle"),
        ("Toulouse      ", "Haute-Garonne"),
        ("PARIS", "Paris"),
        ("STRASBOurG", "Bas-Rhin"),
        ("BoRDeauX", "Gironde"),
        ("LiLle", "Nord"),
        ("Nice", "Alpes-Maritimes"),
        ("Lyon", "Rhône"),
    ]
)

def test_get_department(
        city_name,
        expected_city_department,
):
    """
    Tests the `get_department` function to verify that it correctly returns the expected
    department name associated with a given city name.

    This test function uses parameterized inputs to validate the function against various
    city names, ensuring the function handles case sensitivity and extra spaces appropriately.

    Args:
        city_name (str): The name of the city to query for its corresponding department.
        expected_city_department (str): The expected department name for the given city.
    """
    actual_city_department = get_department(city_name)

    assert actual_city_department == expected_city_department, (
        f"Expected {expected_city_department}, but got {actual_city_department}"
    )