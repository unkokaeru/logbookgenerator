"""file_handling.py: Contains functions for handling files."""

from pathlib import Path
from typing import Any

import yaml

from . import logger

logger = logger.getChild(__name__)


def load_yaml(yaml_path: Path) -> dict[str, Any]:
    """
    Load the YAML file.

    Parameters
    ----------
    yaml_path : Path
        Path to the YAML file.

    Returns
    -------
    dict[str, Any]
        The YAML file as a dictionary.
    """
    with open(yaml_path) as file:
        try:
            yaml_dictionary: dict[str, Any] = yaml.safe_load(file)
            return yaml_dictionary
        except yaml.YAMLError as error:
            logger.error(f"Error loading YAML file: {error}")
            raise error
