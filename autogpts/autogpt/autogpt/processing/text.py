"""Text processing functions"""
import logging
import math
from typing import Iterator, Optional, TypeVar

import spacy

from autogpt.config import Config
from autogpt.core.prompting import ChatPrompt
from autogpt.core.resource.model_providers import (
    ChatMessage,
    ChatModelProvider,
    ModelTokenizer,
)
from autogpt.json_utils.utilities import extract_list_from_response

logger = logging.getLogger(__name__)

# Define a type variable for generic type T
T = TypeVar("T")

def batch(
    sequence: list[T], max_batch_length: int, overlap: int = 0
) -> Iterator[list[T]]:
    """
    Batch data from iterable into slices of length N. The last batch may be shorter.

    Example: `batched('ABCDEFGHIJ', 3)` --> `ABC DEF GHI J`
    """
    if max_batch_length < 1:
        raise ValueError("n must be at least one")
    for i in range(0, len(sequence), max_batch_length - overlap):
        yield sequence[i : i + max_batch_length]


def chunk_content(
    content: str,
    max_chunk_length: int,
    tokenizer: ModelTokenizer,
    with_overlap: bool = True
) -> Iterator[tuple[str, int]]:
    """Split content into chunks of approximately equal token length."""

    MAX_OVERLAP = 200  # limit overlap to save tokens

    tokenized_text = tokenizer.encode(content)
    total_length = len(tokenized_text)
    n_chunks = math.ceil(total_length / max_chunk_length)

    chunk_length = math.ceil(total_length / n_chunks)
    overlap = min(max_chunk_length - chunk_length, MAX_OVERLAP) if with_overlap else 0

    for token_batch in batch(tokenized_text, chunk_length + overlap, overlap):
        yield tokenizer.decode(token_batch), len(token_batch)


async def summarize_text(
    text: str,
    llm_provider: ChatModelProvider,
    config: Config,
    question: Optional[str] = None,
    instruction: Optional[str] = None,
) -> tuple[str, list[tuple[str, str]]]:
    """
    Summarize the given text using a language model.

    Args:
        text (str): The text to summarize.
        llm_provider (ChatModelProvider): The language model provider.
        config (Config): The configuration object.
        question (Optional[str]): The question to answer with the summary.
        instruction (Optional[str]): The instruction to give to the language model.

    Returns:
        A tuple containing the summary and a list of (summary, chunk) pairs.
    """
    # Set the instruction based on the input parameters
    if question:
        if instruction:
            raise ValueError(
                "Parameters 'question' and 'instructions' cannot both be set"
            )

        instruction = (
            f'From the text, answer the question: "{question}". '
            "If the answer is not in the text, indicate this clearly "
            "and concisely state why the text is not suitable to answer the question."
        )
    elif not instruction:
        instruction = (
            "Summarize or describe the text clearly and concisely, "
            "whichever seems more appropriate."
        )

    # Call the _process_text function to generate the summary
    return await _process_text(  # type: ignore
        text=text,
        instruction=instruction,
        llm_provider=llm_provider,
        config=config,
    )


async def extract_information(
    source_text: str,
    topics_of_interest: list[str],
    llm_provider: ChatModelProvider,
    config: Config
) -> list[str]:
    """
    Extract information related to the given topics from the source text.

    Args:
        source_text (str): The text to extract information from.
        topics_of_interest (list[str]): The topics to extract information about.
        llm_provider (ChatModelProvider): The language model provider.
        config (Config): The configuration object.

    Returns:
        A list of extracted information strings.
    """
    fmt_topics_list = "\n".join(f"* {topic}." for topic in topics_of_interest)
    instruction = (
        "Extract relevant pieces of information about the following topics:\n"
        f"{fmt_topics_list}\n"
        "Reword pieces of information if needed to make them self-explanatory. "
        "Be concise.\n\n"
        "Respond with an `Array<string>` in JSON format AND NOTHING ELSE. "
        'If the text contains no relevant information, return "[]".'
    )
    return await _process_text(  # type: ignore
        text=source_text,
        instruction=instruction,
        output_type=list[str],
        llm_provider=llm_provider,
        config=config,
    )


async def _process_text(
    text: str,
    instruction: str,
    llm_provider: ChatModelProvider,
    config: Config,
    output_type: type[str | list[str]] = str
) -> tuple[str, list[tuple[str, str]]] | list[str]:
    """
    Process text using the OpenAI API for summarization or information extraction

    Params:
        text (str): The text to process.
        instruction (str): Additional instruction for processing.
        llm_provider: LLM provider to use.
        config (Config): The global application config.
        output_type: `str` for summaries or `list[str]` for piece-wise info extraction.

    Returns:
        For summarization: tuple[str, None | list[(summary, chunk)]]
        For piece-wise information extraction
