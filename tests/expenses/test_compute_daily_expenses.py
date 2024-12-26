import os
import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime
from freezegun import freeze_time

from src.energy_manager.expenses.compute_daily_expenses import compute_daily_expenses

TOL_FLOAT = 1e-06


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

@pytest.fixture
def user_temperature():
    return 20.0

@pytest.fixture
def user_city_name():
    return "Nangis"

@pytest.fixture
def openweathermap_api_key():
    return os.getenv("OPEN_WEATHER_API_KEY")

@pytest.fixture
def user_dpe_usage():
    return 1.0

@pytest.fixture
def user_insulation_factor():
    return 1.5

@pytest.fixture
def expected_daily_expenses_df():
    data_df = pd.read_csv(filepath_or_buffer=Path(__file__).parent / "fixtures/daily_expenses.csv")
    data_df["date_time"] = pd.to_datetime(data_df["date_time"])
    data_df[["weather_description","building_type", "dpe_class"]] = (
        data_df[["weather_description", "building_type", "dpe_class"]]).astype(str)
    data_df[["option_0", "option_1", "option_2", "option_3", "option_4"]] = (
        data_df[["option_0", "option_1", "option_2", "option_3", "option_4"]]).astype(float)
    return data_df

def test_compute_daily_expenses(
        frozen_time,
        user_temperature,
        user_city_name,
        openweathermap_api_key,
        user_dpe_usage,
        user_insulation_factor,
        expected_daily_expenses_df,
):
    """
    Test function to verify the correctness of the `compute_daily_expenses` function by freezing the time and
    comparing the result against expected data. It ensures that the computed daily expenses dataframe matches
    the provided expected dataframe within allowed tolerance.

    Args:
        frozen_time: The specific timestamp string at which the function's output should be evaluated.
        user_temperature: The temperature input provided by the user for expense calculation.
        user_city_name: The name of the city provided by the user to fetch environmental data.
        openweathermap_api_key: The API key used for authenticating requests to the OpenWeatherMap service.
        user_dpe_usage: The user's declared energy consumption level, used for computation.
        user_insulation_factor: The insulation factor provided by the user, influencing energy use estimation.
        expected_daily_expenses_df: The expected pandas DataFrame containing the daily expenses to validate against.
    """
    with freeze_time(frozen_time):
        actual_daily_expenses_df = compute_daily_expenses(
            temperature=user_temperature,
            city_name=user_city_name,
            openweathermap_api_key=openweathermap_api_key,
            dpe_usage=user_dpe_usage,
            insulation_factor=user_insulation_factor
        )

    pd.testing.assert_frame_equal(
        actual_daily_expenses_df,
        expected_daily_expenses_df,
        check_exact=False,
        atol=TOL_FLOAT
    )
