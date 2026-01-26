"""CLI entry point for a11y-assist.

Commands:
- explain: High-confidence assist from cli.error.v0.1 JSON
- triage: Best-effort assist from raw text
- last: Assist from ~/.a11y-assist/last.log
- assist-run: Wrapper that captures output for `last`
"""

from __future__ import annotations

import subprocess
import sys
from typing import Callable

import click

from . import __version__
from .from_cli_error import (
    CliErrorValidationError,
    assist_from_cli_error,
    load_cli_error,
)
from .parse_raw import parse_raw
from .profiles import apply_cognitive_load, render_cognitive_load
from .render import AssistResult, render_assist
from .storage import read_last_log, write_last_log

# Profile registry
PROFILE_CHOICES = ["lowvision", "cognitive-load"]


def get_renderer(profile: str) -> Callable[[AssistResult], str]:
    """Get the renderer function for a profile."""
    if profile == "cognitive-load":
        return render_cognitive_load
    return render_assist


def apply_profile(result: AssistResult, profile: str) -> AssistResult:
    """Apply profile transformation to result."""
    if profile == "cognitive-load":
        return apply_cognitive_load(result)
    return result


def render_with_profile(result: AssistResult, profile: str) -> str:
    """Transform and render result according to profile."""
    transformed = apply_profile(result, profile)
    renderer = get_renderer(profile)
    return renderer(transformed)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__)
def main():
    """a11y-assist: low-vision-first assistant for CLI failures (v0.1 non-interactive)."""
    pass


@main.command("explain")
@click.option(
    "--json",
    "json_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to cli.error.v0.1 JSON file.",
)
@click.option(
    "--profile",
    type=click.Choice(PROFILE_CHOICES),
    default="lowvision",
    help="Accessibility profile (default: lowvision).",
)
def explain_cmd(json_path: str, profile: str):
    """Explain a structured cli.error.v0.1 JSON message."""
    try:
        obj = load_cli_error(json_path)
        result = assist_from_cli_error(obj)
        click.echo(render_with_profile(result, profile), nl=False)
    except CliErrorValidationError as e:
        # Low confidence: we couldn't validate
        res = AssistResult(
            anchored_id=None,
            confidence="Low",
            safest_next_step="Emit a valid cli.error.v0.1 JSON message and retry.",
            plan=[
                "Validate your JSON output against cli.error.v0.1.",
                "Include an (ID: NAMESPACE.CATEGORY.DETAIL) field.",
                "Ensure What/Why/Fix are present for WARN/ERROR.",
            ],
            next_safe_commands=[],
            notes=["Validation errors (first 5): " + "; ".join(e.errors[:5])],
        )
        click.echo(render_with_profile(res, profile), nl=False)
        raise SystemExit(2)


@main.command("triage")
@click.option(
    "--stdin",
    "use_stdin",
    is_flag=True,
    help="Read raw CLI output from stdin.",
)
@click.option(
    "--profile",
    type=click.Choice(PROFILE_CHOICES),
    default="lowvision",
    help="Accessibility profile (default: lowvision).",
)
def triage_cmd(use_stdin: bool, profile: str):
    """Triage raw CLI output (best effort)."""
    if not use_stdin:
        click.echo("Use: a11y-assist triage --stdin", err=True)
        raise SystemExit(2)

    text = sys.stdin.read()
    err_id, status, blocks = parse_raw(text)

    notes = []
    confidence: str = "Low"
    if err_id:
        confidence = "Medium"
    else:
        notes.append("No (ID: ...) found. Emit cli.error.v0.1 for high-confidence assist.")

    safest = "Follow the tool's Fix steps, starting with the least risky check."
    plan = []

    fix_lines = blocks.get("Fix:", [])
    if fix_lines:
        plan = fix_lines[:]
    else:
        plan = [
            "Re-run the command with increased verbosity/logging.",
            "Update the tool to emit (ID: ...) and What/Why/Fix blocks.",
            "If this is your tool, adopt cli.error.v0.1 JSON output.",
        ]

    res = AssistResult(
        anchored_id=err_id,
        confidence=confidence,  # type: ignore[arg-type]
        safest_next_step=safest,
        plan=plan,
        next_safe_commands=[line for line in plan if "--dry-run" in line][:3],
        notes=notes,
    )
    click.echo(render_with_profile(res, profile), nl=False)


@main.command("last")
@click.option(
    "--profile",
    type=click.Choice(PROFILE_CHOICES),
    default="lowvision",
    help="Accessibility profile (default: lowvision).",
)
def last_cmd(profile: str):
    """Assist using the last captured log (~/.a11y-assist/last.log)."""
    text = read_last_log()
    if not text.strip():
        res = AssistResult(
            anchored_id=None,
            confidence="Low",
            safest_next_step="Run a command via assist-run or provide input via triage --stdin.",
            plan=["Try: assist-run <your-command>", "Then: a11y-assist last"],
            next_safe_commands=[],
            notes=["No last.log found."],
        )
        click.echo(render_with_profile(res, profile), nl=False)
        raise SystemExit(2)

    err_id, status, blocks = parse_raw(text)
    confidence: str = "Medium" if err_id else "Low"
    notes = [] if err_id else ["No (ID: ...) found in last.log."]

    plan = blocks.get("Fix:", []) or [
        "Re-run with verbosity.",
        "Adopt cli.error.v0.1 output for high-confidence assistance.",
    ]

    res = AssistResult(
        anchored_id=err_id,
        confidence=confidence,  # type: ignore[arg-type]
        safest_next_step="Start with the first Fix step. Prefer non-destructive checks.",
        plan=plan,
        next_safe_commands=[line for line in plan if "--dry-run" in line][:3],
        notes=notes,
    )
    click.echo(render_with_profile(res, profile), nl=False)


def assist_run():
    """Wrapper entry-point (console_script): captures stdout/stderr to last.log.

    Usage: assist-run <cmd> [args...]
    """
    if len(sys.argv) < 2:
        print("Usage: assist-run <command> [args...]", file=sys.stderr)
        raise SystemExit(2)

    cmd = sys.argv[1:]
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    output = proc.stdout or ""

    # Print original output unchanged
    sys.stdout.write(output)

    # Save for a11y-assist last
    write_last_log(output)

    if proc.returncode != 0:
        print("\nTip: run `a11y-assist last` for help", file=sys.stderr)

    raise SystemExit(proc.returncode)
