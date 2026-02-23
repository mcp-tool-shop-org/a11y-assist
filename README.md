<p align="center">
  <img src="logo.png" alt="a11y-assist logo" width="140" />
</p>
<h1 align="center">a11y-assist</h1>
<p align="center">
  <strong>Low-vision-first assistant for CLI failures. Additive, deterministic, safe.</strong><br/>
  Part of <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
<p align="center">
  <a href="https://pypi.org/project/a11y-assist/"><img src="https://img.shields.io/pypi/v/a11y-assist?color=blue" alt="PyPI version" /></a>
  <a href="https://github.com/mcp-tool-shop-org/a11y-assist/actions"><img src="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <img src="https://img.shields.io/badge/python-3.11%20%7C%203.12-blue" alt="Python versions" />
  <img src="https://img.shields.io/badge/commands-SAFE--only-green" alt="safe" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-black" alt="license" /></a>
</p>

---

**v0.4 is non-interactive and deterministic.**
It never rewrites tool output. It only adds an ASSIST block.

## Why

When a CLI tool fails, the error message is usually written for the developer who built it, not for the person trying to recover from it. If you use a screen reader, have low vision, or are under cognitive load, a wall of stack traces and abbreviated codes is not help -- it is another obstacle.

**a11y-assist** adds a structured recovery block to any CLI failure:

- Anchors suggestions to the original error ID (when available)
- Produces numbered, profile-adapted recovery plans
- Only suggests SAFE commands (read-only, dry-run, status checks)
- Discloses confidence level so the user knows how much to trust the suggestion
- Never rewrites or hides the original tool output

Five accessibility profiles ship out of the box: low vision, cognitive load, screen reader, dyslexia, and plain language.

## Install

```bash
pip install a11y-assist
```

Requires Python 3.11 or later.

## Quick Start

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

## Commands

| Command | Description |
|---------|-------------|
| `a11y-assist explain --json <path>` | High-confidence assist from `cli.error.v0.1` JSON |
| `a11y-assist triage --stdin` | Best-effort assist from raw CLI text |
| `a11y-assist last` | Assist from the last captured log (`~/.a11y-assist/last.log`) |
| `a11y-assist ingest <findings.json>` | Import findings from a11y-evidence-engine |
| `assist-run <cmd> [args...]` | Wrapper that captures output for `last` |

All commands accept `--profile`, `--json-response`, and `--json-out` flags.

## Usage

### Explain from structured ground truth (best)

```bash
a11y-assist explain --json message.json
```

When a tool emits `cli.error.v0.1` JSON, the assist is high-confidence: the error ID is anchored, the plan comes directly from Fix steps, and SAFE commands are extracted verbatim.

### Triage raw CLI output (fallback)

```bash
some-tool do-thing 2>&1 | a11y-assist triage --stdin
```

For tools that don't emit structured JSON, triage parses raw text heuristically. Confidence is lower but still useful.

### Wrapper mode (best UX without tool changes)

```bash
assist-run some-tool do-thing
# if it fails, run:
a11y-assist last
```

`assist-run` captures stdout and stderr to `~/.a11y-assist/last.log`, then `last` processes it. No changes to the wrapped tool required.

### Ingest evidence-engine findings

```bash
a11y-assist ingest findings.json --verify-provenance --strict
```

Imports findings from [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine), producing `ingest-summary.json` and `advisories.json` with fix-oriented tasks and evidence links.

## Accessibility Profiles

Use `--profile` to select output adapted to your needs:

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Profile | Primary benefit | Max steps | Key adaptations |
|---------|-----------------|-----------|-----------------|
| **lowvision** (default) | Visual clarity | 5 | Clear labels, numbered steps, SAFE commands |
| **cognitive-load** | Reduced mental steps | 3 | Goal line, First/Next/Last labels, shorter sentences |
| **screen-reader** | Audio-first | 3-5 | TTS-friendly, abbreviations expanded, no visual refs |
| **dyslexia** | Reduced reading friction | 5 | Explicit labels, no symbolic emphasis, extra spacing |
| **plain-language** | Maximum clarity | 4 | One clause per sentence, simplified structure |

### Low Vision Profile (default)

```
ASSIST (Low Vision):
- Anchored to: PAY.EXPORT.SFTP.AUTH
- Confidence: High

Safest next step:
  Start by confirming the cause described under 'Why', then apply the first Fix step.

Plan:
  1) Verify credentials.
  2) Re-run: payroll export --batch 2026-01-26 --dry-run

Next (SAFE):
  payroll export --batch 2026-01-26 --dry-run

Notes:
  - Original title: Payment export failed
  - This assist block is additive; it does not replace the tool's output.
```

### Cognitive Load Profile

```
ASSIST (Cognitive Load):
- Anchored to: PAY.EXPORT.SFTP.AUTH
- Confidence: High

Goal: Get back to a known-good state.

Safest next step:
  Verify credentials.

Plan:
  First: Verify credentials.
  Next: Re-run with dry-run flag.
  Last: Check output for success.

Next (SAFE):
  payroll export --batch 2026-01-26 --dry-run
```

### Screen Reader Profile

```
ASSIST. Profile: Screen reader.
Anchored I D: PAY.EXPORT.SFTP.AUTH.
Confidence: High.

Summary: Payment export failed.

Safest next step: Confirm the credential method used for S F T P.

Steps:
Step 1: Verify the username and password or the S S H key.
Step 2: Run the dry run export.
Step 3: Retry the upload.

Next safe command:
payroll export --batch 2026-01-26 --dry-run
```

### Dyslexia Profile

```
ASSIST (Dyslexia-Friendly):

Anchored to: PAY.EXPORT.SFTP.AUTH

Confidence: High

Safest next step:
  Verify credentials.

Plan:
  Step 1: Verify credentials.
  Step 2: Re-run with dry-run flag.

Try this safe command:
  payroll export --batch 2026-01-26 --dry-run
```

### Plain Language Profile

```
ASSIST (Plain Language):

Anchored to: PAY.EXPORT.SFTP.AUTH

Confidence: High

Safest next step:
  Verify credentials.

Plan:
  1. Verify credentials.
  2. Re-run with dry-run flag.

Try this safe command:
  payroll export --batch 2026-01-26 --dry-run
```

## Confidence Levels

| Level | Meaning | When |
|-------|---------|------|
| **High** | Validated `cli.error.v0.1` JSON with ID | Tool emits structured error output |
| **Medium** | Raw text with detectable `(ID: ...)` | Error ID found in unstructured text |
| **Low** | Best-effort parse, no ID found | No anchor; suggestions are heuristic |

Confidence is always disclosed in the output. It never increases during profile transformation.

## Safety Guarantees

a11y-assist enforces strict safety invariants at runtime through its Profile Guard system:

- **SAFE-only commands** — only read-only, dry-run, and status-check commands are suggested
- **No invented IDs** — error IDs come from the input or are absent; never fabricated
- **No invented content** — profiles rephrase but never add new factual claims
- **Confidence disclosed** — always shown; can decrease but never increase
- **Additive only** — original tool output is never modified, hidden, or suppressed
- **Deterministic** — same input always produces the same output; no network calls, no randomness
- **Guard-checked** — every profile transform is validated against invariants before rendering

Guard violations produce structured error output with machine-readable codes (e.g., `A11Y.ASSIST.GUARD.COMMANDS.INVENTED`).

## JSON Output (CI / Pipelines)

For automation, use `--json-response` to get machine-readable output:

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

The JSON output follows the `assist.response.v0.1` schema:

```json
{
  "schema": "assist.response.v0.1",
  "anchored_id": "PAY.EXPORT.SFTP.AUTH",
  "confidence": "High",
  "safest_next_step": "Start by confirming the cause...",
  "plan": ["Verify credentials.", "Re-run with --dry-run"],
  "next_safe_commands": ["payroll export --batch 2026-01-26 --dry-run"],
  "notes": ["Original title: Payment export failed"],
  "methods_applied": ["engine.normalize.from_cli_error_v0_1", "profile.lowvision.apply"],
  "evidence": [{"field": "plan[0]", "source": "cli.error.fix[0]"}]
}
```

## Integration with cli.error.v0.1

Tools that emit `cli.error.v0.1` JSON get high-confidence assistance:

```bash
# Tool emits structured error
my-tool --json 2> error.json

# Get high-confidence assist
a11y-assist explain --json error.json
```

Adopting `cli.error.v0.1` in your tool means every user gets anchored recovery plans, regardless of their accessibility needs.

## Architecture

```
Input (JSON / raw text / last.log)
  │
  ├─ from_cli_error.py    ← validates cli.error.v0.1
  ├─ parse_raw.py         ← heuristic ID + block extraction
  │
  ▼
AssistResult (anchored_id, confidence, plan, safe_commands, evidence)
  │
  ├─ profiles/            ← lowvision, cognitive-load, screen-reader, dyslexia, plain-language
  │
  ▼
Profile Transform (rephrase, reduce, adapt)
  │
  ├─ guard.py             ← runtime invariant checker
  │
  ▼
Rendered Output (text or JSON)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
