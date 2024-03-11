import logging  # Import the logging module to handle logging
from collections.abc import Callable  # Import the Callable type hint for callable objects
from typing import (  # Import various type hints from the typing module
    Any,
    ClassVar,
    Dict,
    Final,
    List,
    Literal,
    NoReturn,
    Optional,
    Type,
    TypeVar,
)
from __future__ import annotations  # Import the annotations type hint for type checking

import autogpt.core.ability.base  # Import the base Ability class
import autogpt.core.ability.schema  # Import the Ability schema
import autogpt.core.configuration  # Import the Configuration and Settings classes
import autogpt.core.memory.base  # Import the Memory base class
import autogpt.core.plugin.simple  # Import the SimplePluginService class
import autogpt.core.resource.model_providers  # Import the ModelProvider and ChatModelProvider classes
import autogpt.core.workspace.base  # Import the Workspace base class

T = TypeVar("T")  # Define a type variable T for use with type hints

class AbilityRegistryConfiguration(autogpt.core.configuration.SystemConfiguration):  # Define the AbilityRegistryConfiguration class
    abilities: Dict[str, autogpt.core.ability.base.AbilityConfiguration]  # A dictionary of ability configurations

    def __repr__(self) -> str:  # Define the __repr__ method to provide a string representation of the object
        return f"AbilityRegistryConfiguration(abilities={self.abilities!r})"

class AbilityRegistrySettings(autogpt.core.configuration.SystemSettings):  # Define the AbilityRegistrySettings class
    configuration: AbilityRegistryConfiguration  # The configuration for the ability registry

class SimpleAbilityRegistry(AbilityRegistry, autogpt.core.configuration.Configurable):  # Define the SimpleAbilityRegistry class
    default_settings: ClassVar[AbilityRegistrySettings] = AbilityRegistrySettings(  # Define the default settings for the registry
        name="simple_ability_registry",
        description="A simple ability registry.",
        configuration=AbilityRegistryConfiguration(
            abilities={
                ability_name: ability.default_configuration
                for ability_name, ability in BUILTIN_ABILITIES.items()
            },
        ),
    )

    def __init__(
        self,
        settings: AbilityRegistrySettings,
        logger: logging.Logger,
        memory: autogpt.core.memory.base.Memory,
        workspace: autogpt.core.workspace.base.Workspace,
        model_providers: Dict[autogpt.core.resource.model_providers.ModelProviderName, autogpt.core.resource.model_providers.ChatModelProvider],
    ) -> None:  # Define the constructor for the SimpleAbilityRegistry class
        super().__init__(settings=settings)  # Call the constructor of the parent class
        self._logger = logger  # Set the logger
        self._memory = memory  # Set the memory
        self._workspace = workspace  # Set the workspace
        self._model_providers = model_providers  # Set the model providers
        self._abilities: List[autogpt.core.ability.base.Ability[Any]] = []  # Initialize the list of abilities
        for ability_name, ability_configuration in self._configuration.abilities.items():
            self.register_ability(ability_name, ability_configuration)  # Register each ability

    def register_ability(
        self, ability_name: str, ability_configuration: autogpt.core.ability.base.AbilityConfiguration
    ) -> None:  # Define the register_ability method
        ability_class: Type[autogpt.core.ability.base.Ability[Any]] = autogpt.core.plugin.simple.SimplePluginService.get_plugin(ability_configuration.location)  # Get the ability class from the plugin service
        ability_args: Dict[str, Any] = {  # Initialize the arguments for the ability
            "logger": self._logger.getChild(ability_name),
            "configuration": ability_configuration,
        }
        if ability_configuration.packages_required:
            # TODO: Check packages are installed and maybe install them.
            pass
        if ability_configuration.memory_provider_required:
            ability_args["memory"] = self._memory  # Add the memory provider to the arguments
        if ability_configuration.workspace_required:
            ability_args["workspace"] = self._workspace  # Add the workspace to the arguments
        if ability_configuration.language_model_required:
            ability_args["language_model_provider"] = self._model_providers[ability_configuration.language_model_required.provider_name]  # Add the language model provider to the arguments
        ability: autogpt.core.ability.base.Ability[Any] = ability_class(**ability_args)  # Create the ability instance
        self._abilities.append(ability)  # Add the ability to the list of abilities

    def list_abilities(self) -> List[str]:  # Define the list_abilities method
        return [f"{ability.name()}: {ability.description}" for ability in self._abilities]  # Return a list of strings describing each ability

    def dump_abilities(self) -> List[autogpt.core.ability.schema.CompletionModelFunction]:  # Define the dump_abilities method
        return [ability.spec for ability in self._abilities]  # Return a list of ability specifications

    def get_ability(self, ability_name: str) -> autogpt.core.ability.base.Ability[Any]:  # Define the get_ability method
        for ability in self._abilities:
            if ability.name() == ability_name:
                return ability
        raise ValueError(f"Ability '{ability_name}' not
