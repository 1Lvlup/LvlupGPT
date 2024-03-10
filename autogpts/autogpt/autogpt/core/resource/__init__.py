"""Module containing various provider and resource related schema classes.

This module contains classes representing various schema for providers and
resources used in the autogpt project.
"""

from typing import List

class ProviderBudget:
    """Schema class for provider budget."""

    # Add attributes and methods here
    pass

class ProviderCredentials:
    """Schema class for provider credentials."""

    # Add attributes and methods here
    pass

class ProviderSettings:
    """Schema class for provider settings."""

    # Add attributes and methods here
    pass

class ProviderUsage:
    """Schema class for provider usage."""

    # Add attributes and methods here
    pass

class ResourceType:
    """Schema class for resource types."""

    # Add attributes and methods here
    pass


__all__ = [
    "ProviderBudget",
    "ProviderCredentials",
    "ProviderSettings",
    "ProviderUsage",
    "ResourceType",
]


from .schema import (
    ProviderBudget,
    ProviderCredentials,
    ProviderSettings,
    ProviderUsage,
    ResourceType,
)

__all__ = [
    "ProviderBudget",

