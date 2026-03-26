---
title: Commands
description: All six a11y-assist commands, their arguments, and shared flags.
sidebar:
  order: 2
---

a11y-assist provides six commands: three assist commands (`explain`, `triage`, `last`), one evidence ingestion command (`ingest`), one environment health check (`diagnose`), and one wrapper (`assist-run`).

## explain

High-confidence assist from `cli.error.v0.1` structured JSON.

```bash
a11y-assist explain --json <path>
```

This is the highest-confidence path. When a tool emits structured error JSON following the `cli.error.v0.1` schema, `explain` validates the JSON against the schema, extracts the error ID, and anchors its suggestions to it. If validation fails, it still produces a Low-confidence assist block with guidance on fixing the JSON.

Accepts `--profile`, `--json-response`, and `--json-out`.

## triage

Best-effort assist from raw CLI text.

```bash
some-tool 2>&1 | a11y-assist triage --stdin
```

Parses unstructured text looking for `[OK]`/`[WARN]`/`[ERROR]` status lines and `(ID: NAMESPACE.CATEGORY.DETAIL)` patterns. Confidence is Medium if an ID pattern is found, Low otherwise. If the text contains `What:`/`Why:`/`Fix:` blocks, those are extracted into the recovery plan.

The `--stdin` flag is required. Without it, the command prints a usage hint and exits.

Accepts `--profile`, `--json-response`, and `--json-out`.

## last

Assist from the last captured log.

```bash
a11y-assist last
```

Reads `~/.a11y-assist/last.log`, which is written by `assist-run`. This is the most common workflow: wrap a command with `assist-run`, then run `a11y-assist last` if it fails. The log is parsed the same way as `triage` -- error IDs and `What:`/`Why:`/`Fix:` blocks are extracted when present.

If no log file exists, it produces a Low-confidence assist block telling you to run `assist-run` first.

Accepts `--profile`, `--json-response`, and `--json-out`.

## ingest

Import findings from a11y-evidence-engine.

```bash
a11y-assist ingest <findings.json>
```

Takes a `findings.json` file from a11y-evidence-engine and produces two output files:

- `ingest-summary.json` -- normalized stats grouped by rule and top files
- `advisories.json` -- fix-oriented tasks with evidence links and default guidance

Output files are written to an `a11y-assist/` directory alongside the findings file by default, or to a custom directory with `--out`.

### ingest flags

| Flag | Description |
|------|-------------|
| `--out <dir>` | Output directory for derived artifacts (default: alongside findings under `a11y-assist/`) |
| `--format text\|json` | Output format for stdout summary (default: `text`) |
| `--min-severity info\|warning\|error` | Minimum severity to include (default: `info`) |
| `--strict` | Fail if evidence_ref files are missing or provenance validation fails |
| `--verify-provenance` | Validate each referenced provenance bundle and verify digests |
| `--fail-on error\|warning\|none` | Exit nonzero if findings exist at or above this severity (default: `error`) |

## diagnose

Check environment health.

```bash
a11y-assist diagnose
```

Runs five checks and reports their status:

1. **Python version** -- confirms Python 3.10+ is installed
2. **Dependencies** -- verifies `click` and `jsonschema` are importable
3. **Schemas** -- confirms `cli.error.schema.v0.1.json` is bundled
4. **State directory** -- checks whether `~/.a11y-assist/` exists
5. **Last log** -- reports whether `last.log` exists and its size

Exits 0 if all checks pass, 1 if any fail. Use `--json-response` for machine-readable output.

This command does not accept `--profile` or `--json-out`.

## assist-run

Wrapper that captures command output for `last`.

```bash
assist-run <cmd> [args...]
```

Runs the given command, prints its combined stdout/stderr to the terminal unchanged, and saves a copy to `~/.a11y-assist/last.log`. If the command exits non-zero, a hint is printed to stderr reminding you to run `a11y-assist last`.

The exit code matches the wrapped command's exit code. This command does not accept `--profile`, `--json-response`, or `--json-out`.

## Shared flags for assist commands

The three assist commands (`explain`, `triage`, `last`) all accept these flags:

| Flag | Description |
|------|-------------|
| `--profile <name>` | Select an accessibility profile: `lowvision` (default), `cognitive-load`, `screen-reader`, `dyslexia`, `plain-language` |
| `--json-response` | Output the ASSIST block as JSON to stdout instead of rendered text |
| `--json-out <path>` | Write JSON output to a file while still rendering text to stdout |

The `diagnose` command accepts only `--json-response`. The `ingest` command has its own flag set (see above). The `assist-run` wrapper accepts no flags.
