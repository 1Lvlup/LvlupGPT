"""Tests for JSONFileMemory class"""

import orjson
import pytest

from autogpt.config import Config  # Importing Config class from autogpt.config module
from autogpt.file_workspace import FileWorkspace  # Importing FileWorkspace class from autogpt.file_workspace module
from autogpt.memory.vector import JSONFileMemory, MemoryItem  # Importing JSONFileMemory and MemoryItem classes from autogpt.memory.vector module


def test_json_memory_init_without_backing_file(
    config: Config, workspace: FileWorkspace
):
    """
    Test JSONFileMemory initialization without a backing file.

    This test checks if the index file is created and initialized with an empty list when JSONFileMemory is initialized without a backing file.
    """
    index_file = workspace.root / f"{config.memory_index}.json"

    assert not index_file.exists()  # Check if the index file does not exist before initialization
    JSONFileMemory(config)
    assert index_file.exists()  # Check if the index file is created after initialization
    assert index_file.read_text() == "[]"  # Check if the index file is initialized with an empty list


def test_json_memory_init_with_backing_empty_file(
    config: Config, workspace: FileWorkspace
):
    """
    Test JSONFileMemory initialization with an empty backing file.

    This test checks if the index file is loaded correctly when JSONFileMemory is initialized with an empty backing file.
    """
    index_file = workspace.root / f"{config.memory_index}.json"
    index_file.touch()

    assert index_file.exists()  # Check if the index file exists before initialization
    JSONFileMemory(config)
    assert index_file.exists()  # Check if the index file still exists after initialization
    assert index_file.read_text() == "[]"  # Check if the index file is still empty after initialization


def test_json_memory_init_with_backing_invalid_file(
    config: Config, workspace: FileWorkspace
):
    """
    Test JSONFileMemory initialization with an invalid backing file.

    This test checks if the index file is reinitialized with an empty list when JSONFileMemory is initialized with an invalid backing file.
    """
    index_file = workspace.root / f"{config.memory_index}.json"
    index_file.touch()

    raw_data = {"texts": ["test"]}
    data = orjson.dumps(raw_data, option=JSONFileMemory.SAVE_OPTIONS)
    with index_file.open("wb") as f:
        f.write(data)

    assert index_file.exists()  # Check if the index file exists before initialization
    JSONFileMemory(config)
    assert index_file.exists()  # Check if the index file still exists after initialization
    assert index_file.read_text() == "[]"  # Check if the index file is reinitialized with an empty list


def test_json_memory_add(config: Config, memory_item: MemoryItem):
    """
    Test adding a memory item to the JSONFileMemory index.

    This test checks if the memory item is correctly added to the index.
    """
    index = JSONFileMemory(config)
    index.add(memory_item)
    assert index.memories[0] == memory_item  # Check if the memory item is added to the index


def test_json_memory_clear(config: Config, memory_item: MemoryItem):
    """
    Test clearing the JSONFileMemory index.

    This test checks if the index is correctly cleared.
    """
    index = JSONFileMemory(config)
    assert index.memories == []  # Check if the index is initially empty

    index.add(memory_item)
    assert index.memories[0] == memory_item, "Cannot test clear() because add() fails"

    index.clear()
    assert index.memories == []  # Check if the index is emptied after clear()


def test_json_memory_get(config: Config, memory_item: MemoryItem, mock_get_embedding):
    """
    Test retrieving a memory item from the JSONFileMemory index.

    This test checks if the memory item is correctly retrieved from the index.
    """
    index = JSONFileMemory(config)
    assert (
        index.get("test", config) is None
    ), "Cannot test get() because initial index is not empty"

    index.add(memory_item)
    retrieved = index.get("test", config)
    assert retrieved is not None  # Check if a memory item is retrieved
    assert retrieved.memory_item == memory_item  # Check if the correct memory item is retrieved


def test_json_memory_load_index(config: Config, memory_item: MemoryItem):
    """
    Test loading the JSONFileMemory index from a file.

    This test checks if the index is correctly loaded from a file.
    """
    index = JSONFileMemory(config)
    index.add(memory_item)

    try:
        assert index.file_path.exists(), "index was not saved to file"
        assert len(index) == 1, f"index contains {len(index)} items instead of 1"
        assert index.memories[0] == memory_item, "item in index != added mock item"
    except AssertionError as e:
        raise ValueError(f"Setting up for load_index test failed: {e}")

    index.memories = []
    index.load_index()

    assert len(index) == 1  # Check if the index is correctly loaded from the file
    assert index.memories[0] == memory_item  # Check if the memory item is correctly loaded


@pytest.mark.vcr
@pytest.mark.requires_openai_api_key
def test_json_memory_get_relevant(config: Config, cached_openai_client: None) -> None:
    """
    Test retrieving relevant memory items from the JSONFileMemory index.

    This test checks if the relevant memory items are correctly retrieved from the index.
    """
