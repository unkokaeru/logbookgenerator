"""code_processing.py: Contains the functions for processing the code files."""

import re

from ..config.constants import Constants
from . import logger
from .comment_extraction import (
    extract_block_comment,
    extract_comment_content,
    extract_comment_id,
)

logger = logger.getChild(__name__)


def process_inline_comment(
    comment_line: str,
    code_lines: list[str],
    task_comments: dict[str, list[tuple[str, str]]],
) -> tuple[str, list[str], dict[str, list[tuple[str, str]]]]:
    """
    Process an inline comment to extract answer comments and related code.

    Parameters
    ----------
    comment_line : str
        The comment line.
    code_lines : list[str]
        The code lines.
    task_comments : dict[str, list[tuple[str, str]]]
        A dictionary where keys are task identifiers and values are lists of tuples
        containing comments and associated code.

    Returns
    -------
    tuple[str, list[str], dict[str, list[tuple[str, str]]]]
        The updated comment line, code lines, and task comments.

    Raises
    ------
    ValueError
        If the inline comment is invalid.
    """
    match = re.match(
        Constants.INLINE_ANSWER_COMMENT, comment_line.strip(f"{Constants.INLINE_COMMENT_START} ")
    )

    if not match:
        raise ValueError(f"Invalid inline comment: {comment_line}")

    comment_id = f"task_{match.group(1)}_{match.group(2)}"
    comment_content = match.group(3).strip()

    task_comments.setdefault(comment_id, [])
    task_comments[comment_id].append((comment_content, "\n".join(code_lines)))

    return "", [], task_comments


def process_block_comment(
    comment_lines: list[str],
    code_lines: list[str],
    task_comments: dict[str, list[tuple[str, str]]],
) -> tuple[list[str], list[str], dict[str, list[tuple[str, str]]]]:
    """
    Process a block comment to extract answer comments and related code.

    Parameters
    ----------
    comment_lines : list[str]
        The comment lines.
    code_lines : list[str]
        The code lines.
    task_comments : dict[str, list[tuple[str, str]]]
        A dictionary where keys are task identifiers and values are lists of tuples
        containing comments and associated code.

    Returns
    -------
    tuple[list[str], list[str], dict[str, list[tuple[str, str]]]]
        The updated comment lines, code lines, and task comments.

    Raises
    ------
    ValueError
        If the block comment is empty.
    """
    if not comment_lines:
        raise ValueError("Block comment is empty.")

    if comment_lines[0].startswith(Constants.ANSWER_KEYWORD):
        comment_id = extract_comment_id(comment_lines[0])
        comment_content = extract_comment_content(comment_lines)

        task_comments.setdefault(comment_id, [])
        task_comments[comment_id].append((comment_content, "\n".join(code_lines)))

    return [], [], task_comments


def process_code_comments(code_lines: list[str]) -> dict[str, list[tuple[str, str]]] | str:
    """
    Process the C++ code to extract answer comments and related code. If the code
    contains no answer comments, the function returns the entire code as a string.

    Parameters
    ----------
    code_lines : list[str]
        The code lines.

    Returns
    -------
    dict[str, list[tuple[str, str]]] | str
        A dictionary where keys are task identifiers and values are lists of tuples
        containing comments and associated code.
    """
    task_comments: dict[str, list[tuple[str, str]]] = {}
    current_code_lines: list[str] = []
    line_number = 0

    while line_number < len(code_lines):
        line = code_lines[line_number].strip()

        if line.startswith(Constants.BLOCK_COMMENT_START):
            line_number += 1  # Skip the block comment start line
            current_comment_lines, line_number = extract_block_comment(code_lines, line_number)
            current_comment_lines, current_code_lines, task_comments = process_block_comment(
                current_comment_lines, current_code_lines, task_comments
            )
        elif line.startswith(Constants.INLINE_COMMENT_START):
            line, current_code_lines, task_comments = process_inline_comment(
                line, current_code_lines, task_comments
            )
        else:
            current_code_lines.append(line)

        line_number += 1

    if task_comments:
        return task_comments

    return "\n".join(current_code_lines)
