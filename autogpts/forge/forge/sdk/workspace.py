import abc
import os
import typing
from pathlib import Path

from google.cloud import storage


class Workspace(abc.ABC):
    """Abstract base class for Workspace. Defines the interface for file operations in a workspace.
    """
    @abc.abstractclassmethod
    def __init__(self, base_path: str) -> None:
        """Initializes the Workspace with the base path for file operations.

        Args:
            base_path (str): The root directory or bucket name for file operations.
        """
        self.base_path = base_path

    @abc.abstractclassmethod
    def read(self, task_id: str, path: str) -> bytes:
        """Reads the file content at the given task_id and path.

        Args:
            task_id (str): The task identifier for the file.
            path (str): The file path relative to the base_path.

        Returns:
            bytes: The file content.
        """
        pass

    @abc.abstractclassmethod
    def write(self, task_id: str, path: str, data: bytes) -> None:
        """Writes the data to the file at the given task_id and path.

        Args:
            task_id (str): The task identifier for the file.
            path (str): The file path relative to the base_path.
            data (bytes): The data to write.
        """
        pass

    @abc.abstractclassmethod
    def delete(
        self, task_id: str, path: str, directory: bool = False, recursive: bool = False
    ) -> None:
        """Deletes the file or directory at the given task_id and path.

        Args:
            task_id (str): The task identifier for the file or directory.
            path (str): The file or directory path relative to the base_path.
            directory (bool): Whether the path is a directory. Defaults to False.
            recursive (bool): Whether to delete the directory recursively. Defaults to False.
        """
        pass

    @abc.abstractclassmethod
    def exists(self, task_id: str, path: str) -> bool:
        """Checks if the file or directory at the given task_id and path exists.

        Args:
            task_id (str): The task identifier for the file or directory.
            path (str): The file or directory path relative to the base_path.

        Returns:
            bool: True if the file or directory exists, False otherwise.
        """
        pass

    @abc.abstractclassmethod
    def list(self, task_id: str, path: str) -> typing.List[str]:
        """Lists the files or directories in the given task_id and path.

        Args:
            task_id (str): The task identifier for the directory.
            path (str): The directory path relative to the base_path.

        Returns:
            List[str]: A list of file or directory names in the given path.
        """
        pass


class LocalWorkspace(Workspace):
    """Workspace implementation for local file operations.
    """
    def __init__(self, base_path: str):
        """Initializes the LocalWorkspace with the base path for file operations.

        Args:
            base_path (str): The root directory for local file operations.
        """
        self.base_path = Path(base_path).resolve()

    def _resolve_path(self, task_id: str, path: str) -> Path:
        """Resolves the given task_id and path to an absolute Path.

        Args:
            task_id (str): The task identifier for the file.
            path (str): The file path relative to the base_path.

        Returns:
            Path: The absolute Path for the file.
        """
        path = str(path)
        path = path if not path.startswith("/") else path[1:]
        abs_path = (self.base_path / task_id / path).resolve()
        if not str(abs_path).startswith(str(self.base_path)):
            print("Error")
            raise ValueError(f"Directory traversal is not allowed! - {abs_path}")
        try:
            abs_path.parent.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass
        return abs_path

    def read(self, task_id: str, path: str) -> bytes:
        """Reads the file content at the given task_id and path.

        Args:
            task_id (str): The task identifier for the file.
            path (str): The file path relative to the base_path.

        Returns:
            bytes: The file content.
        """
        with open(self._resolve_path(task_id, path), "rb") as f:
            return f.read()

    def write(self, task_id: str, path: str, data: bytes) -> None:
        """Writes the data to the file at the given task_id and path.

        Args:
            task_id (str): The task identifier for the file.
            path (str): The file path relative to the base_path.
            data (bytes): The data to write.
        """
        file_path = self._resolve_path(task_id, path)
        with open(file_path, "wb") as f:
            f.write(data)

    def delete(
        self, task_id: str, path: str, directory: bool = False, recursive: bool = False
    ) -> None:
        """Deletes the file or directory at the given task_id and path.

        Args:
            task_id (str): The task identifier for the file or directory.
            path (str): The file or directory path relative to the base_path.
            directory (bool): Whether the path is a directory. Defaults to False.
            recursive (bool): Whether to delete the directory recursively. Defaults to False.
        """
        path = self.base_path / task_id / path
        resolved_path = self._resolve_path(task_id, path)
        if directory:
            if
