"""Module containing various provider and resource related schema classes.

This module contains classes representing various schema for providers and
resources used in the autogpt project.
"""

from typing import List

class ProviderBudget:
    """Schema class for provider budget.

    Represents the budget-related information for a specific provider.

    Attributes:
        budget_amount (float): The total budget amount for the provider.
        used_amount (float): The amount of budget already used by the provider.
        pending_charges (float): Any pending charges that have not been processed yet.
    """

    def __init__(self, budget_amount: float, used_amount: float, pending_charges: float):
        """Initialize the ProviderBudget object.

        Args:
            budget_amount (float): The total budget amount for the provider.
            used_amount (float): The amount of budget already used by the provider.
            pending_charges (float): Any pending charges that have not been processed yet.
        """
        self.budget_amount = budget_amount
        self.used_amount = used_amount
        self.pending_charges = pending_charges

class ProviderCredentials:
    """Schema class for provider credentials.

    Represents the credentials required to authenticate with a specific provider.

    Attributes:
        api_key (str): The API key for the provider.
        api_secret (str): The API secret for the provider.
        region (str): The region where the provider is located.
    """

    def __init__(self, api_key: str, api_secret: str, region: str):
        """Initialize the ProviderCredentials object.

        Args:
            api_key (str): The API key for the provider.
            api_secret (str): The API secret for the provider.
            region (str): The region where the provider is located.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.region = region

class ProviderSettings:
    """Schema class for provider settings.

    Represents
