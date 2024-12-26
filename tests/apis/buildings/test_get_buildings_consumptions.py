import pytest
import pandas as pd
from pathlib import Path

from src.energy_manager.apis.buildings.get_buildings_consumptions import get_buildings_consumptions

TOL_FLOAT = 1e-06


@pytest.fixture()
def city_name():
    return "Nice"

@pytest.fixture
def expected_buildings_consumptions_df():
    data_df = pd.read_csv(filepath_or_buffer=Path(__file__).parent / "fixtures/buildings_consumptions.csv")
    data_df["dpe_class"] = pd.Categorical(
        data_df["dpe_class"],
        categories=["A", "B", "C", "D", "E", "F"],
        ordered=True
    )
    data_df["consumption_in_kwh_per_square_meter"] = data_df["consumption_in_kwh_per_square_meter"].astype(float)
    data_df["building_type"] = data_df["building_type"].astype(str)
    return data_df

def test_get_buildings_consumptions(
        city_name,
        expected_buildings_consumptions_df,
):
    """
    Tests the `get_buildings_consumptions` function to ensure that it returns
    a pandas DataFrame whose contents match the expected values for the
    provided city. The function is evaluated by checking the type of the
    returned value and comparing the DataFrame against an expected DataFrame
    with a specified tolerance.

    Args:
        city_name: Name of the city for which building consumption data is
            fetched.
        expected_buildings_consumptions_df: Expected pandas DataFrame containing
            the building consumption data for the city.

    Raises:
        AssertionError: If the returned value is not a pandas DataFrame or
            if the returned DataFrame does not match the expected DataFrame
            within the specified tolerance.
    """
    actual_buildings_consumptions_df = get_buildings_consumptions(city_name=city_name)

    assert isinstance(actual_buildings_consumptions_df, pd.DataFrame), (
        f"Expected a pandas.DataFrame for {city_name}, but got {type(actual_buildings_consumptions_df)}"
    )

    pd.testing.assert_frame_equal(
        expected_buildings_consumptions_df,
        actual_buildings_consumptions_df,
        check_exact=False,
        atol=TOL_FLOAT
    )
