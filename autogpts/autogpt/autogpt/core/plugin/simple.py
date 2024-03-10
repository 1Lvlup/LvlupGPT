from importlib import import_module
from typing import TYPE_CHECKING, Any, TypeVar

from autogpt.core.plugin.base import (
    PluginLocation,
    PluginService,
    PluginStorageFormat,
    PluginStorageRoute,
)

if TYPE_CHECKING:
    from autogpt.core.plugin.base import PluginType

PluginTypeT = TypeVar("PluginTypeT", bound="PluginType")


class SimplePluginService(PluginService):
    @staticmethod
    def get_plugin(plugin_location: dict | PluginLocation) -> PluginTypeT:
        """Get a plugin from a plugin location."""
        if isinstance(plugin_location, dict):
            plugin_location = PluginLocation.from_dict(plugin_location)

        plugin = SimplePluginService._load_plugin(plugin_location)

        return plugin

    @staticmethod
    def _load_plugin(plugin_location: PluginLocation) -> PluginTypeT:
        if plugin_location.storage_format == PluginStorageFormat.WORKSPACE:
            return SimplePluginService._load_from_workspace(plugin_location)
        elif plugin_location.storage_format == PluginStorageFormat.INSTALLED_PACKAGE:
            return SimplePluginService._load_from_installed_package(plugin_location)
        else:
            raise NotImplementedError(
                f"Plugin storage format {plugin_location.storage_format} is not implemented."
            )

    @staticmethod
    def _load_from_workspace(plugin_location: PluginLocation) -> PluginTypeT:
        """Load a plugin from the workspace."""
        plugin = SimplePluginService._load_from_file_path_or_import_path(plugin_location)
        return plugin

    @staticmethod
    def _load_from_installed_package(plugin_location: PluginLocation) -> PluginTypeT:
        """Load a plugin from an installed package."""
        plugin = SimplePluginService._load_from_file_path_or_import_path(plugin_location)
        return plugin

    @staticmethod
    def _load_from_file_path(plugin_route: PluginStorageRoute) -> PluginTypeT:
        """Load a plugin from a file path."""
        # TODO: Define an on-disk storage format and implement this.
        #   Can pull from existing zip file loading implementation
        raise NotImplementedError("Loading a plugin from a file path is not implemented.")

    @staticmethod
    def _load_from_import_path(plugin_route: PluginStorageRoute) -> PluginTypeT:
        """Load a plugin from an import path."""
        module_path, _, class_name = plugin_route.rpartition(".")
        plugin = getattr(import_module(module_path), class_name)
        return plugin

    @staticmethod
    def _load_from_file_path_or_import_path(
        plugin_route: PluginStorageRoute,
    ) -> PluginTypeT:
        """Load a plugin from a file path or an import path."""
        try:
            return SimplePluginService._load_from_import_path(plugin_route)
        except Exception:
            return SimplePluginService._load_from_file_path(plugin_route)

    @staticmethod
    def _resolve_name_to_path(
        plugin_name: str, path_type: str
    ) -> PluginStorageRoute:
        """Resolve a plugin name to a plugin path."""
        if path_type == "import_path":
            return PluginStorageRoute(plugin_name)
        elif path_type == "file_path":
            # TODO: Implement a discovery system for finding plugins by name from known
            #   storage locations.
            raise NotImplementedError(
                f"Resolving plugin name {plugin_name} to a file path is not implemented."
            )
        else:
            raise ValueError(f"Unknown path_type: {path_type}")
