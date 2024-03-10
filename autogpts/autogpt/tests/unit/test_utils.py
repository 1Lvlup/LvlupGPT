import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
import requests
from git import InvalidGitRepositoryError

import autogpt.app.utils
from autogpt.app.utils import (
    get_bulletin_from_web,
    get_current_git_branch,
    get_latest_bulletin,
    set_env_config_value,
)
from autogpt.json_utils.utilities import extract_dict_from_response
from autogpt.utils import validate_yaml_file
from tests.utils import skip_in_ci


@pytest.fixture
def valid_json_response() -> dict:
    return {
        "thoughts": {
            "text": "My task is complete. I will use the 'task_complete' command "
            "to shut down.",
            "reasoning": "I will use the 'task_complete' command because it allows me "
            "to shut down and signal that my task is complete.",
            "plan": "I will use the 'task_complete' command with the reason "
            "'Task complete: retrieved Tesla's revenue in 2022.' to shut down.",
            "criticism": "I need to ensure that I have completed all necessary tasks "
            "before shutting down.",
            "speak": "All done!",
        },
        "command": {
            "name": "task_complete",
            "args": {"reason": "Task complete: retrieved Tesla's revenue in 2022."},
        },
    }


@pytest.fixture
def invalid_json_response() -> dict:
    return {
        "thoughts": {
            "text": "My task is complete. I will use the 'task_complete' command "
            "to shut down.",
            "reasoning": "I will use the 'task_complete' command because it allows me "
            "to shut down and signal that my task is complete.",
            "plan": "I will use the 'task_complete' command with the reason "
            "'Task complete: retrieved Tesla's revenue in 2022.' to shut down.",
            "criticism": "I need to ensure that I have completed all necessary tasks "
            "before shutting down.",
            "speak": "",
        },
        "command": {"name": "", "args": {}},
    }


def test_validate_yaml_file_valid(tmp_path):
    file_path = tmp_path / "valid_test_file.yaml"
    file_path.write_text("setting: value")
    result, message = validate_yaml_file(file_path)

    assert result is True
    assert "Successfully validated" in message
    file_path.unlink()


def test_validate_yaml_file_not_found(tmp_path):
    file_path = tmp_path / "non_existent_file.yaml"
    result, message = validate_yaml_file(file_path)

    assert result is False
    assert "wasn't found" in message


def test_validate_yaml_file_invalid(tmp_path):
    file_path = tmp_path / "invalid_test_file.yaml"
    file_path.write_text(
        "settings:\n"
        "  first_setting: value\n"
        "  second_setting: value\n"
        "    nested_setting: value\n"
        "  third_setting: value\n"
        "unindented_setting: value"
    )
    result, message = validate_yaml_file(file_path)

    assert result is False
    assert "There was an issue while trying to read" in message
    file_path.unlink()


@patch("requests.get")
def test_get_bulletin_from_web_success(mock_get, tmp_path):
    expected_content = "Test bulletin from web"
    bulletin_file = tmp_path / "BULLETIN.md"
    bulletin_file.write_text(expected_content)

    mock_get.return_value.status_code = 200
    mock_get.return_value.text = expected_content
    bulletin = get_bulletin_from_web()

    assert expected_content in bulletin
    mock_get.assert_called_with(
        "https://raw.githubusercontent.com/Significant-Gravitas/AutoGPT/master/autogpts/autogpt/BULLETIN.md"  # noqa: E501
    )
    bulletin_file.unlink()


@patch("requests.get")
def test_get_bulletin_from_web_failure(mock_get, tmp_path):
    mock_get.return_value.status_code = 404
    bulletin = get_bulletin_from_web()

    assert bulletin == ""


@patch("requests.get")
def test_get_bulletin_from_web_exception(mock_get, tmp_path):
    mock_get.side_effect = requests.exceptions.RequestException()
    bulletin = get_bulletin_from_web()

    assert bulletin == ""


def test_get_latest_bulletin_no_file(tmp_path):
    bulletin_file = tmp_path / "CURRENT_BULLETIN.md"
    if bulletin_file.exists():
        bulletin_file.unlink()

    bulletin, is_new = get_latest_bulletin(tmp_path)
    assert is_new


def test_get_latest_bulletin_with_file(tmp_path, valid_json_response):
    expected_content = "Test bulletin"
    bulletin_file = tmp_path / "CURRENT_BULLETIN.md"
    bulletin_file.write_text(expected_content)

    with patch("autogpt.app.utils.get_bulletin_from_web", return_value=""):
        bulletin, is_new = get_latest_bulletin(tmp_path)
        assert expected_content in bulletin
        assert
