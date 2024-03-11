""" GTTS Voice. """
from __future__ import annotations  # Allows using class name in type hints

import os

import gtts  # A text-to-speech conversion library
from playsound import playsound  # A library to play audio files

from autogpt.speech.base import VoiceBase  # Base class for speech-related functionalities


class GTTSVoice(VoiceBase):
    """GTTS Voice. This class implements a text-to-speech voice using the gTTS library."""

    def _setup(self) -> None:
        """
        Set up any necessary resources for the voice.

        This method does not perform any setup, as the gTTS library does not require
        any initialization.
        """
        pass  # No initialization needed

    def _speech(self, text: str, _: int = 0) -> bool:
        """
        Play the given text.

        This method converts the input text into speech using the gTTS library and
        plays the resulting audio file using the playsound library. The method
        returns True if the speech was played successfully, and False otherwise.

        :param text: The text to convert into speech
        :param _: An unused integer parameter, included for compatibility with the base class
        :return: A boolean indicating success or failure
        """
        tts = gtts.gTTS(text)  # Convert the text into speech
        tts.save("speech.mp3")  # Save the speech as an MP3 file
        playsound("speech.mp3", True)  # Play the MP3 file
        os.remove("speech.mp3")  # Delete the MP3 file after playing
        return True  # Return True, indicating success
