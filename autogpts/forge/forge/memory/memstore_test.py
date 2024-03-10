import hashlib
import shutil
import time

import pytest
from forge.sdk.memory.memstore import ChromaMemStore


@pytest.fixture(scope="module")
def memstore():
    mem = ChromaMemStore(".test_mem_store")
    yield mem
    shutil.rmtree(".test_mem_store")
    time.sleep(0.1)  # wait for Chroma to finish indexing before deleting the directory


def test_add(memstore):
    """Test adding a document to the memstore."""
    task_id = "test_task"
    document = "This is a test document."
    metadatas = {"metadata": "test_metadata"}
    memstore.add(task_id, document, metadatas)
    doc_id = hashlib.sha256(document.encode()).hexdigest()[:20]
    assert memstore.client.get_or_create_collection(task_id).count() == 1


@pytest.mark.usefixtures("memstore")
@pytest.mark.parametrize(
    "task_id,document,metadatas,query,expected_count",
    [
        ("test_task", "This is a test document.", {"metadata": "test_metadata"}, "test", 1),
        ("test_task", "This is a different test document.", {"metadata": "test_metadata"}, "different", 1),
        ("test_task", "This is a test document.", {"metadata": "test_metadata"}, "This is a", 1),
        ("test_task", "This is a test document.", {"metadata": "test_metadata"}, "This is a test", 1),
        ("test_task", "This is a test document.", {"metadata": "test_metadata"}, "This is a test document.", 1),
        ("test_task", "This is a test document.", {"metadata": "test_metadata"}, "This is a test document.1", 0),
    ],
)
def test_query(memstore, task_id, document, metadatas, query, expected_count):
    """Test querying the memstore."""
    memstore.add(task_id, document, metadatas)
    results = memstore.query(task_id, query)
    assert results["documents"][0] == document
    assert results["count"] == expected_count


@pytest.mark.usefixtures("memstore")
@pytest.mark.parametrize(
    "task_id,document,metadatas,
