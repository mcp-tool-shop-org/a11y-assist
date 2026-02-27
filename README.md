<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/a11y-assist/readme.png" alt="a11y-assist" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/a11y-assist/"><img src="https://img.shields.io/pypi/v/a11y-assist?color=blue" alt="PyPI"></a>
  <a href="https://codecov.io/gh/mcp-tool-shop-org/a11y-assist"><img src="https://codecov.io/gh/mcp-tool-shop-org/a11y-assist/branch/main/graph/badge.svg" alt="Coverage"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/a11y-assist/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**Deterministic accessibility assistance for CLI failures. Additive, SAFE-only, profile-driven.**

---

**v0.4 is non-interactive and deterministic.**
It never rewrites tool output. It only adds an ASSIST block.

---

## Why

When a CLI tool fails, the error message is usually written for the developer who built it, not for the person trying to recover from it. If you use a screen reader, have low vision, or are under cognitive load, a wall of stack traces and abbreviated codes is not help -- it is another obstacle.

**a11y-assist** adds a structured recovery block to any CLI failure:

- Anchors suggestions to the original error ID (when available)
- Produces numbered, profile-adapted recovery plans
- Only suggests SAFE commands (read-only, dry-run, status checks)
- Discloses confidence level so the user knows how much to trust the suggestion
- Never rewrites or hides the original tool output

Five accessibility profiles ship out of the box: low vision, cognitive load, screen reader, dyslexia, and plain language.

---

## Install

```bash
pip install a11y-assist
```

Requires Python 3.11 or later.

---

## Quick Start

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

---

## Commands

| Command | Description |
|---------|-------------|
| `a11y-assist explain --json <path>` | High-confidence assist from `cli.error.v0.1` JSON |
| `a11y-assist triage --stdin` | Best-effort assist from raw CLI text |
| `a11y-assist last` | Assist from the last captured log (`~/.a11y-assist/last.log`) |
| `a11y-assist ingest <findings.json>` | Import findings from a11y-evidence-engine |
| `assist-run <cmd> [args...]` | Wrapper that captures output for `last` |

All commands accept `--profile`, `--json-response`, and `--json-out` flags.

---

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

---

## Confidence Levels

| Level | Meaning | When |
|-------|---------|------|
| **High** | Validated `cli.error.v0.1` JSON with ID | Tool emits structured error output |
| **Medium** | Raw text with detectable `(ID: ...)` | Error ID found in unstructured text |
| **Low** | Best-effort parse, no ID found | No anchor; suggestions are heuristic |

Confidence is always disclosed in the output. It never increases during profile transformation.

---

## Safety Guarantees

a11y-assist enforces strict safety invariants at runtime through its Profile Guard system:

- **SAFE-only commands** — only read-only, dry-run, and status-check commands are suggested
- **No invented IDs** — error IDs come from the input or are absent; never fabricated
- **No invented content** — profiles rephrase but never add new factual claims
- **Confidence disclosed** — always shown; can decrease but never increase
- **Additive only** — original tool output is never modified, hidden, or suppressed
- **Deterministic** — same input always produces the same output; no network calls, no randomness
- **Guard-checked** — every profile transform is validated against invariants before rendering

---

## JSON Output (CI / Pipelines)

For automation, use `--json-response` to get machine-readable output:

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## Related

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - Headless evidence engine
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - MCP tools for accessibility
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - Demo with CI workflows

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Security & Data Scope

**Data touched:** CLI error JSON/text passed as arguments (read-only), `~/.a11y-assist/last.log` (written by `assist-run`), assist output to stdout or `--json-out` path. **Data NOT touched:** no files outside specified arguments and output paths, no OS credentials, no browser data. **No network egress** — all processing is local and deterministic. **No telemetry** is collected or sent.

## License

[MIT](LICENSE)

---

Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
