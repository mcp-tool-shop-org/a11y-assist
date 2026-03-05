---
title: Profiles
description: Five accessibility profiles that adapt recovery plan output to different needs.
sidebar:
  order: 3
---

a11y-assist ships with five accessibility profiles. Each profile transforms the ASSIST block output to match a specific set of needs. Use `--profile <name>` with any command.

## lowvision (default)

The default profile, optimized for visual clarity.

- **Max steps:** 5
- **Primary benefit:** Clear labels, numbered steps, SAFE commands
- **Adaptations:** High-contrast text structure, explicit step numbering, commands formatted for easy copying, no dense paragraphs

```bash
a11y-assist last --profile lowvision
```

## cognitive-load

Reduces mental effort required to follow recovery steps.

- **Max steps:** 3
- **Primary benefit:** Reduced mental steps with Goal/First/Next/Last labels
- **Adaptations:** Starts with a single Goal line summarizing the fix, steps labeled First/Next/Last instead of numbers, shorter sentences, no unnecessary context

```bash
a11y-assist last --profile cognitive-load
```

## screen-reader

Optimized for audio-first consumption via screen readers and TTS.

- **Max steps:** 3-5
- **Primary benefit:** TTS-friendly output with abbreviations expanded
- **Adaptations:** No visual-only references (colors, icons, spatial directions), abbreviations written out in full, punctuation tuned for natural TTS pauses, no symbolic emphasis like asterisks or backtick formatting

```bash
a11y-assist last --profile screen-reader
```

## dyslexia

Reduces reading friction for users with dyslexia.

- **Max steps:** 5
- **Primary benefit:** Explicit labels with no symbolic emphasis
- **Adaptations:** No italic or bold markers that can blur letter shapes, explicit labels instead of formatting-based emphasis, extra spacing between logical sections, consistent sentence structure

```bash
a11y-assist last --profile dyslexia
```

## plain-language

Maximum clarity for users who benefit from simplified language.

- **Max steps:** 4
- **Primary benefit:** One clause per sentence, simplified structure
- **Adaptations:** No jargon without explanation, one idea per sentence, active voice throughout, simplified vocabulary where possible without losing technical accuracy

```bash
a11y-assist last --profile plain-language
```

## Confidence levels

Every profile discloses a confidence level in its output:

| Level | Meaning | When |
|-------|---------|------|
| **High** | Validated `cli.error.v0.1` JSON with error ID | Tool emits structured error output |
| **Medium** | Raw text with detectable `(ID: ...)` | Error ID found in unstructured text |
| **Low** | Best-effort parse, no ID found | No anchor -- suggestions are heuristic |

Confidence is always shown. It can decrease during profile transformation (for example, if a profile simplifies away some context) but it can never increase.
