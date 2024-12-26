import pytest
from datetime import datetime
from freezegun import freeze_time

from src.energy_manager.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp
from src.energy_manager.utils.generate_daily_timestamps import generate_daily_timestamps


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

def test_generate_daily_timestamps(frozen_time):
    """
    Tests the `generate_daily_timestamps` function by verifying that it generates
    24 hourly timestamps starting from a midnight UTC timestamp. The function
    computes expected timestamps using a frozen time context and compares them
    to the actual output from the tested function.

    Args:
        frozen_time: A string representing the time to freeze in the format
            'YYYY-MM-DD HH:MM:SS', which determines the fixed point for the
            timestamp calculations.
    """
    with freeze_time(frozen_time):

        midnight_utc_timestamp = get_midnight_utc_timestamp()
        expected_timestamps = [
            midnight_utc_timestamp + i * 3600 for i in range(24)
        ]
        actual_timestamps = generate_daily_timestamps(midnight_utc_timestamp)

        assert actual_timestamps == expected_timestamps, (
            f"Expected {expected_timestamps}, but got {actual_timestamps}"
        )