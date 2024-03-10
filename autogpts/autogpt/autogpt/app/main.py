import enum
import logging
import math
import os
import re
import signal
import sys
import typing as tp
from pathlib import Path
from typing import Any, Callable, Coroutine, Optional

import colorama
from colorama import Fore, Style
from forge.sdk.db import AgentDB

if tp.TYPE_CHECKING:
    from autogpt.agents.agent import Agent

from autogpt.agent_factory.configurators import configure_agent_with_state, create_agent
from autogpt.agent_factory.profile_generator import generate_agent_profile_for_task
from autogpt.agent_manager import AgentManager
from autogpt.agents import AgentThoughts, CommandArgs, CommandName
from autogpt.agents.utils.exceptions import AgentTerminated, InvalidAgentResponseError
from autogpt.config import (
    AIDirectives,
    AIProfile,
    Config,
    ConfigBuilder,
    assert_config_has_openai_api_key,
)
from autogpt.core.resource.model_providers.openai import OpenAIProvider
from autogpt.core.runner.client_lib.utils import coroutine
from autogpt.logs.config import configure_chat_plugins, configure_logging
from autogpt.logs.helpers import print_attribute, speak
from autogpt.plugins import scan_plugins
from scripts.install_plugin_deps import install_plugin_dependencies

from .configurator import apply_overrides_to_config
from .setup import apply_overrides_to_ai_settings, interactively_revise_ai_settings
from .spinner import Spinner
from .utils import (
    clean_input,
    get_legal_warning,
    markdown_to_ansi_style,
    print_git_branch_info,
    print_motd,
    print_python_version_info,
)

