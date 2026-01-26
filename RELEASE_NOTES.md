# a11y-assist v0.1.0

Initial stable release of **a11y-assist**, a low-vision-first assistant for CLI failures.

## Added

### Core commands
- `a11y-assist explain --json <path>`
  Deterministic assistance from validated `cli.error.v0.1` JSON

- `a11y-assist triage --stdin`
  Best-effort parsing of raw CLI output with explicit confidence labeling

- `a11y-assist last`
  Assist from the most recent captured command output

- `assist-run <command>`
  Wrapper that captures stdout/stderr and suggests help on failure

### Rendering
- Clear **ASSIST (Low Vision)** output block
- Explicit confidence levels: High / Medium / Low
- Structured sections:
  - Safest next step
  - Numbered plan (max 5)
  - SAFE next commands (when applicable)
  - Notes

### Safety guarantees
- Original CLI output is never modified
- No invented error IDs
- SAFE-only command suggestions in v0.1
- No network calls or background services

### Compatibility
- Anchors to `cli.error.v0.1` when present
- Gracefully degrades on raw text
- Works alongside existing tools without modification

## Stability guarantees

- v0.1 output format is considered stable
- No breaking changes without a major version bump
- Interactive or AI-assisted features will not be added to v0.x

## Known limitations

- Raw text triage is heuristic and lower confidence
- Assistance quality depends on the structure of input
- Interactive mode is intentionally not included

## What's next (v0.2.0)

- Optional interactive mode
- Pluggable AI backends (opt-in)
- Additional accessibility profiles beyond low vision
- Deeper integration with a11y-ci workflows

---

Thank you for helping make developer tools more humane.
