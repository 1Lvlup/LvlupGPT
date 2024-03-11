"""
AGBenchmark's test discovery endpoint for Pytest.

This module is picked up by Pytest's *_test.py file matching pattern, and all challenge
classes in the module that conform to the `Test*` pattern are collected.
"""

import importlib
import logging
from itertools import chain
from typing import List, Dict

# Initialize a logger for this module
logger = logging.getLogger(__name__)

# Define a dictionary to store the category of each challenge
DATA_CATEGORY: Dict[str, str] = {}

def load_challenges() -> List[object]:
    """
    Load all challenges and return them as a list of classes.

    This function loads all available challenges from both the built-in and webarena modules,
    and returns them as a list of classes. It also sets an attribute for each challenge
    class in this module's namespace, and updates the `DATA_CATEGORY` dictionary with the
    category of each challenge.
    """
    challenges = chain(load_builtin_challenges(), load_webarena_challenges())
    for challenge in challenges:
        # Import this module to set the challenge class as an attribute
        module = importlib.import_module(__name__)
        setattr(module, challenge.__name__, challenge)
        # Update the `DATA_CATEGORY` dictionary with the challenge's category
        DATA_CATEGORY[challenge.info.name] = challenge.info.category[0].value
    # Return the list of challenge classes
    return list(challenges)

# Call the `load_challenges` function to load all challenges
load_challenges()
