import hashlib
import os
import re
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
from pytest_mock import MockerFixture

import autogpt.commands.file_operations as file_ops
from autogpt.agents.agent import Agent
from autogpt.agents.utils.exceptions import DuplicateOperationError
from autogpt.config import Config
from autogpt.file_workspace import FileWorkspace
from autogpt.memory.vector.memory_item import MemoryItem
from autogpt.memory.vector.utils import Embedding


@pytest.fixture()
def file_content():
    return "This is a test file.\n"


@pytest.fixture()
def mock_MemoryItem_from_text(
    mocker: MockerFixture, mock_embedding: Embedding, config: Config
):
    async def _mock_from_text(*args, **kwargs):
        return MemoryItem(
            raw_content=args[0],
            summary=f"Summary of content '{args[0]}'",
            chunk_summaries=[f"Summary of content '{args[0]}'"],
            chunks=[args[0]],
            e_summary=mock_embedding,
            e_chunks=[mock_embedding],
            metadata={"source_type": "test"},
        )

    mocker.patch.object(file_ops.MemoryItemFactory, "from_text", _mock_from_text)


@pytest.fixture()
def test_file_name():
    return Path("test_file.txt")


@pytest.fixture
def test_file_path(test_file_name: Path, workspace: FileWorkspace):
    return workspace.get_path(test_file_name)


@pytest.fixture()
def test_file(test_file_path: Path):
    file = open(test_file_path, "w")
    yield file
    if not file.closed:
        file.close()


@pytest.fixture()
def test_file_with_content_path(test_file: TextIOWrapper, file_content, agent: Agent):
    test_file.write(file_content)
    test_file.close()
    file_ops.log_operation(
        "write", Path(test_file.name), agent, file_ops.text_checksum(file_content)
    )
    return Path(test_file.name)


@pytest.fixture()
def test_directory(workspace: FileWorkspace):
    return workspace.get_path("test_directory")


@pytest.fixture()
def test_nested_file(workspace: FileWorkspace):
    return workspace.get_path("nested/test_file.txt")


def test_file_operations_log(test_file: TextIOWrapper):
    log_file_content = (
        "File Operation Logger\n"
        "write: path/to/file1.txt #checksum1\n"
        "write: path/to/file2.txt #checksum2\n"
        "write: path/to/file3.txt #checksum3\n"
        "append: path/to/file2.txt #checksum4\n"
        "delete: path/to/file3.txt\n"
    )
    test_file.write(log_file_content)
    test_file.close()

    expected = [
        ("write", "path/to/file1.txt", "checksum1"),
        ("write", "path/to/file2.txt", "checksum2"),
        ("write", "path/to/file3.txt", "checksum3"),
        ("append", "path/to/file2.txt", "checksum4"),
        ("delete", "path/to/file3.txt", None),
    ]
    assert list(file_ops.operations_from_log(test_file.name)) == expected


def test_file_operations_state(test_file: TextIOWrapper):
    # Prepare a fake log file
    log_file_content = (
        "File Operation Logger\n"
        "write: path/to/file1.txt #checksum1\n"
        "write: path/to/file2.txt #checksum2\n"
        "write: path/to/file3.txt #checksum3\n"
        "append: path/to/file2.txt #checksum4\n"
        "delete: path/to/file3.txt\n"
    )
    test_file.write(log_file_content)
    test_file.close()

    # Call the function and check the returned dictionary
    expected_state = {
        "path/to/file1.txt": "checksum1",
        "path/to/file2.txt": "checksum4",
    }
    assert file_ops.file_operations_state(test_file.name) == expected_state


def test_is_duplicate_operation(agent: Agent, mocker: MockerFixture):
    # Prepare a fake state dictionary for the function to use
    state = {
        "path/to/file1.txt": "checksum1",
        "path/to/file2.txt": "checksum2",
    }
    mocker.patch.object(file_ops, "file_operations_state", lambda _: state)

    # Test cases with write operations
    assert (
        file_ops.is_duplicate_operation(
            "write", Path("path/to/file1.txt"), agent, "checksum1"
        )
        is True
    )
    assert (
        file_ops.is_duplicate_operation(
            "write", Path("path/to/file1.txt"), agent, "checksum2"
        )
        is False
    )
    assert (
        file_ops.is_duplicate_operation(
            "write", Path("path/to/file3.txt"), agent, "checksum3"
        )
        is False
    )
   
