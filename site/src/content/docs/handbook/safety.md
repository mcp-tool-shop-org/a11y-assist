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

The Profile Guard system validates every profile transform against the safety invariants before the output is rendered. If a transform would violate any ERROR-level invariant (for example, by introducing a non-SAFE command or inflating confidence), the guard rejects the output entirely and exits with code 2. It prints the guard violation codes to stderr so the issue can be diagnosed. Guard failures indicate an engine bug, not a user error.

The guard checks are:

1. **ID provenance** -- anchored error IDs cannot be invented or changed by a profile
2. **Confidence monotonicity** -- confidence can only stay the same or decrease, never increase
3. **Command safety** -- every suggested command must exist in the base result's allowed set; no commands are permitted on Low confidence
4. **Step count caps** -- each profile enforces a maximum number of plan steps (e.g., 3 for cognitive-load, 5 for lowvision)
5. **Content support** -- plan steps and suggestions are checked against the original input text to prevent invented content (WARN level)
6. **Profile-specific constraints** -- screen-reader and dyslexia profiles forbid parentheticals and visual navigation references; plain-language forbids parentheticals
