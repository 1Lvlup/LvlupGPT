import logging
from contextlib import suppress
from typing import Any, Sequence, overload  # Import necessary types

import numpy as np

import autogpt.config  # Import the configuration module
from autogpt.core.resource.model_providers import EmbeddingModelProvider  # Import the embedding provider

# Initialize the logger
logger = logging.getLogger(__name__)

# Define the types of Embedding and Tokenized text
Embedding = list[float] | list[np.float32] | np.ndarray[Any, np.dtype[np.float32]]
TText = Sequence[int]
"""Embedding vector and Tokenized text types respectively"""


# Define the get_embedding function with two overloads
@overload
async def get_embedding(
    input: str | TText, config: Config, embedding_provider: EmbeddingModelProvider
) -> Embedding:
    ...


@overload
async def get_embedding(
    input: list[str] | list[TText],
    config: Config,
    embedding_provider: EmbeddingModelProvider,
) -> list[Embedding]:
    ...


async def get_embedding(
    input: str | TText | list[str] | list[TText],
    config: Config,
    embedding_provider: EmbeddingModelProvider,
) -> Embedding | list[Embedding]:
    """Get an embedding from the ada model.

    Args:
        input: Input text to get embeddings for, encoded as a string or array of tokens.
            Multiple inputs may be given as a list of strings or token arrays.
        embedding_provider: The provider to create embeddings.

    Returns:
        List[float]: The embedding.
    """
    multiple = isinstance(input, list) and all(not isinstance(i, int) for i in input)

    # Replace newline characters with spaces in the input string
    if isinstance(input, str):
        input = input.replace("\n", " ")

        # Try to get the embedding using a plugin
        with suppress(NotImplementedError):
            return _get_embedding_with_plugin(input, config)

    elif multiple and isinstance(input[0], str):
        input = [text.replace("\n", " ") for text in input]

        # Try to get embeddings using plugins for each input
        with suppress(NotImplementedError):
            return [_get_embedding_with_plugin(i, config) for i in input]

    # Get the embedding model from the configuration
    model = config.embedding_model

    logger.debug(
        f"Getting embedding{f's for {len(input)} inputs' if multiple else ''}"
        f" with model '{model}'"
    )

    # If there's only one input, get its embedding
    if not multiple:
        return (
            await embedding_provider.create_embedding(
                text=input,
                model_name=model,
                embedding_parser=lambda e: e,
            )
        ).embedding
    else:
        # Otherwise, get embeddings for all inputs
        embeddings = []
        for text in input:
            result = await embedding_provider.create_embedding(
                text=text,
                model_name=model,
                embedding_parser=lambda e: e,
            )
            embeddings.append(result.embedding)
        return embeddings


def _get_embedding_with_plugin(text: str, config: Config) -> Embedding:
    # Iterate through plugins and try to get the embedding using each one
    for plugin in config.plugins:
        if plugin.can_handle_text_embedding(text):
            embedding = plugin.handle_text_embedding(text)
            if embedding is not None:
                return embedding

    # Raise an error if no plugin can handle the text embedding
    raise NotImplementedError
