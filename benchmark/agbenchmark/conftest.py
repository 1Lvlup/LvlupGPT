import contextlib
import json
import logging
import os
import shutil
import threading
import time
from pathlib import Path
from typing import Generator, List, Tuple, Type, Union

import pytest
from _pytest.config import Config
from _pytest.fixtures import FixtureRequest
from _pytest.mark import Mark
from _pytest.nodes import Item
from _pytest.python import Function
from _pytest.terminal import TerminalReporter

import pytest_timeout
from agbenchmark.challenges import BaseChallenge, Category, OPTIONAL_CATEGORIES
from agbenchmark.config import AgentBenchmarkConfig
from agbenchmark.reports.processing.report_types import Test
from agbenchmark.reports.ReportManager import RegressionTestsTracker
from agbenchmark.reports.reports import (
    add_test_result_to_report,
    make_empty_test_report,
    session_finish,
)
from agbenchmark.utils.data_types import ChallengeInfo

GLOBAL_TIMEOUT = 1500  # The tests will stop after 25 minutes so we can send the reports.

agbenchmark_config = AgentBenchmarkConfig.load()
logger = logging.getLogger(__name__)

pytest_plugins = ["agbenchmark.utils.dependencies"]
collect_ignore = ["challenges"]


def pytest_addoption(parser: Config) -> None:
    """
    Pytest hook that adds command-line options to the `pytest` command.
    The added options are specific to agbenchmark and control its behavior:
    * `--mock` is used to run the tests in mock mode.
    * `--host` is used to specify the host for the tests.
    * `--category` is used to run only tests of a specific category.
    * `--nc` is used to run the tests without caching.
    * `--cutoff` is used to specify a cutoff time for the tests.
    * `--improve` is used to run only the tests that are marked for improvement.
    * `--maintain` is used to run only the tests that are marked for maintenance.
    * `--explore` is used to run the tests in exploration mode.
    * `--test` is used to run a specific test.
    * `--no-dep` is used to run the tests without dependencies.
    * `--keep-answers` is used to keep the answers of the tests.

    Args:
        parser: The Pytest CLI parser to which the command-line options are added.
    """
    parser.addoption("-N", "--attempts", action="store")
    parser.addoption("--no-dep", action="store_true")
    parser.addoption("--mock", action="store_true")
    parser.addoption("--host", default=None)
    parser.addoption("--nc", action="store_true")
    parser.addoption("--cutoff", action="store")
    parser.addoption("--category", action="append")
    parser.addoption("--test", action="append")
    parser.addoption("--improve", action="store_true")
    parser.addoption("--maintain", action="store_true")
    parser.addoption("--explore", action="store_true")
    parser.addoption("--keep-answers", action="store_true")


def pytest_configure(config: Config) -> None:
    # Register category markers to prevent "unknown marker" warnings
    for category in Category:
        config.addinivalue_line("markers", f"{category.value}: {category}")

    config.pluginmanager.register(pytest_timeout.TimeoutPlugin(), "timeout")


@pytest.fixture(scope="module")
def config() -> AgentBenchmarkConfig:
    return agbenchmark_config


@pytest.fixture(autouse=True)
def temp_folder(request: FixtureRequest) -> Path:
    """
    Pytest fixture that sets up and tears down the temporary folder for each test.
    It is automatically used in every test due to the 'autouse=True' parameter.
    """
    temp_folder = Path(agbenchmark_config.temp_folder)
    temp_folder.mkdir(parents=True, exist_ok=True)

    yield temp_folder

    if not os.getenv("KEEP_TEMP_FOLDER_FILES"):
        for filename in temp_folder.glob("*"):
            try:
                if filename.is_file() or filename.is_symlink():
                    filename.unlink()
                elif filename.is_dir():
                    shutil.rmtree(filename)
            except Exception as e:
                logger.warning(f"Failed to delete {filename}. Reason: {e}")


def pytest_runtest_makereport(item: Item, call: Function) -> None:
    """
    Pytest hook that is called when a test report is being generated.
    It is used to generate and finalize reports for each test.

    Args:
        item: The test item for which the report is being generated.
        call: The call object from which the test result is retrieved.
    """
    challenge: Type[BaseChallenge] = item.cls  # type: ignore
    challenge_id = challenge.info.eval_id

    if challenge_id not in test_reports:
        test_reports[challenge_id] = make_empty_test_report(challenge.info)

    if call.when == "setup":
        test_name = item.nodeid.split("::")[1]
        item.user_properties.append(("test_name", test_name))

    if call.when == "call":
        add_test_result_to_report(
            test_reports[challenge_id], item, call, agbenchmark_config
        )


def timeout_monitor(start_time: float) -> None:
    """
    Function that limits the total execution time of the test suite.
    This function is supposed to be run in a separate thread and calls `pytest
