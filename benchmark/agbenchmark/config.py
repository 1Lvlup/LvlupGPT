import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pydantic

def calculate_info_test_path(base_path: Path, benchmark_start_time: datetime) -> Path:
    """
    Calculates the path to the directory where the test report will be saved.
    
    This function creates a new directory with a unique name based on the current date and time,
    and the name of the benchmark run. It first checks if the base_path directory exists, and if
    not, it creates it. Then, it creates a new directory for the test report at the base_path
    location with the specified date_stamp and run_name.
    """
# ... rest of the function ...

class AgentBenchmarkConfig(pydantic.BaseSettings, extra="allow"):
    """
    Configuration model and loader for the AGBenchmark.

    This class defines the configuration for the AGBenchmark, which includes the location of the
    config.json file, the categories to be tested, and the host where the subject application
    is running. It uses Pydantic's BaseSettings class to load the configuration from a JSON file.
    """
# ... rest of the class ...

    @classmethod
    def load(cls, config_dir: Optional[Path] = None) -> "AgentBenchmarkConfig":
        """
        Loads the configuration from the config.json file.

        This class method loads the configuration from the config.json file located at the
        specified config_dir path. If no path is provided, it looks for the config.json file
        in the current working directory.
        """
# ... rest of the method ...

    @staticmethod
    def find_config_folder(for_dir: Path = Path.cwd()) -> Path:
        """
        Finds the agbenchmark_config directory.

        This static method searches for the agbenchmark_config directory in the specified
        for_dir directory and its ancestors. If it finds the directory, it returns the Path
        object for that directory. If it doesn't find the directory, it raises a FileNotFoundError.
        """
# ... rest of the method ...

    @property
    def config_file(self) -> Path:
        """
        Returns the Path object for the config.json file.

        This property returns the Path object for the config.json file located at the
        agbenchmark_config_dir directory.
        """
# ... rest of the property ...

    @property
    def reports_folder(self) -> Path:
        """
        Returns the Path object for the reports folder.

        This property returns the Path object for the reports folder located at the
        agbenchmark_config_dir directory.
        """
# ... rest of the property ...

    def get_report_dir(self, benchmark_start_time: datetime) -> Path:
        """
        Returns the Path object for the report directory.

        This method returns the Path object for the report directory located at the
        reports_folder directory with a unique name based on the current date and time,
        and the name of the benchmark run.
        """
# ... rest of the method ...

    @property
    def regression_tests_file(self) -> Path:
        """
        Returns the Path object for the regression_tests.json file.

        This property returns the Path object for the regression_tests.json file located at the
        reports_folder directory.
        """
# ... rest of the property ...

    @property
    def success_rate_file(self) -> Path:
        """
        Returns the Path object for the success_rate.json file.

        This property returns the Path object for the success_rate.json file located at the
        reports_folder directory.
        """
# ... rest of the property ...

    @property
    def challenges_already_beaten_file(self) -> Path:
        """
        Returns the Path object for the challenges_already_beaten.json file.

        This property returns the Path object for the challenges_already_beaten.json file located
        at the agbenchmark_config_dir directory.
        """
# ... rest of the property ...

    @property
    def temp_folder(self) -> Path:
        """
        Returns the Path object for the temp_folder directory.

        This property returns the Path object for the temp_folder directory located at the
        agbenchmark_config_dir directory.
        """
# ... rest of the property ...
