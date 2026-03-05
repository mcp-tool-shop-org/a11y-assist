---
title: Safety
description: Safety guarantees enforced by the Profile Guard system.
sidebar:
  order: 4
---

a11y-assist enforces strict safety invariants at runtime. Every profile transform is validated against these invariants before rendering. This page documents what is guaranteed and how it is enforced.

## SAFE-only commands

Only read-only, dry-run, and status-check commands are ever suggested in recovery plans. a11y-assist maintains an allowlist of safe command patterns and rejects anything that could modify state, delete data, or escalate privileges.

No destructive commands will ever appear in an ASSIST block.

## No invented IDs

Error IDs in the ASSIST block come directly from the input or are absent. a11y-assist never fabricates an error ID. If the input contains `(ID: SOME_ERROR)`, that exact ID is used. If no ID is found, the output says so.

## No invented content

Profiles rephrase the recovery guidance to match their accessibility goals, but they never add new factual claims. A cognitive-load profile may simplify a sentence, but it will not invent a new diagnostic step or claim a cause that was not in the original analysis.

## Confidence disclosed

Every ASSIST block includes a confidence level (High, Medium, or Low). This level is always visible to the user. Confidence can decrease during profile transformation -- for example, if simplification removes context -- but it can never increase. The user always knows how much to trust the suggestion.

## Additive only

a11y-assist never modifies, hides, or suppresses the original tool output. The ASSIST block is appended after the original output. The user always sees exactly what the tool produced, plus the recovery guidance.

## Deterministic

Same input always produces the same output. There are no network calls, no randomness, and no model invocations. a11y-assist is a pure function from input to output. This makes it safe for CI pipelines and reproducible debugging.

## Guard-checked

The Profile Guard system validates every profile transform against the safety invariants before the output is rendered. If a transform would violate any invariant (for example, by introducing a non-SAFE command or inflating confidence), the guard rejects it and falls back to the default lowvision profile.

The guard checks are:

1. **Command safety** -- every suggested command is checked against the SAFE allowlist
2. **ID provenance** -- error IDs are traced back to the input
3. **Content fidelity** -- no new factual claims added by profile transforms
4. **Confidence monotonicity** -- confidence can only stay the same or decrease
5. **Additivity** -- original output is preserved in full
6. **Determinism** -- output is compared against a reference for the same input
