<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# SEO runbook

What to expect in Search Console after the v5 plan, and what to do when a
number moves the wrong way. The weekly search report links here.

## Search Console triage

| Search Console status | Expected after this plan | If it grows |
| --- | --- | --- |
| Excluded by 'noindex' tag | About 7,700 at first, then flat (24 noindexed locales) | A new noindex leak: check the `apply_locale_indexing` and `finalize_seo` counts in the build log |
| Page with redirect | About 3,800 (renamed slugs and merges), falling slowly | `check_live_redirects.py`; every chain must be one hop |
| Alternate page with proper canonical | Small | Fine |
| Duplicate, Google chose different canonical | Falls as translations are reviewed (A-3) and near-duplicates merged (B-3) | A translation too close to English, or near-duplicate articles: see the similarity column of the content audit |
| Crawled, currently not indexed | Falls after the content audit (B-3) | Quality: refresh or merge the page |
| Server error (5xx) | 0 | `/api/*` regressions: Worker logs |
| Submitted URL marked noindex (sitemap report) | 0 | Sitemap staleness: the hourly live-sitemap guard fails first |

## Structured data

- **Person** is the one entity: every page's WebSite `publisher` is
  `{"@id": "https://sebastienrousseau.com/#person"}`, built from
  `_data/profile.yml`. There is no Organization for the site: it is a
  personal site, and inventing one would be wrong.
- **No LocalBusiness.** There are no premises and no service area; do not
  add it.
- **Service and FAQPage** are on the Work with me pages
  (`scripts/generators/build_services.py`); the FAQPage text is the visible
  FAQ, word for word, and a unit test enforces it.

## Rich Results spot check (HUMAN)

Run these through Google's Rich Results Test after each release that
touches structured data, and record the result:

| URL | Date | Result |
| --- | --- | --- |
| https://sebastienrousseau.com/ | | |
| https://sebastienrousseau.com/about/ | | |
| https://sebastienrousseau.com/work-with-me/research/ | | |
| An article | | |
| https://sebastienrousseau.com/fr/ | | |

Check that `Person.jobTitle` reads "Senior Product Manager, Wholesale
Payments & API".
