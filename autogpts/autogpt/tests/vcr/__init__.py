import logging
import os
import sha256
from typing import Any, Callable, Dict, Final, Literal, Optional

import pytest
import requests
from openai import OpenAI, FinalRequestOptions, Omit
from openai._utils import is_given
from openai.exceptions import OpenAIError
from unittest.mock import Mock, patch

from .vcr_filter import PROXY, before_record_request, before_record_response, freeze_request_body

DEFAULT_RECORD_MODE = "new_episodes"
BASE_VCR_CONFIG = {
    "before_record_request": before_record_request,
    "before_record_response": before_record_response,
    "filter_headers": [
        "Authorization",
        "AGENT-MODE",
        "AGENT-TYPE",
        "Cookie",
        "OpenAI-Organization",
        "X-OpenAI-Client-User-Agent",
        "User-Agent",
    ],
    "match_on": ["method", "headers"],
}

logger = logging.getLogger("cached_openai_client")


@pytest.fixture(scope="session")
def vcr_config(get_base_vcr_config):
    return get_base_vcr_config


@pytest.fixture(scope="session")
def get_base_vcr_config(request):
    record_mode: Literal["new_episodes", "once", "all"] = request.config.getoption(
        "--record-mode", default="new_episodes"
    )
    config: Final[Dict[str, Any]] = BASE_VCR_CONFIG

    if record_mode is None:
        config["record_mode"] = DEFAULT_RECORD_MODE

    return config


@pytest.fixture()
def vcr_cassette_dir(request):
    test_name = os.path.splitext(request.node.name)[0]
    return os.path.join("tests/vcr_cassettes", test_name)


@pytest.fixture
def cached_openai_client(mocker: Mock) -> OpenAI:
    client = OpenAI()
    _prepare_options = client._prepare_options

    def _patched_prepare_options(self, options: FinalRequestOptions):
        _prepare_options(options)

        headers: Dict[str, str | Optional[Omit]] = (
            {**options.headers} if is_given(options.headers) else {}
        )
        options.headers = headers
        data: dict = options.json_data

        if PROXY and record_mode == "new_episodes":
            headers["AGENT-MODE"] = os.environ.get("AGENT_MODE", Omit())
            headers["AGENT-TYPE"] = os.environ.get("AGENT_TYPE", Omit())

        logger.debug(
            f"Outgoing API request: {headers}\n{data if data else None}"
        )

        # Add hash header for cheap & fast matching on cassette playback
        headers["X-Content-Hash"] = sha256(
            freeze_request_body(data), usedforsecurity=False
        ).hexdigest()

    if PROXY:
        client.base_url = f"{PROXY}/v1"
    mocker.patch.object(
        client,
        "_prepare_options",
        new
