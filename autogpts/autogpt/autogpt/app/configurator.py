"""Configurator module."""
from __future__ import annotations  # Allows using class names as types before they are defined

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional

# Import other necessary modules

if TYPE_CHECKING:
    from autogpt.core.resource.model_providers.openai import OpenAICredentials

# Initialize the logger for this module
logger = logging.getLogger(__name__)

def apply_overrides_to_config(
    config: Config,  # The config object to update
    continuous: bool = False,  # Whether to run in continuous mode
    continuous_limit: Optional[int] = None,  # The number of times to run in continuous mode
    ai_settings_file: Optional[Path] = None,  # The path to the ai_settings.yaml file
    prompt_settings_file: Optional[Path] = None,  # The path to the prompt_settings.yaml file
    skip_reprompt: bool = False,  # Whether to skip the re-prompting messages on start
    speak: bool = False,  # Whether to enable speak mode
    debug: bool = False,  # Whether to enable debug mode
    log_level: Optional[str] = None,  # The global log level for the application
    log_format: Optional[str] = None,  # The format for the log(s)
    log_file_format: Optional[str] = None,  # Override the format for the log file
    gpt3only: bool = False,  # Whether to enable GPT3.5 only mode
    gpt4only: bool = False,  # Whether to enable GPT4 only mode
    memory_type: Optional[str] = None,  # The type of memory backend to use
    browser_name: Optional[str] = None,  # The name of the browser to use for scraping the web
    allow_downloads: bool = False,  # Whether to allow AutoGPT to download files natively
    skip_news: bool = False,  # Whether to suppress the output of latest news on startup
) -> None:
    """Updates the config object with the given arguments.

    This function modifies the given config object based on the provided arguments.
    It checks the validity of certain inputs and sets the corresponding config values.

    Args:
        config (Config): The config object to update.
        continuous (bool): Whether to run in continuous mode.
        continuous_limit (int): The number of times to run in continuous mode.
        ai_settings_file (Path): The path to the ai_settings.yaml file.
        prompt_settings_file (Path): The path to the prompt_settings.yaml file.
        skip_reprompt (bool): Whether to skip the re-prompting messages on start.
        speak (bool): Whether to enable speak mode.
        debug (bool): Whether to enable debug mode.
        log_level (int): The global log level for the application.
        log_format (str): The format for the log(s).
        log_file_format (str): Override the format for the log file.
        gpt3only (bool): Whether to enable GPT3.5 only mode.
        gpt4only (bool): Whether to enable GPT4 only mode.
        memory_type (str): The type of memory backend to use.
        browser_name (str): The name of the browser to use for scraping the web.
        allow_downloads (bool): Whether to allow AutoGPT to download files natively.
        skips_news (bool): Whether to suppress the output of latest news on startup.
    """
    config.continuous_mode = False
    config.tts_config.speak_mode = False

    # Set log level
    if debug:
        config.logging.level = logging.DEBUG
    elif log_level and type(_level := logging.getLevelName(log_level.upper())) is int:
        config.logging.level = _level

    # Set log format
    if log_format and log_format in LogFormatName._value2member_map_:
        config.logging.log_format = LogFormatName(log_format)
    if log_file_format and log_file_format in LogFormatName._value2member_map_:
        config.logging.log_file_format = LogFormatName(log_file_format)

    # Functionality for continuous mode
    if continuous:
        logger.warning(
            "Continuous mode is not recommended. It is potentially dangerous and may"
            " cause your AI to run forever or carry out actions you would not usually"
            " authorise. Use at your own risk.",
        )
        config.continuous_mode = True

        if continuous_limit:
            config.continuous_limit = continuous_limit

    # Check if continuous limit is used without continuous mode
    if continuous_limit and not continuous:
        raise click.UsageError("--continuous-limit can only be used with --continuous")

    # Functionality for speak mode
    if speak:
        config.tts_config.speak_mode = True

    # Set the default LLM models
    if gpt3only:
        # --gpt3only should always use gpt-3.5-turbo, despite user's FAST_LLM config
        config.fast_llm = GPT_3_MODEL
        config.smart_llm = GPT_3_MODEL
    elif (
        gpt4only
        and check_model(
            GPT_4_MODEL,
            model_type="smart_llm",
            api_credentials=config.openai_credentials,
        )
        == GPT_4_MODEL
    ):
        # --gpt4only should always use gpt-4, despite user's SMART_LLM config
        config.fast_llm = GPT_4_MODEL
        config.smart_llm = GPT_4_MODEL
    else:
        config.fast_llm = check_model(
            config.fast_llm, "fast_llm", api_credentials=config.openai_credentials
        )
        config.smart_llm = check_model(
            config.smart_llm, "
