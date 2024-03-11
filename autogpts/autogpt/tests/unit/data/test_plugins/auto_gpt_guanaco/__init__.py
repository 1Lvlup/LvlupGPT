"""This is the Test plugin for AutoGPT."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar

from auto_gpt_plugin_template import AutoGPTPluginTemplate

PromptGenerator = TypeVar("PromptGenerator")

class AutoGPTGuanaco(AutoGPTPluginTemplate):
    """
    This is plugin for AutoGPT.
    """
    def __init__(self):
        super().__init__()
        # Set the name of the plugin
        self._name = "AutoGPT-Guanaco"
        # Set the version of the plugin
        self._version = "0.1.0"
        # Set the description of the plugin
        self._description = "This is a Guanaco local model plugin."

    def can_handle_on_response(self) -> bool:
        """
        This method checks if the plugin can handle the on_response method.

        Returns:
            bool: True if the plugin can handle the on_response method.
        """
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        """
        This method is called when a response is received from the model.
        If the response is not empty, it prints "OMG OMG It's Alive!",
        otherwise it prints "Is it alive?".

        Args:
            response (str): The response from the model.

        Returns:
            str: The response from the model.
        """
        if len(response):
            print("OMG OMG It's Alive!")
        else:
            print("Is it alive?")
        return response

    def can_handle_post_prompt(self) -> bool:
        """
        This method checks if the plugin can handle the post_prompt method.

        Returns:
            bool: True if the plugin can handle the post_prompt method.
        """
        return False

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """
        This method is called just after the generate_prompt is called,
        but actually before the prompt is generated.

        Args:
            prompt (PromptGenerator): The prompt generator.

        Returns:
            PromptGenerator: The prompt generator.
        """
        return prompt

    def can_handle_on_planning(self) -> bool:
        """
        This method checks if the plugin can handle the on_planning method.

        Returns:
            bool: True if the plugin can handle the on_planning method.
        """
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[str]
    ) -> Optional[str]:
        """
        This method is called before the planning chat completion is done.

        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.

        Returns:
            Optional[str]: The resulting message.
        """

    def can_handle_post_planning(self) -> bool:
        """
        This method checks if the plugin can handle the post_planning method.

        Returns:
            bool: True if the plugin can handle the post_planning method.
        """
        return False

    def post_planning(self, response: str) -> str:
        """
        This method is called after the planning chat completion is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """

    def can_handle_pre_instruction(self) -> bool:
        """
        This method checks if the plugin can handle the pre_instruction method.

        Returns:
            bool: True if the plugin can handle the pre_instruction method.
        """
        return False

    def pre_instruction(self, messages: List[str]) -> List[str]:
        """
        This method is called before the instruction chat is done.

        Args:
            messages (List[str]): The list of context messages.

        Returns:
            List[str]: The resulting list of messages.
        """

    def can_handle_on_instruction(self) -> bool:
        """
        This method checks if the plugin can handle the on_instruction method.

        Returns:
            bool: True if the plugin can handle the on_instruction method.
        """
        return False

    def on_instruction(self, messages: List[str]) -> Optional[str]:
        """
        This method is called when the instruction chat is done.

        Args:
            messages (List[str]): The list of context messages.

        Returns:
            Optional[str]: The resulting message.
        """

    def can_handle_post_instruction(self) -> bool:
        """
        This method checks if the plugin can handle the post_instruction method.

        Returns:
            bool: True if the plugin can handle the post_instruction method.
        """
        return False

    def post_instruction(self, response: str) -> str:
        """
        This method is called after the instruction chat is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """

    def can_handle_pre_command(self) -> bool:
        """
        This method checks if the plugin can handle the pre_command method.

        Returns:
            bool: True if the plugin can handle the pre_command method.
        """
        return False

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """
        This method is called before the command is executed.

        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.

        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """

    def can_handle_post_command(self) -> bool:
        """
        This method checks if the plugin can handle the post_command method.
