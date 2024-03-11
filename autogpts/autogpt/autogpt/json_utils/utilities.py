"""Utilities for the json_fixes package."""

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)  # Initialize the logger for this module


def extract_dict_from_response(response_content: str) -> dict[str, Any]:
    """
    Extract a dictionary from a JSON response string.

    This function searches for JSON content within the response_content string,
    which may be wrapped in a code block (```json or ```JSON). If found, the
    JSON content is extracted and loaded into a dictionary. If no JSON content
    is found, a ValueError is raised.

    Args:
        response_content (str): The response content to extract the dictionary from.

    Returns:
        dict[str, Any]: The extracted dictionary from the JSON response.

    Raises:
        ValueError: If the JSON response cannot be evaluated to a dictionary.
    """
    pattern = r"```(?:json|JSON)*([\s\S]*?)```"
    match = re.search(pattern, response_content)

    if match:
        response_content = match.group(1).strip()
    else:
        # The string may contain JSON.
        json_pattern = r"{[\s\S]*}"
        match = re.search(json_pattern, response_content)

        if match:
            response_content = match.group()

    result = json.loads(response_content)
    if not isinstance(result, dict):
        raise ValueError(
            f"Response '''{response_content}''' evaluated to "
            f"non-dict value {repr(result)}"
        )
    return result


def extract_list_from_response(response_content: str) -> list[Any]:
    """
    Extract a list from a JSON response string.

    This function searches for JSON content within the response_content string,
    which may be wrapped in a code block (```json or ```JSON). If found, the
    JSON content is extracted and loaded into a list. If no JSON content
    is found, a ValueError is raised.

    Args:
        response_content (str): The response content to extract the list from.

    Returns:
        list[Any]: The extracted list from the JSON response.

    Raises:
        ValueError: If the JSON response cannot be evaluated to a list.
   
