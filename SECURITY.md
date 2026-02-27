# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |
| 0.4.x   | No        |

## Reporting a Vulnerability

Email: **64996768+mcp-tool-shop@users.noreply.github.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Version affected
- Potential impact

### Response timeline

| Action | Target |
|--------|--------|
| Acknowledge report | 48 hours |
| Assess severity | 7 days |
| Release fix | 30 days |

## Scope

This tool operates **locally only** — it is a deterministic CLI assistant for accessibility.

- **Data touched:** CLI error JSON/text passed as arguments (read-only), `~/.a11y-assist/last.log` (written by `assist-run`), assist output to stdout or `--json-out` path
- **Data NOT touched:** no files outside specified arguments and output paths, no OS credentials, no browser data
- **No network egress** — all processing is local and deterministic
- **No secrets handling** — does not read, store, or transmit credentials
- **No telemetry** is collected or sent
