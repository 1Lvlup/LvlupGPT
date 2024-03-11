"""
The GCSWorkspace class provides an interface for interacting with a file workspace, and
stores the files in a Google Cloud Storage bucket.
"""
from __future__ import annotations

import inspect
import logging
from io import IOBase
from pathlib import Path

from google.cloud import storage
from google.cloud.exceptions import NotFound

from autogpt.core.configuration.schema import UserConfigurable

logger = logging.getLogger(__name__)


class GCSFileWorkspaceConfiguration(FileWorkspaceConfiguration):
    """A class representing the configuration for a Google Cloud Storage file workspace.

    Attributes:
        bucket (str): The name of the Google Cloud Storage bucket to use for the workspace.
    """
    bucket: str = UserConfigurable("autogpt", from_env="WORKSPACE_STORAGE_BUCKET")


class GCSFileWorkspace(FileWorkspace):
    """A class that represents a Google Cloud Storage workspace.

    Attributes:
        _bucket (storage.Bucket): The Google Cloud Storage bucket used for the workspace.
    """

    def __init__(self, config: GCSFileWorkspaceConfiguration):
        """Initialize the GCSFileWorkspace instance.

        Args:
            config (GCSFileWorkspaceConfiguration): The configuration for the workspace.
        """
        self._bucket_name = config.bucket
        self._root = config.root
        assert self._root.is_absolute()

        self._gcs = storage.Client()
        super().__init__()

    @property
    def root(self) -> Path:
        """Return the root directory of the file workspace.

        Returns:
            Path: The root directory of the file workspace.
        """
        return self._root

    @property
    def restrict_to_root(self) -> bool:
        """Return whether to restrict generated paths to the root.

        Returns:
            bool: True if paths should be restricted to the root, False otherwise.
        """
        return True

    def initialize(self) -> None:
        """Initialize the workspace by creating or getting the Google Cloud Storage bucket.
        """
        logger.debug(f"Initializing {repr(self)}...")
        try:
            self._bucket = self._gcs.get_bucket(self._bucket_name)
        except NotFound:
            logger.info(f"Bucket '{self._bucket_name}' does not exist; creating it...")
            self._bucket = self._gcs.create_bucket(self._bucket_name)

    def get_path(self, relative_path: str | Path) -> Path:
        """Return the Path object for the given relative path, relative to the root.

        Args:
            relative_path (str or Path): The relative path to the file or directory.

        Returns:
            Path: The Path object for the given relative path.
        """
        return super().get_path(relative_path).relative_to("/")

    def _get_blob(self, path: str | Path) -> storage.Blob:
        """Return the Google Cloud Storage Blob object for the given path.

        Args:
            path (str or Path): The path to the file or directory.

        Returns:
            storage.Blob: The Google Cloud Storage Blob object for the given path.
        """
        path = self.get_path(path)
        return self._bucket.blob(str(path))

    def open_file(self, path: str | Path, binary: bool = False) -> IOBase:
        """Open a file in the workspace.

        Args:
            path (str or Path): The path to the file.
            binary (bool): Whether to open the file in binary mode.

        Returns:
            IOBase: A file object that can be used to read or write to the file.
        """
        blob = self._get_blob(path)
        blob.reload()  # pin revision number to prevent version mixing while reading
        return blob.open("rb" if binary else "r")

    def read_file(self, path: str | Path, binary: bool = False) -> str | bytes:
        """Read the contents of a file in the workspace.

        Args:
            path (str or Path): The path to the file.
            binary (bool): Whether to read the file in binary mode.

        Returns:
            str or bytes: The contents of the file.
        """
        return self.open_file(path, binary).read()

    async def write_file(self, path: str | Path, content: str | bytes) -> None:
        """Write the given content to a file in the workspace.

        Args:
            path (str or Path): The path to the file.
            content (str or bytes): The content to write to the file.

        """
        blob = self._get_blob(path)

        blob.upload_from_string(
            data=content,
            content_type=(
                "text/plain"
                if type(content) is str
                # TODO: get MIME type from file extension or binary content
                else "application/octet-stream"
            ),
        )

        if self.on_write_file:
            path = Path(path)
            if path.is_absolute():
                path = path.relative_to(self.root)
            res = self.on_write_file(path)
            if inspect.isawaitable(res):
                await res

    def list(self, path: str | Path = ".") -> list[Path]:
        """List all files (recursively) in a directory in the workspace.

        Args:
            path (str or Path, optional): The path to the directory. Defaults to ".".

        Returns:
            list[Path]: A list of Path objects for the files in the directory.
        """
        path = self.get_path(path)
        return [
            Path(blob.name).relative_to(path)
            for blob in self._bucket.list_blobs(
                prefix=f"{path}/" if path != Path(".") else None
            )
        ]

    def delete_file(self, path: str | Path) -> None:
        """Delete a file in the workspace.

       
