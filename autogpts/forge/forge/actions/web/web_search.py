from __future__ import annotations

import json
import time
from itertools import islice

from duckduckgo_search import DDGS  # Import the DuckDuckGo search module

from ..registry import action  # Import the action module from the registry package

# Define the maximum number of attempts for the web search
DUCKDUCKGO_MAX_ATTEMPTS = 3


@action(
    name="web_search",  # Name of the action
    description="Searches the web",  # Description of the action
    parameters=[
        {
            "name": "query",  # Name of the parameter
            "description": "The search query",  # Description of the parameter
            "type": "string",  # Type of the parameter
            "required": True,  # Whether the parameter is required or not
        }
    ],
    output_type="list[str]",  # Output type of the action
)
async def web_search(agent, task_id: str, query: str) -> str:
    """Return the results of a Google search

    Args:
        query (str): The search query.  # Description of the query parameter
        num_results (int): The number of results to return.  # Description of the num\_results parameter

    Returns:
        str: The results of the search.  # Description of the return value
    """
    search_results = []  # Initialize the search results list
    attempts = 0  # Initialize the number of attempts
    num_results = 8  # Set the number of results to return

    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        if not query:  # Check if the query is empty
            return json.dumps(search_results)  # Return the search results if the query is empty

        results = DDGS().text(query)  # Perform the web search
        search_results = list(islice(results, num_results))  # Get the first num\_results from the results

        if search_results:  # Check if the search results are not empty
            break  # Exit the loop if the search results are not empty

        time.sleep(1)  # Wait for 1 second before the next attempt
        attempts += 1  # Increment the number of attempts

    results = json.dumps(search_results, ensure_ascii=False, indent=4)  # Convert the search results to a JSON string
    return safe_google_results(results)  # Call the safe\_google\_results function to sanitize the results


def safe_google_results(results: str | list) -> str:
    """
        Return the results of a Google search in a safe format.

    Args:
        results (str | list): The search results.

    Returns:
        str: The results of the search.
    """
    if isinstance(results, list):  # Check if the results are a list
