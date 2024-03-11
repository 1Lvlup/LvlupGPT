import enum
from pathlib import Path
from typing import Optional

# Import custom modules for different file workspace backends
from .base import FileWorkspace

# Define an enumeration for the available file workspace backends
class FileWorkspaceBackendName(str, enum.Enum):
    LOCAL = "local"
    GCS = "gcs"
    S3 = "s3"

