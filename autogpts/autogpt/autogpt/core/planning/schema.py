import enum  # Importing enum for creating enumerated types
from typing import Optional  # Importing Optional for specifying optional types

from pydantic import BaseModel, Field  # Importing BaseModel and Field for defining data models

from autogpt.core.ability.schema import AbilityResult  # Importing AbilityResult from another module

# Defining an enumerated type for TaskType with possible values: RESEARCH, WRITE, EDIT, CODE, DESIGN, TEST, PLAN
class TaskType(str, enum.Enum):
    RESEARCH = "research"
    WRITE = "write"
    EDIT = "edit"
    CODE = "code"
    DESIGN = "design"
    TEST = "test"
    PLAN = "plan"

# Defining an enumerated type for TaskStatus with possible values: BACKLOG, READY, IN_PROGRESS, DONE
class TaskStatus(str, enum.Enum):
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"

# Defining TaskContext data model with the following attributes:
# cycle_count: int, default value 0
# status: TaskStatus, default value BACKLOG
# parent: Optional[Task], default value None
# prior_actions: list[AbilityResult], default value empty list
# memories: list, default value empty list
# user_input: list[str], default value empty list
# supplementary_info: list[str], default value empty list
# enough_info: bool, default value False
class TaskContext(BaseModel):
    cycle_count: int = 0
    status: TaskStatus = TaskStatus.BACKLOG
    parent: Optional["Task"] = None
    prior_actions: list[AbilityResult] = Field(default_factory=list)
    memories: list = Field(default_factory=list)
    user_input: list[str] = Field(default_factory=list)
    supplementary_info: list[str] = Field(default_factory=list)
    enough_info: bool =
