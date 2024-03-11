"""The Agent module contains classes and settings related to the autonomous agent.

The `Agent` class is the base class for all agents, representing an autonomous entity
guided by a LLM (Language Learning Model) provider.

The `AgentSettings` class is used to configure the behavior of an agent.

The `SimpleAgent` class is a simple implementation of an agent, using the `Agent`
base class and `AgentSettings` for configuration.

"""
from autogpt.core.agent.base import Agent  # Base class for all agents
from autogpt.core.agent.simple import SimpleAgent  # Simple implementation of an agent

__all__ = [
    "Agent",
    "AgentSettings",
    "SimpleAgent",
]

