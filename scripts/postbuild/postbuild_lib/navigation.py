# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Per-page navigation furniture: anchor links + table of contents,
breadcrumbs, active-nav marking, and prev/next pagination (with the
post-nav index it walks).

Split from article_furniture (Phase 4.1). Imports shared constants + slugify
from article_furniture, _DATED_SLUG_RE from _core, and _labels from _i18n
(one-directional — article_furniture does not import this module).
"""

from __future__ import annotations

import json as _json
import re
import sys
from html import escape as _esc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE
from postbuild_lib._i18n import _all_active_non_en_langs, _labels, _slug_maps
from postbuild_lib.article_furniture import (
    _BASE_URL,
    _H1_RE,
    _HEADING_RE,
    _LDJSON_BLOCK_RE,
    _MAIN_RE,
    PUBLIC,
    slugify,
)


def _relativize(url: str) -> str:
    if url.startswith(_BASE_URL):
        return url[len(_BASE_URL) :] or "/"
    return url


def _trail_from_node(node: object) -> list[tuple[str, str]]:
    """Extract a 3-level ``(name, root-relative href)`` trail from one
    JSON-LD node; empty list when the node isn't a well-formed
    ``BreadcrumbList``."""
    if not isinstance(node, dict) or node.get("@type") != "BreadcrumbList":
        return []
    raw = node.get("itemListElement")
    if not isinstance(raw, list) or len(raw) != 3:
        return []
    items: list[tuple[str, str]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            return []
        name, url = entry.get("name"), entry.get("item")
        if not (isinstance(name, str) and isinstance(url, str)):
            return []
        items.append((name, _relativize(url)))
    return items


def _breadcrumb_items(html: str) -> list[tuple[str, str]]:
    """Return the article's ``BreadcrumbList`` as ``[(name, href), …]``
    with hrefs made root-relative. Empty list when no 3-level trail is
    found (listing / static pages) or the JSON-LD is malformed."""
    for m in _LDJSON_BLOCK_RE.finditer(html):
        if '"BreadcrumbList"' not in m.group(1):
            continue
        try:
            data = _json.loads(m.group(1))
        except ValueError:
            continue
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
        for node in nodes:
            items = _trail_from_node(node)
            if items:
                return items
    return []


def inject_breadcrumbs(html: str) -> str:
    """Render a visible breadcrumb trail mirroring the page's 3-level
    ``BreadcrumbList`` JSON-LD (Home > Articles > Title), inserted
    directly above the H1 hero. Names and URLs come from the JSON-LD —
    already localized by build_translations — so the visible UI can
    never drift from the structured-data markup."""
    if '"@type":"BlogPosting"' not in html:
        return html
    if 'class="crumbs"' in html:
        return html
    items = _breadcrumb_items(html)
    if not items:
        return html
    aria = _esc(_labels(html).get("Breadcrumb", "Breadcrumb"), quote=True)
    parts = []
    for i, (name, url) in enumerate(items):
        current = ' aria-current="page"' if i == 2 else ""
        parts.append(f'<li><a href="{_esc(url, quote=True)}"{current}>{_esc(name)}</a></li>')
    nav = f'<nav class="crumbs" aria-label="{aria}"><ol>{"".join(parts)}</ol></nav>'
    return html.replace('<section class="ap-hero">', f'{nav}<section class="ap-hero">', 1)


_HEADING_ANCHOR_RE = re.compile(
    r'\s*<a\s+class="heading-anchor"[\s\S]*?</a>',
    re.IGNORECASE,
)


def inject_anchor_links_and_toc(html: str) -> str:
    """Add id="…" + a click-to-copy anchor link icon to every H2/H3 inside
    <main>. If the post has ≥5 H2 headings, build a table-of-contents card
    and insert it at the top of <main>.

    Idempotent: if a previous run already injected a ``.article-toc`` or
    any ``.heading-anchor`` link inside <main>, the function no-ops.
    Without this guard, re-running the pass (e.g. when a stale ``public/``
    tree carries last build's HTML) compounds anchors on each H2 and
    stacks N copies of the TOC — and because each rerun strips tags
    rather than the prior anchor's "#" text content, the TOC labels
    accumulate trailing " # # # #" tokens that contaminate every entry.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    m = _MAIN_RE.search(html)
    if not m:
        return html
    pre, body, post = m.group(1), m.group(2), m.group(3)
    # Idempotency guard — either marker means a previous run already
    # owned this <main>. Skipping returns the HTML untouched.
    if 'class="article-toc"' in body or 'class="heading-anchor"' in body:
        return html
    h2_titles: list[tuple[str, str]] = []
    labels = _labels(html)
    # Track slugs already emitted on this page; append -2, -3… on
    # collision. Non-ASCII scripts (Arabic, Cyrillic, CJK) often
    # slugify to the same Latin fragment (e.g. "FHE", "2026") for
    # multiple headings — without dedup, pa11y fails on duplicate ids.
    seen: dict[str, int] = {}

    def _unique(slug: str, idx: int) -> str:
        if not slug:
            slug = f"section-{idx}"
        n = seen.get(slug, 0) + 1
        seen[slug] = n
        return slug if n == 1 else f"{slug}-{n}"

    heading_idx = 0

    def patch_heading(hm: re.Match[str]) -> str:
        nonlocal heading_idx
        heading_idx += 1
        level = hm.group(1).lower()
        inner = hm.group(2)
        # Drop any prior anchor-link markup from the inner content
        # before computing the heading text. The top-level idempotency
        # guard makes this defensive rather than hot-path — kept so
        # narrow regression cases (e.g. tests that hand-craft a partial
        # state) still degrade safely.
        clean_inner = _HEADING_ANCHOR_RE.sub("", inner)
        text = re.sub(r"<[^>]+>", "", clean_inner).strip()
        if not text:
            return hm.group(0)
        slug = _unique(slugify(text), heading_idx)
        if level == "h2":
            h2_titles.append((slug, text))
        return (
            f'<{level} id="{slug}">{clean_inner} '
            f'<a class="heading-anchor" href="#{slug}" aria-label="{labels["Link to"]} {text}">#</a>'
            f"</{level}>"
        )

    new_body = _HEADING_RE.sub(patch_heading, body)
    toc_html = ""
    if len(h2_titles) >= 5:
        items = "".join(f'<li><a href="#{slug}">{text}</a></li>' for slug, text in h2_titles)
        toc_html = (
            f'<aside class="article-toc" aria-label="{labels["Table of contents"]}">'
            f"<h2>{labels['Contents']}</h2>"
            f"<ol>{items}</ol></aside>"
        )
    return html[: m.start()] + pre + toc_html + new_body + post + html[m.end() :]


def build_post_nav_index(
    pages: list[Path],
) -> dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]]:
    """Build a slug -> (prev, next) lookup over every dated post in pages.

    A dated post is one whose parent directory name matches ``YYYY-MM-DD-…``.
    Order is chronological (oldest first); 'prev' is older, 'next' is newer.
    Each entry is (slug, title) so the renderer can localize labels per
    target page.
    """
    dated: list[tuple[str, str, str]] = []
    for p in pages:
        slug = p.parent.name
        if not _DATED_SLUG_RE.match(slug):
            continue
        # Skip non-EN translations — they share the (EN-)slug with the English
        # original at the data level, but live under /<lang>/<lang-slug>/.
        # Including them would double-count and yield wrong nav.
        if p.parent.parent.name in _all_active_non_en_langs():
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        if '"@type":"BlogPosting"' not in html:
            continue
        m = _H1_RE.search(html)
        title = m.group(1).strip() if m else slug
        dated.append((slug[:10], slug, title))
    dated.sort(key=lambda t: t[0])
    out: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]] = {}
    for i, entry in enumerate(dated):
        prev_e = (dated[i - 1][1], dated[i - 1][2]) if i > 0 else None
        next_e = (dated[i + 1][1], dated[i + 1][2]) if i < len(dated) - 1 else None
        out[entry[1]] = (prev_e, next_e)
    return out


def _nav_target_for_en_page(top: str) -> str:
    """Map an EN top-level page slug to its nav-link href.

    Active-state policy (5-item dropdown nav, deliberate): the primary
    nav is About / Articles / Library / Research / Suite Overview.
    Articles is a plain top-level link; the other four carry a
    disclosure dropdown of sub-items. Because the sub-items are
    ordinary anchors inside the nav <ul>, the generic marking below
    covers them too: dated articles mark the top-level Articles link,
    /case-studies/ marks the Research > Real-World Case Studies
    sub-item, /speaking/ marks About > Public Speaking, /topics/ marks
    Library > Browse by Topic, /iso20022-mcp/ marks the Suite Overview
    > ISO 20022 MCP Suite sub-item, and so on. /research/ appears twice
    (top-level Research and the Whitepapers & Reports sub-item, which
    deliberately targets the canonical /research/ hub rather than the
    /papers/ redirect page); the count=1 substitution in
    inject_nav_active marks the first occurrence -- the top-level link
    -- with aria-current="page". Pages mapped to an href that is not in
    the nav (e.g. /tags/, /glossary/) simply produce no match and carry
    no marker -- intentional, not a bug.
    """
    if _DATED_SLUG_RE.match(top):
        return "/articles/index.html"
    return f"/{top}/index.html"


def _nav_target_for_lang_page(lang: str, top: str) -> str:
    """Map a localised top-level page slug to its nav-link href."""
    articles_slug = _slug_maps(lang)["statics_en_to_lang"].get("articles", "articles")
    if _DATED_SLUG_RE.match(top):
        return f"/{lang}/{articles_slug}/index.html"
    return f"/{lang}/{top}/index.html"


def _nav_active_target(page: Path) -> str | None:
    """Return the nav-link href that should be marked active for this
    page, or ``None`` if there's no obvious match.

    Greedy by depth: ``/about/`` → ``/about/index.html``;
    ``/2026-05-12-…/`` → ``/articles/index.html``;
    ``/<lang>/<x>/`` → ``/<lang>/<x>/index.html``.
    """
    rel = page.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return "/index.html"  # home
    parts = rel.split("/")
    if len(parts) == 2 and parts[1] == "index.html":
        return _nav_target_for_en_page(parts[0])
    if len(parts) == 3 and parts[2] == "index.html":
        lang, top = parts[0], parts[1]
        if lang not in _all_active_non_en_langs():
            return None
        return _nav_target_for_lang_page(lang, top)
    return None


def inject_nav_active(html: str, page: Path) -> str:
    """Add ``aria-current="page"`` + ``class="active"`` to the nav link
    matching this page. For home pages (/, /<lang>/), the brand link
    sitting outside the nav menu is the home indicator, so we mark it
    there. Idempotent — re-running doesn't double-mark."""
    target = _nav_active_target(page)
    if not target:
        return html

    # Always clear any pre-existing active markers in the header first.
    header_m = re.search(r"<header\b[^>]*>([\s\S]*?)</header>", html, re.IGNORECASE)
    if not header_m:
        return html
    header_body = header_m.group(1)
    header_clean = re.sub(r'\s+aria-current=["\']?[^"\'>]+["\']?', "", header_body)
    header_clean = re.sub(r'(<a\b[^>]*?)\s+class=["\']?active["\']?', r"\1", header_clean)

    pat = re.compile(
        r'(<a\s+(?:[^>]*?)href=["\']?)(' + re.escape(target) + r')(["\']?)([^>]*>)',
        re.IGNORECASE,
    )

    def repl(m: re.Match[str]) -> str:
        return (
            f'{m.group(1)}{m.group(2)}{m.group(3)} aria-current="page" class="active"{m.group(4)}'
        )

    new_body = pat.sub(repl, header_clean, count=1)
    open_tag = header_m.group(0)[: header_m.group(0).index(">") + 1]
    return html.replace(header_m.group(0), open_tag + new_body + "</header>", 1)


def inject_prev_next_nav(
    html: str,
    slug: str,
    nav_index: dict[str, tuple[tuple[str, str] | None, tuple[str, str] | None]],
    is_fr: bool = False,
    fr_titles: dict[str, str] | None = None,
    *,
    page_lang: str = "en",
) -> str:
    """Inject a ``<nav class="post-pagination">`` with prev/next links
    just before the closing ``</div></main>`` of any dated BlogPosting
    page. Localised via ``_labels(html)``; non-EN pages get translated
    labels and links pointing to the matching translation under
    ``/<lang>/<lang-slug>/``.
    """
    if '"@type":"BlogPosting"' not in html:
        return html
    # Resolve the EN slug regardless of which lang we're patching.
    if page_lang != "en":
        maps = _slug_maps(page_lang)
        lookup_slug = maps["articles_lang_to_en"].get(slug, slug)
    else:
        lookup_slug = slug
    if 'class="post-pagination"' in html:
        return html
    labels = _labels(html)
    # Pages that ship BlogPosting JSON-LD but aren't in the dated nav chain
    # (landing pages with frontmatter schema=Article, dateless reports) get
    # an empty stub block so validate_jsonld's furniture contract holds.
    if lookup_slug not in nav_index:
        stub = (
            f'<nav class="post-pagination" aria-label="{labels["Article pagination"]}">'
            f'<span class="post-pagination-stub" aria-hidden="true"></span>'
            f'<span class="post-pagination-stub" aria-hidden="true"></span>'
            f"</nav>"
        )
        return re.sub(
            r"(</div>)(\s*(?:<aside\b[^>]*>[\s\S]*?</aside>\s*)*</main>)",
            stub + r"\1\2",
            html,
            count=1,
        )
    prev_e, next_e = nav_index[lookup_slug]
    if not prev_e and not next_e:
        return html
    fr_titles = fr_titles or {}

    def render(entry: tuple[str, str] | None, direction: str, label: str) -> str:
        if not entry:
            return '<span class="post-pagination-stub" aria-hidden="true"></span>'
        s, t = entry
        if page_lang != "en":
            articles_map = _slug_maps(page_lang)["articles_en_to_lang"]
            if s in articles_map:
                href = f"/{page_lang}/{articles_map[s]}/"
                if page_lang == "fr":
                    t = fr_titles.get(s, t)
            else:
                href = f"/{s}/"
        else:
            href = f"/{s}/"
        return (
            f'<a class="post-pagination-{direction}" href="{href}">'
            f'<span class="post-pagination-label">{label}</span>'
            f'<span class="post-pagination-title">{t}</span>'
            f"</a>"
        )

    inner = render(prev_e, "prev", labels["Previous"]) + render(next_e, "next", labels["Next"])
    nav = f'<nav class="post-pagination" aria-label="{labels["Article pagination"]}">{inner}</nav>'
    # The anchor used to be `</div>\s*</main>` (the wrap-div directly closing
    # the main element). But the sigstore-attestation pass runs earlier and
    # may have inserted `<aside class="article-sigstore">...</aside>` between
    # `</div>` and `</main>`. Allow an optional aside (or chain of asides) in
    # between, so pagination still anchors against the wrap-div even after
    # sigstore has run. Without this, translated pages with sigstore bundles
    # silently lost prev/next nav.
    patched = re.sub(
        r"(</div>)(\s*(?:<aside\b[^>]*>[\s\S]*?</aside>\s*)*</main>)",
        nav + r"\1\2",
        html,
        count=1,
    )
    return patched
