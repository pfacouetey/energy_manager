import pytest
from datetime import datetime
from freezegun import freeze_time

from energy_manager.src.utils.set_season import set_season
from energy_manager.src.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp


@pytest.fixture
def frozen_time():
    return datetime(2024, 11, 24, 9, 30, 45)

@pytest.fixture()
def expected_season():
    return "Fall"

def test_get_season(frozen_time, expected_season):
    """
    Test the set_season function to ensure it returns the correct season for the given date.
    """
    # Set the frozen time to November 24, 2024, 9:30:45 AM UTC
    with freeze_time(frozen_time):

        # Get the Unix timestamp for midnight UTC of the current date
        midnight_utc_timestamp = get_midnight_utc_timestamp()

        # Get the date corresponding to the midnight UTC timestamp
        midnight_utc_date_time = datetime.fromtimestamp(midnight_utc_timestamp)

        # Get the season for the given date
        actual_season = set_season(midnight_utc_date_time)

        # Assert that the actual season matches the expected season
        assert actual_season == expected_season, f"Expected {expected_season}, but got {actual_season}"
