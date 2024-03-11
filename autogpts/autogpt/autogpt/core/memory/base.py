import abc

# Define a abstract base class named Memory
class Memory(abc.ABC):
    """
    A abstract base class that defines the interface for memory-related operations.
    """
    pass


# Define a abstract base class named MemoryItem
class MemoryItem(abc.ABC):
    """
    A abstract base class that defines the interface for individual memory items.
    """
    pass


# Define a abstract base class named MessageHistory
class MessageHistory(abc.ABC):
    """
    A abstract base class that defines the interface for storing and managing message histories.
    """
    pass
