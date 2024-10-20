"""render_context.py: Contains the logic for rendering the context into a logbook."""

from pathlib import Path
from typing import Any

import jinja2

from ..config.paths import Paths
from . import logger

logger = logger.getChild(__name__)


def render_template(template_path: Path, context: dict[str, Any]) -> str:
    """
    Render the template with the context.

    Parameters
    ----------
    template_path : Path
        Path to the template.
    context : dict[str, Any]
        Context to render the template.

    Returns
    -------
    str
        Rendered template.
    """
    with open(template_path) as file:
        template = jinja2.Template(file.read())

    return template.render(context)


def create_logbook(logbook_contexts: dict[str, Any]) -> str:
    """
    Create the logbook from the contexts.

    Parameters
    ----------
    logbook_contexts : dict
        The contexts to render into the logbook.

    Notes
    -----
    This function renders each part of the logbook and then combines them into
    the final markdown logbook.
    """
    logger.debug("Rendering the logbook.")
    logbook_markdown = ""

    logger.debug("Rendering the logbook cover.")
    logbook_markdown += (
        render_template(
            Paths.TEMPLATES_PATH / "cover.md.j2",
            logbook_contexts["cover"],
        )
        + "\n"
    )

    logger.debug("Rendering the logbook table of contents.")
    logbook_markdown += (
        render_template(
            Paths.TEMPLATES_PATH / "contents.md.j2",
            logbook_contexts["weeks"],
        )
        + "\\newpage"
    )

    logger.debug("Rendering the logbook weekly entries.")
    for week in logbook_contexts["weeks"]["weeks"]:
        logbook_markdown += (
            render_template(
                Paths.TEMPLATES_PATH / "week.md.j2",
                week,
            )
            + "\\newpage"
        )

    logger.debug("Rendering the logbook references.")
    logbook_markdown += render_template(
        Paths.TEMPLATES_PATH / "references.md.j2",
        logbook_contexts["references"],
    )

    return logbook_markdown
