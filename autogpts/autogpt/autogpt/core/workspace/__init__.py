"""The workspace module is the central hub for the Agent's on-disk resources.
It provides a way to manage and interact with the Agent's files and directories.

This module includes the following classes:
- Workspace: The base class for managing a workspace. Provides basic functionality for creating, listing, and deleting directories and files.
- SimpleWorkspace: A concrete implementation of the Workspace class that uses the filesystem directly to manage resources.
- WorkspaceSettings: A class for managing settings related to the workspace, such as the root directory and maximum file size.
"""
from autogpt.core.workspace.base import Workspace  # Base class for managing a workspace
from autogpt.core.workspace.simple import SimpleWorkspace, WorkspaceSettings  # Concrete implementation of Workspace and settings management

# Export the SimpleWorkspace, Workspace, and WorkspaceSettings classes for use in other modules
__all__ = [
    "SimpleWorkspace",
    "Workspace",
    "WorkspaceSettings",
]
