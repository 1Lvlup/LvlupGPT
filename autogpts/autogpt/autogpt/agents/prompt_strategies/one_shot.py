from __future__ import annotations

import json
import platform
import re
from logging import Logger
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

import distro

if TYPE_CHECKING:
    from autogpt.agents.agent import Agent
    from autogpt.agents.utils.exceptions import InvalidAgentResponseError
    from autogpt.config import AIDirectives, AIProfile
    from autogpt.core.configuration.schema import SystemConfiguration, UserConfigurable
    from autogpt.core.prompting import ChatPrompt, LanguageModelClassification, PromptStrategy
    from autogpt.core.resource.model_providers.schema import (
        AssistantChatMessage,
        ChatMessage,
        CompletionModelFunction,
    )
    from autogpt.core.utils.json_schema import JSONSchema
    from autogpt.json_utils.utilities import extract_dict_from_response
    from autogpt.prompts.utils import format_numbered_list, indent


