import logging
from collections.abc import Callable
from typing import (
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
from __future__ import annotations

import autogpt.core.ability.base
import autogpt.core.ability.schema
import autogpt.core.configuration
import autogpt.core.memory.base
import autogpt.core.plugin.simple
import autogpt.core.resource.model_providers
import autogpt.core.workspace.base

T = TypeVar("T")


class AbilityRegistryConfiguration(autogpt.core.configuration.SystemConfiguration):
    abilities: Dict[str, autogpt.core.ability.base.AbilityConfiguration]

    def __repr__(self) -> str:
        return f"AbilityRegistryConfiguration(abilities={self.abilities!r})"


class AbilityRegistrySettings(autogpt.core.configuration.SystemSettings):
    configuration: AbilityRegistryConfiguration


class SimpleAbilityRegistry(AbilityRegistry, autogpt.core.configuration.Configurable):
    default_settings: ClassVar[AbilityRegistrySettings] = AbilityRegistrySettings(
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
    ) -> None:
        super().__init__(settings=settings)
        self._logger = logger
        self._memory = memory
        self._workspace = workspace
        self._model_providers = model_providers
        self._abilities: List[autogpt.core.ability.base.Ability[Any]] = []
        for ability_name, ability_configuration in self._configuration.abilities.items():
            self.register_ability(ability_name, ability_configuration)

    def register_ability(
        self, ability_name: str, ability_configuration: autogpt.core.ability.base.AbilityConfiguration
    ) -> None:
        ability_class: Type[autogpt.core.ability.base.Ability[Any]] = autogpt.core.plugin.simple.SimplePluginService.get_plugin(ability_configuration.location)
        ability_args: Dict[str, Any] = {
            "logger": self._logger.getChild(ability_name),
            "configuration": ability_configuration,
        }
        if ability_configuration.packages_required:
            # TODO: Check packages are installed and maybe install them.
            pass
        if ability_configuration.memory_provider_required:
            ability_args["memory"] = self._memory
        if ability_configuration.workspace_required:
            ability_args["workspace"] = self._workspace
        if ability_configuration.language_model_required:
            ability_args["language_model_provider"] = self._model_providers[ability_configuration.language_model_required.provider_name]
        ability: autogpt.core.ability.base.Ability[Any] = ability_class(**ability_args)
        self._abilities.append(ability)

    def list_abilities(self) -> List[str]:
        return [f"{ability.name()}: {ability.description}" for ability in self._abilities]

    def dump_abilities(self) -> List[autogpt.core.ability.schema.CompletionModelFunction]:
        return [ability.spec for ability in self._abilities]

    def get_ability(self, ability_name: str) -> autogpt.core.ability.base.Ability[Any]:
        for ability in self._abilities:
            if ability.name() == ability_name:
                return ability
        raise ValueError(f"Ability '{ability_name}' not found.")

    def perform(self, ability_name: str, **kwargs) -> autogpt.core.ability.schema.AbilityResult:
        ability = self.get_ability(ability_name)
        return ability(**kwargs)
