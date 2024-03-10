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
    Task,
    TaskRequestBody,
    TaskListResponse,
    TaskStepsListResponse,
    Step,
    StepRequestBody,
    TaskArtifactsListResponse,
    Artifact,
)

router = APIRouter()
LOG = ForgeLogger(__name__)


@router.get("/", tags=["root"])
async def root():
    """Root endpoint that returns a welcome message."""
    return Response(content="Welcome to the AutoGPT Forge")


@router.get("/heartbeat", tags=["server"])
async def check_server_status():
    """Check if the server is running."""
    return Response(content="Server is running.", status_code=200)


@router.post("/agent/tasks", tags=["agent"], response_model=Task)
async def create_agent_task(request: Request, task_request: TaskRequestBody) -> Task:
    ...


@router.get("/agent/tasks", tags=["agent"], response_model=TaskListResponse)
async def list_agent_tasks(
    request: Request,
    page: Optional[int] = Query(1, ge=1),
    page_size: Optional[int] = Query(10, ge=1),
) -> TaskListResponse:
    ...


@router.get("/agent/tasks/{task_id}", tags=["agent"], response_model=Task)
async def get_agent_task(request: Request, task_id: str) -> Task:
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
    ...


@router.post(
    "/agent/tasks/{task_id}/steps", tags=["agent"], response_model=Step
)
async def execute_agent_task_step(
    request: Request, task_id: str, step: Optional[StepRequestBody] = None
) -> Step:
    ...


@router.get(
    "/agent/tasks/{task_id}/steps/{step_id}", tags=["agent"], response_model=Step
)
async def get_agent_task_step(request: Request, task_id: str, step_id: str) -> Step:
    ...


@router.get(
    "/agent/tasks/{task_id}/artifacts",
    tags=["agent"],
    response_model=TaskArtifactsListResponse,
)
async def list_agent_task_artifacts(
    request: Request,
    task_id: str,
    page: Optional[int] = Query(1, ge=1),
    page_size: Optional[int] = Query(10, ge=1),
) -> TaskArtifactsListResponse:
    ...


@router.post(
    "/agent/tasks/{task_id}/artifacts", tags=["agent"], response_model=Artifact
)
async def upload_agent_task_artifacts(
    request: Request, task_id: str, file: UploadFile, relative_path: Optional[str] = ""
) -> Artifact:
    ...


@router.get(
    "/agent/tasks/{task_id}/artifacts/{artifact_id}", tags=["agent"], response_model=str
)
async def download_agent_task_artifact(
    request: Request, task_id: str, artifact_id: str
) -> FileResponse:
    ...
