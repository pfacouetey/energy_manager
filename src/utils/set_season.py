from datetime import datetime


def set_season(date_time: datetime) -> str:
    """
    Given a date, returns the season based on the given month and day.

    Args:
        date_time (datetime): The date to determine the season for.

    Returns:
        str: The season corresponding to the given date.
    """
    month = date_time.month
    day = date_time.day

    if (3 <= month <= 6) and (21 <= day <= 31 if month == 3 else day <= 21 if month == 6 else True):
        return "Spring"
    elif (6 <= month <= 9) and (22 <= day <= 30 if month == 6 else day <= 23 if month == 9 else True):
        return "Summer"
    elif (9 <= month <= 12) and (24 <= day <= 30 if month == 9 else day <= 21 if month == 12 else True):
        return "Fall"
    else:
        return "Winter"
