# Import necessary modules and libraries
import os
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import yaml
from pytest_mock import MockerFixture

# Import custom modules and libraries
from autogpt.agents.agent import Agent, AgentConfiguration, AgentSettings
from autogpt.app.main import _configure_openai_provider
from autogpt.config import AIProfile, Config, ConfigBuilder
from autogpt.core.resource.model_providers import ChatModelProvider, OpenAIProvider
from autogpt.file_workspace.local import (
    FileWorkspace,
    FileWorkspaceConfiguration,
    LocalFileWorkspace,
)
from autogpt.llm.api_manager import ApiManager
from autogpt.logs.config import configure_logging
from autogpt.models.command_registry import CommandRegistry

# pytest-specific configurations
pytest_plugins = [
    "tests.integration.agent_factory",
    "tests.integration.memory.utils",
    "tests.vcr",
]


@pytest.fixture()
def tmp_project_root(tmp_path: Path) -> Path:
    """
    Create a temporary project root directory for tests.

    :param tmp_path: A pytest-provided temporary directory path.
    :return: A Path object representing the temporary project root.
    """
    return tmp_path


@pytest.fixture()
def app_data_dir(tmp_project_root: Path) -> Path:
    """
    Create a temporary app data directory within the project root.

    :param tmp_project_root: A Path object representing the temporary project root.
    :return: A Path object representing the temporary app data directory.
    """
    dir = tmp_project_root / "data"
    dir.mkdir(parents=True, exist_ok=True)
    return dir


@pytest.fixture()
def agent_data_dir(app_data_dir: Path) -> Path:
    """
    Create a temporary agent data directory within the app data directory.

    :param app_data_dir: A Path object representing the temporary app data directory.
    :return: A Path object representing the temporary agent data directory.
    """
    return app_data_dir / "agents/AutoGPT"


@pytest.fixture()
def workspace_root(agent_data_dir: Path) -> Path:
    """
    Create a temporary workspace root directory within the agent data directory.

    :param agent_data_dir: A Path object representing the temporary agent data directory.
    :return: A Path object representing the temporary workspace root directory.
    """
    return agent_data_dir / "workspace"


@pytest.fixture()
def workspace(workspace_root: Path) -> FileWorkspace:
    """
    Create a LocalFileWorkspace instance and initialize it with the given workspace root directory.

    :param workspace_root: A Path object representing the temporary workspace root directory.
    :return: A LocalFileWorkspace object.
    """
    workspace = LocalFileWorkspace(FileWorkspaceConfiguration(root=workspace_root))
    workspace.initialize()
    return workspace


@pytest.fixture
def temp_plugins_config_file():
    """
    Create a temporary plugins_config.yaml file with an empty configuration.

    :return: A Path object representing the temporary plugins_config.yaml file.
    """
    config_directory = TemporaryDirectory()
    config_file = Path(config_directory.name) / "plugins_config.yaml"
    with open(config_file, "w+") as f:
        yaml.dump({}, f)

    yield config_file


@pytest.fixture(scope="function")
def config(
    temp_plugins_config_file: Path,
    tmp_project_root: Path,
    app_data_dir: Path,
    mocker: MockerFixture,
):
    """
    Create a Config object with custom configurations for tests.

    :param temp_plugins_config_file: A Path object representing the temporary plugins_config.yaml file.
    :param tmp_project_root: A Path object representing the temporary project root.
    :param app_data_dir: A Path object representing the temporary app data directory.
    :param mocker: A pytest-mock MockerFixture object.
    :return: A Config object.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "sk-dummy"

    config = ConfigBuilder.build_config_from_env(project_root=tmp_project_root)

    config.app_data_dir = app_data_dir

    config.plugins_dir = "tests/unit/data/test_plugins"
    config.plugins_config_file = temp_plugins_config_file

    config.logging.log_dir = Path(__file__).parent / "logs"
    config.logging.plain_console_output = True
    config.noninteractive_mode = True

    from autogpt.plugins.plugins_config import PluginsConfig

    config.plugins_config = PluginsConfig.load_config(
        plugins_config_file=config.plugins_config_file,
        plugins_denylist=config.plugins_denylist,
        plugins_allowlist=config.plugins_allowlist,
    )

    yield config


@pytest.fixture(scope="session")
def setup_logger(config: Config):
    """
    Configure the logger with the given Config object.

    :param config: A Config object.
    """
    configure_logging(**config.logging.dict())


@pytest.fixture()
def api_manager() -> ApiManager:
    """
    Create an ApiManager instance.

    :return: An ApiManager object.
    """
    if ApiManager in ApiManager._instances:
        del ApiManager._instances[ApiManager]
    return ApiManager()


@pytest.fixture
def llm_provider(config: Config) -> OpenAIProvider:
    """
    Create an OpenAIProvider instance with the given Config object
