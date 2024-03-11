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
    """
    A pytest fixture to create an instance of the Agent class with a mock database and workspace.
    The list_artifacts method is patched to avoid actual database access.
    """
    db = AgentDB("sqlite:///test.db")  # Create a new AgentDB instance
    workspace = LocalWorkspace("./test_workspace")  # Create a new LocalWorkspace instance
    agent = Agent(db, workspace)  # Create an Agent instance with the database and workspace

    # Patch list_artifacts to avoid actual database access
    agent.list_artifacts = AsyncMock(return_value=[])
    return agent


@pytest.mark.asyncio
async def test_create_task(agent: Agent):
    """
    Test the create_task method of the Agent class.
    It creates a new task with the given TaskRequestBody and checks if the input is correct.
    """
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task: Task = await agent.create_task(task_request)  # Create a new task
    assert task.input == "test_input"  # Check if the input is correct


@pytest.mark.asyncio
async def test_list_tasks(agent: Agent):
    """
    Test the list_tasks method of the Agent class.
    It lists all tasks and checks if the response is an instance of TaskListResponse.
    """
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)  # Create a new task
    tasks = await agent.list_tasks()  # List all tasks
    assert isinstance(tasks, TaskListResponse)  # Check if the response is an instance of TaskListResponse


@pytest.mark.asyncio
async def test_get_task(agent: Agent):
    """
    Test the get_task method of the Agent class.
    It retrieves a task by its task_id and checks if the task_id is correct.
    """
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)  # Create a new task
    retrieved_task = await agent.get_task(task.task_id)  # Retrieve the task
    assert retrieved_task.task_id == task.task_id  # Check if the task_id is correct


@pytest.mark.asyncio
async def test_create_and_execute_step(agent: Agent):
    """
    Test the create_and_execute_step method of the Agent class.
    It creates a new step, executes it, and checks if the input and additional_input are correct.
    """
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)  # Create a new task
    step_request = StepRequestBody(
        input="step_input", additional_input={"input": "additional_test_input"}
    )
    step = await agent.create_and_execute_step(task.task_id, step_request)  # Create and execute a new step
    assert step.input == "step_input"  # Check if the input is correct
    assert step.additional_input == {"input": "additional_test_input"}  # Check if the additional_input is correct


@pytest.mark.asyncio
async def test_get_step(agent: Agent):
    """
    Test the get_step method of the Agent class.
    It retrieves a step by its task_id and step_id and checks if the step_id is correct.
    """
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)  # Create a new task
    step_request = StepRequestBody(
        input="step_input", additional_input={"input": "additional_test_input"}
    )
    step = await agent.create_and_execute_step(task.task_id, step_request)  # Create and execute a new step
    retrieved_step = await agent.get_step(task.task_id, step.step_id)  # Retrieve the step
    assert retrieved_step.step_id == step.step_id  # Check if the step_id is correct


@pytest.mark.asyncio
async def test_list_artifacts(agent: Agent):
    """
    Test the list_artifacts method of the Agent class.
    It lists all artifacts and checks if the response is an instance of List[Artifact].
    """
    artifacts = await agent.list_artifacts()  # List all artifacts
    assert isinstance(artifacts, List[Artifact])  # Check if the response is an instance of List[Artifact]


@pytest.mark.asyncio
async def test_create_artifact(agent: Agent):
    """
    Test the create_artifact method of the Agent class.
    It creates a new artifact with the given ArtifactRequestBody and checks if the uri is correct.
    """
    task_request = TaskRequestBody(
        input="test_input", additional_input={"input": "additional_test_input"}
    )
    task = await agent.create_task(task_request)  # Create a new task
    artifact_request = ArtifactRequestBody(file=None
