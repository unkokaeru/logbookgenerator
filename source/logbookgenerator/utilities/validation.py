"""validation.py: Contains functions for validating user input."""

import re
from pathlib import Path

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


def validate_input_directory(input_directory: Path) -> None:
    """
    Validate that the input directory exists and is not empty.

    Parameters
    ----------
    input_directory : Path
        The input directory to validate.

    Raises
    ------
    FileNotFoundError
        If the input directory does not exist.
    ValueError
        If the input directory does not have the expected structure.

    Notes
    -----
    Validates an expected structure of:
    ```
    input_directory/
    ├── weeks/
    │   ├── coursework/
    |   │   ├── coursework1.cpp
    |   │   ├── coursework2.cpp
    |   |   └── ...
    │   ├── week 1/
    |   │   ├── e01-some_text-some_text.cpp
    |   │   ├── l01-some_text-some_text.cpp
    |   │   ├── l02-some_text-some_text.cpp
    |   │   ├── ...
    |   |   └── reflection.md
    │   ├── week 2/
    |   │   ├── e01-some_text-some_text.cpp
    |   │   ├── l01-some_text-some_text.cpp
    |   │   ├── l02-some_text-some_text.cpp
    |   │   ├── ...
    |   |   └── reflection.md
    │   └── ...
    └── references.yaml
    ```
    If the coursework directory is missing, it'll cause a warning but still continue.
    This is the same with the references file.
    There must be at least one week directory, with at least one file in it, though.
    """
    # Check if the input directory exists
    if not input_directory.exists():
        raise FileNotFoundError(f"Input directory {input_directory} does not exist.")

    # Check if the input directory is empty
    if not any(input_directory.iterdir()):
        raise ValueError(f"Input directory {input_directory} is empty.")

    # Check if there is a weeks directory
    weeks_directory = input_directory / "weeks"
    if not weeks_directory.exists():
        raise ValueError(f"Input directory {input_directory} does not have a weeks directory.")

    # Check if there is at least one week directory with at least one file
    week_directories = list(weeks_directory.glob("week*"))
    if not week_directories:
        raise ValueError(f"Weeks directory {weeks_directory} does not have any week directories.")

    # Check if there is at least one file in each week directory
    for week_directory in week_directories:
        week_files = list(week_directory.glob("*.cpp"))
        if not week_files:
            raise ValueError(f"Week directory {week_directory} does not have any week files.")

    # Check if there is a coursework directory
    coursework_directory = weeks_directory / "coursework"
    if not coursework_directory.exists():
        logger.warning(f"Weeks directory {weeks_directory} does not have a coursework directory.")

    # Check if there is a coursework file
    coursework_files = list(coursework_directory.glob("*.cpp"))
    if not coursework_files:
        logger.warning(
            f"Coursework directory {coursework_directory} does not have any coursework files."
        )

    # Check if there is a references file
    references_file = input_directory / "references.yaml"
    if not references_file.exists():
        logger.warning(f"Input directory {input_directory} does not have a references file.")

    logger.info(f"Input directory {input_directory} is valid.")
