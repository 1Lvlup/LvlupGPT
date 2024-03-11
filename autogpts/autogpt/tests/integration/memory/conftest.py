import pytest

from autogpt.memory.vector.memory_item import MemoryItem
from autogpt.memory.vector.utils import Embedding

@pytest.fixture
def memory_item(mock_embedding: Embedding):
    """
    A pytest fixture that returns a MemoryItem object with pre-defined attributes.

    This fixture is used to test functions or methods that require a MemoryItem object as an argument.
    It takes in a mock Embedding object as an argument, which is used to initialize the MemoryItem's
    e_summary and e_chunks attributes.

    Returns:
        MemoryItem: A MemoryItem object with the following attributes:
            - raw_content: str, set to "test content"
            - summary: str, set to "test content summary"
            - chunks: List[str], set to ["test content"]
            - chunk_summaries: List[str], set to ["test content summary"]
            - e_summary: Embedding, set to the mock Embedding object passed in as an argument
            - e_chunks: List[Embedding], set to a list containing the mock Embedding object passed in as an argument
            - metadata: Dict[str, any], set to an empty dictionary
    """
    return MemoryItem(
        raw_content="test content",
        summary="test content summary",
        chunks=["test content"],
        chunk_summaries=["test content summary"],
        e_summary=mock_embedding,
        e_chunks=[mock_embedding],
        metadata={},
    )
