import os

import pytest

# Importing LocalWorkspace class from workspace.py file located in the same directory
from .workspace import LocalWorkspace

# Constants used in the test functions
TEST_BASE_PATH = "/tmp/test_workspace"  # Base path for testing
TEST_FILE_CONTENT = b"Hello World"  # Content of the test file
TEST_TASK_ID = "1234"  # Task ID for testing


# Pytest fixture to set up and clean up the test environment
@pytest.fixture
def setup_local_workspace():
    os.makedirs(TEST_BASE_PATH, exist_ok=True)  # Create base path
    yield  # Execute test functions
    os.system(f"rm -rf {TEST_BASE_PATH}")  # Clean up base path after tests


# Test function to test read, write, delete, and exists methods of LocalWorkspace
def test_local_read_write_delete_exists(setup_local_workspace):
    workspace = LocalWorkspace(TEST_BASE_PATH)  # Initialize LocalWorkspace object

    # Write a file to the workspace
    workspace.write(TEST_TASK_ID, "test_file.txt", TEST_FILE_CONTENT)

    # Check if the file exists in the workspace
    assert workspace.exists(TEST_TASK_ID, "test_file.txt")

    # Read the file from the workspace
    assert workspace.read(TEST_TASK_ID, "test_file.txt") == TEST_FILE_CONTENT

    # Delete the file from the workspace
    workspace.delete(TEST_TASK_ID, "test_file.txt")
    assert not workspace.exists(TEST_TASK_ID, "test_file.txt")


# Test function to test list method of LocalWorkspace
def test_local_list(setup_local_workspace):
    workspace = LocalWorkspace(TEST_BASE_PATH)  # Initialize LocalWorkspace object

    # Write two files to the workspace
    workspace.write(TEST_TASK_ID, "test1.txt", TEST_FILE
