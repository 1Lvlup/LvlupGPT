import os
import uuid
from pathlib import Path

import pytest
import pytest_asyncio
from google.auth.exceptions import GoogleAuthError
from google.cloud import storage
from google.cloud.exceptions import NotFound

from autogpt.file_workspace.gcs import GCSFileWorkspace, GCSFileWorkspaceConfiguration

try:
    storage.Client()  # Check if Google Cloud authentication is configured
except GoogleAuthError:
    pytest.skip("Google Cloud Authentication not configured", allow_module_level=True)


@pytest.fixture(scope="module")
def gcs_bucket_name() -> str:
    """
    Generate a unique test bucket name.
    """
    return f"test-bucket-{str(uuid.uuid4())[:8]}"


@pytest.fixture(scope="module")
def gcs_workspace_uninitialized(gcs_bucket_name: str) -> GCSFileWorkspace:
    """
    Create a GCSFileWorkspace instance with an uninitialized bucket.
    """
    os.environ["WORKSPACE_STORAGE_BUCKET"] = gcs_bucket_name
    ws_config = GCSFileWorkspaceConfiguration.from_env()
    ws_config.root = Path("/workspaces/AutoGPT-some-unique-task-id")
    workspace = GCSFileWorkspace(ws_config)
    yield workspace  # type: ignore
    del os.environ["WORKSPACE_STORAGE_BUCKET"]


def test_initialize(
    gcs_bucket_name: str, gcs_workspace_uninitialized: GCSFileWorkspace
):
    """
    Test the initialization of a GCSFileWorkspace instance.
    """
    gcs = gcs_workspace_uninitialized._gcs

    # Check if the bucket doesn't exist before initialization
    with pytest.raises(NotFound):
        gcs.get_bucket(gcs_bucket_name)

    gcs_workspace_uninitialized.initialize()

    # Check if the bucket has been created after initialization
    bucket = gcs.get_bucket(gcs_bucket_name)

    # Clean up the test bucket
    bucket.delete(force=True)


@pytest.fixture(scope="module")
def gcs_workspace(gcs_workspace_uninitialized: GCSFileWorkspace) -> GCSFileWorkspace:
    """
    Initialize and return a GCSFileWorkspace instance.
    """
    (gcs_workspace := gcs_workspace_uninitialized).initialize()
    yield gcs_workspace  # type: ignore

    # Empty and delete the test bucket
    gcs_workspace._bucket.delete(force=True)


def test_workspace_bucket_name(
    gcs_workspace: GCSFileWorkspace,
    gcs_bucket_name: str,
):
    """
    Test if the workspace bucket name matches the expected bucket name.
    """
    assert gcs_workspace._bucket.name == gcs_bucket_name


NESTED_DIR = "existing/test/dir"
TEST_FILES: list[tuple[str | Path, str]] = [
    ("existing_test_file_1", "test content 1"),
    ("existing_test_file_2.txt", "test content 2"),
    (Path("existing_test_file_3"), "test content 3"),
    (Path(f"{NESTED_DIR}/test/file/4"), "test content 4"),
]


@pytest_asyncio.fixture
async def gcs_workspace_with_files(gcs_workspace: GCSFileWorkspace) -> GCSFileWorkspace:
    """
    Upload test files to the GCSFileWorkspace instance and return it.
    """
    for file_name, file_content in TEST_FILES:
        gcs_workspace._bucket.blob(
            str(gcs_workspace.get_path(file_name))
        ).upload_from_string(file_content)
    yield gcs_workspace  # type: ignore


@pytest.mark.asyncio
async def test_read_file(gcs_workspace_with_files: GCSFileWorkspace):
    """
    Test reading files from the GCSFileWorkspace instance.
    """
    for file_name, file_content in TEST_FILES:
        content = gcs_workspace_with_files.read_file(file_name)
        assert content == file_content

    with pytest.raises(NotFound):
        gcs_workspace_with_files.read_file("non_existent_file")


def test_list_files(gcs_workspace_with_files: GCSFileWorkspace):
    """
    Test listing files in the GCSFileWorkspace instance.
    """
    # List files at the root level
    assert (files := gcs_workspace_with_files.list()) == gcs_workspace_with_files.list()
    assert len(files) > 0
    assert set(files) == set(Path(file_name) for file_name, _ in TEST_FILES)

    # List files at a nested path
    assert (
        nested_files := gcs_workspace_with_files.list(NESTED_DIR)
    ) == gcs_workspace_with_files.list(NESTED_DIR)
    assert len(nested_files) > 0
    assert set(nested_files) == set(
        p.relative_to(NESTED_DIR)
        for file_name, _ in TEST_FILES
        if (p := Path(file_name)).is_relative_to(NESTED_DIR)
    )


@pytest.mark.asyncio
async def test_write_read_file(gcs_workspace: GCSFileWorkspace):
    """
    Test writing and reading files in the GCSFileWorkspace instance.
    """
    await gcs_workspace.write_file("test_file", "test_content")
    assert gcs_workspace.read_file("test_file") == "test_content"


@pytest.mark.
