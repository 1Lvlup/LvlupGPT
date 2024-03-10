import glob
import json
import logging
from pathlib import Path
from typing import Set

import pkg_resources  # for importing modules from package directory

from .base import BaseChallenge, ChallengeInfo
from .builtin import BuiltinChallenge, OPTIONAL_CATEGORIES

logger = logging.getLogger(__name__)


def get_challenge_from_source_uri(source_uri: str) -> type[BaseChallenge]:
    module_name, _ = source_uri.split("/", 1)

    try:
        challenge_module = pkg_resources.import_module(f"..{module_name}", __name__)
    except ModuleNotFoundError:
        raise ValueError(f"Cannot resolve source_uri '{source_uri}'")

    try:
        return getattr(challenge_module, "Challenge")
    except AttributeError:
        raise ValueError(f"Invalid source_uri '{source_uri}'. Module does not define a Challenge class.")


def get_unique_categories() -> Set[str]:
    """
    Reads all challenge spec files and returns a set of all their categories.
    """
    categories: Set[str] = set()

    challenges_dir = Path(__file__).parent
    glob_path = f"{challenges_dir}/**/data.json"

    for data_file in glob.glob(glob_path, recursive=True):
        with open(data_file, "r") as f:
            try:
                challenge_data = json.load(f)
                categories.update(challenge_data.get("category", []))
            except json.JSONDecodeError as e:
                logger.error(f"Error: {data_file} is not a valid JSON file. Error: {e}")
                continue
            except IOError as e:
                logger.error(f"IOError: file could not be read: {data_file}. Error: {e}")
                continue

    return categories


__all__ = [
    "BaseChallenge",
    "ChallengeInfo",
    "get_unique_categories",
    "OPTIONAL_CATEGORIES",
]
