"""Base class for all voice classes."""
from __future__ import annotations

import abc
import re
from threading import Lock
from typing import List, Dict, Any, Optional


class VoiceBase:
    """
    Base class for all voice classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the voice class.
        """
        self._url: Optional[str] = None
        self._headers: Optional[Dict[str, Any]] = None
        self._api_key: Optional[str] = None
        self._voices: List[Dict[str, Any]] = []
        self._mutex = Lock()
        self._setup(*args, **kwargs)

    def say(self, text: str, voice_index: int = 0) -> bool:
        """
        Say the given text.

        Args:
            text (str): The text to say.
            voice_index (int): The index of the voice to use.
        """
        text = re.sub(
            r"\b(?:https?://[-\w_.]+/?\w[-\w_.]*\.(?:[-\w_.]+/?\w[-\w_.]*\.)?[a-z]+(?:/[-\w_.%]+)*\b(?!\.))",  # noqa: E501
            "",
            text,
        )
        with self._mutex:
            if 0 <= voice_index < len(self._voices):
              
