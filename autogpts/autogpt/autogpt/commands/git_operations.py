"""Commands to perform Git operations"""

from pathlib import Path

from git.repo import Repo # This line imports the 'Repo' class from the 'git.repo' module, which is used for interacting with Git repositories.

from autogpt.agents.agent import Agent # This line imports the 'Agent' class from the 'autogpt.agents.agent' module, which is used to represent an agent in the Auto-GPT framework.
from autogpt.agents.utils.exceptions import CommandExecutionError # This line imports the 'CommandExecutionError' class from the 'autogpt.agents.utils.exceptions' module, which is used to raise exceptions when a command fails to execute.
from autogpt.command_decorator import command # This line imports the 'command' decorator from the 'autogpt.command_decorator' module, which is used to define a command that can be executed by the Auto-GPT framework.
from autogpt.core.utils.json_schema import JSONSchema # This line imports the 'JSONSchema' class from the 'autogpt.core.utils.json_schema' module, which is used to define JSON schemas for input validation.
from autogpt.url_utils.validators import validate_url # This line imports the 'validate_url' function from the 'autogpt.url_utils.validators' module, which is used to validate URLs.

from .decorators import sanitize_path_arg # This line imports the 'sanitize_path_arg' decorator from the 'decorators' module in the same package, which is used to sanitize file path arguments.

# Define some constants for the command category and title
COMMAND_CATEGORY = "git_operations"
COMMAND_CATEGORY_TITLE = "Git Operations"


@command(
    "clone_repository",
    "Clones a Repository",
    {
        "url": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The URL of the repository to clone",
            required=True,
        ),
        "clone_path": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The path to clone the repository to",
            required=True,
        ),
    },
    lambda config: bool(config.github_username and config.github_api_key),
    "Configure github_username and github_api_key.",
)
@sanitize_path_arg("clone_path")
@validate_url
def clone_repository(url: str, clone_path: Path, agent: Agent) -> str:
    """Clone a GitHub repository locally.

    Args:
        url (str): The URL of the repository to clone.
        clone_path (Path): The path to clone the repository to.

    Returns:
        str: The result of the clone operation.
    """
    # Split the URL into two parts and replace the username and password with the authenticated username and API key
   
