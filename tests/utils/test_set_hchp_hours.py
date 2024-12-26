import pytest
import pandas as pd

from src.energy_manager.utils.set_hchp_hours import set_hchp_hours


@pytest.fixture()
def expected_columns():
    return ["hour", "option_1", "option_2", "option_3", "option_4"]

@pytest.fixture()
def expected_data_types(expected_columns):
    return pd.DataFrame(
        {
            "columns": expected_columns,
            "data_types": ["int64", "object", "object", "object", "object"],
        }
    )

def test_set_hchp_hours(
        expected_columns,
        expected_data_types,
):
    """
    Validates the output DataFrame structure and data types, ensuring it matches the
    expected schema and value constraints. The function checks that the actual DataFrame
    returned by `set_hchp_hours` meets the required conditions in terms of column names,
    column count, data types, and range of hour values.

    Args:
        expected_columns (List[str]): List of expected column names that the DataFrame
            should have.
        expected_data_types (pd.DataFrame): DataFrame specifying the expected data
            types for the columns. This is used to compare actual data types with
            expected ones.
    """
    actual_hchp_hours_df = set_hchp_hours()

    assert isinstance(actual_hchp_hours_df, pd.DataFrame), (
        f"Expected a pandas.DataFrame, but got {type(actual_hchp_hours_df)}"
    )

    actual_columns = actual_hchp_hours_df.columns.tolist()
    assert len(actual_columns) == len(expected_columns), (
        f"Expected {len(expected_columns)} columns, but got {len(actual_columns)}"
    )
    assert all(column in actual_columns for column in expected_columns), (
        f"Expected columns {expected_columns}, but got {actual_columns}"
    )

    actual_data_types = pd.DataFrame({
        "columns": ["hour", "option_1", "option_2", "option_3", "option_4"],
        "data_types": [
            actual_hchp_hours_df["hour"].dtype,
            actual_hchp_hours_df["option_1"].dtype,
            actual_hchp_hours_df["option_2"].dtype,
            actual_hchp_hours_df["option_3"].dtype,
            actual_hchp_hours_df["option_4"].dtype
        ]
    })
    pd.testing.assert_frame_equal(
        expected_data_types,
        actual_data_types,
        check_like=True,
        check_exact=True,
    )

    assert actual_hchp_hours_df["hour"].between(0, 23).all(), (
        "Expected hours between 0 and 23, but got hours outside this range"
    )