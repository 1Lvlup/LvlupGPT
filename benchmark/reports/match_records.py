import glob
import json
import os
from typing import Dict, List, Optional, Union

import pandas as pd
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Metrics class definitions
# -----------------------------------------------------------------------------

# Define Metrics class to represent the metrics of a test
class Metrics(BaseModel):
    difficulty: str
    success: bool
    success_percent: float = Field(..., alias="success_%")
    run_time: Optional[str] = None
    fail_reason: Optional[str] = None
    attempted: Optional[bool] = None


# Define MetricsOverall class to represent the overall metrics of a suite test
class MetricsOverall(BaseModel):
    run_time: str
    highest_difficulty: str
    percentage: Optional[float] = None


# -----------------------------------------------------------------------------
# Test and SuiteTest class definitions
# -----------------------------------------------------------------------------

# Define Test class to represent a single test
class Test(BaseModel):
    data_path: str
    is_regression: bool
    answer: str
    description: str
    metrics: Metrics
    category: List[str]
    task: Optional[str] = None
    reached_cutoff: Optional[bool] = None


# Define SuiteTest class to represent a suite of tests
class SuiteTest(BaseModel):
    data_path: str
    metrics: MetricsOverall
    tests: Dict[str, Test]
    category: Optional[List[str]] = None
    task: Optional[str] = None
    reached_cutoff: Optional[bool] = None


# -----------------------------------------------------------------------------
# Report class definition
# -----------------------------------------------------------------------------

# Define Report class to represent the report
class Report(BaseModel):
    command: str
    completion_time: str
    benchmark_start_time: str
    metrics: MetricsOverall
    tests: Dict[str, Union[Test, SuiteTest]]
    config: Dict[str, str | dict[str, str]]


# -----------------------------------------------------------------------------
# Function definitions
# -----------------------------------------------------------------------------

# Define get_reports function to get the reports
def get_reports():
    # Initialize an empty list to store the report data
    report_data = []

    # Get the current working directory
    current_dir = os.getcwd()

    # Check if the current directory ends with 'reports'
    if current_dir.endswith("reports"):
        reports_dir = "/"
    else:
        reports_dir = "reports"

    # Iterate over all agent directories in the reports directory
    for agent_name in os.listdir(reports_dir):
        if agent_name is None:
            continue
        agent_dir = os.path.join(reports_dir, agent_name)

        # Check if the item is a directory (an agent directory)
        if os.path.isdir(agent_dir):
            # Construct the path to the report.json file
            # Get all directories and files, but note that this will also include any file, not just directories.
            run_dirs = glob.glob(os.path.join(agent_dir, "*"))

            # Get all json files starting with 'file'
            # old_report_files = glob.glob(os.path.join(agent_dir, "file*
