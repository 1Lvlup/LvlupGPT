"""
This module contains the configuration classes for AutoGPT.
"""

import sys

__version__ = "0.1.0"


def assert_config_has_openai_api_key(config: Config) -> None:
    """
    Assert that the given config object has an OpenAI API key set.

    :param config: The config object to check for an API key.
    """
    if not config.openai_api_key:
        raise ValueError("OpenAI API key not found in the config.")


class ConfigBuilder:
    """
    A builder class for creating Config objects.
    """

    def __init__(self):
        self.config = Config()

    def with_openai_api_key(self, api_key: str) -> "ConfigBuilder":
        """
        Set the OpenAI API key for the config.

        :param api_key: The OpenAI API key.
        :return: The ConfigBuilder instance (for chaining calls).
        """
        self.config.openai_api_key = api_key
        return self

    def build(self) -> Config:
        """
        Build and return the Config object.

        :return: The Config object.
        """
        assert_config_has_openai_api_key(self.config)
        return self.config


class Config:
    """
    The main configuration class for AutoGPT.
    """

    def __init__(self):
        self.openai_api_key = None


class AIProfile:
    """
    A class representing an AI profile.
    """

   
