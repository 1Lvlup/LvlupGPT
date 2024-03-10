from pathlib import Path
import sys
import asyncio
import yaml
import click
from autogpt.core.runner.cli_app.main import run_auto_gpt
from autogpt.core.runner.client_lib.shared_click_commands import (
    DEFAULT_SETTINGS_FILE,
    make_settings,
)
from autogpt.core.runner.client_lib.utils import handle_exceptions

Final = typing.Final

DEFAULT_SETTINGS_FILE: Final = DEFAULT_SETTINGS_FILE

@autogpt.command()
@click.option(
    "--settings-file",
    type=click.Path(exists=True),
    default=DEFAULT_SETTINGS_FILE,
)
@click.option(
    "--pdb",
    is_flag=True,
    help="Drop into a debugger if an error is raised.",
)
@click.pass_context
async def run(ctx: click.Context, settings_file: Path, pdb: bool) -> None:
    """Run the AutoGPT agent."""
    click.echo("Running AutoGPT agent...")
    settings = {}
    if settings_file.exists():
        settings = yaml.safe_load(settings_file.read_text())
    ctx.obj = settings
    main = handle_exceptions(run_auto_gpt, with_debugger=pdb)
   
