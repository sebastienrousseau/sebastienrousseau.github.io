# ADR-0015: Freeze published URLs and index English only

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Accepted
**Date:** 2026-11-21
**Supersedes:** the rename-and-redirect clause of [ADR-0012](0012-locale-slug-policy.md)
**Related:** [ADR-0013](0013-dated-article-urls.md)

---

## Context

Search Console shows a site-wide demotion starting on 11 September 2026.
Daily impressions fell from about 1,000 to about 20 within two days.
English pages fell as far as the translations: 26,106 impressions between
1 July and 10 September, 1,342 between 11 September and 18 November, at
the same average position. Clicks went from about 2 a day to almost none.

Nothing technical explains it. There is no manual action and no security
issue, Googlebot kept crawling at the usual rate, and the pages that lost
their traffic still return 200, carry a self-canonical, are not noindex
and are reported as indexed by URL Inspection. No Google update was
announced for that date: the August 2026 spam update finished on
21 August and the September one started on 24 September.

What did change was the site. Between 26 August and 3 September about
1,600 machine-translated article pages were added and about 1,200 URLs
were renamed when locale slugs were localised (ADR-0012), across 4,860
changed files. Search Console still lists 3,795 "Page with redirect" URLs.
Thousands of automatically translated pages appearing at once matches the
pattern Google's spam policies call scaled content, and that system acts
on the whole site, which is why the English originals fell with them.
This is an inference from timing and shape; Search Console cannot confirm
it.

v0.0.30 (4 November) made 24 locales noindex but kept ten
machine-translated locales indexable, about 1,500 pages. Two weeks later
there is no recovery.

## Decision

1. **English is the only indexed locale.** `_data/seo/locale-indexing.json`
   lists `en` only. Every locale stays published and in the language
   switcher, with `noindex, follow`, out of every sitemap and out of every
   hreflang cluster. A locale comes back only once its translations are
   reviewed by a person.
2. **Published URLs are frozen.** A page that exists on `main` keeps its
   URL. `check_url_freeze.py` runs on every pull request and fails on a
   deleted or renamed `_posts` page or a changed `slugs.json` value.
   `translate_post.py --rederive-slugs` names a new post's translations
   but refuses to rename a published one. There is no allowlist; changing
   a published URL needs this ADR amended first.
3. **Thin listings are noindex.** Tag and category term pages and page 2+
   of every listing carry `noindex, follow`. Hubs and first pages stay
   indexable.
4. **Content links point at final URLs.** `check_stale_links.py` fails when
   a source links to a redirect source.
5. **New posts keep their translations, noindexed.** `/publish-today`
   still translates into all 34 locales, because the i18n gates require
   it (`test_i18n_parity.py` wants every English post in every locale's
   slug map, and `test_body_translation.py --strict` rejects untranslated
   stubs). Those pages are noindex under decision 1, so they no longer
   count towards what Google indexes. Translating into indexed locales
   only would mean reworking those gates, the language switcher and the
   locale listings; that is a separate decision, not part of this one.
6. **Pages are served stale-while-revalidate at the edge.** Googlebot
   measured about 1.1 s per request: the 10-minute edge cache misses
   almost every crawl of a rarely visited URL, which then waits on GitHub
   Pages. The Worker now keeps each page in the Cache API for 7 days,
   serves it at once, and refreshes it in the background when it is older
   than 10 minutes.

## Consequences

- The locale archives stop changing. A published locale slug that no
  longer derives from an edited title stays as it is; the title edit is
  the thing to avoid.
- Recovery, if it comes, is expected at a later Google core or spam
  update, not within days. Track it in Search Console (Performance,
  comparing against 1 July to 10 September) before adding any locale back.

## Amendment, 22 November 2026: French is indexed

The author decided that French, the site's second language, is indexed
again. `_data/seo/locale-indexing.json` lists `en` and `fr`: French pages
drop `noindex`, return to the sitemaps, and join English in every hreflang
cluster. The other 33 locales are unchanged.

This reverses decision 1 for one locale before the recovery check in the
Consequences above. It adds about 200 machine-translated French pages,
126 of them articles, to the index, against the 1,500 that v0.0.30 kept
indexable without a recovery. Watch French impressions and the English trend in Search
Console after the change; if English falls further, French is the first
thing to take back out.

## Amendment, 25 November 2026: locales that earned clicks are indexed

The author decided to index again the locales that brought search
traffic before the demotion, and to keep the rest noindex. Search Console
page data for 11 June to 10 September 2026 (the three months before
11 September; the top 1,000 pages, 489 of the period's 492 clicks) gave
these clicks per locale:

| Locale | Clicks | Locale | Clicks | Locale | Clicks |
| :--- | ---: | :--- | ---: | :--- | ---: |
| en | 160 | vi | 14 | id | 5 |
| zh-hant | 77 | it | 12 | pt-br | 5 |
| fr | 42 | fa | 11 | sv | 4 |
| ru | 21 | cs | 10 | pl, ha, tr, ms, uk | 3 each |
| ko | 18 | de | 10 | yo, bn, ar | 2 each |
| es | 18 | th | 8 | nl | 1 |
| zh-hans | 17 | ro | 7 | mr, fil, hu, ta, te, hi | 0 |
| ja | 16 | he, el | 6 each | | |

The threshold is 10 clicks in those three months. `_data/seo/locale-indexing.json`
lists English and the twelve locales that met it: zh-hant, fr, ru, ko,
es, zh-hans, ja, vi, it, fa, cs and de. Together they had 426 of the 489
clicks (87 %). The other 22 locales, 63 clicks between them, stay
`noindex, follow`, out of the sitemaps and out of the hreflang clusters.
Decisions 2 to 6 are unchanged.

This widens decision 1 from two locales to thirteen. On 25 November
Search Console still reported 5,890 indexed pages, 410 of a 501-URL
sample in locales that were noindex, so the noindex locales had mostly
not left the index yet. Watch the English trend after this change; if
English falls further, the newly indexed locales are the change to take
back.
