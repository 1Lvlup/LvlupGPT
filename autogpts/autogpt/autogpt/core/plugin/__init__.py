"""The plugin system allows the Agent to be extended with new functionality."""
from autogpt.core.plugin.base import Plugin
from typing import List

class PluginService:
    """A service for managing plugins in the AutoGPT system."""

    def __init__(self):
        """Initialize the PluginService with an empty list of plugins."""
        self.plugins: List[Plugin] = []

    def load_plugins(self, plugin_paths: List[str]) -> None:
        """Load plugins from the given paths.

        Args:
            plugin_paths (List[str]): A list of file paths to the plugin modules.
        """
        # Implement the logic to load plugins from the given paths
        pass

    def enable_plugin(self, plugin: Plugin) -> None:
        """Enable the given plugin.

        Args:
            plugin (Plugin): The plugin to enable.
        """
        self.plugins.append(plugin)

    def disable_plugin(self, plugin: Plugin) -> None:
        """Disable the given plugin.

        Args:
            plugin (Plugin): The plugin to disable.
        """
        self.plugins.remove(plugin)

    def execute_plugin_action(self, plugin_name: str, action_name: str, *args, **kwargs) -> any:
        """Execute an action on the specified plugin.

        Args:
            plugin_name (str): The name of the plugin.
            action_name (str): The name of the action.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            any: The result of the action execution.
        """
        # Implement the logic to find the plugin and execute the action
        pass
