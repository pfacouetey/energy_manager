import pytest
import pandas as pd
from datetime import datetime
from freezegun import freeze_time

from energy_manager.src.apis.get_hourly_weather import get_hourly_weather
from energy_manager.src.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

@pytest.fixture
def city_name():
    return "Paris"

@pytest.fixture
def df_expected_hourly_weather():
    return pd.DataFrame([{
        "date_time": datetime(2024, 11, 24, 0, 0, 0),
        "temperature": 11.22,
        "weather_description": "clear sky",
    }])


def test_get_hourly_weather(frozen_time, city_name, df_expected_hourly_weather):
    """
    Test the get_hourly_weather function to ensure it returns the correct
    DataFrame with hourly weather data.
    """
    # Set the frozen time to November 24, 2024, 9:30:45 AM UTC
    with freeze_time(frozen_time):

        # Get the Unix timestamp for midnight UTC of the frozen date using the get_midnight_utc function
        midnight_utc_timestamp = get_midnight_utc_timestamp()

        # Get hourly weather data for the specified city using the get_hourly_weather function
        df_actual_hourly_weather = get_hourly_weather(city_name=city_name, timestamp=midnight_utc_timestamp)

        # Assert that actual DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(df_actual_hourly_weather, df_expected_hourly_weather, check_like=True, check_exact=True)