"""parsing.py: Contains the functions for parsing the input directory."""

import os
from pathlib import Path

from ..utilities.file_handling import load_yaml
from . import logger

logger = logger.getChild(__name__)


def parse_weeks_directory(weeks_directory: Path) -> list[dict[str, dict[str, str] | str]]:
    """
    Parse the weeks directory.

    Parameters
    ----------
    weeks_directory : Path
        Path to the weeks directory.

    Returns
    -------
    list[dict[str, dict[str, str] | str]]
        The CPP files and reflections for each week, given as a list of weeks,
        where each week has keys "cpp" and "reflection", each containing a
        dictionary of files or a string respectively.
    """
    weeks_files: list[dict[str, dict[str, str] | str]] = []

    # Get the weeks, organised chronologically so that the dictionary is ordered
    weeks = sorted(os.listdir(weeks_directory))

    for week in weeks:
        week_files: dict[str, dict[str, str] | str] = {
            "cpp": {},
            "reflection": "",
        }
        week_path = weeks_directory / week

        # Parse CPP files
        for file_path in week_path.glob("*.cpp"):
            with open(file_path) as file:
                week_files["cpp"][file_path.stem] = file.read()  # type: ignore

        # Parse reflection
        reflection_path = week_path / "reflection.md"
        with open(reflection_path) as file:
            week_files["reflection"] = file.read()

        # Add the week to the list
        weeks_files.append(week_files)

    return weeks_files


def parse_input_directory(
    input_directory: Path,
) -> tuple[list[dict[str, dict[str, str] | str]], list[dict[str, str]]]:
    """
    Parse the input directory.

    Parameters
    ----------
    input_directory : Path
        Path to the input directory.

    Returns
    -------
    tuple[list[dict[str, dict[str, str] | str]], list[dict[str, str]]]
        The weekly files (code and reflections) and the references.
    """
    weeks_path = input_directory / "weeks"
    weeks = parse_weeks_directory(weeks_path)

    references_path = input_directory / "references.yaml"
    references_dictionary = load_yaml(references_path)
    references = references_dictionary["references"]

    return weeks, references
