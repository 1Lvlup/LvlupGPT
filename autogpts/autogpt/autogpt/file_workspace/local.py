"""
The LocalFileWorkspace class implements a FileWorkspace that works with local files.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import IO, List

from .base import FileWorkspace, FileWorkspaceConfiguration

logger = logging.getLogger(__name__)


class LocalFileWorkspace(FileWorkspace):
    """A class that represents a file workspace."""

    def __init__(self, config: FileWorkspaceConfiguration):
        self._root = self._sanitize_path(config.root)
        self._restrict_to_root = config.restrict_to_root
        super().__init__()

    @property
    def root(self) -> Path:
        """The root directory of the file workspace."""
        return self._root

    @property
    def restrict_to_root(self) -> bool:
        """Whether to restrict generated paths to the root."""
        return self._restrict_to_root

    def initialize(self) -> None:
        self._root.mkdir(exist_ok=True, parents=True)

    def open_file(self, path: str | Path, binary: bool = False) -> IO[str | bytes]:
        """Open a file in the workspace."""
        return open(os.fspath(self._open_path(path)), "rb" if binary else "r")

    def _open_path(self, path: str | Path) -> Path:
        return self._root.joinpath(path)

    def _open_file(self, path: str | Path, mode: str = "r") -> IO[str | bytes]:
        full_path = self._open_path(path)
        return open(os.fspath(full_path), mode)

    def read_file(self, path: str | Path, binary: bool = False) -> str | bytes:
        """Read a file in the workspace."""
        with self._open_file(path, "rb" if binary else "r") as file:
            return file.read()

    async def write_file(self, path: str | Path, content: str | bytes) -> None:
        """Write to a file in the workspace."""
        with self._open_file(path, "wb" if isinstance(content, bytes) else "w") as file:
            file.write(content)

        if self.on_write_file:
            file_path = self._open_path(path)
            if file_path.is_absolute():
                file_path = file_path.relative_to(self._root)
            res = self.on_write_file(file_path)
            if inspect.isawaitable(res):
                await res

    def list(self, path: str | Path = ".") -> List[Path]:
        """List all files (recursively) in a directory in the workspace."""
        path = self._open_path(path)
        return [file for file in path.iterdir() if file.is_file()]

    def delete_file(self, path: str | Path) -> None:
        """Delete a file in the workspace."""
        full_path = self._open_path(path)
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_
