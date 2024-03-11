import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import pytest
from pydantic import ValidationError

import agbenchmark.challenges  # type: ignore
from agbenchmark.config import AgentBenchmarkConfig
from agbenchmark.reports.processing.report_types import (
    Test,
    TestMetrics,
    TestResult,
)
from agbenchmark.reports.ReportManager import SingletonReportManager
from agbenchmark.utils.data_types import DifficultyLevel

# Initialize the logger for the module
logger = logging.getLogger(__name__)


def get_and_update_success_history(
    test_name: str, success: bool | None
) -> List[bool | None]:
    """
    Retrieve the previous test results from the success rate tracker,
    append the new result, and update the tracker.
    If not in mock mode, the function will update the tracker.

    Args:
        test_name (str): The name of the test.
        success (bool | None): The result of the latest test run.

    Returns:
        List[bool | None]: The list of previous test results, including the new one.
    """
    mock = os.getenv("IS_MOCK")

    prev_test_results = SingletonReportManager().SUCCESS_RATE_TRACKER.tests.get(
        test_name, []
    )

    if not mock:
        prev_test_results.append(success)
        SingletonReportManager().SUCCESS_RATE_TRACKER.update(test_name, prev_test_results)

    return prev_test_results


def update_regression_tests(
    prev_test_results: List[bool | None],
    test_report: Test,
    test_name: str,
) -> None:
    """
    Check if the last three test results are True and update the test report
    and regression manager accordingly.

    Args:
        prev_test_results (List[bool | None]): The list of previous test results.
        test_report (Test): The test report to be updated.
        test_name (str): The name of the test.
    """
    if len(prev_test_results) >= 3 and all(prev_test_results[-3:]):
        test_report.metrics.is_regression = True
        SingletonReportManager().REGRESSION_MANAGER.add_test(
            test_name, test_report.dict(include={"difficulty", "data_path"})
        )


def make_empty_test_report(challenge_info: agbenchmark.challenges.ChallengeInfo) -> Test:
    """
    Create an empty test report with the given challenge information.

    Args:
        challenge_info (agbenchmark.challenges.ChallengeInfo): The challenge information.

    Returns:
        Test: The empty test report.
    """
    difficulty = challenge_info.difficulty
    if isinstance(difficulty, DifficultyLevel):
        difficulty = difficulty.value

    return Test(
        category=[c.value for c in challenge_info.category],
        difficulty=difficulty,
        data_path=challenge_info.source_uri,
        description=challenge_info.description or "",
        task=challenge_info.task,
        answer=challenge_info.reference_answer or "",
        metrics=TestMetrics(attempted=False, is_regression=False),
        results=[],
    )


def add_test_result_to_report(
    test_report: Test,
    item: pytest.Item,
    call: pytest.CallInfo,
    config: AgentBenchmarkConfig
) -> None:
    """
    Add the test result to the test report and update the success rate tracker,
    regression manager, and challenges already beaten.

    Args:
        test_report (Test): The test report to be updated.
        item (pytest.Item): The pytest item.
        call (pytest.CallInfo): The pytest call information.
        config (AgentBenchmarkConfig): The configuration object.
    """
    user_properties: Dict[str, Any] = dict(item.user_properties)
    test_name: str = user_properties.get("test_name", "")

    mock = os.getenv("IS_MOCK")

    if call.excinfo:
        if not mock:
            SingletonReportManager().REGRESSION_MANAGER.remove_test(test_name)

        test_report.metrics.attempted = call.excinfo.typename != "Skipped"
    else:
        test_report.metrics.attempted = True

    try:
        test_report.results.append(
            TestResult(
                success=not call.excinfo,
                run_time=str(round(call.duration, 3)) + " seconds",
                fail_reason=str(call.excinfo.value) if call.excinfo else None,
                reached_cutoff=user_properties.get("timed_out", False),
                n_steps=user_properties.get("n_steps"),
                steps=user_properties.get("steps", []),
                cost=user_properties.get("agent_task_cost"),
            )
        )
        test_report.metrics.success_percentage = (
            sum(r.success for r in test_report.results) / len(test_report.results) * 100
        )
    except ValidationError:
        if call.excinfo:
            logger.error(
                "Validation failed on TestResult; "
                f"call.excinfo = {repr(call.excinfo)};\n{call.excinfo.getrepr()})"
            )
        raise

    prev_test_results: List[bool | None] = get_and_update_success_history(
        test_name, test_report.results[-1].success
    )

    update_regression_tests
