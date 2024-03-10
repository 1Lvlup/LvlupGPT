import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from forge.sdk.db import (
    AgentDB,
    ArtifactModel,
    StepModel,
    TaskModel,
    convert_to_artifact,
    convert_to_step,
    convert_to_task,
)
from forge.sdk.errors import NotFoundError as DataNotFoundError
from forge.sdk.model import (
    Artifact,
    Status,
    Step,
    StepInput,
    StepRequestBody,
    Task,
)

pytestmark = pytest.mark.asyncio

Base = declarative_base()


class TestDatabase(AgentDB):
    def __init__(self, db_name: str):
        engine = create_engine(db_name)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        super().__init__(SessionLocal, engine)


@pytestmark.mark.asyncio
def test_table_creation(test_database: TestDatabase) -> None:
    # Test for tasks table existence
    assert (
        test_database.session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'").fetchone()
        is not None
    )

    # Test for steps table existence
    assert (
        test_database.session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='steps'").fetchone()
        is not None
    )

    # Test for artifacts table existence
    assert (
        test_database.session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artifacts'").fetchone()
        is not None
    )


@pytestmark.mark.asyncio
async def test_task_schema(test_database: TestDatabase) -> None:
    now = datetime.now()
    task = Task(
        task_id="50da533e-3904-4401-8a07-c49adf88b5eb",
        input="Write the words you receive to the file 'output.txt'.",
        created_at=now,
        modified_at=now,
        artifacts=[
            Artifact(
                artifact_id="b225e278-8b4c-4f99-a696-8facf19f0e56",
                agent_created=True,
                file_name="main.py",
                relative_path="python/code/",
                created_at=now,
                modified_at=now,
            )
        ],
    )

    assert task.task_id == "50da533e-3904-4401-8a07-c49adf88b5eb"
    assert task.input == "Write the words you receive to the file 'output.txt'."
    assert len(task.artifacts) == 1
    assert task.artifacts[0].artifact_id == "b225e278-8b4c-4f99-a696-8facf19f0e56"


@pytestmark.mark.asyncio
async def test_step_schema(test_database: TestDatabase) -> None:
    now = datetime.now()
    step = Step(
        task_id="50da533e-3904-4401-8a07-c49adf88b5eb",
        step_id="6bb1801a-fd80-45e8-899a-4dd723cc602e",
        created_at=now,
        modified_at=now,
        name="Write to file",
        input="Write the words you receive to the file 'output.txt'.",
        status=Status.created,
        output="I am going to use the write_to_file command and write Washington to a file called output.txt <write_to_file('output.txt', 'Washington')>",
        artifacts=[
            Artifact(
                artifact_id="b225e278-8b4c-4f99-a696-8facf19f0e56",
                file_name="main.py",
                relative_path="python/code/",
                created_at=now,
                modified_at=now,
                agent_created=True,
            )
        ],
        is_last=False,
    )

    assert step.task_id == "50da533e-3904-4401-8a07-c49adf88b5eb"
    assert step.step_id == "6bb1801a-fd80-45e8-899a-4dd723cc602e"
    assert step.name == "Write to file"
    assert step.status == Status.created
    assert (
        step.output
        == "I am going to use the write_to_file command and write Washington to a file called output.txt <write_to_file('output.txt', 'Washington')>"
    )
    assert len(step.artifacts) == 1
    assert step.artifacts[0].artifact_id == "b225e278-8b4c-4f99-a696-8facf19f0e56"
    assert step.is_last == False


@pytestmark
