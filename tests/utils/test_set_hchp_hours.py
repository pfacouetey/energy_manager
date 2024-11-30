import pytest
import pandas as pd

from energy_manager.src.utils.set_hchp_hours import set_hchp_hours


@pytest.fixture()
def expected_columns():
    return ["hour", "option_1", "option_2", "option_3", "option_4"]

@pytest.fixture()
def expected_data_types(expected_columns):
    return pd.DataFrame({
        "columns": expected_columns,
        "data_types": ["int64", "object", "object", "object", "object"]
    })

def test_set_hchp_hours(expected_columns, expected_data_types):
    """
    Test that the function set_hchp_hours returns the expected DataFrame.
    """
    df_actual_hchp_hours = set_hchp_hours()

    # Check if the DataFrame is of type pandas.DataFrame
    assert isinstance(df_actual_hchp_hours, pd.DataFrame), (
        f"Expected a pandas.DataFrame, but got {type(df_actual_hchp_hours)}"
    )

    # Check if the DataFrame contains the expected columns
    actual_columns = df_actual_hchp_hours.columns.tolist()
    assert len(actual_columns) == len(expected_columns), (
        f"Expected {len(expected_columns)} columns, but got {len(actual_columns)}"
    )
    assert all(column in actual_columns for column in expected_columns), (
        f"Expected columns {expected_columns}, but got {actual_columns}"
    )

    # Check if the DataFrame data types are as expected
    actual_data_types = pd.DataFrame({
        "columns": ["hour", "option_1", "option_2", "option_3", "option_4"],
        "data_types": [
            df_actual_hchp_hours["hour"].dtype,
            df_actual_hchp_hours["option_1"].dtype,
            df_actual_hchp_hours["option_2"].dtype,
            df_actual_hchp_hours["option_3"].dtype,
            df_actual_hchp_hours["option_4"].dtype
        ]
    })
    pd.testing.assert_frame_equal(actual_data_types, expected_data_types, check_like=True, check_exact=True)

    # Check if the DataFrame contains the expected hours
    assert df_actual_hchp_hours["hour"].between(0, 23).all(), (
        "Expected hours between 0 and 23, but got hours outside this range"
    )