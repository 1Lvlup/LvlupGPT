from enum import Enum
from typing import Literal

from pydantic import BaseModel

class DifficultyLevel(str, Enum):
    INTERFACE = "interface"
    BASIC = "basic"
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    HUMAN = "human"

DIFFICULTY_MAP = {level: i for i, level in enumerate(DifficultyLevel, start=1)}
STRING_DIFFICULTY_MAP = {level.value: level for level in DifficultyLevel}

class Category(str, Enum):
    GENERALIST = "general"
    DATA = "data"
    CODING = "coding"
    SCRAPING_SYNTHESIS = "scrape_synthesize"
    WEB = "web"
    GAIA_1 = "GAIA_1"
    GAIA_2 = "GAIA_2"
    GAIA_3 = "GAIA_3"

class EvalResult(BaseModel):
    result: str
    result_source: Literal["step_output", str]
    score: float
    passed: bool
