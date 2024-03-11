"""Commands to interact with the user"""

from __future__ import annotations  # Allows using class names in type hints before they are defined

import asyncio
from typing import Any

from autogpt.agents.agent import Agent  # Base class for agents
from autogpt.app.utils import clean_input  # Utility function for cleaning user input
from autogpt.command_decorator import command  # Decorator for defining commands
from autogpt.core.utils.json_schema import JSONSchema  # Class for defining JSON schemas

# Command metadata
COMMAND_CATEGORY = "user_interaction"
COMMAND_CATEGORY_TITLE = "User Interaction"


@command(
    "ask_user",  # Command name
    (
        "If you need more details or information regarding the given goals,"
        " you can ask the user for input"
    ),  # Command description
    {
        "question": JSONSchema(
            type=JSONSchema.Type.STRING,  # The question should be a string
            description="The question or prompt to the user",
            required=True,  # The question is required
        )
    },
    enabled=lambda config: not config.noninteractive_mode,  # Enable the command if not in non-interactive mode
)
async def ask_user(question: str, agent: Agent) -> str:
    """Ask the user a question and return their answer."""
    
    print(f"\nQ: {question}")  # Print the question to the console
    resp = await clean_input(agent.legacy_config, "A:")  # Get the user's answer and clean it up
    return f"The user's answer: '{resp}'"  # Return the user's answer as a string
