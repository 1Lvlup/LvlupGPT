from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Final, List, Literal, Optional

import pydantic
from pydantic import Field, SecretStr, validator

from autogpt.core.configuration.schema import (
    SystemSettings,
    UserConfigurable,
)
from autogpt.core.resource.model_providers.openai import (
    OPEN_AI_CHAT_MODELS,
    OpenAICredentials,
)
from autogpt.file_workspace import FileWorkspaceBackendName
from autogpt.logs.config import LoggingConfig
from autogpt.plugins.plugins_config import PluginsConfig
from autogpt.speech import TTSConfig

PROJECT_ROOT: Final = Path(__file__).parent.parent
AI_SETTINGS_FILE: Final = Path("ai_settings.yaml")
AZURE_CONFIG_FILE: Final = Path("azure.yaml")
PLUGINS_CONFIG_FILE: Final = Path("plugins_config.yaml")
PROMPT_SETTINGS_FILE: Final = Path("prompt_settings.yaml")

GPT_4_MODEL: Literal["gpt-4"] = "gpt-4"
GPT_3_MODEL: Literal["gpt-3.5-turbo"] = "gpt-3.5-turbo"


class Config(SystemSettings, arbitrary_types_allowed=True):
    name: str = Field("Auto-GPT configuration", const=True)
    description: str = Field("Default configuration for the Auto-GPT application.", const=True)

    project_root: Path = Field(PROJECT_ROOT, const=True)
    app_data_dir: Path = project_root / "data"
    skip_news: bool = False
    skip_reprompt: bool = False
    authorise_key: str = UserConfigurable(default="y", from_env="AUTHORISE_COMMAND_KEY")
    exit_key: str = UserConfigurable(default="n", from_env="EXIT_KEY")
    noninteractive_mode: bool = False
    chat_messages_enabled: bool = UserConfigurable(
        default=True, from_env=lambda: os.getenv("CHAT_MESSAGES_ENABLED") == "True"
    )

    tts_config: TTSConfig = TTSConfig()
    logging: LoggingConfig = LoggingConfig()

    workspace_backend: FileWorkspaceBackendName = UserConfigurable(
        default=FileWorkspaceBackendName.LOCAL,
        from_env=lambda: FileWorkspaceBackendName(v)
        if (v := os.getenv("WORKSPACE_BACKEND"))
        else None,
    )

    # Paths
    ai_settings_file: Path = UserConfigurable(
        default=AI_SETTINGS_FILE,
        from_env=lambda: Path(f) if (f := os.getenv("AI_SETTINGS_FILE")) else None,
    )
    prompt_settings_file: Path = UserConfigurable(
        default=PROMPT_SETTINGS_FILE,
        from_env=lambda: Path(f) if (f := os.getenv("PROMPT_SETTINGS_FILE")) else None,
    )

    # Model configuration
    fast_llm: str = UserConfigurable(
        default="gpt-3.5-turbo-0125",
        from_env=lambda: os.getenv("FAST_LLM"),
    )
    smart_llm: str = UserConfigurable(
        default="gpt-4-turbo-preview",
        from_env=lambda: os.getenv("SMART_LLM"),
    )
    temperature: float = UserConfigurable(
        default=0,
        from_env=lambda: float(v) if (v := os.getenv("TEMPERATURE")) else None,
    )
    openai_functions: bool = UserConfigurable(
        default=False, from_env=lambda: os.getenv("OPENAI_FUNCTIONS", "False") == "True"
    )
    embedding_model: str = UserConfigurable(
        default="text-embedding-3-small", from_env="EMBEDDING_MODEL"
    )
    browse_spacy_language_model: str = UserConfigurable(
        default="en_core_web_sm", from_env="BROWSE_SPACY_LANGUAGE_MODEL"
    )

    # Run loop configuration
    continuous_mode: bool = False
    continuous_limit: int = 0

    # Memory
    memory_backend: str = UserConfigurable("json_file", from_env="MEMORY_BACKEND")
    memory_index: str = UserConfigurable("auto-gpt-memory", from_env="MEMORY_INDEX")
    redis_host: str = UserConfigurable("localhost", from_env="REDIS_HOST")
    redis_port: int = UserConfigurable(
        default=6379,
        from_env=lambda: int(v) if (v := os.getenv("REDIS_PORT")) else None,
    )
    redis_password: str = UserConfigurable("", from_env="REDIS_PASSWORD")
    wipe_redis_on_start: bool = UserConfigurable(
        default=True,
        from_env=lambda: os.getenv("WIPE_REDIS_ON_START", "True") == "True",
    )

    # Commands
   
