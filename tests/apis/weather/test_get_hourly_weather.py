import os
import pytest
import pandas as pd
from datetime import datetime
from freezegun import freeze_time

from src.energy_manager.apis.weather.get_hourly_weather import get_hourly_weather
from src.energy_manager.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp

TOL_FLOAT = 1e-06


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

@pytest.fixture
def city_name():
    return "Paris"

@pytest.fixture
def openweathermap_api_key():
    return os.getenv("OPEN_WEATHER_API_KEY")

@pytest.fixture
def expected_hourly_weather_df():
    return pd.DataFrame(
        [
            {
                "date_time": datetime(2024, 11, 24, 0, 0, 0),
                "temperature": 11.22,
                "weather_description": "clear sky",
            }
        ]
    )


def test_get_hourly_weather(
        frozen_time,
        city_name,
        openweathermap_api_key,
        expected_hourly_weather_df,
):
    """
    Tests the function `get_hourly_weather` to ensure it retrieves the hourly weather
    data for the specified city and matches the expected data. The function uses a
    predefined frozen time to validate time-dependent logic, such as timestamp
    handling.

    Args:
        frozen_time: The mock time to be frozen during the test, allowing consistent
            evaluation of time-dependent functionalities.
        city_name: The name of the city for which the hourly weather data is to be
            fetched.
        openweathermap_api_key: The API key required to authenticate requests to the
            OpenWeatherMap API.
        expected_hourly_weather_df: The expected pandas DataFrame containing the
            hourly weather data against which the actual fetched data is validated.

    Raises:
        AssertionError: If the actual hourly weather DataFrame doesn't match the
            expected DataFrame.
    """
    with freeze_time(frozen_time):

        midnight_utc_timestamp = get_midnight_utc_timestamp()

        actual_hourly_weather_df = get_hourly_weather(
            city_name=city_name,
            openweathermap_api_key=openweathermap_api_key,
            timestamp=midnight_utc_timestamp
        )

        pd.testing.assert_frame_equal(
            actual_hourly_weather_df,
            expected_hourly_weather_df,
            check_exact=False,
            atol=TOL_FLOAT
        )