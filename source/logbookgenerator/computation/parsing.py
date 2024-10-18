"""parsing.py: Contains the functions for parsing the input directory."""

import os
from pathlib import Path

from ..utilities.file_handling import load_yaml
from . import logger

logger = logger.getChild(__name__)


def parse_weeks_directory(weeks_directory: Path) -> list[dict[str, str]]:
    """
    Parse the weeks directory.

    Parameters
    ----------
    weeks_directory : Path
        Path to the weeks directory.

    Returns
    -------
    list[dict[str, str]]
        The CPP files.
    """
    weeks_files: list[dict[str, str]] = []

    weeks = sorted(os.listdir(weeks_directory))

    for week in weeks:
        week_files: dict[str, str] = {}
        week_path = weeks_directory / week

        for file_path in week_path.glob("*.cpp"):
            with open(file_path) as file:
                week_files[file_path.stem] = file.read()

        weeks_files.append(week_files)

    return weeks_files


def parse_input_directory(
    input_directory: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Parse the input directory.

    Parameters
    ----------
    input_directory : Path
        Path to the input directory.

    Returns
    -------
    tuple[list[dict[str, str]], list[dict[str, str]]]
        The CPP files and the references.
    """
    weeks_path = input_directory / "weeks"
    weeks = parse_weeks_directory(weeks_path)

    references_path = input_directory / "references.yaml"
    references_dictionary = load_yaml(references_path)
    references = references_dictionary["references"]

    return weeks, references
