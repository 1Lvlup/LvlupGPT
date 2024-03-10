import enum
from typing import Any, Dict

from pydantic import BaseModel

class ContentType(str, enum.Enum):
    """Content type enumeration."""
    TEXT = "text"
    CODE = "code"

class Knowledge(BaseModel):
    """Knowledge model for storing content and metadata."""
    content: str
    content_type: ContentType
    content_metadata: Dict[str, Any]

class AbilityResult(BaseModel):
    """The AbilityResult is a standard response struct for an ability."""

    ability_name: str
    ability_args: Dict[str, str]
    success: bool
    message: str
    new_knowledge: Knowledge = None

    @property
    def summary(self) -> str:
        """Return a summary of the ability result."""
        kwargs = ", ".join(f"{k}={v}" for k, v in self.ability_args.items())
        return f"{self.ability_name}({kwargs}): {self.message}"
