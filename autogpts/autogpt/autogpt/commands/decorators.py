import functools
import logging
import re
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

from autogpt.agents.agent import Agent  # Import Agent class from autogpt.agents.agent

P = ParamSpec("P")
T = TypeVar("T")

# Initialize a logger for this module
logger = logging.getLogger(__name__)

def sanitize_path_arg(
    arg_name: str, make_relative: bool = False
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """A decorator that sanitizes the specified path argument of a function.

    This decorator resolves the path argument to a Path object and makes it relative
    to the agent's workspace if the 'make_relative' parameter is set to True.

    Args:
        arg_name (str): The name of the path argument to sanitize.
        make_relative (bool, optional): Whether to make the sanitized path relative
            to the agent's workspace. Defaults to False.

    Returns:
        Callable[[Callable[P, T]], Callable[P, T]]: A decorator for the given function.
    """

    def decorator(func: Callable) -> Callable:
        # Get the position of the path parameter in the function's arguments
        try:
            arg_index = list(func.__annotations__.keys()).index(arg_name)
        except ValueError:
            raise TypeError(
                f"Sanitized parameter '{arg_name}' absent or not annotated"
                f" on function '{func.__name__}'"
            )

        # Get the position of the agent parameter in the function's arguments
        try:
            agent_arg_index = list(func.__annotations__.keys()).index("agent")
        except ValueError:
            raise TypeError(
                f"Parameter 'agent' absent or not annotated"
                f" on function '{func.__name__}'"
            )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Sanitizing arg '{arg_name}' on function '{func.__name__}'")

            # Get the Agent instance from the function's arguments
            agent = kwargs.get(
                "agent", len(args) > agent_arg_index and args[agent_arg_index]
            )
            if not isinstance(agent, Agent):
                raise RuntimeError("Could not get Agent from decorated command's args")

            # Sanitize the specified path argument
            given_path: str | Path | None = kwargs.get(
                arg_name, len(args) > arg_index and args[arg_index] or None
            )
            if given_path:
                if type(given_path) is str:
                    # Fix workspace path from output in docker environment
                    given_path = re.sub(r"^\/workspace", ".", given_path)

                if given_path in {"", "/", "."}:
                    sanitized_path = agent.workspace.root
                else:
                    sanitized_path = agent.workspace.get_path(given_path)

                # Make path relative if possible
                if make_relative and sanitized_path.is_relative_to(
                    agent.workspace.root
              
