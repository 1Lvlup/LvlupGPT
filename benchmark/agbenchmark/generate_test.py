"""
AGBenchmark's test discovery endpoint for Pytest.

This module is picked up by Pytest's *_test.py file matching pattern, and all challenge
classes in the module that conform to the `Test*` pattern are collected.
"""

import importlib
import logging
from itertools import chain
from typing import List, Dict

from agbenchmark.challenges.builtin import load_builtin_challenges
from agbenchmark.challenges.webarena import load_webarena_challenges

logger = logging.getLogger(__name__)

DATA_CATEGORY: Dict[str, str] = {}

def load_challenges() -> List[object]:
    """Load all challenges and return them as a list of classes."""
    challenges = chain(load_builtin_challenges(), load_webarena_challenges())
    for challenge in challenges:
        module = importlib.import_module(__name__)
        setattr(module, challenge.__name__, challenge)
        DATA_CATEGORY[challenge.info.name] = challenge.info.category[0].value
    return list(challenges)

load_challenges()
