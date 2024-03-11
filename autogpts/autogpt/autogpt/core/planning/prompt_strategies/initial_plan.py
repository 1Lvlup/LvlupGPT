import logging

from autogpt.core.configuration import SystemConfiguration, UserConfigurable
from autogpt.core.planning.schema import Task, TaskType
from autogpt.core.prompting import PromptStrategy
from autogpt.core.prompting.schema import ChatPrompt, LanguageModelClassification
from autogpt.core.prompting.utils import json_loads, to_numbered_list
from autogpt.core.resource.model_providers import (
    AssistantChatMessage,
    ChatMessage,
    CompletionModelFunction,
)
from autogpt.core.utils.json_schema import JSONSchema

# Initialize the logger for this module
logger = logging.getLogger(__name__)

class InitialPlanConfiguration(SystemConfiguration):
    """Configuration for the InitialPlan class.

    Attributes:
        model_classification (LanguageModelClassification): The classification
            of the language model.
        system_prompt_template (str): The template for the system prompt.
        system_info (list[str]): The system information to include in the prompt.
        user_prompt_template (str): The template for the user prompt.
        create_plan_function (dict): The function for creating the initial plan.
    """
    def __init__(
        self,
        model_classification: LanguageModelClassification,
        system_prompt_template: str,
        system_info: list[str],
        user_prompt_template: str,
        create_plan_function: dict,
    ):
        """Initialize the InitialPlanConfiguration object.

        Args:
            model_classification (LanguageModelClassification): The classification
                of the language model.
            system_prompt_template (str): The template for the system prompt.
            system_info (list[str]): The system information to include in the prompt.
            user_prompt_template (str): The template for the user prompt.
            create_plan_function (dict): The function for creating the initial plan.
        """
        self.model_classification = model_classification
        self.system_prompt_template = system_prompt_template
        self.system_info = system_info
        self.user_prompt_template = user_prompt_template
        self.create_plan_function = create_plan_function

class InitialPlan(PromptStrategy):
    """Strategy for creating an initial plan for an autonomous agent.

    The InitialPlan class has several default configurations for the prompt template,
    system information, user prompt template, and the function for creating the plan.

    Attributes:
        DEFAULT_SYSTEM_PROMPT_TEMPLATE (str): The default template for the system prompt.
        DEFAULT_SYSTEM_INFO (list[str]): The default system information to include
            in the prompt.
        DEFAULT_USER_PROMPT_TEMPLATE (str): The default template for the user prompt.
        DEFAULT_CREATE_PLAN_FUNCTION (CompletionModelFunction): The default function
            for creating the initial plan.
        default_configuration (InitialPlanConfiguration): The default configuration
            for the InitialPlan class.
    """
    DEFAULT_SYSTEM_PROMPT_TEMPLATE = (
        "You are an expert project planner. "
        "Your responsibility is to create work plans for autonomous agents. "
        # ...
    )

    DEFAULT_SYSTEM_INFO = [
        "The OS you are running on is: {os_info}",
        # ...
    ]

    DEFAULT_USER_PROMPT_TEMPLATE = (
        "You are {agent_name}, {agent_role}\n" "Your goals are:\n" "{agent_goals}"
    )

    DEFAULT_CREATE_PLAN_FUNCTION = CompletionModelFunction(
        # ...
    )

    default_configuration = InitialPlanConfiguration(
        model_classification=LanguageModelClassification.SMART_MODEL,
        system_prompt_template=DEFAULT_SYSTEM_PROMPT_TEMPLATE,
        system_info=DEFAULT_SYSTEM_INFO,
        user_prompt_template=DEFAULT_USER_PROMPT_TEMPLATE,
        create_plan_function=DEFAULT_CREATE_PLAN_FUNCTION.schema,
    )

    def __init__(
        self,
        model_classification: LanguageModelClassification,
        system_prompt_template: str,
        system_info: list[str],
        user_prompt_template: str,
        create_plan_function: dict,
    ):
        """Initialize the InitialPlan object.

        Args:
            model_classification (LanguageModelClassification): The classification
                of the language model.
            system_prompt_template (str): The template for the system prompt.
            system_info (list[str]): The system information to include in the prompt.
            user_prompt_template (str): The template for the user prompt.
            create_plan_function (dict): The function for creating the initial plan.
        """
        self._model_classification = model_classification
        self._system_prompt_template = system_prompt_template
       
