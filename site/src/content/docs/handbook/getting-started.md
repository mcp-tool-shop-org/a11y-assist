---
title: Getting Started
description: Install a11y-assist, run your first assisted command, and switch profiles.
sidebar:
  order: 1
---

## Install

Install from PyPI:

```bash
pip install a11y-assist
```

Requires **Python 3.11** or later.

## Quick Start

Wrap any command with `assist-run` so a11y-assist can capture its output:

```bash
assist-run some-tool do-thing
```

If the command fails, get accessible recovery guidance:

```bash
a11y-assist last
```

Switch profiles to match your needs:

```bash
a11y-assist last --profile cognitive-load
```

## How it works

1. `assist-run` wraps a command and saves its stdout/stderr to `~/.a11y-assist/last.log`
2. `a11y-assist last` reads the captured log and produces a structured ASSIST block
3. The ASSIST block contains numbered recovery steps using only SAFE commands
4. The `--profile` flag adapts the output for different accessibility needs

## Structured input

For higher-confidence results, pass structured error JSON directly:

```bash
a11y-assist explain --json error.json
```

Or pipe raw text for best-effort analysis:

```bash
some-tool 2>&1 | a11y-assist triage --stdin
```
