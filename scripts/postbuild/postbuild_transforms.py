"""Page-level HTML transform passes: ItemList JSON-LD, comprehensive
last-modified stamping, home/topic hreflang blocks, localhost-URL scrubbing,
redundant link-title stripping, theme-init inlining, and persisted-transform
rewriting. Split from postbuild (Phase 4.1).

Imports the i18n slug helpers from postbuild_lib, the CDN transform builder from
postbuild_assets, and (type-only) the orchestration counters from postbuild —
all one-directional; postbuild imports the pass entry points back.
"""

from __future__ import annotations

import html as _html
import json as _json
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import rjsmin

sys.path.insert(0, str(Path(__file__).resolve().parent))
from postbuild_assets import _CDN_HOST, _build_cdn_transform_url
from postbuild_lib._i18n import _all_active_non_en_langs, _slug_maps
from postbuild_lib.hreflang import HREFLANG_LINK_RE, _resolve_en_slug

PUBLIC = Path("public")
_theme_init_src_path = Path("_layouts/theme-init.js")

_PERSISTED_TRANSFORM_RE = re.compile(
    re.escape(_CDN_HOST)
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


THEME_INIT_MINIFIED = (
    rjsmin.jsmin(_theme_init_src_path.read_text(encoding="utf-8"))
    if _theme_init_src_path.is_file()
    else ""
)
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


LISTING_PAGES = {
    "articles/index.html": ("newsroom-card", "newsroom-featured"),
    "papers/index.html": ("newsroom-card", "book"),
    "projects/index.html": ("newsroom-card",),
    # Playlists embed Spotify iframes per card, not internal links, so an
    # ItemList over those is semantically wrong — Schema.org's ItemList is
    # for an enumerated list of items addressable by URL on this site.
}
SITE = "https://sebastienrousseau.com"
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


def _strip_previous_itemlist(html: str, page_url: str) -> str:
    """Remove an ItemList block this pass wrote on an earlier run.

    Scoped to this pass's exact signature *including the page URL*, so it
    cannot touch an ItemList emitted by build_topics, build_changelog or
    the case-study builder that happens to share the page.
    """
    return re.sub(
        r'<script type="application/ld\+json">'
        r'\{"@context":"https://schema\.org","@type":"ItemList","url":"'
        + re.escape(page_url)
        + r'"[\s\S]*?</script>',
        "",
        html,
    )


def inject_itemlist(page: Path, html: str) -> str:
    """Set the listing page's ItemList JSON-LD.

    Replaces rather than appends. Postbuild is re-run over built pages, and
    this inserted a fresh <script> before </body> every time with nothing
    checking for one already there — /projects/ grew by a full 29-item
    graph per run, about 18.7 KB, and never reached a fixed point.
    """
    rel = page.relative_to(PUBLIC).as_posix()
    classes = LISTING_PAGES.get(rel)
    if not classes:
        return html
    page_url = f"{SITE}/{rel.replace('index.html', '').rstrip('/')}/"
    html = _strip_previous_itemlist(html, page_url)
    payload = build_itemlist(html, classes, page_url)
    if not payload:
        return html
    block = '<script type="application/ld+json">' + payload + "</script>"
    # Insert just before </body> so the existing CSP-hash pass picks it up.
    return re.sub(r"(?i)</body>", block + "</body>", html, count=1)


_LOCALHOST_HOST_RE = re.compile(
    r"https?://(?:127\.0\.0\.1(?::\d+)?|localhost(?::\d+)?)",
    re.IGNORECASE,
)


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


def _bump(fn: Callable[[str], str], html: str, ctr: Any, attr: str) -> str:
    """Run a one-arg HTML→HTML injector, bump ``ctr.<attr>`` if the page
    actually changed, return the new HTML. Centralises the
    ``prev = out; out = fn(out); if out != prev: ctr.X += 1`` pattern
    so ``_apply_article_passes`` stays at CC ≤ B as new WS2/WS3 passes
    are added."""
    out = fn(html)
    if out != html:
        setattr(ctr, attr, getattr(ctr, attr) + 1)
    return out


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
    cleaned = HREFLANG_LINK_RE.sub("", html)
    topic_links = "".join(
        f'<link rel="alternate" hreflang="{lc}" href="{u}" />' for lc, u in topic_alts
    )
    topic_links += f'<link rel="alternate" hreflang="x-default" href="{en_url}" />'
    return re.sub(r"</head>", topic_links + "</head>", cleaned, count=1, flags=re.IGNORECASE)


def _home_hreflang(html: str) -> str:
    """Build + inject the home-page hreflang triple."""
    _head_re = re.compile(r"</head>", re.IGNORECASE)
    cleaned = HREFLANG_LINK_RE.sub("", html)
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


def update_last_modified_date(html: str, page: Path, ctx: Any) -> str:
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
        rf"\g<1>{new_date}\g<3>",
        html,
        count=1,
    )
