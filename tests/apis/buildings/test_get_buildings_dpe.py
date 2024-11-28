import pytest
import pandas as pd
from energy_manager.src.apis.buildings.get_buildings_dpe import get_buildings_dpe


@pytest.fixture()
def city_name():
    return "Nice"

@pytest.fixture()
def expected_columns():
    return ["dpe_class", "building_type", "min_surface_in_square_meters", "max_surface_in_square_meters"]

@pytest.fixture()
def expected_data_types():
    return pd.DataFrame({
        "columns": ["dpe_class", "building_type", "min_surface_in_square_meters", "max_surface_in_square_meters"],
        "data_types": ["category", "object", "float64", "float64"]
    })

@pytest.fixture()
def expected_dpe_classes():
    return ["A", "B", "C", "D", "E", "F", "G"]

def test_get_buildings_dpe(city_name, expected_columns, expected_data_types, expected_dpe_classes):
    """
    Test that the function get_buildings_dpe returns a DataFrame when it successfully fetches buildings DPE data.
    """
    df_actual_buildings_dpe = get_buildings_dpe(city_name=city_name)

    # Check if the DataFrame is of type pandas.DataFrame
    assert isinstance(df_actual_buildings_dpe, pd.DataFrame), (
        f"Expected a pandas.DataFrame for {city_name}, but got {type(df_actual_buildings_dpe)}"
    )

    # Check if the DataFrame contains the expected columns
    assert len(df_actual_buildings_dpe.columns.tolist()) == len(expected_columns), (
        f"Expected {len(expected_columns)} columns for {city_name}, but got {len(df_actual_buildings_dpe.columns.tolist())}"
    )
    assert all(column in df_actual_buildings_dpe.columns.tolist() for column in expected_columns), (
        f"Expected columns {expected_columns} for {city_name}, but got {df_actual_buildings_dpe.columns.tolist()}"
    )

    # Check if the DataFrame data types are as expected
    actual_data_types = pd.DataFrame({
        "columns": ["dpe_class", "building_type", "min_surface_in_square_meters", "max_surface_in_square_meters"],
        "data_types": [
            df_actual_buildings_dpe["dpe_class"].dtype,
            df_actual_buildings_dpe["building_type"].dtype,
            df_actual_buildings_dpe["min_surface_in_square_meters"].dtype,
            df_actual_buildings_dpe["max_surface_in_square_meters"].dtype
        ]
    })
    pd.testing.assert_frame_equal(actual_data_types, expected_data_types, check_like=True, check_exact=True)

    # Check if the DataFrame contains the expected DPE classes
    assert list(df_actual_buildings_dpe["dpe_class"].cat.categories) == expected_dpe_classes
