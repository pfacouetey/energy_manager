import pytest
import pandas as pd

from energy_manager.src.apis.buildings.get_buildings_consumptions import get_buildings_consumptions


@pytest.fixture()
def city_name():
    return "Nice"

@pytest.fixture()
def expected_columns():
    return [
        "dpe_class", "building_type", "min_surface_in_square_meters", "max_surface_in_square_meters",
        "consumption_in_kwh_per_square_meter"
    ]

@pytest.fixture()
def expected_data_types(expected_columns):
    return pd.DataFrame({
        "columns": expected_columns,
        "data_types": ["category", "object", "float64", "float64", "float64"]
    })

@pytest.fixture()
def expected_dpe_classes():
    return ["A", "B", "C", "D", "E", "F"]

def test_get_buildings_consumptions(city_name, expected_columns, expected_data_types, expected_dpe_classes):
    """
    Test that the function get_buildings_consumptions returns a DataFrame.
    """
    df_actual_buildings_consumptions = get_buildings_consumptions(city_name=city_name)

    # Check if the DataFrame is of type pandas.DataFrame
    assert isinstance(df_actual_buildings_consumptions, pd.DataFrame), (
        f"Expected a pandas.DataFrame for {city_name}, but got {type(df_actual_buildings_consumptions)}"
    )

    # Check if the DataFrame contains the expected columns
    assert len(df_actual_buildings_consumptions.columns.tolist()) == len(expected_columns), (
        f"Expected {len(expected_columns)} columns for {city_name}, but got {len(df_actual_buildings_consumptions.columns.tolist())}"
    )
    assert all(column in df_actual_buildings_consumptions.columns.tolist() for column in expected_columns), (
        f"Expected columns {expected_columns} for {city_name}, but got {df_actual_buildings_consumptions.columns.tolist()}"
    )

    # Check if the DataFrame data types are as expected
    actual_data_types = pd.DataFrame({
        "columns": [
            "dpe_class", "building_type", "min_surface_in_square_meters", "max_surface_in_square_meters",
            "consumption_in_kwh_per_square_meter"
        ],
        "data_types": [
            df_actual_buildings_consumptions["dpe_class"].dtype,
            df_actual_buildings_consumptions["building_type"].dtype,
            df_actual_buildings_consumptions["min_surface_in_square_meters"].dtype,
            df_actual_buildings_consumptions["max_surface_in_square_meters"].dtype,
            df_actual_buildings_consumptions["consumption_in_kwh_per_square_meter"].dtype
        ]
    })
    pd.testing.assert_frame_equal(actual_data_types, expected_data_types, check_like=True, check_exact=True)

    # Check if the DataFrame contains the expected DPE classes
    assert list(df_actual_buildings_consumptions["dpe_class"].cat.categories) == expected_dpe_classes
