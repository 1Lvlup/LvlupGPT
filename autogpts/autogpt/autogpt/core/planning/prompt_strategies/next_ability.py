import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import json_schema
from autogpt.core.configuration import SystemConfiguration, UserConfigurable
from autogpt.core.planning.schema import Task
from autogpt.core.prompting import PromptStrategy
from autogpt.core.prompting.schema import ChatPrompt, LanguageModelClassification
from autogpt.core.prompting.utils import json_loads, to_numbered_list
from autogpt.core.resource.model_providers import (
    AssistantChatMessage,
    ChatMessage,
    CompletionModelFunction,
)

# Initialize a logger for this module
logger = logging.getLogger(__name__)

# Define the NextAbilityConfiguration class that inherits from SystemConfiguration
class NextAbilityConfiguration(SystemConfiguration):
    # Declare class variables
    model_classification: LanguageModelClassification = UserConfigurable()
    system_prompt_template: str = UserConfigurable()
    system_info: List[str] = UserConfigurable()
    user_prompt_template: str = UserConfigurable()
    additional_ability_arguments: Dict[str, json_schema.Schema] = UserConfigurable(
        default_factory=dict
    )

# Define the NextAbility class that inherits from PromptStrategy
class NextAbility(PromptStrategy):
    # Define class variables
    DEFAULT_SYSTEM_PROMPT_TEMPLATE = "System Info:\n{system_info}"

    DEFAULT_SYSTEM_INFO = [
        "The OS you are running on is: {os_info}",
        "It takes money to let you run. Your API budget is ${api_budget:.3f}",
        "The current time and date is {current_time}",
    ]

    DEFAULT_USER_PROMPT_TEMPLATE = (
        "Your current task is is {task_objective}.\n"
        "You have taken {cycle_count} actions on this task already. "
        "Here is the actions you have taken and their results:\n"
        "{action_history}\n\n"
        "Here is additional information that may be useful to you:\n"
        "{additional_info}\n\n"
        "Additionally, you should consider the following:\n"
        "{user_input}\n\n"
        "Your task of {task_objective} is complete when the following acceptance"
        " criteria have been met:\n"
        "{acceptance_criteria}\n\n"
        "Please choose one of the provided functions to accomplish this task. "
        "Some tasks may require multiple functions to accomplish. If that is the case,"
        " choose the function that you think is most appropriate for the current"
        " situation given your progress so far."
    )

    DEFAULT_ADDITIONAL_ABILITY_ARGUMENTS = {
        "motivation": json_schema.Schema(
            type=json_schema.Schema.Type.STRING,
            description=(
                "Your justification for choosing choosing this function instead of a "
                "different one."
            ),
        ),
        "self_criticism": json_schema.Schema(
            type=json_schema.Schema.Type.STRING,
            description=(
                "Thoughtful self-criticism that explains why this function may not be "
                "the best choice."
            ),
        ),
        "reasoning": json_schema.Schema(
            type=json_schema.Schema.Type.STRING,
            description=(
                "Your reasoning for choosing this function taking into account the "
                "`motivation` and weighing the `self_criticism`."
            ),
        ),
    }

    # Define the default configuration for the NextAbility class
    default_configuration: NextAbilityConfiguration = NextAbilityConfiguration(
        model_classification=LanguageModelClassification.SMART_MODEL,
        system_prompt_template=DEFAULT_SYSTEM_PROMPT_TEMPLATE,
        system_info=DEFAULT_SYSTEM_INFO,
        user_prompt_template=DEFAULT_USER_PROMPT_TEMPLATE,
        additional_ability_arguments={
            k: v for k, v in DEFAULT_ADDITIONAL_ABILITY_ARGUMENTS.items()
        },
    )

    # Initialize the NextAbility class with the given parameters
    def __init__(
        self,
        model_classification: LanguageModelClassification,
        system_prompt_template: str,
        system_info: List[str],
        user_prompt_template: str,
        additional_ability_arguments: Dict[str, json_schema.Schema],
    ):
        # Set the class variables to the given parameters
        self._model_classification = model_classification
        self._system_prompt_template = system_prompt_template
        self._system_info = system_info
        self._user_prompt_template = user_prompt_template
        self._additional_ability_arguments = {
            k: v.to_dict() for k, v in additional_ability_arguments.items()
        }
        for p in self._additional_ability_arguments.values():
            p["required"] = True

    # Define a property for the model_classification variable
    @property
    def model_classification(self) -> LanguageModelClassification:
        return self._model_classification

    # Define a method for building a prompt based on the given parameters
    def build_prompt(
        self,
        task: Task,
        ability_specs: List[CompletionModelFunction],
        os_info: str,
        api_budget: float,
        current_time: str,
        **kwargs,
    ) -> ChatPrompt:
        # Set the template_kwargs variable to the given parameters
        template_kwargs = {
            "os_info": os_info,
            "api_budget": api_budget,
            "current_time": current_time,
            **kwargs,
        }

        # Loop through the ability_specs list and update the parameters with the additional_ability_arguments
        for ability in ability_specs:
            ability.parameters.update
