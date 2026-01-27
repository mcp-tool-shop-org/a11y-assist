# a11y-assist v0.2.1

Third stable release of **a11y-assist**, adding the screen-reader accessibility profile.

## Added

### Screen-reader profile (`--profile screen-reader`)
Designed for users consuming output via:
- Screen readers / TTS
- Braille displays
- Listen-first workflows (hands busy, eyes fatigued)

Features:
- Spoken-friendly headers (periods instead of colons)
- "Step N:" labels for predictable listening
- Abbreviations expanded (CLI → command line, ID → I D, JSON → J S O N, SFTP → S F T P)
- No visual navigation references (above, below, left, right, arrow)
- No parentheticals (screen readers read them awkwardly)
- Low confidence reduces to 3 steps (less listening time)
- Summary line for quick context

### Profile selection now includes screen-reader
All commands support `--profile lowvision|cognitive-load|screen-reader`:
- `a11y-assist explain --json <path> --profile screen-reader`
- `a11y-assist triage --stdin --profile screen-reader`
- `a11y-assist last --profile screen-reader`

### Screen-reader invariants (in addition to base invariants)
- No meaning in punctuation/formatting alone
- No "visual navigation" references
- Avoid parentheticals as meaning carriers
- Abbreviations expanded for TTS clarity

## Changed

- Version bump to 0.2.1
- 56 new tests for screen-reader profile (132 total)

## Unchanged from v0.2.0

All v0.2.0 features remain stable:
- Cognitive-load profile (`--profile cognitive-load`)
- Low-vision profile (`--profile lowvision`, default)
- Core commands: explain, triage, last, assist-run
- Safety guarantees: no invented IDs, SAFE-only, deterministic

## Stability guarantees

- v0.2.x output format is considered stable for all three profiles
- No breaking changes without a major version bump
- Interactive or AI-assisted features will not be added to v0.x

## What's next (v0.3.0)

- Optional interactive mode
- Pluggable AI backends (opt-in)
- Deeper integration with a11y-ci workflows

---

# a11y-assist v0.2.0

Second stable release of **a11y-assist**, adding the cognitive-load accessibility profile.

## Added

### Cognitive-load profile (`--profile cognitive-load`)
Designed for users who benefit from reduced cognitive load:
- ADHD / executive dysfunction
- Autism / sensory overload
- Anxiety under incident conditions
- Novices under stress

Features:
- Fixed "Goal" line for orientation
- Max 3 plan steps (vs 5 in low-vision)
- First/Next/Last labels instead of numbers
- One SAFE command max (vs 3)
- Shorter, simpler sentences
- No parentheticals or verbose explanations

### Profile selection via `--profile` flag
All commands now support `--profile lowvision|cognitive-load`:
- `a11y-assist explain --json <path> --profile cognitive-load`
- `a11y-assist triage --stdin --profile cognitive-load`
- `a11y-assist last --profile cognitive-load`

### Invariants (non-negotiable)
The cognitive-load profile enforces strict invariants:
1. **No invented facts** - only rephrases existing content
2. **No invented commands** - SAFE commands are verbatim from input
3. **SAFE-only** remains absolute
4. **Additive** - doesn't rewrite original output
5. **Deterministic** - no randomness, no network calls

## Changed

- Default profile is `lowvision` (backward compatible)
- Version bump to 0.2.0

---

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

---

Thank you for helping make developer tools more humane.
