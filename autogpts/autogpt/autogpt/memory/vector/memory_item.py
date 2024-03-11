from __future__ import annotations

import json
import logging
from typing import Literal

import ftfy
import numpy as np
from pydantic import BaseModel

import autogpt.config  # Importing the config module
from autogpt.core.resource.model_providers import (
    ChatMessage,
    ChatModelProvider,
    EmbeddingModelProvider,
)
from autogpt.processing.text import chunk_content, split_text, summarize_text

from .utils import Embedding, get_embedding  # Importing the Embedding class and get_embedding function

logger = logging.getLogger(__name__)

# Define MemoryDocType as an enumeration representing different types of memory items
MemoryDocType = Literal["webpage", "text_file", "code_file", "agent_history"]


class MemoryItem(BaseModel, arbitrary_types_allowed=True):
    """Memory object containing raw content as well as embeddings"""

    raw_content: str
    summary: str
    chunks: list[str]
    chunk_summaries: list[str]
    e_summary: Embedding
    e_chunks: list[Embedding]
    metadata: dict

    def relevance_for(self, query: str, e_query: Embedding | None = None):
        return MemoryItemRelevance.of(self, query, e_query)

    def dump(self, calculate_length=False) -> str:
        n_chunks = len(self.e_chunks)
        return f"""
=============== MemoryItem ===============
Size: {n_chunks} chunks
Metadata: {json.dumps(self.metadata, indent=2)}
---------------- SUMMARY -----------------
{self.summary}
------------------ RAW -------------------
{self.raw_content}
==========================================
"""

    def __eq__(self, other: MemoryItem):
        return (
            self.raw_content == other.raw_content
            and self.chunks == other.chunks
            and self.chunk_summaries == other.chunk_summaries
            # Embeddings can either be list[float] or np.ndarray[float32],
            # and for comparison they must be of the same type
            and np.array_equal(
                self.e_summary
                if isinstance(self.e_summary, np.ndarray)
                else np.array(self.e_summary, dtype=np.float32),
                other.e_summary
                if isinstance(other.e_summary, np.ndarray)
                else np.array(other.e_summary, dtype=np.float32),
            )
            and np.array_equal(
                self.e_chunks
                if isinstance(self.e_chunks[0], np.ndarray)
                else [np.array(c, dtype=np.float32) for c in self.e_chunks],
                other.e_chunks
                if isinstance(other.e_chunks[0], np.ndarray)
                else [np.array(c, dtype=np.float32) for c in other.e_chunks],
            )
        )


class MemoryItemFactory:
    def __init__(
        self,
        llm_provider: ChatModelProvider,
        embedding_provider: EmbeddingModelProvider,
    ):
        self.llm_provider = llm_provider
        self.embedding_provider = embedding_provider

    async def from_text(
        self,
        text: str,
        source_type: MemoryDocType,
        config: Config,
        metadata: dict = {},
        how_to_summarize: str | None = None,
        question_for_summary: str | None = None,
    ):
        logger.debug(f"Memorizing text:\n{'-'*32}\n{text}\n{'-'*32}\n")

        # Fix encoding, e.g. removing unicode surrogates (see issue #778)
        text = ftfy.fix_text(text)

        # FIXME: needs ModelProvider
        chunks = [
            chunk
            for chunk, _ in (
                split_text(
                    text=text,
                    config=config,
                    max_chunk_length=1000,  # arbitrary, but shorter ~= better
                    tokenizer=self.llm_provider.get_tokenizer(config.fast_llm),
                )
                if source_type != "code_file"
                # TODO: chunk code based on structure/outline
                else chunk_content(
                    content=text,
                    max_chunk_length=1000,
                    tokenizer=self.llm_provider.get_tokenizer(config.fast_llm),
                )
            )
        ]
        logger.debug("Chunks: " + str(chunks))

        chunk_summaries = [
            summary
            for summary, _ in [
                await summarize_text(
                    text=text_chunk,
                    instruction=how_to_summarize,
                    question=question_for_summary,
                    llm_
