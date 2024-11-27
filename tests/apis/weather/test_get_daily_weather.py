import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime
from freezegun import freeze_time

from energy_manager.src.apis.weather.get_daily_weather import get_daily_weather
from energy_manager.src.utils.generate_daily_timestamps import generate_daily_timestamps
from energy_manager.src.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

@pytest.fixture
def timestamps(frozen_time):
    # Set the frozen time to November 24, 2024, 9:30:45 AM UTC
    with freeze_time(frozen_time):
        midnight_utc_timestamp = get_midnight_utc_timestamp()
        return generate_daily_timestamps(start_timestamp=midnight_utc_timestamp)

@pytest.fixture
def city_name():
    return "Paris"

@pytest.fixture
def df_expected_daily_weather():
    data_df = pd.read_csv(filepath_or_buffer=Path(__file__).parent.parent / "fixtures/daily_weather.csv")
    data_df["date_time"] = pd.to_datetime(data_df["date_time"])
    data_df["temperature"] = data_df["temperature"].astype(float)
    data_df["weather_description"] = data_df["weather_description"].astype(str)
    return data_df

def test_get_daily_weather(city_name, timestamps, df_expected_daily_weather):
    """
    Test the test_get_daily_weather function to ensure it returns the correct
    DataFrame with daily weather data.
    """
    # Get daily weather data for the specified city using the get_daily_weather function
    df_actual_daily_weather = get_daily_weather(city_name=city_name, timestamps=timestamps)

    # Assert that actual DataFrame matches the expected DataFrame
    pd.testing.assert_frame_equal(df_actual_daily_weather, df_expected_daily_weather, check_like=True, check_exact=True)
