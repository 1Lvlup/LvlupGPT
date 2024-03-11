from __future__ import annotations  # Allows using the class name in type hints before it is defined

from typing import TYPE_CHECKING  # Used to specify type hints that only apply during type checking

if TYPE_CHECKING:
    from pathlib import Path  # Used for handling file paths

    from ..base import BaseAgent, Config  # Base Agent and Configuration classes

from autogpt.file_workspace import (  # Importing the FileWorkspace module
    FileWorkspace,
    FileWorkspaceBackendName,
    get_workspace,
)

from ..base import AgentFileManager, BaseAgentSettings  # Importing AgentFileManager and BaseAgentSettings classes


