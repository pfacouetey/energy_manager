import pytz
import pytest
from datetime import datetime
from freezegun import freeze_time

from energy_manager.src.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

def test_get_midnight_utc(frozen_time):
    """
    Test the get_midnight_utc function to ensure it returns the correct
    Unix timestamp for midnight UTC of the frozen date.
    """
    # Set the frozen time to November 24, 2024, 9:30:45 AM UTC
    with freeze_time(frozen_time):

        # Get the Unix timestamp for midnight UTC of the current date
        expected_midnight_utc = datetime(2024, 11, 24, 0, 0, 0, tzinfo=pytz.utc)

        # Calculate the expected Unix timestamp for midnight UTC of the frozen date
        expected_midnight_utc_timestamp = int(expected_midnight_utc.timestamp())

        # Get the Unix timestamp for midnight UTC of the frozen date using the get_midnight_utc function
        actual_midnight_utc_timestamp = get_midnight_utc_timestamp()

        # Assert that the actual Unix timestamp matches the expected Unix timestamp
        assert actual_midnight_utc_timestamp == expected_midnight_utc_timestamp, (
            f"Expected {expected_midnight_utc_timestamp}, but got {actual_midnight_utc_timestamp}"
        )