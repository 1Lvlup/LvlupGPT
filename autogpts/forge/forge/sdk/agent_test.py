import pytest
from typing import List, Optional
from unittest.mock import AsyncMock, patch

from .agent import Agent
from .db import AgentDB
from .model import (
    Artifact,
    ArtifactRequestBody,
    Step,
    StepRequestBody,
    Task,
    TaskListResponse,
    TaskRequestBody,
)
from .workspace import LocalWorkspace


@pytest.fixture
def agent():
    db = AgentDB("sqlite:///test.db")
    workspace = LocalWorkspace("./test_workspace")
    agent = Agent(db, workspace)
    # Patch list_artifacts to avoid actual database access
    agent.list_artifacts = AsyncMock(return_value=[])
    return agent


@pytest.mark.asyncio
async def test_create_task(agent: Agent):
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task: Task = await agent.create_task(task_request)
    assert task.input == "test_input"


@pytest.mark.asyncio
async def test_list_tasks(agent: Agent):
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)
    tasks = await agent.list_tasks()
    assert isinstance(tasks, TaskListResponse)


@pytest.mark.asyncio
async def test_get_task(agent: Agent):
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)
    retrieved_task = await agent.get_task(task.task_id)
    assert retrieved_task.task_id == task.task_id


@pytest.mark.asyncio
async def test_create_and_execute_step(agent: Agent):
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)
    step_request = StepRequestBody(
        input="step_input", additional_input={"input": "additional_test_input"}
    )
    step = await agent.create_and_execute_step(task.task_id, step_request)
    assert step.input == "step_input"
    assert step.additional_input == {"input": "additional_test_input"}


@pytest.mark.asyncio
async def test_get_step(agent: Agent):
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)
    step_request = StepRequestBody(
        input="step_input", additional_input={"input": "additional_test_input"}
    )
    step = await agent.create_and_execute_step(task.task_id, step_request)
    retrieved_step = await agent.get_step(task.task_id, step.step_id)
    assert retrieved_step.step_id == step.step_id


@pytest.mark.asyncio
async def test_list_artifacts(agent: Agent):
    artifacts = await agent.list_artifacts()
    assert isinstance(artifacts, List[Artifact])


@pytest.mark.asyncio
async def test_create_artifact(agent: Agent):
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)
    artifact_request = ArtifactRequestBody(file=None, uri="test_uri")
    artifact = await agent.create_artifact(task.task_id, artifact_request)
    assert artifact.uri == "test_uri"


@pytest.mark.asyncio
async def test_get_artifact(agent: Agent):
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)
    artifact_request = ArtifactRequestBody(file=None, uri="test_uri")
    artifact = await agent.create_artifact(task.task_id, artifact_request)
    with patch("pathlib.Path.exists", return_value=True):
        retrieved_artifact = await agent.get_artifact(task.task_id, artifact.artifact_id)
    assert retrieved_artifact.artifact_id == artifact.artifact_id
