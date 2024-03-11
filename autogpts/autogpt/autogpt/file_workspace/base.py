"""
The FileWorkspace class provides an interface for interacting with a file workspace.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from io import IOBase, TextIOBase
from pathlib import Path
from typing import IO, Any, BinaryIO, Callable, Literal, Optional, TextIO, overload

from autogpt.core.configuration.schema import SystemConfiguration

