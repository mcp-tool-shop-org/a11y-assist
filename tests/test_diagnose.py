"""Tests for the diagnose command."""

from __future__ import annotations

import json

from click.testing import CliRunner

from a11y_assist.cli import main


def test_diagnose_text_output():
    """Diagnose command should produce readable text output."""
    runner = CliRunner()
    result = runner.invoke(main, ["diagnose"])
    assert result.exit_code == 0
    assert "a11y-assist v" in result.output
    assert "python_version" in result.output
    assert "All checks passed" in result.output


def test_diagnose_json_output():
    """Diagnose --json-response should produce valid JSON."""
    runner = CliRunner()
    result = runner.invoke(main, ["diagnose", "--json-response"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "ok" in data
    assert "checks" in data
    assert isinstance(data["checks"], list)
    assert data["ok"] is True


def test_diagnose_checks_python_version():
    """Diagnose should check Python version."""
    runner = CliRunner()
    result = runner.invoke(main, ["diagnose", "--json-response"])
    data = json.loads(result.output)
    py_check = next(c for c in data["checks"] if c["check"] == "python_version")
    assert py_check["status"] == "ok"


def test_diagnose_checks_dependencies():
    """Diagnose should check click and jsonschema dependencies."""
    runner = CliRunner()
    result = runner.invoke(main, ["diagnose", "--json-response"])
    data = json.loads(result.output)
    check_names = [c["check"] for c in data["checks"]]
    assert "dependency.click" in check_names
    assert "dependency.jsonschema" in check_names


def test_diagnose_checks_schemas():
    """Diagnose should verify schema files exist."""
    runner = CliRunner()
    result = runner.invoke(main, ["diagnose", "--json-response"])
    data = json.loads(result.output)
    schema_check = next(c for c in data["checks"] if c["check"] == "schemas")
    assert schema_check["status"] == "ok"


def test_diagnose_checks_package_version():
    """Diagnose should report the package version."""
    runner = CliRunner()
    result = runner.invoke(main, ["diagnose", "--json-response"])
    data = json.loads(result.output)
    ver_check = next(c for c in data["checks"] if c["check"] == "package_version")
    assert ver_check["status"] == "ok"
    assert ver_check["value"] == "1.0.0"


def test_diagnose_checks_state_directory():
    """Diagnose should report state directory status."""
    runner = CliRunner()
    result = runner.invoke(main, ["diagnose", "--json-response"])
    data = json.loads(result.output)
    state_check = next(c for c in data["checks"] if c["check"] == "state_directory")
    assert state_check["status"] in ("ok", "info")
