"""validation.py: Contains functions for validating user input."""

import re

from ..config.constants import Constants
from . import logger

logger = logger.getChild(__name__)


def validate_year(year: str) -> str:
    """
    Validate that the year is a four-digit number.

    Parameters
    ----------
    year : str
        The year to validate.

    Returns
    -------
    str
        The validated year.

    Raises
    ------
    ValueError
        If the year is not a four-digit number.
    """
    if re.match(Constants.YEAR_FORMAT, year):
        return year
    raise ValueError("Year must be a four-digit number.")


def validate_student_id(student_id: str) -> str:
    """
    Validate that the student ID is an eight-digit number.

    Parameters
    ----------
    student_id : str
        The student ID to validate.

    Returns
    -------
    str
        The validated student ID.

    Raises
    ------
    ValueError
        If the student ID is not an eight-digit number.
    """
    if re.match(Constants.ID_FORMAT, student_id):
        return student_id
    raise ValueError("Student ID must be an eight-digit number.")


def validate_date(date: str) -> str:
    """
    Validate that the date is in the format YYYY-MM-DD.

    Parameters
    ----------
    date : str
        The date to validate.

    Returns
    -------
    str
        The validated date.

    Raises
    ------
    ValueError
        If the date is not in the format YYYY-MM-DD.
    """
    if re.match(Constants.DATE_FORMAT, date):
        return date
    raise ValueError("Date must be in the format YYYY-MM-DD.")
