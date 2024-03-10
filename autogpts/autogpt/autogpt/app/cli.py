"""Main script for the autogpt package."""
import os
import sys
from typing import Any
from typing import Optional

import click
from click.types import Path
from logging import _nameToLevel as log_level_map
from typing import Tuple

import autogpt.logs.config as logs_config
from autogpt.logs.config import LogFormatName
from autogpt.app.main import run_auto_gpt
from autogpt.app.main import run_auto_gpt_server


def setup_telemetry() -> None:
    # Implement telemetry setup here
    pass


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    setup_telemetry()

    if ctx.invoked_subcommand is None:
        ctx.invoke(run_command)


@cli.command()
@click.option(
    "-c",
    "--continuous",
    is_flag=True,
    help="Enable Continuous Mode",
)
@click.option(
    "-l",
    "--continuous-limit",
    type=int,
    help="Defines the number of times to run in continuous mode",
)
@click.option("--speak", is_flag=True, help="Enable Speak Mode")
@click.option("--gpt3only", is_flag=True, help="Enable GPT3.5 Only Mode")
@click.option("--gpt4only", is_flag=True, help="Enable GPT4 Only Mode")
@click.option(
    "-b",
    "--browser-name",
    help="Specifies which web-browser to use when using selenium to scrape the web.",
)
@click.option(
    "--allow-downloads",
    is_flag=True,
    help="Dangerous: Allows AutoGPT to download files natively.",
)
@click.option(
    "--workspace-directory",
    "-w",
    type=Path(file_okay=False),
    hidden=True,
)
@click.option(
    "--install-plugin-deps",
    is_flag=True,
    help="Installs external dependencies for 3rd party plugins.",
)
@click.option(
    "--skip-news",
    is_flag=True,
    help="Specifies whether to suppress the output of latest news on startup.",
)
@click.option(
    "--skip-reprompt",
    "-y",
    is_flag=True,
    help="Skips the re-prompting messages at the beginning of the script",
)
@click.option(
    "--ai-settings",
    "-C",
    type=Path(exists=True, dir_okay=False, path_type=Path),
    help=(
        "Specifies which ai_settings.yaml file to use, relative to the AutoGPT"
        " root directory. Will also automatically skip the re-prompt."
    ),
)
@click.option(
    "--ai-name",
    type=str,
    help="AI name override",
)
@click.option(
    "--ai-role",
    type=str,
    help="AI role override",
)
@click.option(
    "--prompt-settings",
    "-P",
    type=Path(exists=True, dir_okay=False, path_type=Path),
    help="Specifies which prompt_settings.yaml file to use.",
)
@click.option(
    "--constraint",
    type=str,
    multiple=True,
    help=(
        "Add or override AI constraints to include in the prompt;"
        " may be used multiple times to pass multiple constraints"
    ),
)
@click.option(
    "--resource",
    type=str,
    multiple=True,
    help=(
        "Add or override AI resources to include in the prompt;"
        " may be used multiple times to pass multiple resources"
    ),
)
@click.option(
    "--best-practice",
    type=str,
    multiple=True,
    help=(
        "Add or override AI best practices to include in the prompt;"
        " may be used multiple times to pass multiple best practices"
    ),
)
@click.option(
    "--override-directives",
    is_flag=True,
    help=(
        "If specified, --constraint, --resource and --best-practice will override"
        " the AI's directives instead of being appended to them"
    ),
)
@click.option(
    "--debug",
    is_flag=True,
    help="Implies --log-level=DEBUG --log-format=debug"
)
@click.option("--log-level", type=click.Choice([*log_level_map.keys()]))
@click.option(
    "--log-format",
    help=(
        "Choose a log format; defaults to 'simple'."
        " Also implies --log-file-format, unless it is specified explicitly."
        " Using the 'structured_google_cloud' format disables log file output."
    ),
    type=click.Choice([i.value for i in LogFormatName]),
)
@click.option(
    "--log-file-format",
    help=(
        "Override the format used for the log file output."
        " Defaults to the application's global --log-format."
    ),
    type=click.Choice([i.value for i in LogFormatName]),
)
@click.pass_context
def run_command(
    ctx: click.Context,
    continuous: bool = False,
    continuous_limit: Optional[int] = None,
    speak: bool = False,
    gpt3only: bool = False,
    gpt4only: bool = False,
    browser_name: Optional[str] = None,
    allow_downloads: bool
