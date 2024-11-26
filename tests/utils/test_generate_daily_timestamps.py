import pytest
from datetime import datetime
from freezegun import freeze_time

from energy_manager.src.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp
from energy_manager.src.utils.generate_daily_timestamps import generate_daily_timestamps


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

def test_generate_daily_timestamps(frozen_time):
    """
    Test the generate_daily_timestamps function to ensure it returns the correct
    Unix timestamps for each hour of the frozen date.
    """
    # Set the frozen time to November 24, 2024, 9:30:45 AM UTC
    with freeze_time(frozen_time):

        # Get the Unix timestamp for midnight UTC of the frozen date
        midnight_utc_timestamp = get_midnight_utc_timestamp()

        # Generate Unix timestamps for each day of the week from the frozen date
        expected_timestamps = [
            midnight_utc_timestamp + i * 3600 for i in range(24)
        ]

        # Get Unix timestamps for frozen date using the generate_daily_timestamps function
        actual_timestamps = generate_daily_timestamps(midnight_utc_timestamp)

        # Assert that actual Unix timestamps match expected Unix timestamps
        assert actual_timestamps == expected_timestamps, (
            f"Expected {expected_timestamps}, but got {actual_timestamps}"
        )