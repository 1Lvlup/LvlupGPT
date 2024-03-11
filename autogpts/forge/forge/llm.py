from pathlib import Path

from litellm import AuthenticationError, InvalidRequestError, ModelResponse, acompletion
from openai import OpenAI
from openai.types import CreateEmbeddingResponse
from openai.types.audio import Transcription
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .sdk.forge_log import ForgeLogger  # Importing ForgeLogger to log messages

LOG = ForgeLogger(__name__)  # Creating a logger instance with the name of the current module

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))  # Decorator to retry the function if it fails
async def chat_completion_request(model, messages, **kwargs) -> ModelResponse:
    """
    Generate a response to a list of messages using OpenAI's API.

    This function sends a request to the OpenAI API to generate a response to a list of messages.
    It retries the request up to 3 times if it fails, with a random exponential wait time between 1 and 40 seconds.

    Args:
        model (str): The model to use for generating the response.
        messages (list): A list of message dictionaries, each containing a 'role' and 'content' key.
        **kwargs: Additional keyword arguments to pass to the acompletion function.

    Returns:
        ModelResponse: The response from the OpenAI API, containing the generated text and any metadata.

    Raises:
        AuthenticationError: If there is an authentication error with the OpenAI API.
        InvalidRequestError: If the request to the OpenAI API is invalid.
        Exception: If there is an unknown error while generating the response.
    """
    try:
        # Setting the model and messages in the kwargs dictionary
        kwargs["model"] = model
        kwargs["messages"] = messages

        # Sending the request to the OpenAI API using the acompletion function
        resp = await acompletion(**kwargs)
        return resp
    except AuthenticationError as e:
        LOG.exception("Authentication Error")  # Logging the exception
        raise
    except InvalidRequestError as e:
        LOG.exception("Invalid Request Error")  # Logging the exception
        raise
    except Exception as e:
        LOG.error("Unable to generate ChatCompletion response")  # Logging the error
        LOG.error(f"Exception: {e}")  # Logging the exception
        raise

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
async def create_embedding_request(
    messages, model="text-embedding-ada-002"
) -> CreateEmbeddingResponse:
    """
    Generate an embedding for a list of messages using OpenAI's API.

    This function sends a request to the OpenAI API to generate an embedding for a list of messages.
    It retries the request up to 3 times if it fails, with a random exponential wait time between 1 and 40 seconds.

    Args:
        messages (list): A list of message dictionaries, each containing a 'role' and 'content' key.
        model (str, optional): The model to use for generating the embedding. Defaults to "text-embedding-ada-002".

    Returns:
        CreateEmbeddingResponse: The response from the OpenAI API, containing the generated embedding and any metadata.

    Raises:
        Exception: If there is an unknown error while generating
