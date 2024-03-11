from __future__ import annotations

from typing import Iterator, Optional

from autogpt.config.config import Config
from .. import MemoryItem
from .base import VectorMemoryProvider

class NoMemory(VectorMemoryProvider):
    """
    A class that does not store any data. This is the default memory provider.

    This class is intended to be used as a placeholder memory provider when no other memory provider is specified.
    It does not store any data, and all methods that attempt to add, retrieve, or modify data will have no effect.

    Attributes:
        config (Optional[Config]): Optional configuration object for the memory provider.

    Methods:
        __iter__(): Iterator[MemoryItem]: An iterator that returns no MemoryItems.
        __contains__(x: MemoryItem) -> bool: Returns False, indicating that no MemoryItems are present in the provider.
        __len__() -> int: Returns 0, indicating that there are no MemoryItems in the provider.
        add(item: MemoryItem): Does nothing.
        discard(item: MemoryItem): Does nothing.
        clear(): Does nothing.
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initializes a new instance of the NoMemory class.

        Args:
            config (Optional[Config], optional): Optional configuration object for the memory provider. Defaults to None.
        """
        pass

    def __iter__(self) -> Iterator[MemoryItem]:
        """
        Returns an iterator that returns no MemoryItems.

        Returns:
            Iterator[MemoryItem]: An iterator that returns no MemoryItems.
        """
        return iter([])

    def __contains__(self, x: MemoryItem) -> bool:
        """
        Returns False, indicating that no MemoryItems are present in the provider.

        Args:
            x (MemoryItem): The MemoryItem to check for presence in the provider.

        Returns:
            bool: False, indicating that the MemoryItem is not present in the provider.
        """
        return False
