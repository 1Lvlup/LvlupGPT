import pathlib

import click
import yaml
from agent_protocol import Agent as AgentProtocol  # Import Agent class from agent_protocol module

from autogpt.core.runner.cli_web_app.server.api import task_handler  # Import task_handler function
from autogpt.core.runner.client_lib.shared_click_commands import (
    DEFAULT_SETTINGS_FILE,
    make_settings,
)
from autogpt.core.runner.client_lib.utils import coroutine  # Import coroutine decorator


