import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from agbenchmark.reports.processing.get_files import (
    get_latest_report_from_agent_directories,
)
from agbenchmark.reports.processing.report_types import Report
from agbenchmark.utils.data_types import STRING_DIFFICULTY_MAP

logger = logging.getLogger(__name__)

def get_reports_data(report_path: str) -> Dict[str, Report]:
    """
    Get the latest report files from the agent directories and parse them into Report objects.

    :param report_path: The path to the reports directory.
    :return: A dictionary containing the Report objects.
    """
    latest_files = get_latest_report_from_agent_directories(report_path)

    reports_data = {}

    if latest_files is None:
        raise Exception("No files found in the reports directory")

    for subdir, file in latest_files:
        subdir_name = subdir.name
        file_path = subdir / file
        with file_path.open("r") as f:
            json_data = json.load(f)
            converted_data = Report.parse_obj(json_data)
            reports_data[subdir_name] = converted_data

    return reports_data


def get_highest_achieved_difficulty_per_category(report: Report) -> Dict[str, int]:
    """
    Get the highest achieved difficulty per category in a Report object.

    :param report: The Report object.
    :return: A dictionary containing the highest achieved difficulty per category.
    """
    categories = {}

    for _, test_data in report.tests.items():
        for category in test_data.category:
            if category in ("interface", "iterate", "product_advisor"):
                continue
            categories.setdefault(category, 0)
            if (
                test_data.results
                and all(r.success for r in test_data.results)
                and test_data.difficulty
            ):
                num_dif = STRING_DIFFICULTY_MAP[test_data.difficulty]
                if num_dif > categories[category]:
                    categories[category] = num_dif

    return categories


def all_agent_categories(reports_data: Dict[str, Report]) -> Dict[str, Dict[str, int]]:
    """
    Get the highest achieved difficulty per category for all agents in the reports data.

    :param reports_data: A dictionary containing the Report objects.
    :return: A dictionary containing the highest achieved difficulty per category for all agents.
    """
    all_categories = {}

    for name, report in reports_data.items():
        categories = get_highest_achieved_difficulty_per_category(report)
        if categories:  # only add to all_categories if categories is not empty
            all_categories[name] = categories

    return all_categories
