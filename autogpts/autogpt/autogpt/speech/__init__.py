"""This module contains the speech recognition and speech synthesis functions."""
from autogpt.speech.say import TextToSpeechProvider, TTSConfig  # Importing TextToSpeechProvider and TTSConfig from the 'say' module in 'autogpt.speech'

class SpeechSynthesis:
    """Speech synthesis class to convert text to speech."""

    def __init__(self, config: TTSConfig):
        """
        Initialize the SpeechSynthesis class with the TTSConfig object.

        :param config: TTSConfig object containing the configuration for the TextToSpeechProvider
        """
        self.tts = TextToSpeechProvider(config)  # Initialize TextToSpeechProvider with the given config

    def say(self, text: str):
        """
        Convert the given text to speech.

        :param text: The text to be converted to speech
        """
        self.tts.say(text)  # Call the 'say' method of TextToSpeechProvider to convert the text to speech

if __name__ == "__main__":
    # Example usage
    config = TTSConfig(voice="male", rate=150)  # Create a TTSConfig object with 'male' voice and rate of 150
    synthesizer = SpeechSynthesis(config)  # Initialize SpeechSynthesis class with the created config
    synthesizer.say("Hello, Autogpt!")  # Use the 'say' method to convert the text "Hello, Autogpt!" to speech

__all__ = ["SpeechSynthesis", "TTSConfig"]  # Export SpeechSynthesis and TTSConfig classes for use in other modules
