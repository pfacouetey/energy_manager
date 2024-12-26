import pytz
import pytest
from datetime import datetime
from freezegun import freeze_time

from src.energy_manager.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

def test_get_midnight_utc(frozen_time):
    """
    Tests the `get_midnight_utc_timestamp` function by freezing the time to a specific
    datetime value and validating that the function correctly calculates the timestamp
    for midnight UTC of the same date.

    Args:
        frozen_time (str): The datetime string to freeze time at for testing the function.
    """
    with freeze_time(frozen_time):

        expected_midnight_utc = datetime(2024, 11, 24, 0, 0, 0, tzinfo=pytz.utc)
        expected_midnight_utc_timestamp = int(expected_midnight_utc.timestamp())
        actual_midnight_utc_timestamp = get_midnight_utc_timestamp()

        assert actual_midnight_utc_timestamp == expected_midnight_utc_timestamp, (
            f"Expected {expected_midnight_utc_timestamp}, but got {actual_midnight_utc_timestamp}"
        )