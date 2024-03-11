#!/usr/bin/env python3

import click
from typing import Dict, List, Optional

from agbenchmark.reports.processing.report_types import Report, Test

@click.command()
@click.argument("report_json_file", type=click.Path(exists=True, dir_okay=False))
def print_markdown_report(report_json_file: str):
    """
    Generates a Markdown report from a given report.json file.
    This function uses the `click` library to create a command line interface.
    The `@click.command()` decorator defines the command and its arguments.
    Here, the command is `print_markdown_report` and it takes one argument,
    `report_json_file`, which is the path to the report JSON file.
    """
    report = Report.parse_file(report_json_file)

    print_header_metadata(report)
    print_test_results(report.tests)
    print_summary(report.tests)


def print_header_metadata(report: Report):
    """Prints the header and metadata of the report."""

    click.echo(f"# Benchmark Report")
    click.echo(f"- ⌛ **Run time:** `{report.metrics.run_time}`")
    click.echo(
        f"  - **Started at:** `{report.benchmark_start_time[:16].replace('T', '` `')}`"
    )
    if report.completion_time:
        click.echo(
            f"  - **Completed at:** `{report.completion_time[:16].replace('T', '` `')}`"
        )
    if report.metrics.total_cost:
        click.echo(f"- 💸 **Total cost:** `${round(report.metrics.total_cost, 2)}`")
    click.echo(
        f"- 🏅 **Highest achieved difficulty:** `{report.metrics.highest_difficulty}`"
    )
    click.echo(f"- ⚙️ **Command:** `{report.command}`")

    click.echo()  # spacing


def print_test_results(tests: Dict[str, Test]):
    """Prints the test results."""

    click.echo("## Challenges")
    for test in tests.values():
        print_test_result(test)


def print_test_result(test: Test):
    """Prints the result of a single test."""

        click.echo()  # spacing

        result_indicator = (
            "✅"
            if test.metrics.success_percentage == 100.0
            else "⚠️"
            if test.metrics.success_percentage > 0
            else "❌"
        )
        click.echo(
            f"### {test.name} {result_indicator if test.metrics.attempted else '❔'}"
        )
        click.echo(f"{test.description}")

        click.echo()  # spacing

        click.echo(f"- **Attempted:** {'Yes 👍' if test.metrics.attempted else 'No 👎'}")
        click.echo(
            f"- **Success rate:** {round(test.metrics.success_percentage)}% "
            f"({len([r for r in test.results if r.success])}/{len(test.results)})"
        )
        click.echo(f"- **Difficulty:** `{test.difficulty}`")
        click.echo(f"- **Categories:** `{'`, `'.join(test.category)}`")
        click.echo(
            f"<details>\n<summary><strong>Task</strong> (click to expand)</summary>\n\n"
            f"{indent('> ', test.task)}\n\n"
            f"Reference answer:\n{indent('> ', test.answer)}\n"
            "</details>"
        )

        click.echo()  # spacing

        click.echo("\n#### Attempts")
        for i, attempt in enumerate(test.results, 1):
            click.echo(
                f"\n{i}. **{'✅ Passed' if attempt.success else '❌ Failed'}** "
                f"in **{attempt.run_time}** "
                f"and **{quantify('step', attempt.n_steps)}**\n"
            )
            if attempt.cost is not None:
                click.echo(f"   - **Cost:** `${round(attempt.cost, 3)}`")
            if attempt.fail_reason:
                click.echo(
                    "   - **Failure reason:**\n"
                    + indent("      > ", attempt.fail_reason)
                    + "\n"
                )
            if attempt.steps:
                click.echo(
                    indent(
                        3 * " ",
                        "<details>\n<summary><strong>Steps</strong></summary>\n",
                    )
                )
                for j, step in enumerate(attempt.steps, 1):
                    click.echo()
                    click.echo(
                        indent(3 * " ", f"{j}. {indent(3*' ', step.output, False)}")
                    )
                click.echo("\n</details>")


def print_summary(tests: Dict[str, Test]):
    """Prints the summary of the test results."""

    click.echo()  # spacing
    click.echo("## Summary")

    successful, failed, unreliable = get_test_status_counts(tests)

    click.echo(f"- **`{successful}` passed** {'✅'*successful}")
    click.echo(f"- **`{failed}` failed** {'❌'*failed}")
    click.echo(f"- **`{unreliable}` unreliable** {'⚠️'*unreliable}")


def get_test_status_counts(tests: Dict[str,
