# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-02-27

### Added

- Verify script: test + CLI smoke + build in one command
- Dependency audit job in CI
- Codecov upload in CI (Python 3.12)
- Threat model paragraph in README (Security & Data Scope)
- Codecov badge in README
- Shipcheck compliance: SHIP_GATE.md, SCORECARD.md

### Changed

- Bumped to v1.0.0 — production-stable
- Classifier updated to Production/Stable
- SECURITY.md updated with real data scope
- Added pytest-cov to dev dependencies

## [0.4.3] — 2026-02-25

### Added

- Landing page via @mcptoolshop/site-theme
- 7 translations (ja, zh, es, fr, hi, it, pt-BR)
- Brand logo in README

## [0.4.0] — 2026-02-24

### Added

- `ingest` command for a11y-evidence-engine findings
- Profile Guard system with safety invariants
- CI pipeline with lint, test (3.11/3.12), build

## [0.3.0] — 2026-02-23

### Added

- Five accessibility profiles: lowvision, cognitive-load, screen-reader, dyslexia, plain-language
- Confidence levels (High/Medium/Low) with disclosure
- `assist-run` wrapper command

## [0.1.0] — 2026-02-22

### Added

- Initial release
- `explain` command for structured cli.error.v0.1 JSON
- `triage` command for raw CLI text
- `last` command for captured output
- SAFE-only command suggestions
