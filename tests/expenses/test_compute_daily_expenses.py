import os
import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime
from freezegun import freeze_time

from src_copy.energy_manager.expenses.compute_daily_expenses import compute_daily_expenses

TOL_FLOAT = 1e-06


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

@pytest.fixture
def temperature():
    return 20.0

@pytest.fixture
def city_name():
    return "Nangis"

@pytest.fixture
def openweathermap_api_key():
    return os.getenv("OPEN_WEATHER_API_KEY")

@pytest.fixture
def dpe_usage():
    return 1.0

@pytest.fixture
def insulation_factor():
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
        temperature,
        city_name,
        openweathermap_api_key,
        dpe_usage,
        insulation_factor,
        expected_daily_expenses_df,
):
    """
    Tests the `compute_daily_expenses` function by comparing its output against the expected
    DataFrame of daily expenses. The comparison ensures accuracy within a defined tolerance
    level (`TOL_FLOAT`). The test uses a frozen time to provide consistent, deterministic
    results during execution.

    Args:
        frozen_time: The datetime to freeze time at during the test.
        temperature: The temperature value used as part of the input to compute daily expenses.
        city_name: The name of the city used to fetch weather data in the calculation.
        openweathermap_api_key: The API key to access the OpenWeatherMap service, which is
            used to fetch weather-related data.
        dpe_usage: The energy consumption data used in the daily expenses computation.
        insulation_factor: A factor reflecting the efficiency of insulation used in the
            energy cost calculations.
        expected_daily_expenses_df: The expected DataFrame containing the calculated daily
            expenses to validate the function output against.
    """
    with freeze_time(frozen_time):
        actual_daily_expenses_df = compute_daily_expenses(
            temperature=temperature,
            city_name=city_name,
            openweathermap_api_key=openweathermap_api_key,
            dpe_usage=dpe_usage,
            insulation_factor=insulation_factor
        )

    pd.testing.assert_frame_equal(
        actual_daily_expenses_df,
        expected_daily_expenses_df,
        check_exact=False,
        atol=TOL_FLOAT
    )
