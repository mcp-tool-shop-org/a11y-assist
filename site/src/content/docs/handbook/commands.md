---
title: Commands
description: All five a11y-assist commands, their arguments, and shared flags.
sidebar:
  order: 2
---

## explain

High-confidence assist from `cli.error.v0.1` structured JSON.

```bash
a11y-assist explain --json <path>
```

This is the highest-confidence path. When a tool emits structured error JSON following the `cli.error.v0.1` schema, `explain` can anchor its suggestions to the original error ID.

## triage

Best-effort assist from raw CLI text.

```bash
some-tool 2>&1 | a11y-assist triage --stdin
```

Parses unstructured text and attempts to detect error IDs. Confidence is Medium if an `(ID: ...)` pattern is found, Low otherwise.

## last

Assist from the last captured log.

```bash
a11y-assist last
```

Reads `~/.a11y-assist/last.log`, which is written by `assist-run`. This is the most common workflow: wrap a command, then ask for help if it fails.

## ingest

Import findings from a11y-evidence-engine.

```bash
a11y-assist ingest <findings.json> --verify-provenance
```

Accepts evidence-engine finding files and produces recovery plans from their structured data. The `--verify-provenance` flag validates that findings have not been tampered with.

## assist-run

Wrapper that captures command output for `last`.

```bash
assist-run <cmd> [args...]
```

Runs the given command, pipes its output to the terminal as normal, and saves a copy to `~/.a11y-assist/last.log`. If the command exits non-zero, a hint is printed reminding you to run `a11y-assist last`.

## Shared flags

All commands accept these flags:

| Flag | Description |
|------|-------------|
| `--profile <name>` | Select an accessibility profile (lowvision, cognitive-load, screen-reader, dyslexia, plain-language) |
| `--json-response` | Output the ASSIST block as JSON to stdout instead of rendered text |
| `--json-out <path>` | Write JSON output to a file while still rendering text to stdout |
