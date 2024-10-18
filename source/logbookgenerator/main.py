"""main.py: Called when the package is ran as a script."""

from logging import shutdown as shutdown_logging

from .computation.context_generation import create_logbook_contexts
from .computation.parsing import parse_input_directory
from .config.constants import Constants
from .interface.command_line import command_line_interface
from .logs.setup_logging import setup_logging
from .utilities.file_handling import load_yaml
from .utilities.validation import validate_input_directory


def main() -> None:
    """
    Overall control flow of the application.

    Notes
    -----
    This function is the entry point for the application, so only really
    contains overall control flow logic. The actual work is done in the
    other modules.
    """
    # Get the arguments from the command line
    user_arguments = command_line_interface()

    # Setup logging
    setup_logging(
        user_arguments["log_output_location"],
        console_logging_level=(
            "DEBUG" if user_arguments["verbose"] else Constants.LOGGING_LEVEL_CONSOLE_DEFAULT
        ),
    )

    # Validate the structure of the input directory
    validate_input_directory(user_arguments["input_directory"])

    # Load the configuration file
    config = load_yaml(user_arguments["config_file"])

    # Parse through the input directory
    weekly_files, references = parse_input_directory(user_arguments["input_directory"])

    # Create the template contexts
    logbook_contexts = create_logbook_contexts(config, weekly_files, references)

    # Create the logbook
    # create_logbook(logbook_contexts, config)

    shutdown_logging()


if __name__ == "__main__":
    main()
