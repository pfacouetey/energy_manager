import os
import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime
from freezegun import freeze_time

from src.energy_manager.apis.weather.get_daily_weather import get_daily_weather
from src.energy_manager.utils.generate_daily_timestamps import generate_daily_timestamps
from src.energy_manager.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp

TOL_FLOAT = 1e-06


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

@pytest.fixture
def timestamps(frozen_time):
    with freeze_time(frozen_time):
        midnight_utc_timestamp = get_midnight_utc_timestamp()
        return generate_daily_timestamps(start_timestamp=midnight_utc_timestamp)

@pytest.fixture
def city_name():
    return "Paris"

@pytest.fixture
def openweathermap_api_key():
    return os.getenv("OPEN_WEATHER_API_KEY")

@pytest.fixture
def expected_daily_weather_df():
    data_df = pd.read_csv(filepath_or_buffer=Path(__file__).parent / "fixtures/daily_weather.csv")
    data_df["date_time"] = pd.to_datetime(data_df["date_time"])
    data_df["temperature"] = data_df["temperature"].astype(float)
    data_df["weather_description"] = data_df["weather_description"].astype(str)
    return data_df

def test_get_daily_weather(
        city_name,
        openweathermap_api_key,
        timestamps,
        expected_daily_weather_df,
):
    """
    Tests the `get_daily_weather` function by comparing the function's output with expected
    results to ensure accuracy and correctness. The function retrieves daily weather data
    based on the provided city, API key, and timestamps.

    Args:
        city_name: The name of the city for which the weather data is retrieved.
        openweathermap_api_key: The API key required to access the OpenWeatherMap service.
        timestamps: A list of timestamps representing the desired dates or times for
            which to retrieve the weather data.
        expected_daily_weather_df: The expected daily weather data in DataFrame format for
            comparison with the actual output.

    """
    actual_daily_weather_df = get_daily_weather(
        city_name=city_name,
        openweathermap_api_key=openweathermap_api_key,
        timestamps=timestamps
    )

    pd.testing.assert_frame_equal(
        actual_daily_weather_df,
        expected_daily_weather_df,
        check_exact=False,
        atol=TOL_FLOAT
    )
