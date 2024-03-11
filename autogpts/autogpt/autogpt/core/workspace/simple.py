import json
import logging
import typing
from pathlib import Path

from pydantic import SecretField

from autogpt.core.configuration import (
    Configurable,
    SystemConfiguration,
    SystemSettings,
    UserConfigurable,
)
from autogpt.core.workspace.base import Workspace

if typing.TYPE_CHECKING:
    # Cyclic import
    from autogpt.core.agent.simple import AgentSettings


