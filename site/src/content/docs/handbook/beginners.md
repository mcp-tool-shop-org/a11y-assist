---
title: For Beginners
description: New to a11y-assist? Start here for a gentle introduction.
sidebar:
  order: 99
---

## What is this tool?

When a command-line tool fails, it usually shows an error message written for the developer who built it -- not for the person trying to recover. Stack traces, abbreviated error codes, and dense output can be especially hard to work with if you use a screen reader, have low vision, are under cognitive load, or experience reading difficulties.

a11y-assist adds a structured recovery block to CLI failures. It reads the error output, extracts what went wrong, and presents numbered recovery steps adapted to your accessibility needs. It never changes or hides the original output -- it only adds help alongside it.

The tool is fully deterministic: same input always produces the same output. It makes no network calls, uses no AI models, and collects no data.

## Who is this for?

- **Developers with accessibility needs** who want clearer error recovery guidance from CLI tools
- **Teams building accessible tooling** who want to add structured error assistance to their CLI workflows
- **CI/CD pipelines** that need machine-readable accessibility reports from evidence-engine findings
- **Anyone** who finds raw CLI error output hard to parse and wants a simpler recovery path

## Prerequisites

Before installing a11y-assist, you need:

- **Python 3.10 or later** -- check with `python --version` or `python3 --version`
- **pip** -- the Python package installer (included with Python 3.10+)
- **Basic terminal skills** -- you should be comfortable running commands in a terminal (bash, zsh, PowerShell, or similar)

No additional system dependencies are required. a11y-assist has only two Python dependencies (`click` and `jsonschema`), which pip installs automatically.

## Your First 5 Minutes

**Step 1: Install a11y-assist**

```bash
pip install a11y-assist
```

This installs two commands: `a11y-assist` (the main tool) and `assist-run` (a wrapper for capturing output).

**Step 2: Verify the installation**

```bash
a11y-assist diagnose
```

You should see all checks passing. If any fail, follow the hints printed next to each check.

**Step 3: Wrap a command that might fail**

Pick any CLI command and prefix it with `assist-run`:

```bash
assist-run python -c "raise ValueError('example error')"
```

The command runs normally and its output appears in your terminal. Behind the scenes, `assist-run` saves a copy of the output to `~/.a11y-assist/last.log`.

**Step 4: Get recovery help**

```bash
a11y-assist last
```

You will see a structured ASSIST block with a confidence level, a safest next step, and numbered recovery plan steps. Since this was raw text without structured error data, the confidence will be Low.

**Step 5: Try a different profile**

```bash
a11y-assist last --profile cognitive-load
```

The same recovery plan, now adapted for reduced cognitive effort -- fewer steps, labeled First/Next/Last instead of numbers, and shorter sentences.

## Common Mistakes

**1. Forgetting to use `assist-run` before `a11y-assist last`**

The `last` command reads from `~/.a11y-assist/last.log`, which only exists after you run a command through `assist-run`. If you run `a11y-assist last` without wrapping a command first, you will get a "No last.log found" message.

**2. Confusing `explain` and `triage`**

`explain` requires structured JSON input following the `cli.error.v0.1` schema -- it gives High-confidence results. `triage` accepts raw text via stdin and gives Medium or Low confidence. If you pass raw text to `explain`, it will fail with a validation error. Use `triage --stdin` for unstructured output.

**3. Expecting a11y-assist to fix the error**

a11y-assist does not fix errors. It provides structured recovery guidance using only safe, read-only commands. You still need to follow the steps and apply the fix yourself. The tool is an assistant, not an auto-fixer.

**4. Missing the `--stdin` flag on triage**

The `triage` command requires the `--stdin` flag. Running `a11y-assist triage` without it prints a usage hint and exits. The correct usage is:

```bash
some-tool 2>&1 | a11y-assist triage --stdin
```

**5. Assuming high confidence means the suggestion is correct**

High confidence means the input was well-structured (valid `cli.error.v0.1` JSON with an error ID). It does not guarantee the recovery plan will solve your problem -- it means the plan is anchored to specific error data rather than guessing from raw text.

## Next Steps

- **[Getting Started](/a11y-assist/handbook/getting-started/)** -- More detail on installation, structured input, and the `explain` command
- **[Commands](/a11y-assist/handbook/commands/)** -- Full reference for all six commands and their flags
- **[Profiles](/a11y-assist/handbook/profiles/)** -- Deep dive into each of the five accessibility profiles
- **[Safety](/a11y-assist/handbook/safety/)** -- How the Profile Guard system enforces safety invariants

## Glossary

- **ASSIST block** -- The structured recovery output that a11y-assist adds after the original tool output. Contains a confidence level, safest next step, numbered plan, and optional safe commands.
- **Anchored ID** -- An error identifier (like `NAMESPACE.CATEGORY.DETAIL`) extracted from the input. When present, it links the recovery plan to a specific known error.
- **Confidence** -- A level (High, Medium, or Low) indicating how much structured data the recovery plan is based on. High means validated JSON with an ID. Low means best-effort parsing of raw text.
- **cli.error.v0.1** -- A JSON schema that CLI tools can adopt to emit structured error messages. Using this schema enables the highest-confidence assist path.
- **Profile** -- An accessibility adaptation that transforms ASSIST block output for specific needs (low vision, cognitive load, screen reader, dyslexia, or plain language).
- **Profile Guard** -- A runtime validation system that checks every profile transform against safety invariants before rendering. Prevents profiles from inventing content, inflating confidence, or suggesting unsafe commands.
- **SAFE commands** -- Commands that are read-only, dry-run, or status-check only. a11y-assist never suggests commands that could modify state, delete data, or escalate privileges.
- **Deterministic** -- Same input always produces the same output. No network calls, no randomness, no model invocations.
- **Provenance** -- Evidence tracing in the `ingest` command that links findings back to their original evidence bundles, with digest verification to detect tampering.
