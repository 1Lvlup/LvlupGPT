"""The command system provides a way to extend the functionality of the AI agent.

This module contains the base classes and configurations for abilities and the
ability registry.
"""
from autogpt.core.ability.base import Ability, AbilityConfiguration, AbilityRegistry, AbilityResult
from autogpt.core.ability.simple import (
    AbilityRegistryConfiguration,
    SimpleAbilityRegistry,
)

__all__ = [
    "Ability",
    "AbilityConfiguration",
    "AbilityRegistry",
    "AbilityResult",
    "AbilityRegistryConfiguration",
    "SimpleAbilityRegistry",
]
