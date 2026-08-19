# ADR-0012: One rule for localising article slugs

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-08-19
**Supersedes:** —
**Related:** [i18n](../i18n.md), [ADR-0003](0003-build-copy-pipeline.md)

---

## Context

Article slugs are localised inconsistently across the 28 active locales, and no
document records why. Measured across the corpus, as the share of each locale's
posts whose filename is byte-identical to the English one:

| Locales | EN-identical slugs |
|---|---|
| `ar` `bn` `el` `fa` `fil` `ha` `he` `hu` `mr` `ms` `ro` `ta` `te` `yo` | 100 % |
| `cs` `id` `ja` `ko` `nl` `pl` `ru` `sv` `th` `tr` `uk` `vi` `zh-hans` `zh-hant` | ~57 % |
| `de` `es` `it` | ~49 % |
| `pt-br` | ~48 % |
| `fr` | ~33 % |

The same article ships as
`de/2026-08-01-eudi-wallet-eidas-2-banks-relying-party-2026` and
`fr/2026-08-01-eudi-wallet-eidas-2-banques-relying-party-2026` — German keeps
the English noun, French translates it, and nothing explains the difference.

Three separate things were tangled together:

1. **Whether to localise at all.** A localised slug is a real in-market ranking
   signal for Latin-script locales.
2. **Whether it is even useful.** For a non-Latin script the choice is between a
   percent-encoded IRI (`/ar/…-البنوك/`, unreadable when pasted anywhere that
   escapes it) and a romanisation nobody searches for. Neither beats the English
   slug, which at least stays stable, linkable and diffable.
3. **Consistency.** Whatever the answer, it should be the same answer every
   time. The current state is not a considered trade-off; it is drift.

The 100 % column is not one thing either. It mixes locales that never localised
(`ro`, `hu`, `ms`, `fil`, `ha`, `yo`) with `ar`, `he`, `bn`, `ta`, `te`, `mr`,
`fa` — where an argument could be made that the English slug is *better*.

That argument does not survive contact with what the site already does.
`ja`, `ko`, `zh-hans`, `zh-hant`, `th`, `hi`, `ru` and `uk` already localise
about 43 % of their slugs, in native script, and have for months. A policy of
"non-Latin scripts keep English" would declare almost half of eight locales'
live URLs to be violations, and would have to explain why Cyrillic and Greek —
perfectly ordinary URL scripts — are grouped with CJK. It would be a rule
invented to fit a table rather than the site.

## Decision

**Every locale localises the article slug, following its translated title.
There is no script-based carve-out.**

One rule, no exceptions to remember, and it matches the direction the corpus
was already moving in. Percent-encoded IRIs are handled correctly by every
search engine the site targets and render natively in the address bar.

**Existing URLs are not rewritten.** Live slugs keep their accumulated link
equity; the policy governs new articles, and migrating an existing one is a
deliberate, individually-redirected change. Bringing the ~14 locales still at
100 % English into line is follow-up work, not a bulk rename.

**The gate ratchets rather than blocks.** `tests/validation/test_slug_policy.py`
records each locale's current localisation rate as a baseline and fails only if
a locale goes *backwards*. The remaining gap is reported every run, so the
backlog is visible instead of silently permanent. Same mechanism as the mypy
tier and the complexity allowlist.

## Consequences

**Good**

* One rule, written down and testable, with no script carve-out to argue about.
* Drift is now visible: the gate prints every locale's localisation rate on
  every run, and fails on regression.
* Nothing that is live today becomes a violation, so the ADR costs no URLs.

**Bad / accepted**

* The backlog is large — 14 locales at 100 % English and most of the rest around
  half. This ADR makes it measurable; it does not clear it.
* Percent-encoded slugs are uglier when pasted somewhere that escapes them.
  Accepted: it is cosmetic, and it is what the site already ships for `ja`,
  `zh-*`, `th`, `hi`, `ru` and `uk`.

**Neutral**

* Whether localised slugs actually earn their keep per locale is unverifiable
  until the analytics added alongside this change have run for a quarter. If
  the data says they do not, this ADR is the thing to revisit.
