import numpy as np
from typing import Any

import pytest
from pytest_mock import MockerFixture

import autogpt.memory.vector.memory_item as vector_memory_item
import autogpt.memory.vector.providers.base as memory_provider_base
from autogpt.config.config import Config
from autogpt.core.resource.model_providers import OPEN_AI_EMBEDDING_MODELS
from autogpt.memory.vector import get_memory
from autogpt.memory.vector.utils import Embedding

