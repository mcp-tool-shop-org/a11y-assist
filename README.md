> ⚠️ **This repository has moved to [accessibility-suite](https://github.com/mcp-tool-shop/accessibility-suite)**
> Source now lives at: `src/a11y-assist/`

---

# a11y-assist

![assist](https://img.shields.io/badge/assist-low--vision--first-blue)
![safe](https://img.shields.io/badge/commands-SAFE--only-green)
![license](https://img.shields.io/badge/license-MIT-black)

Low-vision-first assistant for CLI failures.

**v0.3 is non-interactive and deterministic.**
It never rewrites tool output. It only adds an `ASSIST` block.

## Install

```bash
pip install a11y-assist
```

## Usage

### Explain from structured ground truth (best)

```bash
a11y-assist explain --json message.json
```

### Triage raw CLI output (fallback)

```bash
some-tool do-thing 2>&1 | a11y-assist triage --stdin
```

### Wrapper mode (best UX without tool changes)

```bash
assist-run some-tool do-thing
# if it fails, run:
a11y-assist last
```

### Accessibility profiles

Use `--profile` to select output format:

```bash
# Default: low-vision profile (numbered steps, max 5)
a11y-assist explain --json message.json --profile lowvision

# Cognitive-load profile (reduced, max 3 steps, First/Next/Last labels)
a11y-assist explain --json message.json --profile cognitive-load

# Screen-reader profile (TTS-optimized, expanded abbreviations)
a11y-assist explain --json message.json --profile screen-reader

# Dyslexia profile (reduced reading friction, explicit labels)
a11y-assist explain --json message.json --profile dyslexia

# Plain-language profile (maximum clarity, one clause per sentence)
a11y-assist explain --json message.json --profile plain-language
```

Available profiles:
- **lowvision** (default): Clear labels, numbered steps, SAFE commands
- **cognitive-load**: Reduced cognitive load for ADHD, autism, anxiety, or stress
- **screen-reader**: TTS-optimized for screen readers, braille displays, listen-first workflows
- **dyslexia**: Reduced reading friction, explicit labels, no symbolic emphasis
- **plain-language**: Maximum clarity, one clause per sentence, simplified structure

## Output Format

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

Designed for users who benefit from reduced cognitive load (ADHD, autism, anxiety, stress):

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

Key differences:
- Fixed "Goal" line for orientation
- Max 3 plan steps (vs 5)
- First/Next/Last labels (vs numbers)
- One SAFE command max (vs 3)
- Shorter, simpler sentences
- No parentheticals or verbose explanations

### Screen Reader Profile

Designed for users consuming output via screen readers, TTS, or braille displays:

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

Key differences:
- Spoken-friendly headers (periods instead of colons)
- "Step N:" labels for predictable listening
- Abbreviations expanded (CLI → command line, ID → I D, JSON → J S O N)
- No visual navigation references (above, below, arrow)
- No parentheticals (screen readers read them awkwardly)
- Low confidence reduces to 3 steps (less listening time)

## Confidence Levels

| Level | Meaning |
|-------|---------|
| High | Validated `cli.error.v0.1` JSON with ID |
| Medium | Raw text with detectable `(ID: ...)` |
| Low | Best-effort parse, no ID found |

## Safety

- **SAFE-only** suggested commands in v0.1
- Never invents error IDs
- Confidence is disclosed (High/Medium/Low)
- No network calls
- Never rewrites original output

## Commands

| Command | Description |
|---------|-------------|
| `a11y-assist explain --json <path>` | High-confidence assist from cli.error.v0.1 |
| `a11y-assist triage --stdin` | Best-effort assist from raw text |
| `a11y-assist last` | Assist from `~/.a11y-assist/last.log` |
| `assist-run <cmd> [args...]` | Wrapper that captures output for `last` |

## Integration with a11y-lint

Tools that emit `cli.error.v0.1` JSON get high-confidence assistance:

```bash
# Tool emits structured error
my-tool --json 2> error.json

# Get high-confidence assist
a11y-assist explain --json error.json
```

## Integration (CI / Pipelines)

For automation, use `--json-response` to get machine-readable output:

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

The JSON output follows `assist.response.v0.1` schema and includes:
- `confidence`: High | Medium | Low
- `safest_next_step`: One-sentence recommendation
- `plan`: Ordered list of steps
- `next_safe_commands`: SAFE-only commands (if any)
- `methods_applied`: Audit trail of engine methods used
- `evidence`: Source anchors mapping output to input

See [METHODS_CATALOG.md](METHODS_CATALOG.md) for the full list of method IDs.

## License

MIT
