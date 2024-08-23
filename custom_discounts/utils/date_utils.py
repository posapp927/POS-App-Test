# custom_discounts/utils/date_utils.py

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Union

logger = logging.getLogger('custom_discounts.utils.date_utils')


def parse_date(date_str: str, formats: Optional[List[str]] = None) -> datetime:
    """
    Parses a date string into a datetime object.

    Args:
        date_str (str): The date string to parse.
        formats (List[str], optional): A list of date formats to try for parsing. Defaults to common formats.

    Returns:
        datetime: The parsed datetime object.

    Raises:
        ValueError: If the date string cannot be parsed into any of the provided formats.
    """
    if formats is None:
        formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']

    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            logger.debug(f"Successfully parsed {date_str} with format {fmt}.")
            return parsed_date
        except ValueError:
            continue

    logger.error(f"Failed to parse date string {date_str} with provided formats.")
    raise ValueError(f"Date string {date_str} is not in a recognized format.")


def format_date(date_obj: datetime, format_str: str = '%Y-%m-%d') -> str:
    """
    Formats a datetime object into a string based on the provided format.

    Args:
        date_obj (datetime): The datetime object to format.
        format_str (str): The format string. Defaults to '%Y-%m-%d'.

    Returns:
        str: The formatted date string.
    """
    formatted_date = date_obj.strftime(format_str)
    logger.debug(f"Formatted date {date_obj} as {formatted_date} using format {format_str}.")
    return formatted_date


def is_date_in_range(date: datetime, start_date: datetime, end_date: datetime) -> bool:
    """
    Checks if a date is within a specific range.

    Args:
        date (datetime): The date to check.
        start_date (datetime): The start of the range.
        end_date (datetime): The end of the range.

    Returns:
        bool: True if the date is within the range, False otherwise.
    """
    in_range = start_date <= date <= end_date
    logger.debug(f"Date {date} is {'within' if in_range else 'not within'} the range {start_date} to {end_date}.")
    return in_range


def days_between(start_date: datetime, end_date: datetime) -> int:
    """
    Calculates the number of days between two dates.

    Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.

    Returns:
        int: The number of days between the dates.
    """
    delta = (end_date - start_date).days
    logger.debug(f"Days between {start_date} and {end_date}: {delta} days.")
    return delta


def add_days(date: datetime, days: int) -> datetime:
    """
    Adds a specific number of days to a date.

    Args:
        date (datetime): The date to add days to.
        days (int): The number of days to add.

    Returns:
        datetime: The new date after adding the days.
    """
    new_date = date + timedelta(days=days)
    logger.debug(f"Added {days} days to {date}. New date: {new_date}.")
    return new_date


def subtract_days(date: datetime, days: int) -> datetime:
    """
    Subtracts a specific number of days from a date.

    Args:
        date (datetime): The date to subtract days from.
        days (int): The number of days to subtract.

    Returns:
        datetime: The new date after subtracting the days.
    """
    new_date = date - timedelta(days=days)
    logger.debug(f"Subtracted {days} days from {date}. New date: {new_date}.")
    return new_date


def get_current_datetime() -> datetime:
    """
    Returns the current date and time.

    Returns:
        datetime: The current date and time.
    """
    current_datetime = datetime.now()
    logger.debug(f"Current datetime: {current_datetime}.")
    return current_datetime


def is_weekend(date: datetime) -> bool:
    """
    Checks if a given date falls on a weekend.

    Args:
        date (datetime): The date to check.

    Returns:
        bool: True if the date is a Saturday or Sunday, False otherwise.
    """
    is_weekend = date.weekday() >= 5  # 5 = Saturday, 6 = Sunday
    logger.debug(f"Date {date} is {'a weekend' if is_weekend else 'a weekday'}.")
    return is_weekend


def get_start_of_month(date: datetime) -> datetime:
    """
    Returns the first day of the month for a given date.

    Args:
        date (datetime): The date to get the start of the month from.

    Returns:
        datetime: The first day of the month.
    """
    start_of_month = date.replace(day=1)
    logger.debug(f"Start of the month for {date}: {start_of_month}.")
    return start_of_month


def get_end_of_month(date: datetime) -> datetime:
    """
    Returns the last day of the month for a given date.

    Args:
        date (datetime): The date to get the end of the month from.

    Returns:
        datetime: The last day of the month.
    """
    next_month = date.replace(day=28) + timedelta(days=4)  # this will never fail
    end_of_month = next_month - timedelta(days=next_month.day)
    logger.debug(f"End of the month for {date}: {end_of_month}.")
    return end_of_month


def get_holidays_for_year(year: int) -> List[datetime]:
    """
    Returns a list of holidays for a given year.

    Args:
        year (int): The year to get holidays for.

    Returns:
        List[datetime]: A list of holidays as datetime objects.
    """
    # Example: New Year's Day, Independence Day, and Christmas
    holidays = [
        datetime(year, 1, 1),   # New Year's Day
        datetime(year, 7, 4),   # Independence Day
        datetime(year, 12, 25), # Christmas
    ]
    logger.debug(f"Holidays for year {year}: {holidays}.")
    return holidays
