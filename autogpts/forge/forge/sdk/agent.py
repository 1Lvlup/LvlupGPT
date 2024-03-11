import os
import pathlib
from io import BytesIO
from uuid import uuid4

import uvicorn
from fastapi import APIRouter, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .db import AgentDB
from .errors import NotFoundError
from .forge_log import ForgeLogger
from .middlewares import AgentMiddleware
from .model import (
    Artifact,
    Step,
    StepRequestBody,
    Task,
    TaskArtifactsListResponse,
    TaskListResponse,
    TaskRequestBody,
    TaskStepsListResponse,
)
from .routes.agent_protocol import base_router
from .workspace import Workspace

# Initialize the logger for this module
LOG = ForgeLogger(__name__)

class Agent:
    def __init__(self, database: AgentDB, workspace: Workspace):
        """
        Initialize the Agent class with a database and workspace.

        :param database: An instance of AgentDB for database operations
        :param workspace: An instance of Workspace for managing the workspace
        """
        self.db = database
        self.workspace = workspace

    def get_agent_app(self, router: APIRouter = base_router):
        """
        Create and configure the FastAPI application.

        :param router: The API router instance
        :return: The configured FastAPI application
        """

        app = FastAPI(
            title="AutoGPT Forge",  # The title of the API
            description="Modified version of The Agent Protocol.",  # Description of the API
            version="v0.4",  # Version of the API
        )

        # Configure CORS middleware
        origins = [
            "http://localhost:5000",
            "http://127.0.0.1:5000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            # Add any other origins you want to whitelist
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(router, prefix="/ap/v1")  # Include the base router with a prefix
        script_dir = os.path.dirname(os.path.realpath(__file__))
        frontend_path = pathlib.Path(
            os.path.join(script_dir, "../../../../frontend/build/web")
        ).resolve()

        if os.path.exists(frontend_path):
            app.mount("/app", StaticFiles(directory=frontend_path), name="app")

            @app.get("/", include_in_schema=False)
            async def root():
                """
                Redirect the root path to the index.html file.
                """
                return RedirectResponse(url="/app/index.html", status_code=307)

        else:
            LOG.warning(
                f"Frontend not found. {frontend_path} does not exist. The frontend will not be served"
            )
        app.add_middleware(AgentMiddleware, agent=self)  # Add the custom Agent middleware

        return app

    def start(self, port):
        """
        Start the agent server using uvicorn.

        :param port: The port number to start the server on
        """
        uvicorn.run(
            "forge.app:app", host="localhost", port=port, log_level="error", reload=True
        )

    async def create_task(self, task_request: TaskRequestBody) -> Task:
        """
        Create a new task in the database.

        :param task_request: The task details
        :return: The created task
        """
        try:
            task = await self.db.create_task(
                input=task_request.input,
                additional_input=task_request.additional_input,
            )
            return task
        except Exception as e:
            raise

    async def list_tasks(self, page: int = 1, pageSize: int = 10) -> TaskListResponse:
        """
        List tasks in the database.

        :param page: The page number to retrieve
        :param pageSize: The number of tasks per page
        :return: A paginated list of tasks
        """
        try:
            tasks, pagination = await self.db.list_tasks(page, pageSize)
            response = TaskListResponse(tasks=tasks, pagination=pagination)
            return response
        except Exception as e:
            raise

    async def get_task(self, task_id: str) -> Task:
        """
        Retrieve a task from the database.

        :param task_id: The ID of the task to retrieve
        :return: The task with the given ID
        """
        try:
            task = await self.db.get_task(task_id)
        except Exception as e:
            raise
        return task

    async def list_steps(
        self, task_id: str, page: int = 1, pageSize: int = 10
    ) -> TaskStepsListResponse:
        """
        List steps for a task.

        :param task_id: The ID of the task
        :param page: The page number to retrieve
        :param pageSize: The number of steps per page
        :return: A paginated list of steps
        """
        try:
            steps, pagination = await self.db.list_steps(task_id, page, pageSize)
            response = TaskStepsListResponse(steps=steps, pagination=pagination)
            return response
        except Exception as e:
            raise

    async def execute_step(
