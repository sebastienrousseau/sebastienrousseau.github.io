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

import base64
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

PUBLIC = Path("public")


def b64_sha256(data: bytes) -> str:
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


# ---------------------------------------------------------------------------
# 1. /_csp/* SRI fix
# ---------------------------------------------------------------------------

_csp_dir = PUBLIC / "_csp"
asset_hashes: dict[str, str] = {}
if _csp_dir.is_dir():
    for asset in _csp_dir.iterdir():
        if asset.is_file() and asset.suffix in (".js", ".css"):
            asset_hashes[asset.name] = b64_sha256(asset.read_bytes())

bogus_re = re.compile(r' integrity="sha256-[a-f0-9]+"')
asset_path_re = re.compile(r'(?:src|href)=["\']?/_csp/([^"\' ]+)')


def fix_sri(html: str) -> str:
    out: list[str] = []
    last = 0
    # Walk every <script>/<link> opening tag, look at its asset path + integrity.
    for m in re.finditer(r'<(?:script|link)[^>]+>', html):
        chunk = m.group(0)
        ap = asset_path_re.search(chunk)
        if not ap:
            continue
        digest = asset_hashes.get(ap.group(1))
        if not digest:
            continue
        # Strip any existing (bogus) integrity, then inject the real one.
        stripped = bogus_re.sub('', chunk)
        if 'integrity=' not in stripped:
            replaced = stripped.rstrip(' />') + f' integrity="sha256-{digest}" crossorigin="anonymous"' + stripped[-2:]
        else:
            replaced = stripped
        out.append(html[last:m.start()])
        out.append(replaced)
        last = m.end()
    out.append(html[last:])
    return "".join(out)


# ---------------------------------------------------------------------------
# 2. CSP hash for inline JSON-LD
# ---------------------------------------------------------------------------

# Capture the literal inline body of every <script type="application/ld+json"> tag.
# (Static Site Generator may emit either single- or double-quoted type attribute and may have
# attribute order vary, so the regex is intentionally loose.)
jsonld_re = re.compile(
    r'<script[^>]*type=["\']?application/ld\+json["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
# Speculation Rules also need a CSP allowance. Chrome 124+ accepts the
# `'inline-speculation-rules'` keyword in script-src, but adding the
# block's actual sha256 hash gives belt-and-braces coverage for older
# browsers / unusual configs.
speculation_re = re.compile(
    r'<script[^>]*type=["\']?speculationrules["\']?[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
# Match the CSP meta tag whether attributes are quoted or not, in either order
# (Static Site Generator's minifier emits `<meta content="..." http-equiv=Content-Security-Policy>`).
csp_tag_re = re.compile(
    r'<meta\b[^>]*?http-equiv=["\']?Content-Security-Policy["\']?[^>]*?>',
    re.IGNORECASE,
)
content_attr_re = re.compile(
    r'(content=)(["\'])(.+?)(\2)',
    re.IGNORECASE | re.DOTALL,
)


def inject_jsonld_hashes(html: str) -> str:
    bodies = [m.group(1) for m in jsonld_re.finditer(html)]
    bodies.extend(m.group(1) for m in speculation_re.finditer(html))
    if not bodies:
        return html
    hashes = sorted({b64_sha256(b.encode("utf-8")) for b in bodies})
    hash_tokens = " ".join(f"'sha256-{h}'" for h in hashes)

    def patch_csp(tag_match: re.Match[str]) -> str:
        tag = tag_match.group(0)

        def patch_content(c: re.Match[str]) -> str:
            policy = c.group(3)
            new_policy = re.sub(r"(script-src[^;]*?)\s*'unsafe-inline'", r"\1", policy)
            new_policy = re.sub(
                r"(script-src)(\s+)",
                r"\1 " + hash_tokens + r"\2",
                new_policy,
                count=1,
            )
            return c.group(1) + c.group(2) + new_policy + c.group(4)

        return content_attr_re.sub(patch_content, tag, count=1)

    return csp_tag_re.sub(patch_csp, html, count=1)


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
    "papers/index.html":   ("newsroom-card", "book"),
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
_strip_tags_re = re.compile(r'<[^>]+>')
_ws_re = re.compile(r'\s+')


def _strip_tags(s: str) -> str:
    return _ws_re.sub(' ', _strip_tags_re.sub('', s)).strip()


def _card_title_url(body: str) -> tuple[str, str] | None:
    """Pick the canonical ``(title, url)`` pair from one card body.
    The card's H3-title link carries the visible text; the media link
    (wrapping the thumbnail) carries the URL but no text — we want the
    longest-text candidate."""
    best: tuple[int, str, str] | None = None
    for lm in _first_link_re.finditer(body):
        href = _html.unescape(lm.group(1))
        text = _strip_tags(lm.group(2))
        if not href or href.startswith('#') or len(text) < 3:
            continue
        if href.startswith('/'):
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
    return _json.dumps(_itemlist_graph(items, page_url), separators=(',', ':'), ensure_ascii=False)


def inject_itemlist(page: Path, html: str) -> str:
    rel = page.relative_to(PUBLIC).as_posix()
    classes = LISTING_PAGES.get(rel)
    if not classes:
        return html
    page_url = f"{SITE}/{rel.replace('index.html', '').rstrip('/')}/"
    payload = build_itemlist(html, classes, page_url)
    if not payload:
        return html
    block = (
        '<script type="application/ld+json">'
        + payload +
        '</script>'
    )
    # Insert just before </body> so the existing CSP-hash pass picks it up.
    return re.sub(r'(?i)</body>', block + '</body>', html, count=1)


# SEO + Schema.org injection — moved to postbuild_lib.seo
# Article UI furniture — moved to postbuild_lib.article_furniture
from postbuild_lib.article_furniture import (  # noqa: F401 — re-exports
    AUTHOR_AVATAR,
    AUTHOR_NAME,
    AUTHOR_URL,
    _all_active_non_en_langs,
    _alternates_for_en_slug,
    _convert_faq_to_qa,
    _detect_page_lang,
    _is_french,
    _labels,
    _labels_for_lang,
    _nav_active_target,
    _resolve_en_slug,
    _slug_maps,
    _slug_maps_for,
    _translated_slugs,
    _translated_slugs_per_lang,
    build_fr_title_index,
    build_post_nav_index,
    hoist_body_link_stylesheets,
    inject_anchor_links_and_toc,
    inject_article_furniture,
    inject_citations,
    inject_hreflang,
    inject_mermaid,
    inject_nav_active,
    inject_prev_next_nav,
    inject_sigstore_attestation,
    inject_sources_list,
    inject_speculation_rules,
    slugify,
)

# Live GitHub repo stats — moved to postbuild_lib.github_stats
from postbuild_lib.github_stats import (
    gh_stats_index as _gh_stats_index,
)
from postbuild_lib.github_stats import (
    inject_github_stats,
)

# Output emitters — moved to postbuild_lib.output. Re-exported so
# tests/test_postbuild.py + any external probe keeps working.
from postbuild_lib.output import (  # noqa: F401 — re-exports
    build_lastmod_index,
    build_llms_full_txt,
    build_llms_txt,
    escape_xml_ampersands,
    fix_xml_feed_urls,
    fix_xml_feeds,
    refresh_sitemap_lastmod,
    shrink_news_sitemap,
    write_json_feed,
    write_llms_full_txt,
    write_llms_txt,
    write_robots,
)
from postbuild_lib.schemas import (
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


class _PostbuildCounters:
    """Per-pass counters threaded through ``_process_page``.

    Using a mutable container so the per-page helper can bump counters
    in-place without returning a 20-tuple. The orchestrator reads them
    once at the end for the summary line.
    """

    __slots__ = (
        "about_patched",
        "anchor_patched",
        "asset_fp_patched",
        "citation_patched",
        "csp_patched",
        "furniture_patched",
        "howto_patched",
        "hreflang_patched",
        "img_dims_patched",
        "itemlist_patched",
        "link_hoisted",
        "localhost_patched",
        "mermaid_patched",
        "nav_patched",
        "og_patched",
        "social_patched",
        "softwaresourcecode_patched",
        "sources_patched",
        "sri_patched",
        "techarticle_patched",
        "wc_patched",
    )

    def __init__(self) -> None:
        for name in self.__slots__:
            setattr(self, name, 0)


class _PostbuildContext:
    """Pre-pass artefacts read once and shared across pages."""

    __slots__ = ("counters", "fr_titles", "gh_stats", "nav_index", "translated_per_lang")

    def __init__(self, pages: list[Path]) -> None:
        self.nav_index = build_post_nav_index(pages)
        self.fr_titles = build_fr_title_index(pages)
        # Legacy FR-only sets are kept around in case anything probes them;
        # the new lang-keyed dict drives the modern hreflang path.
        _translated_slugs()
        self.translated_per_lang = _translated_slugs_per_lang()
        self.gh_stats = _gh_stats_index()
        self.counters = _PostbuildCounters()


_LOCALHOST_HOST_RE = re.compile(
    r'https?://(?:127\.0\.0\.1(?::\d+)?|localhost(?::\d+)?)',
    re.IGNORECASE,
)


# Build the bare-name → fingerprinted-name map once, at module import time —
# every page references the same assets, so the lookup is shared.
_FP_ASSET_MAP: dict[str, str] = {}
for _fp in PUBLIC.glob("main.*.js"):
    if _fp.stem.count(".") == 1:  # e.g. "main.b5833c97" (one dot before suffix)
        _FP_ASSET_MAP["/main.js"] = "/" + _fp.name
for _fp in PUBLIC.glob("highlight.*.css"):
    if _fp.stem.count(".") == 1:
        _FP_ASSET_MAP["/highlight.css"] = "/" + _fp.name


# Match the bare-name asset reference in `<script src=...>` / `<link href=...>`.
# Quoted ("/main.js") and unquoted (src=/main.js) forms — SSG's minifier emits
# the unquoted form for short attribute values.
def _build_fp_pattern() -> re.Pattern[str] | None:
    if not _FP_ASSET_MAP:
        return None
    bares = sorted(_FP_ASSET_MAP, key=len, reverse=True)
    alternation = "|".join(re.escape(b) for b in bares)
    return re.compile(
        r'(<(?:script|link)\b[^>]*\b(?:src|href)=["\']?)('
        + alternation
        + r')(["\']?[^>]*>)',
        re.IGNORECASE,
    )


_FP_PATTERN = _build_fp_pattern()


def stamp_asset_fingerprints(html: str) -> tuple[str, int]:
    """Rewrite bare ``/main.js`` / ``/highlight.css`` references in
    ``<script src>`` / ``<link href>`` tags to their fingerprinted
    counterparts (``/main.b5833c97.js``, ``/highlight.a92b9694.css``).

    The bare-name aliases are kept on disk by ``build.sh`` for any
    code path that still references them (service-worker fetches,
    legacy bookmarks), but every HTML page should reference the
    fingerprinted name so that an edge cache (Cloudflare/Fastly) is
    forced to fetch fresh bytes whenever the file content changes.

    Returns ``(new_html, swaps)``."""
    if _FP_PATTERN is None:
        return html, 0
    n = 0

    def replace(m: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return m.group(1) + _FP_ASSET_MAP[m.group(2)] + m.group(3)

    return _FP_PATTERN.sub(replace, html), n


def scrub_localhost_urls(html: str) -> tuple[str, int]:
    """Replace any ``http://127.0.0.1[:port]`` or ``http://localhost[:port]``
    leftover inside the page (typically <link rel="canonical"> or the
    Atom feed alternate) with the production origin.

    Shokunin bakes these in based on the dev-server it was built against;
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
    prev = out
    out = inject_tech_article(page, out)
    if out != prev:
        ctr.techarticle_patched += 1
    prev = out
    out = inject_software_source_code(page, out)
    if out != prev:
        ctr.softwaresourcecode_patched += 1
    return out


def _apply_article_passes(html: str, page: Path, ctr: _PostbuildCounters) -> str:
    """Article-furniture + body-content injection passes."""
    prev = html
    out = inject_article_furniture(html)
    if out != prev:
        ctr.furniture_patched += 1
    out = inject_sigstore_attestation(out, page.parent.name)
    prev = out
    out = inject_anchor_links_and_toc(out)
    if out != prev:
        ctr.anchor_patched += 1
    out = _convert_faq_to_qa(out)
    prev = out
    out = inject_citations(out)
    if out != prev:
        ctr.citation_patched += 1
    prev = out
    out = inject_sources_list(out)
    if out != prev:
        ctr.sources_patched += 1
    prev = out
    out2 = inject_mermaid(out)
    if out2 != prev:
        ctr.mermaid_patched += 1
        out = out2
    return out


def _apply_nav_passes(html: str, page: Path, ctx: _PostbuildContext) -> str:
    """Prev/next nav + active-link marker. Must run after sources-list
    (which anchors against either the nav or </main>)."""
    parent_dir_name = page.parent.parent.name
    page_lang_for_nav = (
        parent_dir_name if parent_dir_name in _all_active_non_en_langs() else "en"
    )
    page_is_fr = page_lang_for_nav == "fr"
    out = inject_prev_next_nav(
        html, page.parent.name, ctx.nav_index, is_fr=page_is_fr,
        fr_titles=ctx.fr_titles, page_lang=page_lang_for_nav,
    )
    out = inject_nav_active(out, page)
    if out != html:
        ctx.counters.nav_patched += 1
    return out


def _is_topic_page(page: Path) -> tuple[bool, bool, list[str]]:
    """Return (is_en_topic, is_fr_topic, is_lang_topic_codes) for the
    topic-subpage hreflang branch."""
    is_en_topic = (
        page.parent.parent.name == "topics"
        and page.parent.parent.parent == PUBLIC
    )
    is_fr_topic = (
        page.parent.parent.name == "sujets"
        and page.parent.parent.parent.name == "fr"
    )
    is_lang_topic_codes: list[str] = []
    for _code in _all_active_non_en_langs():
        _topic_dir = _slug_maps(_code)["statics_en_to_lang"].get("topics", "topics")
        if (
            page.parent.parent.name == _topic_dir
            and page.parent.parent.parent.name == _code
        ):
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
    cleaned = _hf_re.sub('', html)
    topic_links = ''.join(
        f'<link rel="alternate" hreflang="{lc}" href="{u}" />'
        for lc, u in topic_alts
    )
    topic_links += f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    return re.sub(r'</head>', topic_links + '</head>', cleaned, count=1, flags=re.IGNORECASE)


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
    _head_re = re.compile(r'</head>', re.IGNORECASE)
    _hf_re = re.compile(r'<link rel="alternate"[^>]+hreflang="[^"]+"[^/]*/>', re.IGNORECASE)
    cleaned = _hf_re.sub('', html)
    home_alts: list[tuple[str, str]] = [("en", "https://sebastienrousseau.com/")]
    home_alts.extend(
        (_code, f"https://sebastienrousseau.com/{_code}/")
        for _code in _all_active_non_en_langs()
    )
    home_links = ''.join(
        f'<link rel="alternate" hreflang="{lc}" href="{u}" />'
        for lc, u in home_alts
    )
    home_links += '<link rel="alternate" hreflang="x-default" href="https://sebastienrousseau.com/" />'
    return _head_re.sub(home_links + '</head>', cleaned, count=1)


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
        page.parent.parent.name
        if page.parent.parent.name in ctx.translated_per_lang
        else "en"
    )
    return inject_hreflang(html, rel_slug, page_lang, ctx.translated_per_lang)


def _process_page(page: Path, ctx: _PostbuildContext) -> None:
    """Run every per-page transform pass on ``page``."""
    original = page.read_text(encoding="utf-8", errors="ignore")
    patched_about = _apply_seo_passes(original, page, ctx.counters)
    patched_src = _apply_article_passes(patched_about, page, ctx.counters)
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
    patched2 = inject_jsonld_hashes(patched_hl)
    if patched2 != prev_hl:
        ctx.counters.csp_patched += 1
    if patched2 != original:
        page.write_text(patched2, encoding="utf-8")


def _finalize_build() -> tuple[int, bool, bool, bool, int, int, int]:
    """Run post-page-loop tasks: sitemap lastmod refresh, robots.txt
    rewrite, llms.txt + llms-full.txt rewrite, JSON Feed emission,
    XML feed URL fix + ampersand scrub. Returns the counters for the
    summary line."""
    lastmod_index = build_lastmod_index()
    sitemap_patched = refresh_sitemap_lastmod(PUBLIC / "sitemap.xml", lastmod_index)
    robots_written = write_robots(PUBLIC)
    llms_written = write_llms_txt(PUBLIC)
    llms_full_written = write_llms_full_txt(PUBLIC)
    write_json_feed(PUBLIC)
    feed_urls_patched = fix_xml_feed_urls(PUBLIC)
    xml_patched = fix_xml_feeds(PUBLIC)
    news_shrunk = shrink_news_sitemap(PUBLIC)
    return (
        sitemap_patched, robots_written, llms_written, llms_full_written,
        feed_urls_patched, xml_patched, news_shrunk,
    )


def main() -> None:
    """Walk every public/*.html page and run the per-page transform
    pipeline; then run the post-loop finalisation tasks (sitemap,
    robots, feeds) and print the summary line.
    """
    pages = list(PUBLIC.rglob("*.html"))
    ctx = _PostbuildContext(pages)
    for page in pages:
        _process_page(page, ctx)

    (
        sitemap_patched, robots_written, llms_written, llms_full_written,
        feed_urls_patched, xml_patched, news_shrunk,
    ) = _finalize_build()

    c = ctx.counters
    print(
        f"postbuild: {len(pages)} HTML pages, "
        f"{c.localhost_patched} got localhost→prod scrubbed, "
        f"{c.asset_fp_patched} got asset URLs fingerprinted, "
        f"{c.sri_patched} got real SRI, "
        f"{c.itemlist_patched} got ItemList JSON-LD, "
        f"{c.techarticle_patched} got TechArticle, "
        f"{c.softwaresourcecode_patched} got SoftwareSourceCode, "
        f"{c.social_patched} got og:image fixed, "
        f"{c.og_patched} got og:url/locale/site_name, "
        f"{c.img_dims_patched} img(s) stamped w/h, "
        f"{c.howto_patched} HowTo schema(s) injected, "
        f"{c.wc_patched} got wordCount, "
        f"{c.about_patched} got about/mentions entities, "
        f"{c.furniture_patched} got tag badges + meta bar, "
        f"{c.anchor_patched} got anchor links + ToC, "
        f"{c.citation_patched} got citation graphs, "
        f"{c.sources_patched} got visible sources list, "
        f"{c.mermaid_patched} got mermaid blocks, "
        f"{c.nav_patched} got prev/next nav, "
        f"{c.hreflang_patched} got hreflang pairs, "
        f"{c.csp_patched} got CSP JSON-LD hashes, "
        f"{sitemap_patched} sitemap entries refreshed, "
        f"{feed_urls_patched} feed(s) URL-repaired, "
        f"{xml_patched} XML feed(s) scrubbed, "
        f"{news_shrunk} news-sitemap shrunk, "
        f"robots.txt {'updated' if robots_written else 'unchanged'}, "
        f"llms.txt {'updated' if llms_written else 'unchanged'}, "
        f"llms-full.txt {'updated' if llms_full_written else 'unchanged'}"
    )


if __name__ == "__main__":
    main()
