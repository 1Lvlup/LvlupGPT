""" Text to speech module """
from __future__ import annotations

import os
import threading
from typing import Literal, Optional

from autogpt.core.configuration.schema import SystemConfiguration, UserConfigurable

from .base import VoiceBase
from .eleven_labs import ElevenLabsConfig, ElevenLabsSpeech
from .gtts import GTTSVoice
from .macos_tts import MacOSTTS
from .stream_elements_speech import StreamElementsConfig, StreamElementsSpeech

class TTSConfig(SystemConfiguration):
    speak_mode: bool = False
    elevenlabs: Optional[ElevenLabsConfig] = None
    streamelements: Optional[StreamElementsConfig] = None
    provider: Literal[
        "elevenlabs", "gtts", "macos", "streamelements"
    ] = UserConfigurable(
        default="gtts",
        from_env=lambda: os.getenv("TEXT_TO_SPEECH_PROVIDER")
        or (
            "macos"
            if os.getenv("USE_MAC_OS_TTS")
            else "elevenlabs"
            if os.getenv("ELEVENLABS_API_KEY")
            else "streamelements"
            if os.getenv("USE_BRIAN_TTS")
            else "gtts"
        ),
    )  # type: ignore

class TextToSpeechProvider:
    def __new__(cls, config: TTSConfig):
        tts_provider = config.provider
        if tts_provider == "elevenlabs":
            return ElevenLabsSpeech(config.elevenlabs)
        elif tts_provider == "macos":
            return MacOSTTS()
        elif tts_provider == "streamelements":
            return StreamElementsSpeech(config.streamelements)
        else:
            return GTTSVoice()

    def __init__(self, config: TTSConfig):
        self._config = config
        self._voice_engine = self.__new__(self, config)

    async def say_async(self, text, voice_index: int = 0) -> None:
        """Generate speech asynchronously"""
        await self._voice_engine.say_async(text, voice_index)

    def say(self, text, voice_index: int = 0) -> None:
        """Generate speech synchronously"""
        def _speak() -> None:
            self._voice_engine.say(text, voice_index)

        if self._config.speak_mode:
            thread = threading.Thread(target=_speak)
            thread.start()
            thread.join()

    def stop(self) -> None:
        """Stop any ongoing speech generation"""
        self._voice_engine.stop()

    def __repr__(self):
        return "{class_name}(provider={voice_engine_name})".format(
            class_name=self.__class__.__name__,
            voice_engine_name=self._voice_engine.__class__.__name__,
        )
