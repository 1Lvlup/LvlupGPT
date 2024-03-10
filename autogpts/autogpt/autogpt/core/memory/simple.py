import json
import logging
from pathlib import Path
from collections import deque
from typing import Any, Dict, List, Optional

class MemoryConfiguration(typing.TypedDict):
    name: str
    description: str

class MemorySettings(typing.TypedDict):
    configuration: MemoryConfiguration

class MessageHistory:
    def __init__(self, previous_message_history: List[str]):
        self._message_history = deque(previous_message_history, maxlen=100)

    def add_message(self, message: str):
        self._message_history.append(message)

    def get_messages(self) -> List[str]:
        return list(self._message_history)

