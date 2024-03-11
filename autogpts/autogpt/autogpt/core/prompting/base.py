import abc  # Importing the abc module for abstract base classes

from autogpt.core.configuration import SystemConfiguration  # Importing SystemConfiguration class
from autogpt.core.resource.model_providers import AssistantChatMessage  # Importing AssistantChatMessage class
from .schema import ChatPrompt, LanguageModelClassification  # Importing ChatPrompt and LanguageModelClassification classes


class PromptStrategy(abc.ABC):  # Defining an abstract base class for prompt strategies
    def __init__(self, default_configuration: SystemConfiguration):
        """
        Initialize the PromptStrategy class with the default configuration.

        :param default_configuration: An instance of SystemConfiguration class, representing the default configuration.
        """
        self.default_configuration = default_configuration

