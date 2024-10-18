"""context_generation.py: Contains the functions for generating the context for the logbook."""

from datetime import datetime
from typing import Any

from ..config.constants import Constants
from . import logger

logger = logger.getChild(__name__)


def generate_weeks_context(
    weekly_files: list[dict[str, dict[str, str] | str]], start_date: datetime
) -> list[dict[str, Any]]:
    """
    Generate the weeks context.

    Parameters
    ----------
    weekly_files: list[dict[str, dict[str, str] | str]]
        The weekly files, containing the CPP files and reflections.
    start_date : datetime
        The start date of the university.

    Returns
    -------
    list[dict[str, Any]]
        The weeks context.
    """
    return []


def generate_logbook_contexts(
    config: dict[str, Any],
    weekly_files: list[dict[str, dict[str, str] | str]],
    references: list[dict[str, str]],
) -> dict[str, Any]:
    """
    Generate the contexts for the logbook.

    Parameters
    ----------
    config : dict[str, Any]
        The configuration file.
    weekly_files: list[dict[str, dict[str, str] | str]]
        The weekly files, containing the CPP files and reflections.
    references : list[dict[str, str]]
        The references.

    Returns
    -------
    dict[str, Any]
        The logbook contexts.
    """
    logbook_contexts: dict[str, Any] = {}

    logbook_contexts["cover"] = config

    start_date = datetime.strptime(
        config["university"]["start"],
        Constants.DATE_FORMAT,
    )
    logbook_contexts["weeks"] = generate_weeks_context(weekly_files, start_date)

    logbook_contexts["references"] = references

    return logbook_contexts
