import enum  # Importing enum module to define custom enumerated types
import logging  # Importing logging module to log messages and errors
import math  # Importing math module for mathematical operations
import os  # Importing os module for operating system dependent functionality
import re  # Importing re module for regular expression operations
import signal  # Importing signal module for handling signals
import sys  # Importing sys module for system-specific parameters and functions
import typing as tp  # Importing typing module for type hints
from pathlib import Path  # Importing Path class from pathlib module for file and directory path operations
from typing import Any, Callable, Coroutine, Optional  # Importing various types from typing module

# Importing specific modules and functions from other packages and modules
from colorama import Fore, Style  # Importing Fore and Style classes from colorama module for text coloring
from forge.sdk.db import AgentDB  # Importing AgentDB class from forge.sdk.db module for managing agent databases

# Importing type hints for type checking
if tp.TYPE_CHECKING:
    from autogpt.agents.agent import Agent  # Importing Agent class from autogpt.agents.agent module for agent-related functionality

# Importing various functions, classes, and modules from autogpt package
from autogpt.agent_factory.configurators import configure_agent_with_state, create_agent  # Importing functions for configuring and creating agents
from autogpt.agent_factory.profile_generator import generate_agent_profile_for_task  # Importing function for generating agent profiles for tasks
from autogpt.agent_manager import AgentManager  # Importing AgentManager class for managing agents
from autogpt.agents import AgentThoughts, CommandArgs, CommandName  # Importing various classes and enums from autogpt.agents module
from autogpt.agents.utils.exceptions import AgentTerminated, InvalidAgentResponseError  # Importing custom exceptions
from autogpt.config import (  # Importing various configuration-related modules and functions
    AIDirectives,
    AIProfile,
    Config,
    ConfigBuilder,
    assert_config_has_openai_api_key,
)
from autogpt.core.resource.model_providers.openai import OpenAIProvider  # Importing OpenAIProvider class for OpenAI model provider
from autogpt.core.runner.client_lib.utils import coroutine  # Importing coroutine function for defining coroutines
from autogpt.logs.config import configure_chat_plugins, configure_logging  # Importing functions for configuring logging and chat plugins

