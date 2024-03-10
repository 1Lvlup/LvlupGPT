from math import ceil, floor
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from autogpt.core.prompting import ChatPrompt

SEPARATOR_LENGTH = 42

def separator(text: str) -> str:
    """
    Generate a separator line with the given text centered.

    :param text: The text to center in the separator line.
    :return: A separator line with the text centered.
    """
    half_sep_len = (SEPARATOR_LENGTH - 2 - len(text)) // 2
    if half_sep_len < 0:
        raise ValueError(f"Separation length {SEPARATOR_LENGTH} is too small for text {text}")
    return f"{half_sep_len*'-'} {text.upper()} {half_sep_len*'-'}"

def dump_prompt(prompt: "ChatPrompt") -> str:
    """
    Generate a string representation of a ChatPrompt object.

    :param prompt: The ChatPrompt object to represent as a string.
    :return: A string representation of the ChatPrompt object.
    """
    formatted_messages = "\n".join([separator(m.role) + "\n" + m.content for m in prompt.messages])
    return f"""
============== {prompt.__class__.__name__} ==============
Length: {len(prompt.messages)} messages
{formatted_messages}
==========================================
"""
