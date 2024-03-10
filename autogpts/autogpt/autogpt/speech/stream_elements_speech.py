from __future__ import annotations

import logging
import os
import requests
from typing import Boolean, Final

from autogpt.core.configuration import SystemConfiguration, UserConfigurable

logger = logging.getLogger(__name__)

STREAM_ELEMENTS_API_BASE_URL: Final = "https://api.streamelements.com/kappa/v2/speech"


class StreamElementsConfig(SystemConfiguration):
    voice: str = UserConfigurable(default="Brian", from_env="STREAMELEMENTS_VOICE")
    api_key: str = UserConfigurable(default=None, from_env="STREAMELEMENTS_API_KEY")


class StreamElementsSpeech(VoiceBase):
    """Streamelements speech module for autogpt"""

    def __init__(self, config: StreamElementsConfig):
        self.config = config
        self.set_api_key(config.api_key)

    def set_api_key(self, api_key: str | None) -> None:
        """Set the API key for streamelements

        Args:
            api_key (str | None): The API key
        """
        if api_key is not None:
            self.headers = {"Authorization": f"Bearer {api_key}"}
        else:
            logger.warning("API key not set for streamelements")
            self.headers = {}

    def api_key_is_set(self) -> Boolean:
        """Check if the API key is set for streamelements

        Returns:
            Boolean: True if the API key is set, False otherwise
        """
        return self.headers.get("Authorization") is not None

    def get_tts_url(self, text: str, voice: str) -> str:
        """Get the TTS url for streamelements

        Args:
            text (str): The text to speak
            voice (str): The voice to use

        Returns:
            str: The TTS url
        """
        return f"{STREAM_ELEMENTS_API_BASE_URL}?voice={voice}&text={text}"

    def _speech(self, text: str, voice: str, _: int
