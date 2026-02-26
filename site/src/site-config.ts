import type { SiteConfig } from '@mcptoolshop/site-theme';

export const config: SiteConfig = {
  title: 'a11y-assist',
  description: 'Deterministic accessibility assistance for CLI failures \u2014 additive, SAFE-only, profile-driven',
  logoBadge: 'AA',
  brandName: 'a11y-assist',
  repoUrl: 'https://github.com/mcp-tool-shop-org/a11y-assist',
  footerText: 'MIT Licensed \u2014 built by <a href="https://github.com/mcp-tool-shop-org" style="color:var(--color-muted);text-decoration:underline">mcp-tool-shop-org</a>',

  hero: {
    badge: 'Python / CLI',
    headline: 'a11y-assist,',
    headlineAccent: 'recovery plans for everyone.',
    description: 'Deterministic accessibility assistance for CLI failures. Five profiles, SAFE-only commands, anchored error IDs, and disclosed confidence \u2014 never rewrites tool output, only adds a structured ASSIST block.',
    primaryCta: { href: '#quick-start', label: 'Get started' },
    secondaryCta: { href: '#features', label: 'Learn more' },
    previews: [
      { label: 'Install', code: 'pip install a11y-assist' },
      { label: 'Wrap', code: 'assist-run some-tool do-thing' },
      { label: 'Assist', code: 'a11y-assist last --profile cognitive-load' },
    ],
  },

  sections: [
    {
      kind: 'features',
      id: 'features',
      title: 'Why a11y-assist?',
      subtitle: 'Error recovery that adapts to how you work.',
      features: [
        { title: 'SAFE-Only Commands', desc: 'Only read-only, dry-run, and status-check commands are ever suggested. No destructive operations, ever.' },
        { title: 'Five Profiles', desc: 'Low vision, cognitive load, screen reader, dyslexia, and plain language. Each adapts output structure, step count, and phrasing.' },
        { title: 'Anchored Error IDs', desc: 'Suggestions link back to the original error ID when available. No fabricated IDs, no invented content.' },
        { title: 'Confidence Disclosed', desc: 'High, Medium, or Low \u2014 always shown, can decrease but never increase. You know how much to trust each suggestion.' },
        { title: 'Additive Only', desc: 'Original tool output is never modified, hidden, or suppressed. a11y-assist only adds a structured ASSIST block.' },
        { title: 'Deterministic', desc: 'Same input always produces the same output. No network calls, no randomness, no model invocations.' },
      ],
    },
    {
      kind: 'code-cards',
      id: 'quick-start',
      title: 'Quick Start',
      cards: [
        {
          title: 'Wrap & assist',
          code: 'pip install a11y-assist\n\n# Wrap any command\nassist-run some-tool do-thing\n\n# If it fails, get recovery guidance\na11y-assist last\n\n# Switch profiles\na11y-assist last --profile cognitive-load',
        },
        {
          title: 'Structured input',
          code: '# High-confidence from cli.error.v0.1 JSON\na11y-assist explain --json error.json\n\n# Best-effort from raw text\nsome-tool 2>&1 | a11y-assist triage --stdin\n\n# Import evidence-engine findings\na11y-assist ingest findings.json --verify-provenance',
        },
      ],
    },
    {
      kind: 'data-table',
      id: 'commands',
      title: 'Commands',
      columns: ['Command', 'Description'],
      rows: [
        ['a11y-assist explain --json <path>', 'High-confidence assist from cli.error.v0.1 JSON'],
        ['a11y-assist triage --stdin', 'Best-effort assist from raw CLI text'],
        ['a11y-assist last', 'Assist from the last captured log'],
        ['a11y-assist ingest <findings.json>', 'Import findings from a11y-evidence-engine'],
        ['assist-run <cmd> [args...]', 'Wrapper that captures output for last'],
      ],
    },
    {
      kind: 'data-table',
      id: 'profiles',
      title: 'Accessibility Profiles',
      subtitle: 'Five profiles ship out of the box.',
      columns: ['Profile', 'Primary Benefit', 'Max Steps'],
      rows: [
        ['lowvision (default)', 'Visual clarity \u2014 clear labels, numbered steps, SAFE commands', '5'],
        ['cognitive-load', 'Reduced mental steps \u2014 Goal line, First/Next/Last labels', '3'],
        ['screen-reader', 'Audio-first \u2014 TTS-friendly, abbreviations expanded', '3\u20135'],
        ['dyslexia', 'Reduced reading friction \u2014 explicit labels, no symbolic emphasis', '5'],
        ['plain-language', 'Maximum clarity \u2014 one clause per sentence, simplified structure', '4'],
      ],
    },
    {
      kind: 'data-table',
      id: 'confidence',
      title: 'Confidence Levels',
      subtitle: 'Always disclosed, never inflated.',
      columns: ['Level', 'Meaning', 'When'],
      rows: [
        ['High', 'Validated cli.error.v0.1 JSON with ID', 'Tool emits structured error output'],
        ['Medium', 'Raw text with detectable (ID: ...)', 'Error ID found in unstructured text'],
        ['Low', 'Best-effort parse, no ID found', 'No anchor \u2014 suggestions are heuristic'],
      ],
    },
    {
      kind: 'data-table',
      id: 'safety',
      title: 'Safety Guarantees',
      subtitle: 'Enforced at runtime by the Profile Guard system.',
      columns: ['Invariant', 'Guarantee'],
      rows: [
        ['SAFE-only commands', 'Only read-only, dry-run, and status-check commands suggested'],
        ['No invented IDs', 'Error IDs come from input or are absent \u2014 never fabricated'],
        ['No invented content', 'Profiles rephrase but never add new factual claims'],
        ['Confidence disclosed', 'Always shown; can decrease but never increase'],
        ['Additive only', 'Original tool output never modified, hidden, or suppressed'],
        ['Deterministic', 'Same input, same output \u2014 no network, no randomness'],
        ['Guard-checked', 'Every profile transform validated against invariants before rendering'],
      ],
    },
  ],
};
