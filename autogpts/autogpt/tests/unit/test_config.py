"""
Test cases for the config class, which handles the configuration settings
for the AI and ensures it behaves as a singleton.
"""
import os
import pytest
from unittest.mock import patch
from typing import Any

import openai
from openai.models import Model
from openai.pagination import SyncPage
from pydantic import SecretStr

from autogpt.app.configurator import GPT_3_MODEL, GPT_4_MODEL, apply_overrides_to_config
from autogpt.config import Config, ConfigBuilder


def test_initial_values(config: Config) -> None:
    """
    Test if the initial values of the config class attributes are set correctly.
    """
    assert not config.continuous_mode
    assert not config.tts_config.speak_mode
    assert config.fast_llm.startswith("gpt-3.5-turbo")
    assert config.smart_llm.startswith("gpt-4")


def test_set_continuous_mode(config: Config) -> None:
    """
    Test if the set_continuous_mode() method updates the continuous_mode attribute.
    """
    continuous_mode = config.continuous_mode
    config.continuous_mode = True
    assert config.continuous_mode is True
    config.continuous_mode = continuous_mode


def test_set_speak_mode(config: Config) -> None:
    """
    Test if the set_speak_mode() method updates the speak_mode attribute.
    """
    speak_mode = config.tts_config.speak_mode
    config.tts_config.speak_mode = True
    assert config.tts_config.speak_mode is True
    config.tts_config.speak_mode = speak_mode


def test_set_fast_llm(config: Config) -> None:
    """
    Test if the set_fast_llm() method updates the fast_llm attribute.
    """
    fast_llm = config.fast_llm
    config.fast_llm = "gpt-3.5-turbo-test"
    assert config.fast_llm == "gpt-3.5-turbo-test"
    config.fast_llm = fast_llm


def test_set_smart_llm(config: Config) -> None:
    """
    Test if the set_smart_llm() method updates the smart_llm attribute.
    """
    smart_llm = config.smart_llm
    config.smart_llm = "gpt-4-test"
    assert config.smart_llm == "gpt-4-test"
    config.smart_llm = smart_llm


@patch("openai.Models.list")
def test_fallback_to_gpt3_if_gpt4_not_available(
    mock_list_models: Any, config: Config
) -> None:
    """
    Test if models update to gpt-3.5-turbo if gpt-4 is not available.
    """
    fast_llm = config.fast_llm
    smart_llm = config.smart_llm

    config.fast_llm = "gpt-4"
    config.smart_llm = "gpt-4"

    mock_list_models.return_value = SyncPage(
        data=[Model(id=GPT_3_MODEL)], object="Models"
    )

    apply_overrides_to_config(
        config=config,
        gpt3only=False,
        gpt4only=False,
    )

    assert config.fast_llm == "gpt-3.5-turbo"
    assert config.smart_llm == "gpt-3.5-turbo"

    # Reset config
    config.fast_llm = fast_llm
    config.smart_llm = smart_llm


def test_missing_azure_config(config: Config) -> None:
    assert config.openai_credentials is not None

    config_file = config.app_data_dir / "azure_config.yaml"
    with pytest.raises(FileNotFoundError):
        config.openai_credentials.load_azure_config(config_file)

    config_file.write_text("")
    with pytest.raises(ValueError):
        config.openai_credentials.load_azure_config(config_file)

    assert config.openai_credentials.api_type != "azure"
    assert config.openai_credentials.api_version == ""
    assert config.openai_credentials.azure_model_to_deploy_id_map is None


@pytest.fixture
def config_with_azure(config: Config):
    config_file = config.app_data_dir / "azure_config.yaml"
    config_file.write_text(
        f"""
azure_api_type: azure
azure_api_version: 2023-06-01-preview
azure_endpoint: https://dummy.openai.azure.com
azure_model_map:
    {config.fast_llm}: FAST-LLM_ID
    {config.smart_llm}: SMART-LLM_ID
    {config.embedding_model}: embedding-deployment-id-for-azure
"""
    )
    os.environ["USE_AZURE"] = "True"
    os.environ["AZURE_CONFIG_FILE"] = str(config_file)
    config_with_azure = ConfigBuilder.build_config_from_env(
        project_root=config.project_root
    )
    yield config_with_azure
    del os.environ["USE_AZURE"]
    del os.environ["AZURE_CONFIG_FILE"]


def test_azure_config(config_with_azure: Config) -> None:
    assert (credentials := config_with_azure.openai_credentials) is not None
    assert credentials.api_type ==
