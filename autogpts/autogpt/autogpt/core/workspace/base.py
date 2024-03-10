from __future__ import annotations

import abc
import logging
import os
import pathlib
import typing
from typing import Optional

if typing.TYPE_CHECKING:
    from autogpt.core.configuration import AgentConfiguration


class Workspace(abc.ABC):
    """The workspace is the root directory for all generated files.

    The workspace is responsible for creating the root directory and
    providing a method for getting the full path to an item in the
    workspace.

    """

    def __init__(self, root_directory: Optional[pathlib.Path] = None):
        self.logger = logging.getLogger(__name__)
        self.root_directory = root_directory or pathlib.Path().absolute()

    @property
    def root(self) -> pathlib.Path:
        """The root directory of the workspace."""
        return self.root_directory

    @property
    def restrict_to_workspace(self) -> bool:
        """Whether to restrict generated paths to the workspace."""
        return True

    @staticmethod
    @abc.abstractmethod
    def setup_workspace(
        configuration: AgentConfiguration, logger: logging.Logger
    ) -> pathlib.Path:
        """Create the workspace root directory and set up all initial content.

        Parameters
        ----------
        configuration
            The Agent's configuration.
        logger
            The Agent's logger.

        Returns
        -------
        pathlib.Path
            The path to the workspace root directory.

        """
        workspace_root = pathlib.Path(configuration.workspace_root)
        workspace_root.mkdir(parents=True, exist_ok=True)
        return workspace_root

    def get_path(self, relative_path: str | pathlib.Path) -> pathlib.Path:
        """Get the full path for an item in the workspace.

        Parameters
        ----------
        relative_path
            The path to the item relative to the workspace root.

        Returns
        -------
        pathlib.Path
            The full path to the item.

        """
        full_path = pathlib.Path(self.root) / relative_path
        return full_path

    def joinpath(self, *args) -> pathlib.Path:
        """Join paths and return a new path object.

        This method is similar to pathlib.Path.joinpath(), but it ensures
        that the resulting path is within the workspace.

        """
        path = pathlib.Path(*args)
        if self.restrict_to_workspace and not (
            self.root / path
        ).is_relative_to(self.root):
            raise ValueError(f"Path {
