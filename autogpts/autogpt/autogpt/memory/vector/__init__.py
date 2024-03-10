from autogpt.config import Config
from .memory_item import MemoryItem, MemoryItemFactory, MemoryItemRelevance
from .providers.base import VectorMemoryProvider as VectorMemory
from .providers.json_file import JSONFileMemory
from .providers.no_memory import NoMemory

SUPPORTED_MEMORY_BACKENDS = ["json_file", "no_memory"]

try:
    from .providers.redis import RedisMemory

    SUPPORTED_MEMORY_BACKENDS.append("redis")
except ImportError:
    RedisMemory = None

# ... continue this pattern for other memory backends

def get_memory(config: Config) -> VectorMemory:
    if config.memory_backend not in SUPPORTED_MEMORY_BACKENDS:
        raise ValueError(
            f"Unknown memory backend '{config.memory_backend}'."
            " Please check your config."
        )

    if config.memory_backend == "json_file":
        return JSONFileMemory(config)
    # ... continue this pattern for other memory backends
    elif config.memory_backend == "no_memory":
        return NoMemory()
    else:
        memory = import_memory_backend(config.memory_backend)
        return memory(config)

def import_memory_backend(backend):
    """Dynamically import memory backend classes."""
    module_path = f".providers.{backend}"
    module = __import__(module_path, fromlist=[backend])
    return getattr(module, backend)

# ... continue with the rest of the code
