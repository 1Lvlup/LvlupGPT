"""The memory subsystem manages the Agent's long-term memory."""
from typing import Dict, Any

class MemorySettings:
    """Settings for managing memory behavior."""

    def __init__(self, capacity: int = 100):
        """
        Initialize MemorySettings.

        :param capacity: The maximum number of memories that can be stored. Defaults to 100.
        """
        self.capacity = capacity

