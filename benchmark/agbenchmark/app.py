import datetime
import glob
import json
import logging
import sys
import time
import uuid
from typing import Any, Dict, List, Optional

import httpx
import psutil
from agent_protocol_client import AgentApi, ApiClient, ApiException, Configuration
from agent_protocol_client.models import Task, TaskRequestBody
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Extra, ValidationError

sys.path.append(str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)

CHALLENGES: dict[str, ChallengeInfo] = {}
challenges_path = Path(__file__).parent / "challenges"
challenge_spec_files = deque(
    glob.glob(
        f"{challenges_path}/**/data.json",
        recursive=True,
    )
)

class CreateReportRequest(BaseModel):
    test: str = None
    test_run_id: str = None
    mock: Optional[bool] = False

    class Config:
        extra = Extra.forbid  # this will forbid any extra fields

async def run_single_test(body: CreateReportRequest) -> dict[str, Any]:
    pids = find_agbenchmark_without_uvicorn()
    logger.info(f"pids already running with agbenchmark: {pids}")

    logger.info(f"Request to /reports: {body.json(indent=2)}")

    # Start the benchmark in a separate thread
    benchmark_process = Process(
        target=lambda: run_benchmark(
            config=agbenchmark_config,
            tests=(body.test,),
            mock=body.mock or False,
        )
    )
    benchmark_process.start()

    # Wait for the benchmark to finish, with a timeout of 200 seconds
    timeout = 200
    start_time = time.monotonic()
    while benchmark_process.is_alive():
        if time.monotonic() - start_time > timeout:
            logger.warning(f"Benchmark run timed out after {timeout} seconds")
            benchmark_process.terminate()
            break
        await asyncio.sleep(1)
    else:
        logger.debug(f"Benchmark finished running in {time.monotonic() - start_time} s")

    # List all folders in the current working directory
    path_reports = agbenchmark_config.reports_folder
    folders = [folder for folder in path_reports.iterdir() if folder.is_dir()]

    # Sort the folders based on their names
    sorted_folders = sorted(folders, key=lambda x: x.name)

    # Get the last folder
    latest_folder = sorted_folders[-1] if sorted_folders else None

    # Read report.json from this folder
    if latest_folder:
        report_path = latest_folder / "report.json"
        logger.debug(f"Getting latest report from {report_path}")
        if report_path.exists():
            with report_path.open() as file:
                data = json.load(file)
            logger.debug(f"Report data: {json.dumps(data, indent=2)}")
        else:
            logger.error(
                "Could not get result after running benchmark: "
                f"'report.json' does not exist in '{latest_folder}'"
            )
    else:
        logger.error(
            "Could not get result after running benchmark: no reports found"
        )

    return data

# ... (rest of the code remains the same)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... (rest of the code remains the same)

if __name__ == "__main__":
    # ... (rest of the code remains the same)
