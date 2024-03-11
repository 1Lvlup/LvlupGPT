import logging
import os
from pathlib import Path
from typing import Optional, Sequence, Union

from dotenv import load_dotenv
from agbenchmark.challenges import get_unique_categories
from agbenchmark.config import AgentBenchmarkConfig

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

def run_benchmark(
        config: AgentBenchmarkConfig,  # Configuration object
        maintain: bool = False,  # Run only regression tests
        improve: bool = False,  # Run only non-regression tests
        explore: bool = False,  # Only attempt challenges that have never been beaten
        tests: Union[Sequence[str], None] = None,  # List of specific tests to run
        categories: Union[Sequence[str], None] = None,  # List of categories to run
        skip_categories: Union[Sequence[str], None] = None,  # List of categories to skip
        attempts_per_challenge: int = 1,  # Number of attempts to make for each challenge
        mock: bool = False,  # Use mock mode
        no_dep: bool = False,  # Don't check dependencies
        no_cutoff: bool = False,  # Don't use cutoff time
        cutoff: Optional[int] = None,  # Cutoff time for challenges
        keep_answers: bool = False,  # Keep answers after running challenges
        server: bool = False  # Run in server mode
) -> int:
    """
    Starts the benchmark. If a category flag is provided, only challenges with the
    corresponding mark will be run.
    """
    import pytest  # Pytest module for running tests

    # Validate input arguments
    validate_args(
        maintain=maintain,
        improve=improve,
        explore=explore,
        tests=tests,
        categories=categories,
        skip_categories=skip_categories,
        no_cutoff=no_cutoff,
        cutoff=cutoff,
    )

    # Log configuration variables
    for key, value in vars(config).items():
        logger.debug(f"config.{key} = {repr(value)}")

    # Set up pytest arguments based on input flags
    pytest_args = ["-vs"]

    if tests:
        logger.info(f"Running specific test(s): {' '.join(tests)}")
        pytest_args += [f"--test={t}" for t in tests]
    elif categories or skip_categories or maintain or improve or explore:
        all_categories = get_unique_categories()

        if categories:
            categories_to_run = set(categories)
            if not categories_to_run:
                raise ValueError("Error: You can't run an empty category list")
            categories_to_run = categories_to_run.intersection(all_categories)
            if not categories_to_run:
                raise InvalidInvocationError(
                    "One or more invalid categories were specified: "
                    f"{', '.join(categories)}.\n"
                    f"Valid categories are: {', '.join(all_categories)}."
                )
            pytest_args += [f"--category={c}" for c in categories_to_run]
            logger.info(f"Running tests of category: {categories_to_run}")
        else:
            logger.info("Running all categories")

        if maintain:
            logger.info("Running only regression tests")
        elif improve:
            logger.info("Running only non-regression tests")
        elif explore:
            logger.info("Only attempt challenges that have never been beaten")

    # Set up environment variables and flags based on input arguments
    if mock:
        # TODO: unhack
        os.environ[
            "IS_MOCK"
        ] = "True"  # ugly hack to make the mock work when calling from API

    for flag, active in {
        "--maintain": maintain,
        "--improve": improve,
        "--explore": explore,
        "--no-dep": no_dep,
        "--mock": mock,
        "--nc": no_cutoff,
        "--keep-answers": keep_answers,
    }.items():
        if active:
            pytest_args.append(flag)

    if attempts_per_challenge > 1:
        pytest_args.append(f"--attempts={attempts_per_challenge}")

    if cutoff:
        pytest_args.append(f"--cutoff={cutoff}")
        logger.debug(f"Setting cuttoff override to {cutoff} seconds.")

    # Set up current working directory and pytest command
    current_dir = Path(__file__).resolve().parent
    pytest_args.append(str(current_dir / "generate_test.py"))

    pytest_args.append("--cache-clear")
    logger.debug(f"Running Pytest with args: {pytest_args}")

    # Run pytest and return exit code
    exit_code = pytest.main
