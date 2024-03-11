import logging
import os
import shlex
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional

import docker  # Docker SDK for Python
from docker.errors import DockerException, ImageNotFound, NotFound
from docker.models.containers import Container as DockerContainer

from autogpt.agents.agent import Agent
from autogpt.agents.utils.exceptions import (
    CodeExecutionError,
    CommandExecutionError,
    InvalidArgumentError,
    OperationNotAllowedError,
)
from autogpt.command_decorator import command
from autogpt.config import Config
from autogpt.core.utils.json_schema import JSONSchema

from .decorators import sanitize_path_arg

# COMMAND_CATEGORY and COMMAND_CATEGORY_TITLE are used for command categorization
COMMAND_CATEGORY = "execute_code"
COMMAND_CATEGORY_TITLE = "Execute Code"

logger = logging.getLogger(__name__)

ALLOWLIST_CONTROL = "allowlist"
DENYLIST_CONTROL = "denylist"


def we_are_running_in_a_docker_container() -> bool:
    """Check if we are running in a Docker container

    Returns:
        bool: True if we are running in a Docker container, False otherwise
    """
    return os.path.exists("/.dockerenv")


def is_docker_available() -> bool:
    """Check if Docker is available

    Returns:
        bool: True if Docker is available, False otherwise"""
    try:
        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False


@command(
    "execute_python_code",
    "Executes the given Python code inside a single-use Docker container"
    " with access to your workspace folder",
    {
        "code": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The Python code to run",
            required=True,
        ),
    },
    disabled_reason="To execute python code agent "
    "must be running in a Docker container or "
    "Docker must be available on the system.",
    available=we_are_running_in_a_docker_container() or is_docker_available(),
)
def execute_python_code(code: str, agent: Agent) -> str:
    """
    Create and execute a Python file in a Docker container and return the STDOUT of the
    executed code.

    If the code generates any data that needs to be captured, use a print statement.

    Args:
        code (str): The Python code to run.
        agent (Agent): The Agent executing the command.

    Returns:
        str: The STDOUT captured from the code when it ran.
    """
    # Create a temporary file with the provided code
    with NamedTemporaryFile(
        "w", dir=agent.workspace.root, suffix=".py", encoding="utf-8"
    ) as tmp_code_file:
        tmp_code_file.write(code)
        tmp_code_file.flush()

        try:
            # Execute the Python file in the Docker container
            return execute_python_file(tmp_code_file.name, agent)  # type: ignore
        except Exception as e:
            # Raise a CommandExecutionError if any exception occurs
            raise CommandExecutionError(*e.args)


@command(
    "execute_python_file",
    "Execute an existing Python file inside a single-use Docker container"
    " with access to your workspace folder",
    {
        "filename": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The name of the file to execute",
            required=True,
        ),
        "args": JSONSchema(
            type=JSONSchema.Type.ARRAY,
            description="The (command line) arguments to pass to the script",
            required=False,
            items=JSONSchema(type=JSONSchema.Type.STRING),
        ),
    },
    disabled_reason="To execute python code agent "
    "must be running in a Docker container or "
    "Docker must be available on the system.",
    available=we_are_running_in_a_docker_container() or is_docker_available(),
)
@sanitize_path_arg("filename")
def execute_python_file(
    filename: Path, agent: Agent, args: Optional[List[str]] = []
) -> str:
    """Execute a Python file in a Docker container and return the output

    Args:
        filename (Path): The name of the file to execute
        args (list, optional): The arguments with which to run the python script

    Returns:
        str: The output of the file
    """
    logger.info(
        f"Executing python file '{filename}' "
        f"in working directory '{agent.workspace.root}'"
    )

    if isinstance(args, str):
        args = args.split()  # Convert space-separated string to a list

    if not filename.suffix == ".py":
        # Raise an InvalidArgumentError if the file is not a .py file
        raise InvalidArgumentError("Invalid file type. Only .py files are allowed.")

    file_path = filename
    if not file_path.is_file():
        # Raise a FileNotFoundError if the file does not exist
        raise FileNotFoundError(
            f"python: can't open file '{filename}': [Errno 2] No such file or directory"
        )

    if we_are_running_in_a_docker_container():
        logger.debug(
            "AutoGPT is running in a Docker container; "
            f"executing {file_path} directly..."
        )
        result = subprocess.run(
            ["python", "-B", str(file_path)] + args,
            capture_output=True,
            encoding="utf8",
            cwd=str(agent.workspace.root),
        )

