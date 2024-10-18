"""command_line.py: Command line interface for the application."""

import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from os import getcwd
from pathlib import Path
from typing import Any

import questionary

from ..config.constants import Constants
from ..utilities.validation import (
    validate_date,
    validate_student_id,
    validate_year,
)
from . import __version__

logger = logging.getLogger(__name__)


def build_config_file() -> Path:
    """
    Builds the YAML config file with user input.

    Returns
    -------
    Path
        The path to the configuration file.

    Notes
    -----
    The generated YAML file will have the following structure:
    ```
    ---
    module:
        code: <module_code>
        name: <module_name>
        semester: <module_semester>
        year: <module_year>
    statement:
        text: <statement_text>
    student:
        id: <student_id>
        name: <student_name>
    university:
        department: <university_department>
        name: <university_name>
        start: <university_start>
    ```
    """
    print("No configuration file found, please provide the following information...")

    # Get user input
    module_code = questionary.text("Module code:", default=Constants.DEFAULT_MODULE_CODE).ask()
    module_name = questionary.text("Module name:", default=Constants.DEFAULT_MODULE_NAME).ask()
    module_semester = questionary.select(
        "Module semester:", choices=Constants.SEMESTER_CHOICES
    ).ask()
    module_year = questionary.text("Module year:", validate=validate_year).ask()

    statement_text = questionary.text(
        "Statement text:", default=Constants.DEFAULT_STATEMENT_TEXT
    ).ask()

    student_id = questionary.text("Student ID:", validate=validate_student_id).ask()
    student_name = questionary.text("Student name:").ask()

    university_department = questionary.text(
        "University department:", default=Constants.DEFAULT_UNIVERSITY_DEPARTMENT
    ).ask()
    university_name = questionary.text(
        "University name:", default=Constants.DEFAULT_UNIVERSITY_NAME
    ).ask()
    university_start = questionary.text(
        "University start date (YYYY-MM-DD):", validate=validate_date
    ).ask()

    # Build config file path
    config_file_path = Path(getcwd()) / "config.yaml"

    # Create the config file if it doesn't exist
    if not config_file_path.exists():
        config_file_path.touch()

    # Write the configuration to the file
    with open(config_file_path, "w") as config_file:
        config_file.write(
            f"---\n"
            f"module:\n"
            f"    code: {module_code}\n"
            f"    name: {module_name}\n"
            f"    semester: {module_semester}\n"
            f"    year: {module_year}\n"
            f"statement:\n"
            f"    text: {statement_text}\n"
            f"student:\n"
            f"    id: {student_id}\n"
            f"    name: {student_name}\n"
            f"university:\n"
            f"    department: {university_department}\n"
            f"    name: {university_name}\n"
            f"    start: {university_start}\n"
        )

    print(f"Configuration file saved to {config_file_path}")

    return config_file_path


def command_line_interface() -> dict[str, Any]:
    """
    Takes arguments from the command line and returns them as a dictionary.

    Returns
    -------
    dict[str, Any]
        A dictionary containing the arguments passed to the application.
    """
    argparser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )  # Automatically generates help messages

    argparser.add_argument(
        "--log_output_location",
        "-l",
        action="store",
        type=str,
        required=False,
        default=Constants.DEFAULT_LOG_SAVE_PATH,
        help="Path to save the log file, should end in .txt.",
    )  # Path to save the log file

    argparser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        required=False,
        help="Increase logging verbosity.",
    )  # Increase logging verbosity

    argparser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )  # Display the version number

    argparser.add_argument(
        "--config_file",
        "-c",
        action="store",
        type=str,
        required=False,
        default=build_config_file(),
        help="Path to the YAML configuration file.",
    )  # Path to the configuration file

    argparser.add_argument(
        "--input_directory",
        "-i",
        action="store",
        type=str,
        required=False,
        default=getcwd(),
        help="Path to the directory containing the input files.",
    )  # Path to the input directory

    parsed_args = argparser.parse_args()

    # Create a dictionary to return the parsed arguments
    arguments: dict[str, Any] = {
        "log_output_location": Path(parsed_args.log_output_location),
        "verbose": parsed_args.verbose,
        "config_file": Path(parsed_args.config_file),
        "input_directory": Path(parsed_args.input_directory),
    }

    logger.debug(f"Arguments: {arguments}")

    return arguments
