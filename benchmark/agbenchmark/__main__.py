import argparse
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import toml

from agbenchmark.config import AgentBenchmarkConfig
from agbenchmark.main import run_benchmark, validate_args
from agbenchmark.utils.data_types import Category, DifficultyLevel
from agbenchmark.utils.logging import configure_logging
from agbenchmark.utils.utils import pretty_print_model

CURRENT_DIRECTORY = Path(".").resolve()

load_dotenv()


class InvalidInvocationError(ValueError):
    pass


logger = logging.getLogger(__name__)

BENCHMARK_START_TIME_DT = datetime.now(timezone.utc)
BENCHMARK_START_TIME = BENCHMARK_START_TIME_DT.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def load_challenges() -> List[Any]:
    from agbenchmark.challenges.builtin import load_builtin_challenges
    from agbenchmark.challenges.webarena import load_webarena_challenges

    return load_builtin_challenges() + load_webarena_challenges(skip_unavailable=False)


def config_command():
    try:
        config = AgentBenchmarkConfig.load()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    pretty_print_model(config, include_header=False)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the benchmark on the agent in the current directory.")

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug output",
    )

    subparsers = parser.add_subparsers(dest="command")

    start_parser = subparsers.add_parser("start", help="Deprecated. Use `agbenchmark run` instead.")
    start_parser.add_argument("agent_path", nargs="?", type=argparse.FileType("r"), default=sys.stdin)

    run_parser = subparsers.add_parser("run", help="Run the benchmark.")

    run_parser.add_argument(
        "-N",
        "--attempts",
        type=int,
        default=1,
        help="Number of times to run each challenge.",
    )

    categories = run_parser.add_mutually_exclusive_group(required=False)
    categories.add_argument(
        "-c",
        "--category",
        metavar="CATEGORY",
        action="append",
        help="(+) Select a category to run.",
    )
    categories.add_argument(
        "-s",
        "--skip-category",
        metavar="CATEGORY",
        action="append",
        help="(+) Exclude a category from running.",
    )

    run_parser.add_argument(
        "--test",
        metavar="TEST",
        action="append",
        help="(+) Select a test to run.",
    )

    run_parser.add_argument(
        "--maintain",
        action="store_true",
        help="Run only regression tests.",
    )

    run_parser.add_argument(
        "--improve",
        action="store_true",
        help="Run only non-regression tests.",
    )

    run_parser.add_argument(
        "--explore",
        action="store_true",
        help="Run only challenges that have never been beaten.",
    )

    run_parser.add_argument(
        "--no-dep",
        action="store_true",
        help="Run all (selected) challenges, regardless of dependency success/failure.",
    )

    run_parser.add_argument(
        "--cutoff",
        type=int,
        help="Override the challenge time limit (seconds).",
    )

    run_parser.add_argument(
        "--nc",
        action="store_true",
        help="Disable the challenge time limit.",
    )

    run_parser.add_argument(
        "--mock",
        action="store_true",
        help="Run with mock.",
    )

    run_parser.add_argument(
        "--keep-answers",
        action="store_true",
        help="Keep answers.",
    )

    run_parser.add_argument(
        "--backend",
        action="store_true",
        help="Write log output to a file instead of the terminal.",
    )

    serve_parser = subparsers.add_parser("serve", help="Serve the benchmark frontend and API on port 8080.")
    serve_parser.add_argument(
        "--port",
        type=int,
        help="Port to run the API on.",
    )

    challenge_parser = subparsers.add_parser("challenge", help="Challenge-related commands.")

    challenge_list_parser = challenge_parser.add_parser(
        "list", help="Lists [available|all] challenges."
    )
    challenge_list_parser.add_argument(
        "--all",
        action="store_true",
        help="Include unavailable challenges.",
    )
    challenge_list_parser.add_argument(
        "--names",
        action="store_true",
        help="List only the challenge names.",
    )
    challenge_list_parser.add_argument(
