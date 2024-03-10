import json
import logging
import os
import re
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, List, Optional, TypeVar, Union

import click
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

AgentName = str = os.getenv("AGENT_NAME")

logger = logging.getLogger(__name__)

T = TypeVar("T")
E = TypeVar("E", bound=Enum)


def replace_backslash(value: Union[str, List, Dict]) -> Union[str, List, Dict]:
    if isinstance(value, str):
        return re.sub(r"\\+", "/", value)  # replace one or more backslashes with a forward slash
    elif isinstance(value, list):
        return [replace_backslash(i) for i in value]
    elif isinstance(value, dict):
        return {k: replace_backslash(v) for k, v in value.items()}
    else:
        return value


def get_test_path(json_file: Union[str, Path]) -> str:
    if isinstance(json_file, str):
        json_file = Path(json_file)

    try:
        agbenchmark_index = json_file.parts.index("benchmark")
    except ValueError:
        raise ValueError("Invalid challenge location.")

    challenge_location = Path(*json_file.parts[agbenchmark_index:])

    formatted_location = replace_backslash(str(challenge_location))
    if isinstance(formatted_location, str):
        return formatted_location
    else:
        return str(challenge_location)


def get_highest_success_difficulty(
    data: Dict[str, Test], just_string: Optional[bool] = None
) -> str:
    highest_difficulty = None
    highest_difficulty_level = 0

    for test_name, test_data in data.items():
        try:
            if any(r.success for r in test_data.results):
                difficulty_str = test_data.difficulty
                if not difficulty_str:
                    continue

                try:
                    difficulty_enum = DifficultyLevel[difficulty_str.lower()]
                    difficulty_level = DIFFICULTY_MAP[difficulty_enum]

                    if difficulty_level > highest_difficulty_level:
                        highest_difficulty = difficulty_enum
                        highest_difficulty_level = difficulty_level
                except KeyError:
                    logger.warning(
                        f"Unexpected difficulty level '{difficulty_str}' "
                        f"in test '{test_name}'"
                    )
                    continue
        except Exception as e:
            logger.warning(
                "An unexpected error occurred while analyzing report. "
                "Please notify a maintainer.\n"
                f"Report data: {data}\n"
                f"Error: {e}"
            )
            logger.warning(
                "Make sure you selected the right test, no reports were generated."
            )
            break

    if highest_difficulty is not None:
        highest_difficulty_str = highest_difficulty.name  # convert enum to string
    else:
        highest_difficulty_str = ""

    if highest_difficulty_level and not just_string:
        return f"{highest_difficulty_str}: {highest_difficulty_level}"
    elif highest_difficulty_str:
        return highest_difficulty_str
    return "No successful tests"


# def get_git_commit_sha(directory: Path) -> Optional[str]:
#     # ...
#

def write_pretty_json(data, json_file):
    sorted_data = deep_sort(data)
    json_graph = json.dumps(sorted_data, indent=4)
    with open(json_file, "w") as f:
        f.write(json_graph)
        f.write("\n")


def pretty_print_model(model: BaseModel, include_header: bool = True) -> None:
    indent = ""
    if include_header:
        identifiers = []
        for attr, value in model.dict().items():
            if attr == "id" or attr.endswith("_id"):
                identifiers.append(value)
            if attr.endswith("name"):
                identifiers.append(value)
        identifiers_str = repr(identifiers) if identifiers else ""
        click.echo(f"{model.__repr_name__()}{identifiers_str}:")
        indent = " " * 2

    k_col_width = max(len(k) for k in model.dict().keys())
    for k, v in model.dict().items():
        v_fmt = repr(v)
        if v is None or v == "":
            v_fmt = click.style(v_fmt, fg="black")
        elif type(v) is bool:
            v_fmt = click.style(v_fmt, fg="green" if v else "red")
        elif type(v) is str and "\n" in v:
            v_fmt = f"\n{v}".replace(
                "\n", f"\n{indent} {click.style('|', fg='black')} "
            )
        if isinstance(v, Enum):
            v_fmt = click.style(v.value, fg="blue")
        elif type(v) is list and len(v) > 0 and isinstance(v[0], Enum):
            v_fmt = ", ".join(click.style(lv.value, fg="blue") for lv in v)
        click.echo(f"{indent}{k: <{k_col_width}}  = {v_fmt}")


def deep_sort(obj):
