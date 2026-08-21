#!/usr/bin/env python3
"""Post-build pass on Static Site Generator's ``public/`` output.

Tasks performed:
1. **Real SRI** — replace every ``integrity="sha256-<short-hex>"`` placeholder
   that Static Site Generator emits on its ``/_csp/*`` assets with a real base64-encoded
   SHA-256 of the asset's actual byte content. Browsers will now enforce SRI.

2. **CSP for inline JSON-LD** — compute the SHA-256 of every
   ``<script type="application/ld+json">`` block inside each HTML page and
   inject those hashes into that page's ``script-src`` directive. The previous
   ``'unsafe-inline'`` carve-out is removed.
"""

from __future__ import annotations

import sys as _sys  # path bootstrap — scripts reorg (scripts/lib/ on sys.path)
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "lib"))

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

PUBLIC = Path("public")
from postbuild_assets import (
    add_responsive_srcset,
    fix_sri,
    inject_jsonld_hashes,
    inject_lcp_preload,
    normalise_csp,
    setup_asset_state,
    stamp_asset_fingerprints,
    wrap_cdn_images_in_transform,
)
from postbuild_transforms import (
    _bump,
    _home_hreflang,
    _topic_hreflang,
    build_comprehensive_lastmod_index,
    inject_itemlist,
    inline_theme_init,
    rewrite_persisted_transforms,
    scrub_localhost_urls,
    strip_redundant_link_titles,
    update_last_modified_date,
)

# Asset setup (minify -> SRI hashes -> fingerprint map/pattern) runs once at
# import time, in order, inside postbuild_assets; the minify stats feed the
# _finalize_build summary.
_ASSET_STATS = setup_asset_state(PUBLIC)


# ---------------------------------------------------------------------------
# LCP preload — auto-inject `<link rel="preload" as="image">` for the
# first image on each page (the LCP candidate) when the page doesn't
# already have one. The homepage uses an explicit ``{{image}}`` slot;
# every other listing/article page would otherwise wait for HTML parse
# + image discovery before fetching the LCP candidate, costing 0.5–1s
# on simulated slow 4G. This closes that gap.
# ---------------------------------------------------------------------------

# Match a preload image link regardless of attribute order — SSG's
# minifier alphabetises ``as=image`` before ``rel=preload``, so the
# straightforward ``rel=preload[…]as=image`` regex misses the
# layout-emitted form. Walk every <link> tag and check both attrs are
# present independently.


# ---------------------------------------------------------------------------
# CDN image transform — wrap every raster <img src="https://cloudcdn.pro/...">
# in CloudCDN's /api/transform endpoint so Cloudflare Image Resizing serves
# a width-appropriate WebP at q=80 (q=85 for LCP/hero). Slashes Lighthouse's
# ``uses-responsive-images`` saving on the listing pages (~370 KiB on /
# articles/) and drops the about-page portrait from 360 KiB → ~3 KiB.
#
# CDN contract (functions/api/transform.js in cloudcdn.pro):
#   - GET only — HEAD returns 404.
#   - `url` must be a relative path starting with `/`; absolute URLs and
#     paths containing `..`, `//`, or NUL are rejected with 400.
#   - `w` is 1–8192, `q` is 1–100; SVG sources pass through unchanged.
#   - Response is cached `public, max-age=31536000, immutable` and varies on
#     Accept + Save-Data + Sec-CH-Effective-Connection-Type, so we don't
#     need to thread bandwidth hints in the URL — the CDN downgrades to
#     q≤60 + WebP automatically for slow-2g/2g/3g clients.
#   - Rate limit: 50,000 transforms / calendar month. Even with multiple
#     widths per asset, real-world fresh-cache hits stay well under that.
# ---------------------------------------------------------------------------


# Pre-generated responsive-variant widths emitted by the CDN's image
# ingestion pipeline. CDN policy (2026-06-23): /api/transform requires
# authentication; public pages must use these pre-gen variants instead
# (named `<original-stem>-<width>.webp` next to the original).
# Paths under these prefixes have pre-generated variants. Paths
# elsewhere (logos, client artwork, ad-hoc uploads) pass through as
# the bare CDN URL — no variant swap, no transform call.


# Match an already-suffixed variant filename:
#   foo-1200.webp  → group(1)="foo", group(2)="1200"
#   foo-640.webp   → group(1)="foo", group(2)="640"
# Only the exact 4 widths from _VARIANT_WIDTHS, anchored to .webp end.


# Match a fully-formed /api/transform URL we want to rewrite in-place.
# This catches transform URLs persisted in markdown source (post_enrich
# emitted them before the 2026-06-23 CDN hardening) so they don't survive
# from old _posts/*.md through ssg rendering into served HTML.


# ---------------------------------------------------------------------------
# 1c. Redundant link title strip — WAVE alert remediation.
#
# Markdown citations frequently come in as ``[Article Title](url "Article Title")``,
# which markdown-it renders as ``<a href="url" title="Article Title">Article
# Title</a>``. Both WAVE and pa11y note this as a redundant alternative-text
# alert: a title attribute that duplicates the visible text adds noise for
# screen readers without giving sighted users any extra information.
#
# Strip ``title=`` when (and only when) it matches the inner text verbatim
# after whitespace + trailing-period normalisation. Non-matching titles
# (e.g. "Article Title · sebastienrousseau.com" or "Read on at IBM")
# stay — they're carrying signal.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 2. CSP hash for inline JSON-LD
# ---------------------------------------------------------------------------

# Capture the literal inline body of every <script type="application/ld+json"> tag.
# (Static Site Generator may emit either single- or double-quoted type attribute and may have
# attribute order vary, so the regex is intentionally loose.)
# Speculation Rules also need a CSP allowance. Chrome 124+ accepts the
# `'inline-speculation-rules'` keyword in script-src, but adding the
# block's actual sha256 hash gives belt-and-braces coverage for older
# browsers / unusual configs.
# Bare inline <script> blocks (no src, no type) — used for the inlined
# theme bootstrap. Each one needs its own sha256 in CSP script-src.

# ---------------------------------------------------------------------------


# Match the CSP meta tag whether attributes are quoted or not, in either order
# (Static Site Generator's minifier emits `<meta content="..." http-equiv=Content-Security-Policy>`).


# ---------------------------------------------------------------------------
# 3. ItemList JSON-LD on listing pages
# ---------------------------------------------------------------------------


# Listing pages we know about. The key is the relative path; the value is the
# CSS-selector-style article class pattern that identifies an item card on
# that page. Cards we'd otherwise pick up (e.g. "newsroom-featured" on the
# /articles/ page) are folded in via wildcard prefix matching below.


# Parse one <article class="..."> ... </article> block and extract (title, url).
# The card markup varies but always includes the canonical link as the first
# <a href="..."> with text content matching the card's H2/H3 title.


# SEO + Schema.org injection — moved to postbuild_lib.seo
# Article UI furniture — moved to postbuild_lib.article_furniture
from postbuild_lib.analytics import beacon_token, inject_analytics_beacon
from postbuild_lib.article_furniture import (  # noqa: F401 — re-exports
    AUTHOR_AVATAR,
    AUTHOR_NAME,
    AUTHOR_URL,
    _all_active_non_en_langs,
    _detect_page_lang,
    _is_french,
    _labels,
    _labels_for_lang,
    _slug_maps,
    _slug_maps_for,
    inject_article_furniture,
    inject_deck,
    inject_eyebrow,
    slugify,
)
from postbuild_lib.asset_dedupe import (
    find_duplicate_assets,
    remove_duplicate_files,
    rewrite_asset_refs,
)
from postbuild_lib.citations import (
    inject_citations,
    inject_cite_popover,
    inject_sources_list,
)
from postbuild_lib.content_blocks import (
    _convert_faq_to_qa,
    inject_footnotes,
    inject_hero_banner,
    inject_mermaid,
    inject_pullquotes,
    inject_section_rules,
    inject_speculation_rules,
)
from postbuild_lib.feeds import (  # noqa: F401 — re-exports (split from output)
    augment_sitemap_with_rendered_pages,
    build_lastmod_index,
    dedupe_sitemap_index_html,
    dedupe_xml_feeds,
    escape_xml_ampersands,
    fix_xml_feed_urls,
    fix_xml_feeds,
    refresh_sitemap_lastmod,
    shrink_news_sitemap,
)

# Live GitHub repo stats — moved to postbuild_lib.github_stats
from postbuild_lib.github_stats import (
    gh_stats_index as _gh_stats_index,
)
from postbuild_lib.github_stats import (
    inject_github_stats,
)
from postbuild_lib.hreflang import (  # noqa: F401 — re-exports (split from article_furniture)
    _alternates_for_en_slug,
    _resolve_en_slug,
    _translated_slugs,
    _translated_slugs_per_lang,
    build_fr_title_index,
    inject_hreflang,
    inject_lang_switcher,
)
from postbuild_lib.html_passes import (
    decode_entities_in_jsonld,
    hoist_body_link_stylesheets,
    inject_sigstore_attestation,
    inject_table_labels,
    strip_duplicate_body_h1,
)
from postbuild_lib.index_scorecard import inject_index_scorecard
from postbuild_lib.internal_links import (
    _alias_patterns,
    canonicalise_absolute_self_links,
    inject_contextual_links,
    inject_related_cluster,
    load_corpus,
    load_taxonomy,
)
from postbuild_lib.navigation import (
    build_post_nav_index,
    inject_anchor_links_and_toc,
    inject_breadcrumbs,
    inject_nav_active,
    inject_prev_next_nav,
)

# Output emitters — moved to postbuild_lib.output. Re-exported so
# tests/test_postbuild.py + any external probe keeps working.
from postbuild_lib.output import (  # noqa: F401 — re-exports
    build_llms_ctx_txt,
    build_llms_full_txt,
    build_llms_txt,
    normalise_cname,
    write_ai_txt,
    write_humans,
    write_json_feed,
    write_llms_ctx_txt,
    write_llms_full_txt,
    write_llms_txt,
    write_robots,
    write_security_txt,
)

# Legacy-URL redirect conversion (/papers -> /research + locale forks)
from postbuild_lib.redirects import apply_redirect_pages
from postbuild_lib.schemas import (
    align_article_identity,
    inject_faq_schema,
    inject_news_article,
    inject_software_source_code,
    inject_tech_article,
)
from postbuild_lib.seo import (  # noqa: F401 — re-exports for back-compat
    _keywords_re,
    align_jsonld_inlanguage,
    build_about_graph,
    canonicalise_internal_links,
    clean_meta_description,
    compute_word_count,
    fix_article_og_type,
    fix_home_social_image,
    fix_social_image,
    inject_about,
    inject_howto,
    inject_kpi_metrics,
    inject_og_completeness,
    inject_word_count,
    normalize_canonical,
    stamp_image_dimensions,
)
from postbuild_lib.sharing import (
    inject_action_rail,
    inject_byline_strap,
    inject_oembed_link,
    inject_reuse_panel,
    inject_share_rail,
    inject_syndication_panel,
)


class _PostbuildCounters:
    """Per-pass counters threaded through ``_process_page``.

    Using a mutable container so the per-page helper can bump counters
    in-place without returning a 20-tuple. The orchestrator reads them
    once at the end for the summary line.
    """

    __slots__ = (
        "about_patched",
        "action_rails_set",
        "analytics_injected",
        "anchor_patched",
        "article_identity_aligned",
        "asset_dupes_rewritten",
        "asset_fp_patched",
        "body_h1_stripped",
        "byline_straps_set",
        "cdn_wrapped",
        "citation_patched",
        "cite_panels_set",
        "cluster_blocks_added",
        "contextual_links_added",
        "crumbs_patched",
        "csp_normalised",
        "csp_patched",
        "decks_set",
        "desc_cleaned",
        "eyebrows_set",
        "faq_schema_patched",
        "footnotes_set",
        "furniture_patched",
        "howto_patched",
        "hreflang_patched",
        "img_dims_patched",
        "itemlist_patched",
        "jsonld_entities_decoded",
        "langswitch_patched",
        "lastmod_meta_patched",
        "lcp_preloaded",
        "link_hoisted",
        "localhost_patched",
        "mermaid_patched",
        "nav_patched",
        "newsarticle_patched",
        "oembed_links_set",
        "og_patched",
        "pretty_links_patched",
        "pullquotes_set",
        "redundant_titles_stripped",
        "reuse_panels_set",
        "section_rules_set",
        "self_links_canonicalised",
        "share_rails_set",
        "social_patched",
        "softwaresourcecode_patched",
        "sources_patched",
        "srcset_added",
        "sri_patched",
        "syndicate_panels_set",
        "tables_carded",
        "techarticle_patched",
        "theme_inlined",
        "wc_patched",
    )

    def __init__(self) -> None:
        for name in self.__slots__:
            setattr(self, name, 0)


class _PostbuildContext:
    """Pre-pass artefacts read once and shared across pages."""

    __slots__ = (
        "alias_patterns",
        "analytics_token",
        "asset_dupes",
        "corpus",
        "counters",
        "fr_titles",
        "gh_stats",
        "last_reviewed_index",
        "nav_index",
        "taxonomy",
        "translated_per_lang",
    )

    def __init__(self, pages: list[Path]) -> None:
        self.nav_index = build_post_nav_index(pages)
        self.fr_titles = build_fr_title_index(pages)
        # Legacy FR-only sets are kept around in case anything probes them;
        # the new lang-keyed dict drives the modern hreflang path.
        _translated_slugs()
        self.translated_per_lang = _translated_slugs_per_lang()
        self.gh_stats = _gh_stats_index()
        self.counters = _PostbuildCounters()
        self.last_reviewed_index = build_comprehensive_lastmod_index()
        # Article corpus + tag taxonomy for contextual internal linking.
        # Read once here (not per page) — the alias patterns are ~200
        # compiled regexes and the corpus is a full front-matter scan.
        self.taxonomy = load_taxonomy()
        self.corpus = load_corpus(taxonomy=self.taxonomy)
        self.alias_patterns = _alias_patterns(self.taxonomy)
        # None unless CF_BEACON_TOKEN / _data/analytics.json is set.
        self.analytics_token = beacon_token()
        # Byte-identical /_csp/ assets ssg fingerprinted separately, mapped
        # duplicate -> canonical. Computed once; the files themselves are
        # removed after the page loop, once nothing references them.
        self.asset_dupes = find_duplicate_assets(PUBLIC)


def _apply_seo_passes(html: str, page: Path, ctr: _PostbuildCounters) -> str:
    """SEO + JSON-LD passes that don't depend on lang context.

    Sequence is order-sensitive: ItemList must run before the JSON-LD
    CSP-hash pass (so its hash gets included); furniture must run
    after wordCount + about populate the BlogPosting JSON-LD; etc.
    """
    out, n_lh = scrub_localhost_urls(html)
    ctr.localhost_patched += n_lh
    out, n_ti = inline_theme_init(out)
    ctr.theme_inlined += n_ti
    out, n_fp = stamp_asset_fingerprints(out)
    ctr.asset_fp_patched += n_fp
    prev = out
    out = fix_sri(out)
    if out != prev:
        ctr.sri_patched += 1
    prev = out
    out = inject_itemlist(page, out)
    if out != prev:
        ctr.itemlist_patched += 1
    prev = out
    out = fix_social_image(out)
    if out != prev:
        ctr.social_patched += 1
    prev = out
    out = inject_og_completeness(page, out)
    if out != prev:
        ctr.og_patched += 1
    prev = out
    out = clean_meta_description(page, out)
    if out != prev:
        ctr.desc_cleaned += 1
    out = fix_article_og_type(out)
    # Home page only: rebuild the social card from the authored landscape
    # banner and declare its dimensions (the index layout emits no
    # banner-src marker, so fix_social_image above cannot reach it).
    out = fix_home_social_image(page, out)
    out = inject_kpi_metrics(out)
    # Point internal links at the same URL the canonical and sitemap
    # advertise. Without this, every `/x/index.html` href is a second
    # crawlable URL for the same page and Search Console files it under
    # "Alternate page with proper canonical tag".
    out, n_pretty = canonicalise_internal_links(out)
    ctr.pretty_links_patched += n_pretty
    # Belt-and-suspenders: align JSON-LD inLanguage to <html lang> for the
    # few content items the translation-time localiser misses (runs before
    # inject_jsonld_hashes so the CSP hash covers the aligned bytes).
    out = align_jsonld_inlanguage(out)
    out, n_dim = stamp_image_dimensions(out)
    ctr.img_dims_patched += n_dim
    # Wrap CDN images in /api/transform AFTER stamp_image_dimensions so
    # the lookup against _IMG_DIMS sees the bare CDN URL (not the
    # transform URL, which would miss the table). LCP preload then runs
    # against the wrapped URL so preload + img src agree byte-for-byte.
    out, n_cdn = wrap_cdn_images_in_transform(out)
    ctr.cdn_wrapped += n_cdn
    # Clean up any /api/transform URLs persisted in markdown (related-
    # card srcs, OpenGraph meta, feed metadata) that wrap_cdn_images_…
    # leaves alone because it only touches bare CDN paths. After CDN's
    # 2026-06-23 hardening these would 404; rewrite them to pre-gen
    # variants too.
    out, n_unwrap = rewrite_persisted_transforms(out)
    ctr.cdn_wrapped += n_unwrap
    out, n_pl = inject_lcp_preload(out)
    ctr.lcp_preloaded += n_pl
    prev = out
    out = inject_howto(page, out)
    if out != prev:
        ctr.howto_patched += 1
    prev = out
    out = inject_word_count(out)
    if out != prev:
        ctr.wc_patched += 1
    prev = out
    out = inject_about(out)
    if out != prev:
        ctr.about_patched += 1
    return _apply_schema_subtype_passes(out, page, ctr)


def _apply_schema_subtype_passes(
    html: str,
    page: Path,
    ctr: _PostbuildCounters,
) -> str:
    """Article-subtype JSON-LD passes: TechArticle / ScholarlyArticle
    (auto-dispatched by inject_tech_article), NewsArticle for posts
    inside the 48-hour Google News carousel window, and
    SoftwareSourceCode on the projects index. Each is idempotent;
    the per-pass counter is bumped on the first run that mutates HTML."""
    prev = html
    out = inject_tech_article(page, html)
    if out != prev:
        ctr.techarticle_patched += 1
    prev = out
    out = inject_news_article(page, out)
    if out != prev:
        ctr.newsarticle_patched += 1
    prev = out
    out = inject_software_source_code(page, out)
    if out != prev:
        ctr.softwaresourcecode_patched += 1
    # Last, so every Article node that exists on the page — ssg's BlogPosting
    # and whichever subtype was just injected — agrees with <link rel=
    # canonical> and with itself. Runs before inject_jsonld_hashes so the CSP
    # hash covers the aligned bytes.
    return out


def _apply_article_passes(html: str, page: Path, ctr: _PostbuildCounters) -> str:
    """Article-furniture + body-content injection passes."""
    out = _bump(inject_eyebrow, html, ctr, "eyebrows_set")
    out = _bump(inject_deck, out, ctr, "decks_set")
    out = _bump(inject_article_furniture, out, ctr, "furniture_patched")
    out = _bump(inject_breadcrumbs, out, ctr, "crumbs_patched")
    out = _bump(inject_table_labels, out, ctr, "tables_carded")
    out = _bump(decode_entities_in_jsonld, out, ctr, "jsonld_entities_decoded")
    # Hero banner (figure pulled from the article's og:image). Runs after
    # furniture so its anchor regex sees the post-furniture document, and
    # before the lang switcher so the switcher slots in after the banner.
    out = inject_hero_banner(out)
    out = inject_sigstore_attestation(out, page.parent.name)
    out = _bump(inject_anchor_links_and_toc, out, ctr, "anchor_patched")
    out = _bump(inject_section_rules, out, ctr, "section_rules_set")
    out = _bump(strip_duplicate_body_h1, out, ctr, "body_h1_stripped")
    out = _convert_faq_to_qa(out)
    out = _bump(inject_pullquotes, out, ctr, "pullquotes_set")
    out = _bump(inject_citations, out, ctr, "citation_patched")
    out = _bump(inject_sources_list, out, ctr, "sources_patched")
    out = _bump(inject_mermaid, out, ctr, "mermaid_patched")
    out = _bump(inject_footnotes, out, ctr, "footnotes_set")
    # Interactive index scorecard — upgrade the authored mount marker into the
    # inert <index-scorecard> element + data island + module script. Runs after
    # fix_sri (in _apply_seo_passes), so the module script's SRI is stamped by
    # the pass itself. Idempotent + a no-op on pages without the marker.
    out = inject_index_scorecard(out)
    out = _bump(inject_share_rail, out, ctr, "share_rails_set")
    out = _bump(inject_action_rail, out, ctr, "action_rails_set")
    # Wrap-foot stack — order matters: each _WRAP_CLOSE_RE.sub inserts
    # BEFORE </div></main>, so the LAST pass ends up closest to it.
    # We want: syndicate (top) → cite → reuse → byline (bottom).
    out = _bump(inject_oembed_link, out, ctr, "oembed_links_set")
    out = _bump(inject_syndication_panel, out, ctr, "syndicate_panels_set")
    out = _bump(inject_cite_popover, out, ctr, "cite_panels_set")
    out = _bump(inject_reuse_panel, out, ctr, "reuse_panels_set")
    out = _bump(inject_byline_strap, out, ctr, "byline_straps_set")
    return out


def _apply_nav_passes(html: str, page: Path, ctx: _PostbuildContext) -> str:
    """Prev/next nav + active-link marker. Must run after sources-list
    (which anchors against either the nav or </main>)."""
    parent_dir_name = page.parent.parent.name
    page_lang_for_nav = parent_dir_name if parent_dir_name in _all_active_non_en_langs() else "en"
    page_is_fr = page_lang_for_nav == "fr"
    out = inject_prev_next_nav(
        html,
        page.parent.name,
        ctx.nav_index,
        is_fr=page_is_fr,
        fr_titles=ctx.fr_titles,
        page_lang=page_lang_for_nav,
    )
    out = inject_nav_active(out, page)
    if out != html:
        ctx.counters.nav_patched += 1
    return out


def _is_topic_page(page: Path) -> tuple[bool, bool, list[str]]:
    """Return (is_en_topic, is_fr_topic, is_lang_topic_codes) for the
    topic-subpage hreflang branch."""
    is_en_topic = page.parent.parent.name == "topics" and page.parent.parent.parent == PUBLIC
    is_fr_topic = page.parent.parent.name == "sujets" and page.parent.parent.parent.name == "fr"
    is_lang_topic_codes: list[str] = []
    for _code in _all_active_non_en_langs():
        _topic_dir = _slug_maps(_code)["statics_en_to_lang"].get("topics", "topics")
        if page.parent.parent.name == _topic_dir and page.parent.parent.parent.name == _code:
            is_lang_topic_codes.append(_code)
    return is_en_topic, is_fr_topic, is_lang_topic_codes


def _is_home_page(page: Path) -> bool:
    return (
        page.parent.name == "public"
        or (page.name == "index.html" and page.parent == PUBLIC)
        or (
            page.name == "index.html"
            and page.parent.parent == PUBLIC
            and page.parent.name in _all_active_non_en_langs()
        )
    )


def _apply_hreflang_pass(html: str, page: Path, ctx: _PostbuildContext) -> str:
    """Lang-aware hreflang injection. Topic pages have a dedicated
    triple; home pages emit alternates for every active lang; everything
    else delegates to inject_hreflang."""
    rel_slug = page.parent.name
    is_en_topic, is_fr_topic, is_lang_topic_codes = _is_topic_page(page)
    if is_en_topic or is_fr_topic or is_lang_topic_codes:
        return _topic_hreflang(html, rel_slug)
    if _is_home_page(page):
        return _home_hreflang(html)
    page_lang = (
        page.parent.parent.name if page.parent.parent.name in ctx.translated_per_lang else "en"
    )
    # Slug-keyed pairing applies ONLY to top-level pages: EN
    # ``/<slug>/index.html`` or locale ``/<lang>/<slug>/index.html``.
    # Deeper surfaces (tag landings ``/tags/<tag>/`` and their locale
    # forks, paged listings, case-study details) manage their own
    # hreflang chains — and their LEAF directory name can collide with a
    # top-level slug. Concretely: the "research" TAG page
    # ``/tags/research/`` must never inherit the ``/research/`` static
    # hub's alternate cluster (5-item nav re-architecture); before that
    # slug existed the leaf simply resolved to None, so this guard
    # restores the historical no-op for every non-top-level page.
    try:
        rel_parts = page.relative_to(PUBLIC).parts
    except ValueError:  # absolute page path (tests) vs relative PUBLIC
        rel_parts = page.resolve().relative_to(PUBLIC.resolve()).parts
    expected_depth = 2 if page_lang == "en" else 3
    if len(rel_parts) != expected_depth:
        return html
    return inject_hreflang(html, rel_slug, page_lang, ctx.translated_per_lang)


def _apply_internal_link_passes(html: str, page: Path, ctx: _PostbuildContext) -> str:
    """Wire the article into its topic cluster.

    Three steps, in order: give same-origin absolute article links their
    canonical trailing slash; link the first in-prose mention of a shared
    topic to the sibling article that owns it; then append the nearest
    siblings that are still unlinked so no article is left isolated. All
    three are idempotent and English-only (see internal_links).
    """
    ctr = ctx.counters
    out = canonicalise_absolute_self_links(html)
    if out != html:
        ctr.self_links_canonicalised += 1
    prev = out
    out = inject_contextual_links(page, out, ctx.corpus, ctx.taxonomy, patterns=ctx.alias_patterns)
    if out != prev:
        ctr.contextual_links_added += 1
    prev = out
    out = inject_related_cluster(page, out, ctx.corpus)
    if out != prev:
        ctr.cluster_blocks_added += 1
    return out


def _sweep_duplicate_assets(ctx: _PostbuildContext, had_failures: bool) -> None:
    """Delete the byte-identical ``/_csp/`` assets whose references were all
    rewritten to a canonical twin.

    Runs after the page loop, never during it: a page not yet processed still
    points at them. Skipped when any page failed, since that page kept its
    original references."""
    if had_failures or not ctx.asset_dupes:
        return
    n_removed = remove_duplicate_files(PUBLIC, ctx.asset_dupes)
    print(f"  asset dedupe       : {n_removed} byte-identical /_csp/ asset(s) removed")


def _apply_final_schema_passes(html: str, page: Path, ctr: _PostbuildCounters) -> str:
    """JSON-LD passes that must see the FINAL DOM.

    Both of these depend on markup earlier passes produce, so they run last —
    after article furniture, navigation, hreflang and canonical normalisation,
    and immediately before the CSP hash pass so the hashes cover their bytes.

    * ``inject_faq_schema`` reads the FAQ section, which it locates by the
      heading's ``id``. That ``id`` is added by ``inject_anchor_links_and_toc``
      in the article passes — running earlier found no heading and silently
      emitted nothing.
    * ``align_article_identity`` binds every Article node to the canonical
      URL, so it has to run after ``normalize_canonical`` has settled what
      that URL is, and after every pass that may have added an Article node.
    """
    prev = html
    out = inject_faq_schema(page, html)
    if out != prev:
        ctr.faq_schema_patched += 1
    prev = out
    out = align_article_identity(out)
    if out != prev:
        ctr.article_identity_aligned += 1
    return out


def _process_page(page: Path, ctx: _PostbuildContext) -> None:
    """Run every per-page transform pass on ``page``."""
    original = page.read_text(encoding="utf-8", errors="ignore")
    patched_about = _apply_seo_passes(original, page, ctx.counters)
    patched_about = _apply_internal_link_passes(patched_about, page, ctx)
    patched_src = _apply_article_passes(patched_about, page, ctx.counters)
    # Per-article inline language switcher — runs after article furniture
    # because it inserts between the hero <section> and <main>, which
    # furniture has already populated. Needs ctx for translated_per_lang.
    slug = page.parent.name
    parent_dir = page.parent.parent.name
    page_lang_for_ls = parent_dir if parent_dir in ctx.translated_per_lang else "en"
    new_src = inject_lang_switcher(
        patched_src,
        slug,
        page_lang_for_ls,
        ctx.translated_per_lang,
    )
    if new_src != patched_src:
        ctx.counters.langswitch_patched += 1
        patched_src = new_src
    patched_nav = _apply_nav_passes(patched_src, page, ctx)
    prev_hl = patched_nav
    patched_hl = _apply_hreflang_pass(patched_nav, page, ctx)
    if patched_hl != prev_hl:
        ctx.counters.hreflang_patched += 1
    # Speculation Rules — hover-prerender every internal link.
    patched_hl = inject_speculation_rules(patched_hl)
    # Live GitHub stats on project / home cards.
    patched_hl = inject_github_stats(patched_hl, ctx.gh_stats)
    # Hoist any <link rel=stylesheet> SSG injected inside <body> back
    # into <head> so pa11y AAA stops flagging "link in body".
    patched_hl, n_hoisted = hoist_body_link_stylesheets(patched_hl)
    ctx.counters.link_hoisted += n_hoisted
    # Late-binding CDN-transform pass: inject_article_furniture +
    # inject_github_stats can ADD new <img src="https://cloudcdn.pro/...">
    # tags AFTER the first wrap pass ran in _apply_seo_passes. Without a
    # second pass those late-added imgs ship as raw CDN URLs, which
    # bypasses WebP conversion + width-matching and dings PSI/Lighthouse
    # LCP scores. Already-wrapped URLs are no-op (skipped by the
    # "starts with /api/" guard in _wrap_cdn_path).
    patched_hl, n_cdn_late = wrap_cdn_images_in_transform(patched_hl)
    ctx.counters.cdn_wrapped += n_cdn_late
    # Responsive WebP srcset on large /stocks/images/ content images (after
    # the wrap, so src is already a width-matched variant). WebP-only — the
    # CDN has no AVIF variants.
    patched_hl, n_srcset = add_responsive_srcset(patched_hl)
    ctx.counters.srcset_added += n_srcset
    # Strip redundant title="..." on links where it duplicates the inner
    # text. WAVE flags these as a "redundant alternative text" alert.
    # Run AFTER every furniture / inject pass so author-card + citation
    # links added late also get cleaned.
    patched_hl, n_rt = strip_redundant_link_titles(patched_hl)
    ctx.counters.redundant_titles_stripped += n_rt
    # Update last-modified meta tag to use last_reviewed
    prev_meta = patched_hl
    patched_hl = update_last_modified_date(patched_hl, page, ctx)
    if patched_hl != prev_meta:
        ctx.counters.lastmod_meta_patched += 1
    # Collapse canonical + og:url onto one trailing-slash form (matches the
    # sitemap). Runs after hreflang + furniture so it overrides any earlier
    # writer. Idempotent.
    patched_hl = normalize_canonical(page, patched_hl)
    patched_hl = _apply_final_schema_passes(patched_hl, page, ctx.counters)
    # Traffic beacon — inert unless a token is configured. Deferred and
    # appended last so measurement can never sit on the LCP path.
    prev_beacon = patched_hl
    patched_hl = inject_analytics_beacon(patched_hl, ctx.analytics_token)
    if patched_hl != prev_beacon:
        ctx.counters.analytics_injected += 1
    # Point identical-content stylesheets at one URL so a reader crossing
    # between page types does not re-download bytes they already have.
    prev_dedupe = patched_hl
    patched_hl = rewrite_asset_refs(patched_hl, ctx.asset_dupes)
    if patched_hl != prev_dedupe:
        ctx.counters.asset_dupes_rewritten += 1
    # ssg emits its own listing pages (tag indexes) without our layouts and
    # ships them a weaker default policy. Normalise before hashing so the
    # JSON-LD hashes land in the canonical policy rather than ssg's.
    patched_hl, csp_replaced = normalise_csp(patched_hl)
    if csp_replaced:
        ctx.counters.csp_normalised += 1
    patched2 = inject_jsonld_hashes(patched_hl)
    if patched2 != prev_hl:
        ctx.counters.csp_patched += 1
    if patched2 != original:
        page.write_text(patched2, encoding="utf-8")


def _finalize_build() -> tuple[int, bool, bool, bool, int, int, int, int]:
    """Run post-page-loop tasks: sitemap lastmod refresh, robots.txt
    rewrite, llms.txt + llms-full.txt rewrite, JSON Feed emission,
    XML feed URL fix + ampersand scrub + duplicate-block dedup.
    Returns the counters for the summary line. JS minification runs
    at module init (before SRI hashing) and is reported via the
    module-level _JS_MINIFY_* counters."""
    lastmod_index = build_lastmod_index()
    sitemap_patched = refresh_sitemap_lastmod(PUBLIC / "sitemap.xml", lastmod_index)
    # Append any rendered page (e.g. post-hoc topic clusters) missing
    # from the SSG-generated sitemap. Counted into sitemap_patched so
    # the existing report shape is unchanged.
    sitemap_patched += augment_sitemap_with_rendered_pages(PUBLIC)
    # Drop the stale `<loc>...slug/index.html</loc>` entries that ssg
    # emits with a homepage-stub lastmod. The canonical pretty URL
    # (`<loc>...slug/</loc>`) is added by `_splice_fr_urls` with the
    # article's actual last_reviewed date. Counted into sitemap_patched.
    sitemap_patched += dedupe_sitemap_index_html(PUBLIC / "sitemap.xml")
    robots_written = write_robots(PUBLIC)
    # humans.txt + root security.txt: the SSG emits empty placeholders;
    # copy through from the repo-root sources so both land non-empty.
    write_humans(PUBLIC, Path("."))
    write_security_txt(PUBLIC, Path("."))
    # GitHub Pages re-reads CNAME on every deploy and needs a bare
    # hostname; the SSG emits a full DNS record line.
    if normalise_cname(PUBLIC):
        print("  CNAME              : normalised to bare hostname")
    llms_written = write_llms_txt(PUBLIC)
    llms_ctx_written = write_llms_ctx_txt(PUBLIC)
    llms_full_written = write_llms_full_txt(PUBLIC)
    ai_written = write_ai_txt(PUBLIC)
    write_json_feed(PUBLIC)
    feed_urls_patched = fix_xml_feed_urls(PUBLIC)
    xml_patched = fix_xml_feeds(PUBLIC)
    feeds_deduped = dedupe_xml_feeds(PUBLIC)
    news_shrunk = shrink_news_sitemap(PUBLIC)
    return (
        sitemap_patched,
        robots_written,
        llms_written,
        llms_ctx_written,
        llms_full_written,
        ai_written,
        feed_urls_patched,
        xml_patched,
        feeds_deduped,
        news_shrunk,
    )


def main() -> None:
    """Walk every public/*.html page and run the per-page transform
    pipeline; then run the post-loop finalisation tasks (sitemap,
    robots, feeds) and print the summary line.
    """
    pages = list(PUBLIC.rglob("*.html"))
    ctx = _PostbuildContext(pages)
    # Contain per-page failures so one malformed page can't abort the
    # whole pass silently mid-tree; collect and fail loudly at the end.
    failures: list[tuple[Path, BaseException]] = []
    for page in pages:
        try:
            _process_page(page, ctx)
        except Exception as exc:  # boundary: report + exit 1 below
            failures.append((page, exc))

    _sweep_duplicate_assets(ctx, bool(failures))

    (
        sitemap_patched,
        robots_written,
        llms_written,
        llms_ctx_written,
        llms_full_written,
        ai_written,
        feed_urls_patched,
        xml_patched,
        feeds_deduped,
        news_shrunk,
    ) = _finalize_build()

    # Legacy-URL redirect conversion (/papers -> /research, EN + locale
    # forks). Must run after _finalize_build: the sitemap augment pass
    # would re-add the purged entries, and the per-page loop's
    # normalize_canonical would undo the target canonical. See
    # postbuild_lib/redirects.py for the full policy.
    redirect_pages, redirect_purged = apply_redirect_pages(PUBLIC)
    print(
        f"postbuild: redirects — {redirect_pages} legacy page(s) converted, "
        f"{redirect_purged} sitemap entrie(s) purged"
    )

    c = ctx.counters
    js_saved = _ASSET_STATS[1] - _ASSET_STATS[2]
    js_count = _ASSET_STATS[0]
    css_saved = _ASSET_STATS[4] - _ASSET_STATS[5]
    css_count = _ASSET_STATS[3]
    print(
        f"postbuild: {len(pages)} HTML pages, "
        f"{c.localhost_patched} got localhost→prod scrubbed, "
        f"{c.theme_inlined} got theme-init inlined, "
        f"{c.cdn_wrapped} img(s) wrapped in CDN transform, "
        f"{c.redundant_titles_stripped} redundant link title(s) stripped, "
        f"{c.pretty_links_patched} internal link(s) canonicalised to pretty URLs, "
        f"{c.lastmod_meta_patched} last-modified meta tag(s) updated, "
        f"{c.lcp_preloaded} got LCP image preloaded, "
        f"{c.asset_fp_patched} got asset URLs fingerprinted, "
        f"{c.sri_patched} got real SRI, "
        f"{c.itemlist_patched} got ItemList JSON-LD, "
        f"{c.techarticle_patched} got TechArticle, "
        f"{c.article_identity_aligned} had Article identity aligned to canonical, "
        f"{c.faq_schema_patched} got FAQPage, "
        f"{c.analytics_injected} got the analytics beacon, "
        f"{c.asset_dupes_rewritten} had duplicate asset URLs collapsed, "
        f"{c.contextual_links_added} got contextual internal links, "
        f"{c.cluster_blocks_added} got a cluster block, "
        f"{c.self_links_canonicalised} had absolute self-links canonicalised, "
        f"{c.newsarticle_patched} got NewsArticle, "
        f"{c.softwaresourcecode_patched} got SoftwareSourceCode, "
        f"{c.social_patched} got og:image fixed, "
        f"{c.og_patched} got og:url/locale/site_name, "
        f"{c.img_dims_patched} img(s) stamped w/h, "
        f"{c.howto_patched} HowTo schema(s) injected, "
        f"{c.wc_patched} got wordCount, "
        f"{c.about_patched} got about/mentions entities, "
        f"{c.furniture_patched} got tag badges + meta bar, "
        f"{c.crumbs_patched} got visible breadcrumbs, "
        f"{c.tables_carded} got card-collapse tables, "
        f"{c.eyebrows_set} got FT eyebrow, "
        f"{c.decks_set} got FT deck, "
        f"{c.section_rules_set} got section rules, "
        f"{c.pullquotes_set} got pull-quotes, "
        f"{c.footnotes_set} got footnotes, "
        f"{c.share_rails_set} got share rail, "
        f"{c.syndicate_panels_set} got syndicate panel, "
        f"{c.oembed_links_set} got oEmbed link, "
        f"{c.action_rails_set} got action rail, "
        f"{c.cite_panels_set} got cite popover, "
        f"{c.reuse_panels_set} got reuse panel, "
        f"{c.byline_straps_set} got byline strap, "
        f"{c.langswitch_patched} got inline language rail, "
        f"{c.anchor_patched} got anchor links + ToC, "
        f"{c.body_h1_stripped} got duplicate body H1 stripped, "
        f"{c.citation_patched} got citation graphs, "
        f"{c.sources_patched} got visible sources list, "
        f"{c.mermaid_patched} got mermaid blocks, "
        f"{c.nav_patched} got prev/next nav, "
        f"{c.hreflang_patched} got hreflang pairs, "
        f"{c.csp_patched} got CSP JSON-LD hashes, "
        f"{c.csp_normalised} got CSP normalised, "
        f"{js_count} JS file(s) minified saving {js_saved} bytes, "
        f"{css_count} CSS file(s) minified saving {css_saved} bytes, "
        f"{sitemap_patched} sitemap entries refreshed, "
        f"{feed_urls_patched} feed(s) URL-repaired, "
        f"{xml_patched} XML feed(s) scrubbed, "
        f"{feeds_deduped} XML feed(s) deduped, "
        f"{news_shrunk} news-sitemap shrunk, "
        f"robots.txt {'updated' if robots_written else 'unchanged'}, "
        f"llms.txt {'updated' if llms_written else 'unchanged'}, "
        f"llms-ctx.txt {'updated' if llms_ctx_written else 'unchanged'}, "
        f"llms-full.txt {'updated' if llms_full_written else 'unchanged'}, "
        f"ai.txt {'updated' if ai_written else 'unchanged'}; "
        f"patched {len(pages) - len(failures)}, failed {len(failures)}"
    )
    if failures:
        for page, exc in failures:
            print(
                f"postbuild: FAILED {page.relative_to(PUBLIC)}: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
        raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover — exercised by build.sh
    main()
