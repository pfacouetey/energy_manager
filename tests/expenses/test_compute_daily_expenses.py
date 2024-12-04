import os
import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime
from freezegun import freeze_time

from energy_manager.src.expenses.compute_daily_expenses import compute_daily_expenses


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
def df_expected_daily_expenses():
    data_df = pd.read_csv(filepath_or_buffer=Path(__file__).parent / "fixtures/daily_expenses.csv")
    data_df["date_time"] = pd.to_datetime(data_df["date_time"])
    data_df[["weather_description","building_type", "dpe_class"]] = (
        data_df[["weather_description", "building_type", "dpe_class"]]).astype(str)
    data_df[["option_1", "option_2", "option_3", "option_4", "option_0"]] = (
        data_df[["option_1", "option_2", "option_3", "option_4", "option_0"]]).astype(float)
    return data_df

def test_compute_daily_expenses(
        frozen_time,
        user_temperature,
        user_city_name,
        openweathermap_api_key,
        user_dpe_usage,
        user_insulation_factor,
        df_expected_daily_expenses
):
    """
    Test the compute_daily_expenses function with a fixed date and time to ensure it returns the correct DataFrame of daily expenses.
    """
    # Set the frozen time to November 24, 2024, 9:30:45 AM UTC
    with freeze_time(frozen_time):
        df_actual_daily_expenses = compute_daily_expenses(
        user_temperature=user_temperature,
        user_city_name=user_city_name,
        openweathermap_api_key=openweathermap_api_key,
        user_dpe_usage=user_dpe_usage,
        user_insulation_factor=user_insulation_factor
        )

    # Assert that the actual DataFrame of daily expenses matches the expected DataFrame
    pd.testing.assert_frame_equal(df_actual_daily_expenses, df_expected_daily_expenses, check_like=True)