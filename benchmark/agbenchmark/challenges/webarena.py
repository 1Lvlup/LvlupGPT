import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Iterator, List, Literal, NamedTuple, Optional, Union

import pytest
import requests
from agent_protocol_client import AgentApi, Step
from pydantic import BaseModel, ValidationError, validator

from agbenchmark.config import AgentBenchmarkConfig
from agbenchmark.utils.data_types import Category

logger = logging.getLogger(__name__)


class EvalType(Enum):
    STRING_MATCH = "string_match"
    URL_MATCH = "url_match"
    PROGRAM_HTML = "program_html"


class WebArenaSite(Enum):
    GITLAB = "gitlab"
    MAP = "map"
    REDDIT = "reddit"
    SHOPPING = "shopping"
    SHOPPING_ADMIN = "shopping_admin"
    WIKIPEDIA = "wikipedia"


class ReferenceAnswerType(Enum):
    EXACT_MATCH = "exact_match"
    FUZZY_MATCH = "fuzzy_match"
    MUST_INCLUDE = "must_include"


