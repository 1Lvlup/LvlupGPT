from enum import Enum
from typing import Literal

import pydantic

# Define an Enum for difficulty levels
class DifficultyLevel(str, Enum):
    """
    Enum class for difficulty levels with predefined values.
    """
    INTERFACE = "interface"
    BASIC = "basic"
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

