"""
Routes for the Agent Service.
"""
import json
from typing import Optional

from fastapi import APIRouter, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse
from forge.sdk.errors import NotFoundError, ForgeSDKError
from forge.sdk.forge_log import ForgeLogger
from forge.sdk.model import (
    # Importing Task, TaskRequestBody, TaskListResponse, TaskStepsListResponse, 
    # Step, StepRequestBody, TaskArtifactsListResponse, Artifact classes
    # from the forge.sdk.model module.
    # These classes are used to represent tasks, steps, and artifacts in the AutoGPT Forge system.
    
)

router = APIRouter()
LOG = ForgeLogger(__name__)


@router.get("/", tags=["root"])
async def root():
    """
    Root endpoint that returns a welcome message.
    This endpoint is the entry point for the API and greets the user with a welcome message.
    """
    return Response(content="Welcome to the AutoGPT Forge")


@router.get("/heartbeat", tags=["server"])
async def check_server_status():
    """
    Check if the server is running.
    This endpoint is used to check if the server is up and running by returning a success message with a 200 status code.
    """
    return Response(content="Server is running.", status_code=200)


@router.post("/agent/tasks", tags=["agent"], response_model=Task)
async def create_agent_task(request: Request, task_request: TaskRequestBody) -> Task:
    """
    Create a new agent task.
    This endpoint is used to create a new task for the AutoGPT agent by accepting a TaskRequestBody object in the request body.
    The function returns the created Task object.
    """
    ...


@router.get("/agent/tasks", tags=["agent"], response_model=TaskListResponse)
async def list_agent_tasks(
    request: Request,
    page: Optional[int] = Query(1, ge=1),
    page_size: Optional[int] = Query(10, ge=1),
) -> TaskListResponse:
    """
    List agent tasks with pagination.
    This endpoint is used to retrieve a list of tasks for the AutoGPT agent with pagination support.
    The page and page_size query parameters are used to control the pagination.
    The function returns a TaskListResponse object containing the list of tasks.
    """
    ...


@router.get("/agent/tasks/{task_id}", tags=["agent"], response_model=Task)
async def get_agent_task(request: Request, task_id: str) -> Task:
    """
    Get an agent task by ID.
    This endpoint is used to retrieve the details of a specific task for the AutoGPT agent using its unique identifier.
    The function returns the Task object corresponding to the given task_id.
    """
    ...


@router.get(
    "/agent/tasks/{task_id}/steps",
    tags=["agent"],
    response_model=TaskStepsListResponse,
)
async def list_agent_task_steps(
    request: Request,
    task_id: str,
    page: Optional[int] = Query(1, ge=1),
    page_size: Optional[int] = Query(10, ge=1),
) -> TaskStepsListResponse:
    """
    List agent task steps with pagination.
    This endpoint is used to retrieve a list of steps for a specific task of the AutoGPT agent with pagination support.
    The page and page_size query parameters are used to control the pagination.
    The function returns a TaskStepsListResponse object containing the list of steps.
    """
    ...


@router.post(
    "/agent/tasks/{task_id}/steps", tags=["agent"], response_model=Step
)
async def execute_agent_task_step(
    request: Request, task_id: str, step: Optional[StepRequestBody] = None
) -> Step:
    """
    Execute an agent task step.
    This endpoint is used to execute a specific step of a task for the AutoGPT agent.
    The step (if provided) is included in the request body.
    The function returns the Step object corresponding to the executed step.
    """
    ...


@router.get(
    "/agent/tasks/{task_id}/steps/{step_id}", tags=["agent"], response_model=Step
)
async def get_agent_task_step(request: Request, task_id: str, step_id: str) -> Step:
    """
    Get an agent task step by ID.
    This endpoint is used to retrieve the details of a specific step of a task for the AutoGPT agent using its unique identifiers.
    The function returns the Step object corresponding to the given task_id
