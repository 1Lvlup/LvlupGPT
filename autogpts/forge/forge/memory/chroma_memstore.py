import hashlib
import typing as t

import chromadb
from chromadb.config import Settings


class ChromaMemStore:
    def __init__(self, store_path: str):
        self.client = chromadb.PersistentClient(
            path=store_path, settings=Settings(anonymized_telemetry=False)
        )

    def generate_doc_id(self, document: str) -> str:
        return hashlib.sha256(document.encode()).hexdigest()[:20]

    def add(self, task_id: str, document: str, metadatas: dict) -> None:
        doc_id = self.generate_doc_id(document)
        collection = self.client.get_or_create_collection(task_id)
        collection.add(documents=[document], metadatas=[metadatas], ids=[doc_id])

    def query(
        self,
        task_id: str,
        query: str,
        filters: dict = None,
        document_search: dict = None,
    ) -> dict:
        collection = self.client.get_or_create_collection(task_id)

        kwargs = {"query_texts": [query], "n_results": 10}

        if filters:
            kwargs["where"] = filters
        elif document_search:
            raise ValueError("document_search parameter provided without filters")

        if document_search:
            kwargs["where_document"] = document_search

        return collection.query(**kwargs)

    def get(self, task_id: str, doc_ids: t.List[str] = None, filters: dict = None) -> dict:
        collection = self.client.get_or_create_collection(task_id)
        kwargs = {}
        if doc_ids:
            kwargs["ids"] = doc_ids
        if filters:
            kwargs["where"] = filters
        return collection.get(**kwargs)

    def update(self, task_id: str, doc_ids: t.List[str], documents: t.List[str], metadatas: t.List[dict]) -> None:
        if not (documents and metadatas):
            raise ValueError("documents and metadatas arguments are required")

        collection = self.client.get_or_create_collection(task_id)
        collection.update(ids=doc_ids, documents=documents, metadatas=metadatas)

    def delete(self, task_id: str, doc_id: str) -> None:
        if not doc_id:
            raise ValueError("doc_id argument is required")

        collection = self.client.get_or_create_collection(task_id)
        collection.delete(ids=[doc_id])


if __name__ == "__main__":
    print("#############################################")
    # Initialize MemStore
    mem = ChromaMemStore(".agent_mem_store")

    # Test add function
    task_id = "test_task"
    document = "This is a another new test document."
    metadatas = {"metadata": "test_metadata"}
    mem.add(task_id, document, metadatas)

    # ... (rest of the test code remains the same)
