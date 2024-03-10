import logging
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from autogpt.logs.helpers import request_user_double_check
from autogpt.utils import validate_yaml_file

logger = logging.getLogger(__name__)

class AIDirectives(BaseModel):
    """An object that contains the basic directives for the AI prompt.

    Attributes:
        constraints (list): A list of constraints that the AI should adhere to.
        resources (list): A list of resources that the AI can utilize.
        best_practices (list): A list of best practices that the AI should follow.
    """
    resources: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    best_practices: list[str] = Field(default_factory=list)

    @staticmethod
    def from_file(prompt_settings_file: Path) -> "AIDirectives":
        validated, message = validate_yaml_file(prompt_settings_file)
        if not validated:
            logger.error(message, extra={"title": "FAILED FILE VALIDATION"})
            request_user_double_check()
            raise RuntimeError(f"File validation failed: {message}")

        with open(prompt_settings_file, encoding="utf-8") as file:
            config_params = yaml.safe_load(file)

        return AIDirectives(
            constraints=config_params.get("constraints", []),
            resources=config_params.get("resources", []),
            best_practices=config_params.get("best_practices", []),
        )

    def __add__(self, other: "AIDirectives") -> "AIDirectives":
        merged_directives = self.dict()
        merged_directives.update(other.dict())
        return AIDirectives(**merged_directives).copy(deep=True)
