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

import re
import sys
from collections.abc import Callable
from pathlib import Path

import rcssmin
import rjsmin

sys.path.insert(0, str(Path(__file__).parent))

PUBLIC = Path("public")
import postbuild_assets as _pa
from postbuild_assets import (
    _build_cdn_transform_url,
    _ensure_trailing_newline,
    _gather_css_targets,
    _gather_js_targets,
    _minify_one,
    b64_sha256,
    fix_sri,
    inject_jsonld_hashes,
    inject_lcp_preload,
    stamp_asset_fingerprints,
    wrap_cdn_images_in_transform,
)

# ---------------------------------------------------------------------------
# 0. JS minification (runs at module init, before any SRI hash is computed)
# ---------------------------------------------------------------------------
#
# Static Site Generator emits ``main.js`` (and the fingerprinted alias
# ``main.<hash>.js``) unminified. Lighthouse's ``unminified-javascript``
# audit flags ~5 KiB of avoidable bytes. We run rjsmin in place *before*
# computing the SRI digests below, so the integrity attributes that
# Static Site Generator (and our own ``fix_sri`` pass) stamp into the
# HTML match the on-disk minified bytes — otherwise the browser blocks
# the script with a "Failed to find a valid digest" error.








def _minify_css(p: Path) -> tuple[int, int]:
    """Minify a CSS file in place + ensure a trailing newline. Same
    SRI-vs-wire reasoning as ``_minify_one``."""
    try:
        src = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0, 0
    candidate = _ensure_trailing_newline(rcssmin.cssmin(src))
    out = candidate if len(candidate) < len(src) else _ensure_trailing_newline(src)
    if out == src:
        return 0, 0
    p.write_text(out, encoding="utf-8")
    return len(src), len(out)




def _bulk_minify_js() -> tuple[int, int, int]:
    """Minify every JS asset under PUBLIC. Returns
    ``(count, bytes_before, bytes_after)``."""
    n = before = after = 0
    for js in _gather_js_targets():
        b, a = _minify_one(js)
        if b:
            before += b
            after += a
            n += 1
    return n, before, after


def _bulk_minify_css() -> tuple[int, int, int]:
    """Minify every CSS asset under PUBLIC. Returns
    ``(count, bytes_before, bytes_after)``."""
    n = before = after = 0
    for css in _gather_css_targets():
        b, a = _minify_css(css)
        if b:
            before += b
            after += a
            n += 1
    return n, before, after


_JS_MINIFY_COUNT, _JS_MINIFY_BEFORE, _JS_MINIFY_AFTER = _bulk_minify_js()
_CSS_MINIFY_COUNT, _CSS_MINIFY_BEFORE, _CSS_MINIFY_AFTER = _bulk_minify_css()


# ---------------------------------------------------------------------------
# 1. SRI fix — /_csp/* + top-level fingerprinted assets
# ---------------------------------------------------------------------------
#
# _pa.asset_hashes is built *after* minification so the digest matches the
# minified bytes. Two flavours of asset path are stamped into the HTML:
#   - /_csp/<hash>.<ext>   — bundled CSS/JS emitted by SSG
#   - /main.<hash>.js      — fingerprinted top-level alias
# Both need to be covered or the browser will refuse to execute scripts
# whose SRI digest doesn't match.

# GitHub Pages / Fastly munges text-class response bodies in flight, but
# the behaviour isn't consistent across edge POPs: some prepend or
# append a trailing ``\n``, others serve the file as-is. We've observed
# both cases on the same deploy depending on which Cloudflare data
# centre routes the request.
#
# SRI requires the integrity attribute to match the bytes the browser
# actually fetches. To handle the variance we publish *both* candidate
# digests in the attribute — the browser accepts any one that matches
# (the SRI spec explicitly supports a whitespace-separated list of
# digests for exactly this kind of edge-byte-flip scenario).
#
# Candidates per asset:
#   - sha256(disk_bytes)              — POP serves file as-is
#   - sha256(disk_bytes + b"\n")      — POP appends one trailing newline
#
# These are the only two states we've observed in the wild; if a third
# variant turns up we add it here.
_PAGES_TRAILING_NEWLINE = b"\n"


def _candidate_digests(body: bytes) -> str:
    """Return one or two space-separated ``sha256-<b64>`` tokens
    covering every observed Pages edge-byte mutation. Whitespace
    separation matches the SRI spec for multi-digest lists."""
    primary = b64_sha256(body)
    appended = b64_sha256(body + _PAGES_TRAILING_NEWLINE)
    if appended == primary:
        return f"sha256-{primary}"
    return f"sha256-{primary} sha256-{appended}"


_csp_dir = PUBLIC / "_csp"
if _csp_dir.is_dir():
    for asset in _csp_dir.iterdir():
        if asset.is_file() and asset.suffix in (".js", ".css"):
            _pa.asset_hashes[asset.name] = _candidate_digests(asset.read_bytes())
# Top-level fingerprinted JS — main.<hash>.js, sw.<hash>.js, theme-init.<hash>.js.
# Keyed by both the bare path (matches HTML reference) and the unprefixed name
# so fix_sri can look it up against either form.
_top_fp_re = re.compile(r"^[a-z\-_]+\.[a-f0-9]+\.js$", re.IGNORECASE)
if PUBLIC.is_dir():
    for asset in PUBLIC.iterdir():
        if asset.is_file() and _top_fp_re.match(asset.name):
            _pa.asset_hashes[asset.name] = _candidate_digests(asset.read_bytes())

# Matches /_csp/<name> OR /<name> for top-level fingerprinted JS aliases.
# Filenames start with a hex digit or letter (SSG emits 16-char hex hashes for
# /_csp/* and 8-char hex hashes appended to the bare /main.<hash>.js alias).






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
_PERSISTED_TRANSFORM_RE = re.compile(
    re.escape(_pa._CDN_HOST)
    + r"/api/transform\?url=(?P<path>/[^&\"' ]+)(?:&[^\"' ]*?w=(?P<w>\d+))?[^\"' ]*"
)


def _rewrite_persisted_transform(match: re.Match[str]) -> str:
    """Convert a persisted /api/transform URL into the equivalent pre-gen
    variant. Used as a single in-place sweep across rendered HTML to clean
    up references the postbuild wrap pass didn't catch (markdown-embedded
    related-card srcs, OpenGraph meta content, JSON feed url fields)."""
    path = match.group("path")
    try:
        width = int(match.group("w") or 1200)
    except (TypeError, ValueError):
        width = 1200
    return _build_cdn_transform_url(path, width, 80)


def rewrite_persisted_transforms(html: str) -> tuple[str, int]:
    """Replace every ``https://cloudcdn.pro/api/transform?url=…`` URL in
    ``html`` with its pre-gen variant equivalent. Returns
    ``(new_html, n_rewrites)``."""
    new_html, n = _PERSISTED_TRANSFORM_RE.subn(_rewrite_persisted_transform, html)
    return new_html, n
















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

_REDUNDANT_LINK_TITLE_RE = re.compile(
    r"<a\b([^>]*)>([^<]+)</a>",
    re.IGNORECASE,
)
_TITLE_ATTR_RE = re.compile(r'\s+title="([^"]+)"', re.IGNORECASE)


def _title_matches_text(title: str, text: str) -> bool:
    """Whitespace + trailing-punctuation insensitive equality."""
    norm_t = re.sub(r"\s+", " ", title).strip().rstrip(".,:;")
    norm_x = re.sub(r"\s+", " ", text).strip().rstrip(".,:;")
    return bool(norm_t) and norm_t == norm_x


def strip_redundant_link_titles(html: str) -> tuple[str, int]:
    """Remove the ``title="…"`` attribute on every ``<a>`` whose title
    matches the visible inner text. Returns ``(new_html, n_removed)``."""
    n = 0

    def patch(m: re.Match[str]) -> str:
        nonlocal n
        attrs, text = m.group(1), m.group(2)
        title_m = _TITLE_ATTR_RE.search(attrs)
        if not title_m or not _title_matches_text(title_m.group(1), text):
            return m.group(0)
        new_attrs = attrs[: title_m.start()] + attrs[title_m.end() :]
        n += 1
        return f"<a{new_attrs}>{text}</a>"

    return _REDUNDANT_LINK_TITLE_RE.sub(patch, html), n


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
# Inline theme-init.js. The original 589-byte file was render-blocking
# (~300 ms wasted on slow 4G per Lighthouse). Inlining the minified
# bootstrap removes the network round-trip entirely and lands the CSS
# request earlier — but the script must still run before paint, so it
# stays in <head> as an inline <script>. Its SHA-256 is collected by
# inject_jsonld_hashes() and added to script-src.
_theme_init_src_path = Path("_layouts/theme-init.js")
THEME_INIT_MINIFIED = (
    rjsmin.jsmin(_theme_init_src_path.read_text(encoding="utf-8"))
    if _theme_init_src_path.is_file()
    else ""
)
# Match the external theme-init reference in any layout-emitted form
# (quoted, unquoted, with or without trailing slash on the close tag).
_theme_init_tag_re = re.compile(
    r'<script\b[^>]*\bsrc=["\']?/theme-init\.js["\']?[^>]*>\s*</script>',
    re.IGNORECASE,
)


def inline_theme_init(html: str) -> tuple[str, int]:
    """Replace the external ``<script src="/theme-init.js">`` tag with an
    inline ``<script>`` carrying the minified theme bootstrap. Returns
    ``(new_html, replacements)``."""
    if not THEME_INIT_MINIFIED:
        return html, 0
    replacement = f"<script>{THEME_INIT_MINIFIED}</script>"
    new, n = _theme_init_tag_re.subn(replacement, html)
    return new, n


# Match the CSP meta tag whether attributes are quoted or not, in either order
# (Static Site Generator's minifier emits `<meta content="..." http-equiv=Content-Security-Policy>`).




# ---------------------------------------------------------------------------
# 3. ItemList JSON-LD on listing pages
# ---------------------------------------------------------------------------

import html as _html
import json as _json

# Listing pages we know about. The key is the relative path; the value is the
# CSS-selector-style article class pattern that identifies an item card on
# that page. Cards we'd otherwise pick up (e.g. "newsroom-featured" on the
# /articles/ page) are folded in via wildcard prefix matching below.
LISTING_PAGES = {
    "articles/index.html": ("newsroom-card", "newsroom-featured"),
    "papers/index.html": ("newsroom-card", "book"),
    "projects/index.html": ("newsroom-card",),
    # Playlists embed Spotify iframes per card, not internal links, so an
    # ItemList over those is semantically wrong — Schema.org's ItemList is
    # for an enumerated list of items addressable by URL on this site.
}

SITE = "https://sebastienrousseau.com"

# Parse one <article class="..."> ... </article> block and extract (title, url).
# The card markup varies but always includes the canonical link as the first
# <a href="..."> with text content matching the card's H2/H3 title.
_card_block_re = re.compile(
    r'<article\b[^>]*\bclass="([^"]+)"[^>]*>([\s\S]*?)</article>',
    re.IGNORECASE,
)
_first_link_re = re.compile(
    r'<a\b[^>]*\bhref="([^"]+)"[^>]*>([\s\S]*?)</a>',
    re.IGNORECASE,
)
_strip_tags_re = re.compile(r"<[^>]+>")
_ws_re = re.compile(r"\s+")


def _strip_tags(s: str) -> str:
    return _ws_re.sub(" ", _strip_tags_re.sub("", s)).strip()


def _card_title_url(body: str) -> tuple[str, str] | None:
    """Pick the canonical ``(title, url)`` pair from one card body.
    The card's H3-title link carries the visible text; the media link
    (wrapping the thumbnail) carries the URL but no text — we want the
    longest-text candidate."""
    best: tuple[int, str, str] | None = None
    for lm in _first_link_re.finditer(body):
        href = _html.unescape(lm.group(1))
        text = _strip_tags(lm.group(2))
        if not href or href.startswith("#") or len(text) < 3:
            continue
        if href.startswith("/"):
            href = SITE + href
        cand = (len(text), text, href)
        if best is None or cand[0] > best[0]:
            best = cand
    return (best[1], best[2]) if best is not None else None


def _itemlist_graph(items: list[tuple[str, str]], page_url: str) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "url": page_url,
        "numberOfItems": len(items),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": url, "name": title}
            for i, (title, url) in enumerate(items)
        ],
    }


def build_itemlist(html: str, classes: tuple[str, ...], page_url: str) -> str | None:
    items: list[tuple[str, str]] = []
    for m in _card_block_re.finditer(html):
        if not any(c in m.group(1).split() for c in classes):
            continue
        pair = _card_title_url(m.group(2))
        if pair is not None:
            items.append(pair)
    if not items:
        return None
    return _json.dumps(_itemlist_graph(items, page_url), separators=(",", ":"), ensure_ascii=False)


def inject_itemlist(page: Path, html: str) -> str:
    rel = page.relative_to(PUBLIC).as_posix()
    classes = LISTING_PAGES.get(rel)
    if not classes:
        return html
    page_url = f"{SITE}/{rel.replace('index.html', '').rstrip('/')}/"
    payload = build_itemlist(html, classes, page_url)
    if not payload:
        return html
    block = '<script type="application/ld+json">' + payload + "</script>"
    # Insert just before </body> so the existing CSP-hash pass picks it up.
    return re.sub(r"(?i)</body>", block + "</body>", html, count=1)


# SEO + Schema.org injection — moved to postbuild_lib.seo
# Article UI furniture — moved to postbuild_lib.article_furniture
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
    hoist_body_link_stylesheets,
    inject_sigstore_attestation,
    inject_table_labels,
    strip_duplicate_body_h1,
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
    write_ai_txt,
    write_humans,
    write_json_feed,
    write_llms_ctx_txt,
    write_llms_full_txt,
    write_llms_txt,
    write_robots,
    write_security_txt,
)
from postbuild_lib.schemas import (
    inject_news_article,
    inject_software_source_code,
    inject_tech_article,
)
from postbuild_lib.seo import (  # noqa: F401 — re-exports for back-compat
    _keywords_re,
    build_about_graph,
    compute_word_count,
    fix_social_image,
    inject_about,
    inject_howto,
    inject_og_completeness,
    inject_word_count,
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
        "anchor_patched",
        "asset_fp_patched",
        "body_h1_stripped",
        "byline_straps_set",
        "cdn_wrapped",
        "citation_patched",
        "cite_panels_set",
        "crumbs_patched",
        "csp_patched",
        "decks_set",
        "eyebrows_set",
        "footnotes_set",
        "furniture_patched",
        "howto_patched",
        "hreflang_patched",
        "img_dims_patched",
        "itemlist_patched",
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
        "pullquotes_set",
        "redundant_titles_stripped",
        "reuse_panels_set",
        "section_rules_set",
        "share_rails_set",
        "social_patched",
        "softwaresourcecode_patched",
        "sources_patched",
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
        "counters",
        "fr_titles",
        "gh_stats",
        "last_reviewed_index",
        "nav_index",
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


_LOCALHOST_HOST_RE = re.compile(
    r"https?://(?:127\.0\.0\.1(?::\d+)?|localhost(?::\d+)?)",
    re.IGNORECASE,
)


# Build the bare-name → fingerprinted-name map once, at module import time —
# every page references the same assets, so the lookup is shared.
for _fp in PUBLIC.glob("main.*.js"):
    if _fp.stem.count(".") == 1:  # e.g. "main.b5833c97" (one dot before suffix)
        _pa._FP_ASSET_MAP["/main.js"] = "/" + _fp.name
for _fp in PUBLIC.glob("highlight.*.css"):
    if _fp.stem.count(".") == 1:
        _pa._FP_ASSET_MAP["/highlight.css"] = "/" + _fp.name


# Match the bare-name asset reference in `<script src=...>` / `<link href=...>`.
# Quoted ("/main.js") and unquoted (src=/main.js) forms — SSG's minifier emits
# the unquoted form for short attribute values.






def scrub_localhost_urls(html: str) -> tuple[str, int]:
    """Replace any ``http://127.0.0.1[:port]`` or ``http://localhost[:port]``
    leftover inside the page (typically <link rel="canonical"> or the
    Atom feed alternate) with the production origin.

    Static Site Generator bakes these in based on the dev-server it was built against;
    they survive its own HTML emission pass and only show up at runtime.
    """
    new = _LOCALHOST_HOST_RE.sub("https://sebastienrousseau.com", html)
    n = 0 if new == html else 1
    return new, n


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
    return out


def _bump(fn: Callable[[str], str], html: str, ctr: _PostbuildCounters, attr: str) -> str:
    """Run a one-arg HTML→HTML injector, bump ``ctr.<attr>`` if the page
    actually changed, return the new HTML. Centralises the
    ``prev = out; out = fn(out); if out != prev: ctr.X += 1`` pattern
    so ``_apply_article_passes`` stays at CC ≤ B as new WS2/WS3 passes
    are added."""
    out = fn(html)
    if out != html:
        setattr(ctr, attr, getattr(ctr, attr) + 1)
    return out


def _apply_article_passes(html: str, page: Path, ctr: _PostbuildCounters) -> str:
    """Article-furniture + body-content injection passes."""
    out = _bump(inject_eyebrow, html, ctr, "eyebrows_set")
    out = _bump(inject_deck, out, ctr, "decks_set")
    out = _bump(inject_article_furniture, out, ctr, "furniture_patched")
    out = _bump(inject_breadcrumbs, out, ctr, "crumbs_patched")
    out = _bump(inject_table_labels, out, ctr, "tables_carded")
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


def _topic_hreflang(html: str, rel_slug: str) -> str:
    """Build + inject the topic-subpage hreflang triple."""
    topic_alts: list[tuple[str, str]] = [
        ("en", f"https://sebastienrousseau.com/topics/{rel_slug}/"),
    ]
    topic_alts.extend(
        (
            _code,
            f"https://sebastienrousseau.com/{_code}/"
            f"{_slug_maps(_code)['statics_en_to_lang'].get('topics', 'topics')}/{rel_slug}/",
        )
        for _code in _all_active_non_en_langs()
    )
    en_url = topic_alts[0][1]
    _hf_re = re.compile(r'<link rel="alternate"[^>]+hreflang="[^"]+"[^/]*/>', re.IGNORECASE)
    cleaned = _hf_re.sub("", html)
    topic_links = "".join(
        f'<link rel="alternate" hreflang="{lc}" href="{u}" />' for lc, u in topic_alts
    )
    topic_links += f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    return re.sub(r"</head>", topic_links + "</head>", cleaned, count=1, flags=re.IGNORECASE)


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


def _home_hreflang(html: str) -> str:
    """Build + inject the home-page hreflang triple."""
    _head_re = re.compile(r"</head>", re.IGNORECASE)
    _hf_re = re.compile(r'<link rel="alternate"[^>]+hreflang="[^"]+"[^/]*/>', re.IGNORECASE)
    cleaned = _hf_re.sub("", html)
    home_alts: list[tuple[str, str]] = [("en", "https://sebastienrousseau.com/")]
    home_alts.extend(
        (_code, f"https://sebastienrousseau.com/{_code}/") for _code in _all_active_non_en_langs()
    )
    home_links = "".join(
        f'<link rel="alternate" hreflang="{lc}" href="{u}" />' for lc, u in home_alts
    )
    home_links += (
        '<link rel="alternate" hreflang="x-default" href="https://sebastienrousseau.com/" />'
    )
    return _head_re.sub(home_links + "</head>", cleaned, count=1)


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
    return inject_hreflang(html, rel_slug, page_lang, ctx.translated_per_lang)


_LAST_MODIFIED_META_RE = re.compile(
    r'(<meta\s+itemprop="dateModified"\s+content=")([^"]*)("\s+id="last-modified"\s*/?>)',
    re.IGNORECASE,
)


def _parse_lastmod_date(last: str) -> str:
    """Helper to parse raw lastmod strings into YYYY-MM-DD format."""
    from datetime import datetime

    if re.match(r"^\d{4}-\d{2}-\d{2}$", last):
        return last
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            return datetime.strptime(last.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return last


def build_comprehensive_lastmod_index() -> dict[str, str]:
    """Walk _posts/ to parse last_reviewed for all pages (falling back to
    last_build_date or date, normalized to YYYY-MM-DD format)."""
    from _frontmatter import read_fm

    out: dict[str, str] = {}
    posts_dir = Path("_posts")
    if not posts_dir.is_dir():
        return out
    for md in posts_dir.glob("*.md"):
        fm = read_fm(md)
        last = fm.get("last_reviewed") or fm.get("last_build_date") or fm.get("date") or ""
        if last:
            out[md.stem] = _parse_lastmod_date(last)
    return out


def update_last_modified_date(html: str, page: Path, ctx: _PostbuildContext) -> str:
    """Update `<meta itemprop="dateModified" content="..." id="last-modified" />`
    to the dynamic `last_reviewed` date from the source page's frontmatter."""
    from datetime import date

    rel_parts = page.relative_to(PUBLIC).parts
    if len(rel_parts) > 1 and rel_parts[0] in ctx.translated_per_lang:
        lang = rel_parts[0]
        slug = rel_parts[1]
    else:
        lang = "en"
        slug = rel_parts[0] if len(rel_parts) > 0 else ""

    en_slug = _resolve_en_slug(slug, lang) or slug
    if en_slug.endswith(".html"):
        en_slug = en_slug[:-5]

    new_date = ctx.last_reviewed_index.get(en_slug, "")
    if not new_date:
        new_date = date.today().isoformat()

    return _LAST_MODIFIED_META_RE.sub(
        rf'\g<1>{new_date}\g<3>',
        html,
        count=1,
    )


def _process_page(page: Path, ctx: _PostbuildContext) -> None:
    """Run every per-page transform pass on ``page``."""
    original = page.read_text(encoding="utf-8", errors="ignore")
    patched_about = _apply_seo_passes(original, page, ctx.counters)
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

    c = ctx.counters
    js_saved = _JS_MINIFY_BEFORE - _JS_MINIFY_AFTER
    js_count = _JS_MINIFY_COUNT
    css_saved = _CSS_MINIFY_BEFORE - _CSS_MINIFY_AFTER
    css_count = _CSS_MINIFY_COUNT
    print(
        f"postbuild: {len(pages)} HTML pages, "
        f"{c.localhost_patched} got localhost→prod scrubbed, "
        f"{c.theme_inlined} got theme-init inlined, "
        f"{c.cdn_wrapped} img(s) wrapped in CDN transform, "
        f"{c.redundant_titles_stripped} redundant link title(s) stripped, "
        f"{c.lastmod_meta_patched} last-modified meta tag(s) updated, "
        f"{c.lcp_preloaded} got LCP image preloaded, "
        f"{c.asset_fp_patched} got asset URLs fingerprinted, "
        f"{c.sri_patched} got real SRI, "
        f"{c.itemlist_patched} got ItemList JSON-LD, "
        f"{c.techarticle_patched} got TechArticle, "
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
                f"postbuild: FAILED {page.relative_to(PUBLIC)}: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
        raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover — exercised by build.sh
    main()
