import abc
import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

import logging
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

class PluginLocation(TypedDict):
    storage_format: Literal[
        "INSTALLED_PACKAGE",
        "FILE_SYSTEM",
        "REMOTE_URL",
    ]
    storage_route: str

class AgentSystemSettings(BaseModel):
    name: str = Field(default="simple_agent", title="Name of the agent system")
    description: str = Field(
        default="A simple agent system.", title="Description of the agent system"
    )
    configuration: "AgentConfiguration" = Field(
        default_factory=AgentConfiguration, title="Configuration of the agent system"
    )

class AgentConfiguration(BaseModel):
    name: str = Field(default="Entrepreneur-GPT", title="Name of the agent")
    role: str = Field(
        default=(
            "An AI designed to autonomously develop and run businesses with "
            "the sole goal of increasing your net worth."
        ),
        title="Role of the agent",
    )
    goals: List[str] = Field(
        default=["Increase net worth", "Grow Twitter Account"], title="Goals of the agent"
    )
    cycle_count: int = Field(default=0, title="Cycle count of the agent")
    max_task_cycle_count: int = Field(default=3, title="Maximum task cycle count")
    creation_time: Optional[str] = Field(
        default=None, title="Creation time of the agent"

