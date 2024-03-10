import copy
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import dataclasses
import dateutil.standard_file_parser

from agbenchmark.config import AgentBenchmarkConfig
from agbenchmark.reports.processing.graphs import save_single_radar_chart
from agbenchmark.reports.processing.process_report import (
    get_highest_achieved_difficulty_per_category,
)
from agbenchmark.reports.processing.report_types import MetricsOverall, Report, Test
from agbenchmark.utils.utils import get_highest_success_difficulty

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class BaseReportManager:
    """Abstracts interaction with the report file"""

    report_file: Path
    tests: Dict[str, Any]

    def __post_init__(self):
        self.load()

    def load(self) -> None:
        if not self.report_file.exists():
            self.tests = {}
            return

        try:
            with self.report_file.open("r") as f:
                data = json.loads(f.read(), object_hook=dateutil.standard_file_parser.parse)
                self.tests = {k: data[k] for k in sorted(data)}
        except json.decoder.JSONDecodeError as e:
            logger.warning(f"Could not parse {self.report_file}: {e}")
            self.tests = {}

    def save(self) -> None:
        with self.report_file.open("w") as f:
            f.write(json.dumps(self.tests, indent=4))

    def remove_test(self, test_name: str) -> None:
        if test_name in self.tests:
            del self.tests[test_name]
            self.save()

    def reset(self) -> None:
        self.tests = {}
        self.save()


@dataclasses.dataclass
class SessionReportManager(BaseReportManager):
    """Abstracts interaction with the session report file"""

    start_time: float
    benchmark_start_time: datetime

    def save(self) -> None:
        with self.report_file.open("w") as f:
            if isinstance(self.tests, Report):
                f.write(self.tests.json(indent=4))
            else:
                f.write(json.dumps({k: v.dict() for k, v in self.tests.items()}, indent=4))

    def load(self) -> None:
        super().load()
        if "tests" in self.tests:  # type: ignore
            self.tests = Report.parse_obj(self.tests)
        else:
            self.tests = {n: Test.parse_obj(d) for n, d in self.tests.items()}

    def add_test_report(self, test_name: str, test_report: Test) -> None:
        if isinstance(self.tests, Report):
            raise RuntimeError("Session report already finalized")

        if test_name.startswith("Test"):
            test_name = test_name[4:]
        self.tests[test_name] = test_report

        self.save()

    def finalize_session_report(self, config: AgentBenchmarkConfig) -> None:
        command = " ".join(sys.argv)

        if isinstance(self.tests, Report):
            raise RuntimeError("Session report already finalized")

        self.tests = Report(
            command=command.split(os.sep)[-1],
            benchmark_git_commit_sha="---",
            agent_git_commit_sha="---",
            completion_time=datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S+00:00"
            ),
            benchmark_start_time=self.benchmark_start_time.strftime(
                "%Y-%m-%dT%H:%M:%S+00:00"
            ),
            metrics=MetricsOverall(
                run_time=str(round(time.time() - self.start_time, 2)) + " seconds",
                highest_difficulty=get_highest_success_difficulty(self.tests),
                total_cost=self.get_total_costs(),
            ),
            tests=copy.copy(self.tests),
            config=config.dict(exclude={"reports_folder"}, exclude_none=True),
        )

        agent_categories = get_highest_achieved_difficulty_per_category(self.tests)
        if len(agent_categories) > 1:
            save_single_radar_chart(
                agent_categories,
                config.get_report_dir(self.benchmark_start_time) / "radar_chart.png",
            )

       
