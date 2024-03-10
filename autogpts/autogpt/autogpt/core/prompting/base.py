import abc

from autogpt.core.configuration import SystemConfiguration
from autogpt.core.resource.model_providers import AssistantChatMessage
from .schema import ChatPrompt, LanguageModelClassification

class PromptStrategy(abc.ABC):
    def __init__(self, default_configuration: SystemConfiguration):
        self.default_configuration = default_configuration

