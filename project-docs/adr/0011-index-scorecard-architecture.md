# ADR-0011: Interactive index scorecard — component architecture and URL-state encoding

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-07-03
**Related:** [Developer-Experience Plan 2026](../../project-docs/developer-experience-plan-2026.md) Phase 1; [ADR-0002](0002-pin-build-toolchains.md) (pinned toolchains); [ADR-0003](0003-build-copy-pipeline.md) (build copy pipeline)

---

## Context

The site publishes measurement frameworks ("indices") as static tables — the
Agentic AI Index (six dimensions, four maturity levels each, regulatory-
materiality weights) and, on a later branch, the Certified Blockchain Index
(five layers × 0–5 CMM). A static table is authoritative but inert. Phase 1 of
the developer-experience plan turns each index into an *interactive self-
assessment*: the reader scores each dimension, sees a live weighted composite,
a maturity band, a radar, and can share or export the result.

The site's guardrails constrain how this can be built:

* **Hash-strict CSP.** `script-src 'self'` (same-origin modules allowed, no
  inline JS, no `unsafe-eval`); `style-src 'self' 'sha256-<empty>'` — exactly
  one empty inline-style hash, so **no** new inline `<style>` or `style=""` may
  ship. `img-src` allows `data:`/`blob:`.
* **Progressive enhancement is mandatory.** Every feature must degrade to the
  existing static content with JS off, and must not be *replaced* at build time.
* **a11y/perf are blocking CI gates** (pa11y + axe WCAG2AAA, Lighthouse).
* **No backend.** The site is a static artifact; results must be shareable
  without a server.
* **i18n parity** across 28 locales is CI-enforced.

Two structural decisions needed recording: how the interactive UI is delivered
without violating CSP/PE/a11y, and how a scored result round-trips through a URL
with no backend.

## Decision

### 1. One data-driven Web Component, hydrated in place; static table is the baseline

A single custom element `<index-scorecard>` renders *any* index from a JSON
spec in `_data/indices/<slug>.json` (dimensions, levels, weights, scale, bands,
copy). One component, N indices — the Certified Blockchain Index drops in as a
second spec with no code change (its 0–5 CMM scale is just a different
`scale`/`levels`).

Delivery is progressive enhancement, not build-time replacement:

* The article keeps its full static maturity tables (the JS-off baseline).
* The author drops a mount marker where the tool should appear:
  `<div class="index-scorecard" data-index="<slug>"></div>`.
* A postbuild pass (`postbuild_lib/index_scorecard.py`) upgrades that marker,
  at build time, into an **inert** `<index-scorecard>` element carrying (a) a
  light-DOM fallback `<p>` and (b) a `<script type="application/json">` data
  island with the spec + the page-language `scorecard.*` UI strings inlined,
  followed by one `<script type="module" src="/_csp/index-scorecard.js">`.
* Nothing executes at build time. With JS off, the fallback paragraph shows and
  the tables above stand alone. With JS on, the element attaches a **Shadow
  DOM** (which hides the light-DOM fallback), reads the inlined spec (no fetch),
  and builds the interactive UI.

CSP compliance falls out of this shape:

* Styling uses a **constructable stylesheet** (`new CSSStyleSheet()` +
  `replaceSync`, adopted via `adoptedStyleSheets`), which is governed by
  `script-src` (the script that creates it is already trusted), **not**
  `style-src` — so the empty-hash `style-src` is untouched. No inline `<style>`,
  no `style=""`, no inline event handlers; every listener is `addEventListener`.
* The module script is same-origin (`script-src 'self'`) and is staged into
  `public/_csp/` so the existing asset pipeline minifies it, computes its SRI
  digest, and the injection pass stamps `integrity="sha256-…" crossorigin`.
* The data island is `type="application/json"` — not executable, and not
  matched by any of postbuild's inline-script hash regexes, so it needs no CSP
  hash. Its content is unicode-escaped (`<`/`>`/`&`) so a stray `</script>` in
  the copy cannot break out.

a11y: native `<input type=range>` per dimension with `<label>`, `aria-valuetext`
reflecting the live maturity level, an `aria-live="polite"` composite readout,
and — as the **text equivalent of the radar** — a proper `<table>` (the radar
SVG is `aria-hidden`, so assistive tech reads the numbers, not a decorative
chart). Perf: no charting library (hand-rolled SVG + a hand-drawn canvas for
PNG export), and the UI is lazy-built via `IntersectionObserver` so it adds
nothing to initial render.

The score computation + URL codec live in a **pure, DOM-free module**
(`scoring.js`) imported by both the component and a Node golden-file test, so
the number a reader sees is produced by the same code the test pins.

### 2. URL-state encoding: versioned, delimited, base64url in `?s=`

A scored result round-trips through the query string with no backend:

```
scores [0,25,50,75,100,40]  →  "1:0,25,50,75,100,40"  →  base64url  →  ?s=MTow…
```

* **Delimited integer list, not JSON.** For six small integers this is ~an
  order of magnitude shorter than base64(JSON) and has no structural ambiguity
  to parse.
* **Leading version field (`1:`).** The decoder rejects tokens from an
  incompatible future schema instead of silently mis-reading them.
* **base64url** (RFC 4648 §5, `+/=` → `-_`, padding stripped) keeps the token
  URL-safe with no percent-encoding.
* **Decode is total and defensive:** malformed base64, missing separator,
  unknown version, wrong dimension count, or non-numeric fields all return
  `null`, and the component falls back to spec defaults. Every score is clamped
  to the spec scale on both encode and decode.
* State is written with `history.replaceState` (no navigation, no history
  spam); "share" copies the current URL; "download" renders a PNG entirely
  client-side via a hand-drawn canvas (no SVG→`img` round trip, so no
  `img-src` dependency).

Single `?s=` parameter assumes one scorecard per page (true today). A future
multi-scorecard page can namespace the parameter; the codec already takes the
spec, so the change is localized.

## Consequences

* **Positive.** JS-off readers lose nothing; the static tables remain the
  baseline. CSP, SRI, a11y and perf gates are satisfied by construction, with
  zero global policy relaxation. The component is data-driven, so the second
  index is a JSON file, not a code change. Results are shareable and
  bookmarkable with no backend and no new attack surface. The scoring maths is
  pinned by a 100/100/100-covered golden-file test, so a shared score cannot
  silently drift.
* **Negative / trade-offs.** The spec + localized strings are inlined per page
  (small bytes, only on index articles) rather than fetched, trading a little
  page weight for zero runtime requests and full offline behaviour. The radar is
  decorative (`aria-hidden`) with the table as the authoritative text
  equivalent, so screen-reader users get numbers, not a described chart —
  acceptable and simpler than an accessible-SVG description tree. The URL codec
  is bespoke; the versioned prefix is the migration escape hatch.
* **Follow-ups.** Wire the Certified Blockchain Index spec when that branch
  lands (no component change expected). Localizing the index *content* strings
  (dimension/level copy currently English in the spec) is deferred; only the
  component *chrome* is localized via `scorecard.*` today.
