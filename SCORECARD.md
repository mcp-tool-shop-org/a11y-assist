# Scorecard

> Score a repo before remediation. Fill this out first, then use SHIP_GATE.md to fix.

**Repo:** a11y-assist
**Date:** 2026-02-27
**Type tags:** `[all]` `[pypi]` `[cli]`

## Pre-Remediation Assessment

| Category | Score | Notes |
|----------|-------|-------|
| A. Security | 4/10 | SECURITY.md template only, no threat model in README |
| B. Error Handling | 8/10 | Custom exceptions (CliErrorValidationError, IngestError, GuardViolation), exit codes, no raw stacks |
| C. Operator Docs | 7/10 | README comprehensive, CHANGELOG empty, LICENSE present |
| D. Shipping Hygiene | 6/10 | CI has lint+test+build, but no verify script, no dep audit, no coverage |
| E. Identity (soft) | 10/10 | Logo, translations, landing page, GitHub metadata |
| **Overall** | **35/50** | |

## Key Gaps

1. SECURITY.md template only — no real data scope (Section A)
2. CHANGELOG empty — no release entries (Section C)
3. No verify script (Section D)
4. No Codecov upload in CI (Section D)
5. No dependency audit in CI (Section D)

## Post-Remediation

| Category | Before | After |
|----------|--------|-------|
| A. Security | 4/10 | 10/10 |
| B. Error Handling | 8/10 | 10/10 |
| C. Operator Docs | 7/10 | 10/10 |
| D. Shipping Hygiene | 6/10 | 10/10 |
| E. Identity (soft) | 10/10 | 10/10 |
| **Overall** | 35/50 | **50/50** |
