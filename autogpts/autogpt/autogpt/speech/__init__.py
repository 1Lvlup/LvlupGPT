"""This module contains the speech recognition and speech synthesis functions."""
from autogpt.speech.say import TextToSpeechProvider, TTSConfig

class SpeechSynthesis:
    """Speech synthesis class to convert text to speech."""

    def __init__(self, config: TTSConfig):
        """Initialize the SpeechSynthesis class with the TTSConfig object."""
        self.tts = TextToSpeechProvider(config)

    def say(self, text: str):
        """Convert the given text to speech."""
        self.tts.say(text)

if __name__ == "__main__":
    # Example usage
    config = TTSConfig(voice="male", rate=150)
    synthesizer = SpeechSynthesis(config)
    synthesizer.say("Hello, Autogpt!")

__all__ = ["SpeechSynthesis", "TTSConfig"]
