import enum
from typing import Any, Dict

from pydantic import BaseModel

# Define an enumeration of content types
class ContentType(str, enum.Enum):
    """Content type enumeration."""
    TEXT = "text"
    CODE = "code"

# Define a model for storing content and metadata
class Knowledge(BaseModel):
    """Knowledge model for storing content and metadata."""
    content: str
    content_type: ContentType
    content_metadata: Dict[str, Any]

