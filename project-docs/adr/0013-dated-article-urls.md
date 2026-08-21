# ADR-0013: Keep dated article URLs, for now

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-08-19
**Supersedes:** —
**Related:** [ADR-0012](0012-locale-slug-policy.md), [SEO spec](../web-performance-seo-spec.md)

---

## Context

Every article URL carries its publication date, and most 2026 articles repeat
the year in the slug:

```
/2026-08-04-data-act-cloud-switching-dora-exit-strategies-2026/
 └── date prefix                                          └── year again
```

Two costs follow. A dated URL advertises its own age in the SERP, which
suppresses click-through on regulatory analysis that stays relevant for years —
the site's most valuable content, and precisely the content whose value does
*not* decay on the schedule the URL implies. And 37 of 105 articles hard-code a
past year in the filename, so the URL keeps asserting a date the content has
outgrown even after a refresh.

The obvious fix — clean slugs — is also the most expensive change available
here. 105 articles carry accumulated inbound links, AI-engine citations, and
28 locale forks each. A bulk rewrite risks all of it to gain a cosmetic
improvement whose actual traffic effect nobody has measured.

## Decision

**Change nothing about URLs in this pass.**

The site had no analytics of any kind when this was written — no Search
Console, no field data, no referral data, no AI-crawler logs. There was
therefore no way to answer the only questions that matter before a migration:
which articles earn traffic, which earn AI citations, and whether dated URLs
measurably cost either.

Cloudflare Web Analytics, Search Console, and AI-crawler log analysis land in
the same change as this ADR. **The sequence is: instrument, gather a quarter,
then decide.** Acting first and measuring afterwards would be exactly the
mistake this repo's improvement plan already warns about elsewhere.

When the data exists, the migration is a three-step change, not a rename:

1. Adopt clean slugs for **new** articles from a chosen date. Costs nothing —
   no existing URL moves.
2. Serve the dated forms as 301s from the Cloudflare Worker that already
   fronts the origin (`workers/lang-router.js`), which is where redirects
   belong on this stack.
3. Migrate individual legacy articles only where the analytics justify it,
   each with its own redirect, its own locale forks, and its own verification.

## Consequences

**Good**

* No link equity is risked on an unmeasured hypothesis.
* The decision, and what would change it, are written down rather than
  rediscovered in the next audit.

**Bad / accepted**

* The cost identified above continues to be paid for at least another quarter.
* The 37 articles with a year in the title keep asserting a stale date. Partly
  mitigated by the quarterly refresh rotation, which updates the content and
  `dateModified` even when the URL is frozen.

**Neutral**

* If the data eventually shows dated URLs cost nothing measurable, the correct
  outcome is to close this out and keep them. That is a legitimate result, not
  a failure to act.
