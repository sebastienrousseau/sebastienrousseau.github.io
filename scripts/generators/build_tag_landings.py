#!/usr/bin/env python3
"""Generate per-tag landing pages at ``public/tags/<slug>/index.html``.

Runs AFTER ssg, BEFORE build_translations + postbuild. For each
canonical tag with ≥ 3 posts (per ``_data/taxonomy.yml`` resolved
against the corpus), emits a focused landing page:

  - hero        : eyebrow (pillar) + h1 (tag name) + deck (description)
                  + article-count meta
  - main body   : article-card list (newest first) of every post
                  tagged with this canonical, related-tag chips
  - JSON-LD     : CollectionPage + ItemList (Schema.org)

The page reuses the just-emitted ``public/tags/index.html`` cover as
a TEMPLATE skeleton — head/nav/footer/CSS link/CSP placeholders are
all in place, so we just swap the content area. The follow-up
postbuild pass fingerprints CSS, stamps hreflang (we leave a
placeholder), and re-stamps the CSP hashes; locale forks come from
build_translations in a subsequent WS3 commit.

Run from repo root::

    python3 scripts/generators/build_tag_landings.py
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "_data" / "taxonomy.yml"
PUBLIC = ROOT / "public"
TEMPLATE_PATH = PUBLIC / "tags" / "index.html"
# Six editorial pillars from taxonomy.yml's category field. Order
# matches the cover-page pillar grid; same order is used to render
# /categories/index.html.
PILLAR_ORDER = ("ai", "payments", "infra", "policy", "open-source", "leadership")
PILLAR_LABELS: dict[str, str] = {
    "ai": "Applied AI",
    "payments": "Payments & money",
    "infra": "Infrastructure & cryptography",
    "policy": "Policy & resilience",
    "open-source": "Open source",
    "leadership": "Banking leadership",
}
PILLAR_DECKS: dict[str, str] = {
    "ai": "Generative AI, agentic systems, governance, and the LLM tooling that lands in banking workflows.",
    "payments": "Rails, settlement, tokenisation, treasury programmability, and the economics of moving money.",
    "infra": "Post-quantum cryptography, cloud-native banking, platform engineering, and the engineering stack that runs the rail.",
    "policy": "DORA, EU AI Act, NIST standards, third-party risk — the supervisory pressure shaping technology decisions.",
    "open-source": "OSS in regulated banking — supply-chain trust, Rust, MCP, the projects banks rely on and ship.",
    "leadership": "CTO / CIO concerns — strategic technology decisions, organisational design, original analysis.",
}
# Per-locale tags-path segment. Matches the hreflang chain already
# emitted on /tags/index.html. The canonical tag slug stays English
# (post-quantum-cryptography, iso-20022, …) — localising the slug
# itself is a future polish; for now we get URL parity at /<lang>/
# <localised-tags-segment>/<canonical>/index.html.
LOCALE_TAGS_PATH: dict[str, str] = {
    "en": "tags",
    "ar": "wusum",
    "bn": "tag",
    "cs": "stitky",
    "de": "etiketten",
    "es": "etiquetas",
    "fil": "mga-tag",
    "fr": "etiquettes",
    "ha": "tags",
    "he": "tagim",
    "hi": "tag",
    "id": "label",
    "it": "etichette",
    "ja": "tagu",
    "ko": "taegeu",
    "nl": "labels",
    "pl": "tagi",
    "pt-br": "etiquetas",
    "ro": "etichete",
    "ru": "tegi",
    "sv": "taggar",
    "th": "thaek",
    "tr": "etiketler",
    "uk": "tegy",
    "vi": "the",
    "yo": "awon-ami",
    "zh-hans": "biaoqian",
    "zh-hant": "biaoqian-tw",
}
LOCALES_NON_EN = [code for code in LOCALE_TAGS_PATH if code != "en"]

_LANDING_THRESHOLD = 3
_BASE_URL = "https://sebastienrousseau.com"
_TAG_FM_RE = re.compile(r'^tags:\s*"?([^"\n]+)"?', re.MULTILINE)
_TITLE_FM_RE = re.compile(r'^title:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_EXCERPT_FM_RE = re.compile(r'^excerpt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_DESC_FM_RE = re.compile(r'^description:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_BANNER_FM_RE = re.compile(r'^banner:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_BANNER_ALT_FM_RE = re.compile(r'^banner_alt:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
_DEFAULT_BANNER = "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from _core import DATED_SLUG_RE as _DATED_SLUG_RE  # canonical dated-slug matcher

_MAIN_RE = re.compile(
    r'(<main\b[^>]*>)([\s\S]*?)(</main>)',
    re.IGNORECASE,
)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(
    r'<meta name="description" content="[^"]*"', re.IGNORECASE
)
_CANONICAL_RE = re.compile(
    r'<link rel="canonical" href="[^"]*"', re.IGNORECASE
)
_OG_TITLE_RE = re.compile(
    r'<meta property="og:title" content="[^"]*"', re.IGNORECASE
)
_OG_DESC_RE = re.compile(
    r'<meta property="og:description" content="[^"]*"', re.IGNORECASE
)
_OG_URL_RE = re.compile(
    r'<meta property="og:url" content="[^"]*"', re.IGNORECASE
)
_HTML_LANG_RE = re.compile(r'<html lang="[^"]*"', re.IGNORECASE)
# The /tags/index.html cover template carries a leftover hero section
# from its own markdown frontmatter — `<section class="ap-hero"><h1>
# Sebastien Rousseau</h1>…</section>`. Each landing supplies its own
# `<h1>` inside the wrap-div, so we strip the cover's hero to keep
# the page at exactly one h1 (WCAG 2.4.6 + 1.3.1 AAA).
_AP_HERO_BLOCK_RE = re.compile(
    r'<section class="ap-hero">[\s\S]*?</section>',
    re.IGNORECASE,
)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _alias_map(taxonomy: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        out[slug.strip().lower()] = slug
        for alias in entry.get("aliases", []) or []:
            out[alias.strip().lower()] = slug
    return out


# Tiny per-card share rail — 6 monochrome SVG glyphs (X, LinkedIn, Facebook,
# WhatsApp, email, copy-link). Mirrors build_listings._card_share_rail; copied
# here so build_tag_landings stays import-self-contained.
_CARD_SVG_X = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M9.52 6.88L14.86 1h-1.42L8.83 6.07 4.94 1H.78l5.6 7.7L.78 15h1.42l4.78-5.27L11.07 15'
    'h4.16L9.52 6.88zM2.71 2.07h1.83l7.61 10.51h-1.83L2.71 2.07z"/></svg>'
)
_CARD_SVG_LI = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M13.6 13.6h-2.37V9.93c0-.87-.02-2-1.22-2-1.22 0-1.4.95-1.4 1.93v3.74H6.24V6.04h2.27'
    'v1.04h.03c.32-.6 1.09-1.22 2.25-1.22 2.4 0 2.85 1.58 2.85 3.64v4.1zM3.56 5C2.81 5 2.2 4.39 '
    '2.2 3.64S2.81 2.28 3.56 2.28s1.36.61 1.36 1.36S4.31 5 3.56 5zm1.18 8.6H2.39V6.04h2.36V13.6z"/'
    '></svg>'
)
_CARD_SVG_FB = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M9 14H6.5V8.5H5V6h1.5V4.5C6.5 3.07 7.07 2 9.07 2H10.5v2.5H9.43c-.38 0-.43.14-.43.43V'
    '6h1.5L10 8.5H9V14z"/></svg>'
)
_CARD_SVG_WA = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M8 1C4.13 1 1 4.13 1 8c0 1.27.34 2.46.93 3.5L1 15l3.6-.93C5.62 14.66 6.79 15 8 15c3'
    '.87 0 7-3.13 7-7s-3.13-7-7-7zm0 12.7c-1.06 0-2.05-.29-2.9-.78l-.2-.12-2.13.56.57-2.08-.13-.21'
    'A5.69 5.69 0 012.3 8c0-3.14 2.56-5.7 5.7-5.7s5.7 2.56 5.7 5.7-2.56 5.7-5.7 5.7z"/></svg>'
)
_CARD_SVG_EMAIL = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M2 3h12c.55 0 1 .45 1 1v8c0 .55-.45 1-1 1H2c-.55 0-1-.45-1-1V4c0-.55.45-1 1-1zm6 5.'
    '18L13.18 4H2.82L8 8.18zM2 5.46V12h12V5.46L8 9.5 2 5.46z"/></svg>'
)
_CARD_SVG_LINK = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M6.6 10.4a1.5 1.5 0 010-2.1l2.8-2.8a1.5 1.5 0 112.1 2.1L10 9.1l1.1 1.1 1.5-1.5a3 3 0 '
    '00-4.2-4.2L5.6 7.3a3 3 0 000 4.2 3 3 0 002.1.9l-1-1c-.1 0-.1-.1-.1-.1zM9.4 5.6L8.3 6.7l1.4 1.4 '
    '1.1-1.1A1.5 1.5 0 0112.9 9l-2.8 2.8a1.5 1.5 0 11-2.1-2.1L9.1 8.6 8 7.5 6.5 9a3 3 0 004.2 4.2l '
    '2.8-2.8a3 3 0 000-4.2 3 3 0 00-4.1-.6z"/></svg>'
)


def _card_share_rail(url: str, title: str, desc: str) -> str:
    """6-icon per-card share rail: X / LinkedIn / Facebook / WhatsApp /
    email / copy-link. Anchors-only except for copy-link (button +
    data-copy-link)."""
    abs_url = url if url.startswith("http") else f"{_BASE_URL}{url}"
    x_text = f"{title}\n\n{abs_url}"
    li_text = "\n\n".join(p for p in (title, desc, abs_url) if p)
    wa_text = "\n\n".join(p for p in (title, desc, abs_url) if p)
    email_body = "\n\n".join(p for p in (desc, f"Read more: {abs_url}") if p)
    import urllib.parse as _u

    def q(s: str) -> str:
        return _u.quote(s, safe="")

    items = (
        f'<li><a href="https://twitter.com/intent/tweet?text={q(x_text)}" '
        f'rel="noopener noreferrer" aria-label="Share on X">{_CARD_SVG_X}</a></li>'
        f'<li><a href="https://www.linkedin.com/feed/?shareActive=true&text={q(li_text)}" '
        f'rel="noopener noreferrer" aria-label="Share on LinkedIn">{_CARD_SVG_LI}</a></li>'
        f'<li><a href="https://www.facebook.com/sharer/sharer.php?u={q(abs_url)}" '
        f'rel="noopener noreferrer" aria-label="Share on Facebook">{_CARD_SVG_FB}</a></li>'
        f'<li><a href="https://wa.me/?text={q(wa_text)}" '
        f'rel="noopener noreferrer" aria-label="Share on WhatsApp">{_CARD_SVG_WA}</a></li>'
        f'<li><a href="mailto:?subject={q(title)}&body={q(email_body)}" '
        f'aria-label="Share by email">{_CARD_SVG_EMAIL}</a></li>'
        f'<li><button type="button" data-copy-link="{_esc(abs_url)}" '
        f'aria-label="Copy link">{_CARD_SVG_LINK}</button></li>'
    )
    # `<div role="group">` rather than `<nav>` — every card emits the
    # same share rail, so a per-card `<nav aria-label="Share this
    # article">` would trip axe landmark-unique. role="group" carries
    # the semantics without contributing to the page outline.
    return (
        f'<div class="card-share-rail" role="group" aria-label="Share this article">'
        f"<ul>{items}</ul></div>"
    )


def _extract_excerpt(text: str) -> str:
    """Return the post's excerpt or fall back to description."""
    excerpt_m = _EXCERPT_FM_RE.search(text)
    if excerpt_m:
        return excerpt_m.group(1)
    desc_m = _DESC_FM_RE.search(text)
    return desc_m.group(1) if desc_m else ""


def _extract_banner(text: str, title: str) -> tuple[str, str]:
    """Return (banner_url, banner_alt) — banner_alt falls back to title."""
    banner_m = _BANNER_FM_RE.search(text)
    banner_alt_m = _BANNER_ALT_FM_RE.search(text)
    banner = banner_m.group(1) if banner_m else _DEFAULT_BANNER
    banner_alt = banner_alt_m.group(1) if banner_alt_m else title
    return banner, banner_alt


def _parse_raw_tags(tags_line: str) -> list[str]:
    """Split a `tags:` frontmatter line into stripped, non-empty tag
    strings."""
    return [
        t for t in (
            raw.strip().strip('"').strip("'").strip()
            for raw in tags_line.split(",")
        )
        if t
    ]


def _post_meta(path: Path) -> tuple[str, str, str, str, list[str], str, str] | None:
    """Return (title, iso-date, slug, excerpt, [raw tag strings],
    banner, banner_alt) or None."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    tags_m = _TAG_FM_RE.search(text)
    if not tags_m:
        return None
    title_m = _TITLE_FM_RE.search(text)
    title = title_m.group(1) if title_m else path.stem
    excerpt = _extract_excerpt(text)
    banner, banner_alt = _extract_banner(text, title)
    stem_m = _DATED_SLUG_RE.match(path.stem)
    iso_date = stem_m.group(1) if stem_m else ""
    raw_tags = _parse_raw_tags(tags_m.group(1))
    return title, iso_date, path.stem, excerpt, raw_tags, banner, banner_alt


def _canonical_set(raw_tags: list[str], amap: dict[str, str]) -> set[str]:
    """Resolve a post's raw tag strings to a deduplicated set of
    canonical slugs via the alias map."""
    return {amap[r.lower()] for r in raw_tags if r.lower() in amap}


def _post_pillars(raw_tags: list[str], taxonomy: dict, amap: dict[str, str]) -> list[str]:
    """Return ordered list of pillar slugs (categories) this post
    belongs to, derived from its raw tag strings."""
    pillars: set[str] = set()
    for r in raw_tags:
        canon = amap.get(r.lower())
        if not canon:
            continue
        cat = taxonomy.get(canon, {}).get("category")
        if cat:
            pillars.add(cat)
    return [p for p in PILLAR_ORDER if p in pillars]


def _ingest_post(
    path: Path,
    taxonomy: dict,
    amap: dict[str, str],
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    cooccur: dict[str, collections.Counter[str]],
) -> None:
    meta = _post_meta(path)
    if not meta:
        return
    title, iso_date, slug, excerpt, raw_tags, banner, banner_alt = meta
    canons = _canonical_set(raw_tags, amap)
    pillars = _post_pillars(raw_tags, taxonomy, amap)
    for c in canons:
        posts[c].append((title, iso_date, slug, excerpt, pillars, banner, banner_alt))
        for other in canons - {c}:
            cooccur[c][other] += 1


def _walk(taxonomy: dict) -> tuple[
    dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    dict[str, collections.Counter[str]],
]:
    """Return:
    * per-canonical [(title, iso-date, slug, excerpt, pillars, banner,
      banner_alt), ...] newest first
    * per-canonical Counter of OTHER canonicals that co-occur on the
      same posts — drives the "related tags" sidebar.
    """
    amap = _alias_map(taxonomy)
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]] = collections.defaultdict(list)
    cooccur: dict[str, collections.Counter[str]] = collections.defaultdict(
        collections.Counter
    )
    for path in sorted((ROOT / "_posts").glob("*.md")):
        # Skip non-article markdown: hub pages (tags.md / categories.md),
        # the homepage (index.md), and anything else without a YYYY-MM-DD
        # date prefix. Without the prefix we'd otherwise emit cards
        # pointing at `/index/` etc. (an obvious broken-link smell).
        if not _DATED_SLUG_RE.match(path.stem):
            continue
        _ingest_post(path, taxonomy, amap, posts, cooccur)
    for c in posts:
        posts[c].sort(key=lambda p: p[1] or "0000", reverse=True)
    return posts, cooccur


def _render_article_cards(
    posts_for_tag: list[tuple[str, str, str, str, list[str], str, str]],
    href_overrides: dict[str, str] | None = None,
    eyebrow_override: str | None = None,
) -> str:
    """Render the FT-tier image-card list used across tag landings,
    category landings, and the cross-pillar "Recent articles" rail.
    ``href_overrides`` maps EN slug → locale URL (used by locale forks).
    ``eyebrow_override`` overrides the per-pillar caption (used by
    category pages where every card shares the same pillar)."""
    cards: list[str] = []
    overrides = href_overrides or {}
    for title, iso_date, slug, excerpt, pillars, banner, banner_alt in posts_for_tag:
        href = overrides.get(slug) or f"/{slug}/"
        eyebrow_label = eyebrow_override or (
            PILLAR_LABELS[pillars[0]] if pillars else "Editorial"
        )
        eyebrow_html = f'<p class="eyebrow card-eyebrow">{_esc(eyebrow_label).upper()}</p>'
        date_html = (
            f'<time datetime="{iso_date}" class="card-date">{iso_date}</time>'
            if iso_date
            else ""
        )
        excerpt_html = (
            f'<p class="card-excerpt">{_esc(excerpt)}</p>' if excerpt else ""
        )
        safe_alt = banner_alt or title
        img_html = (
            f'<a class="card-media" href="{href}" tabindex="-1" aria-hidden="true">'
            f'<img src="{banner}" alt="{_esc(safe_alt)}" loading="lazy" '
            f'decoding="async" width="800" height="800" />'
            f"</a>"
        )
        share_html = _card_share_rail(href, title, excerpt)
        body_html = (
            f'<div class="card-body">'
            f"{eyebrow_html}"
            f'<h2><a href="{href}">{_esc(title)}</a></h2>'
            f"{date_html}"
            f"{excerpt_html}"
            f"{share_html}"
            f"</div>"
        )
        cards.append(
            f'<article class="tag-landing-card tag-landing-card--ft">'
            f"{img_html}{body_html}"
            f"</article>"
        )
    return "".join(cards)


def _render_related_tags(
    cooccur: collections.Counter[str],
    taxonomy: dict,
    slug: str,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    n: int = 6,
) -> str:
    """Render the top-N co-occurring canonical tags as chip links.

    Filters out canonicals whose post count is below ``_LANDING_THRESHOLD``
    — those don't have a landing page, so linking to them would 404 and
    fail the strict-internal link audit."""
    eligible = [
        (other, cnt)
        for other, cnt in cooccur.most_common()
        if len(posts.get(other, [])) >= _LANDING_THRESHOLD
    ][:n]
    if not eligible:
        return ""
    chips = "".join(
        f'<a href="/tags/{other}/" class="related-tag-chip">'
        f'{_esc(taxonomy[other]["name"])} '
        f'<span class="meta">{cnt}</span></a>'
        for other, cnt in eligible
    )
    return (
        f'<nav aria-labelledby="related-tags-h2-{slug}" class="related-tags">'
        f'<h2 id="related-tags-h2-{slug}">Related tags</h2>'
        f'<p>Topics this tag most often appears with.</p>'
        f"<div class=\"related-tags-grid\">{chips}</div>"
        f"</nav>"
    )


def _render_jsonld(
    slug: str,
    entry: dict,
    posts_for_tag: list[tuple[str, str, str, str, list[str], str, str]],
) -> str:
    """CollectionPage + ItemList. Both Schema.org types Google indexes
    for topic pages and AI summarisers consume."""
    import json

    url = f"{_BASE_URL}/tags/{slug}/"
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"{_BASE_URL}/{post_slug}/",
            "name": title,
        }
        for i, (title, _iso, post_slug, *_rest) in enumerate(posts_for_tag)
    ]
    payload = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": url,
                "url": url,
                "name": f'{entry["name"]} — Articles',
                "description": entry["description"].strip(),
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": f"{_BASE_URL}/#website",
                },
            },
            {
                "@type": "ItemList",
                "@id": f"{url}#itemlist",
                "numberOfItems": len(items),
                "itemListElement": items,
            },
        ],
    }
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{body}</script>'


def _render_landing_body(
    slug: str,
    entry: dict,
    posts_for_tag: list[tuple[str, str, str, str, list[str], str, str]],
    cooccur: collections.Counter[str],
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
) -> str:
    n = len(posts_for_tag)
    pillar = entry.get("category", "leadership").upper()
    return (
        f'<div class="wrap report-wrap">'
        f'<header class="tag-landing-hero">'
        f'<p class="eyebrow">{_esc(pillar)}</p>'
        f"<h1>{_esc(entry['name'])}</h1>"
        f'<p class="deck">{_esc(entry["description"].strip())}</p>'
        f'<p class="tag-landing-meta">{n} article{"s" if n != 1 else ""}</p>'
        f"</header>"
        f'<section class="tag-landing-list" aria-label="Articles tagged {_esc(entry["name"])}">'
        f"{_render_article_cards(posts_for_tag)}"
        f"</section>"
        + _render_related_tags(cooccur, taxonomy, slug, posts)
        + "</div>"
    )


_HREFLANG_LINK_RE = re.compile(
    r'(<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href=")([^"]+?)/"',
    re.IGNORECASE,
)


def _append_slug_to_hreflang(html: str, slug: str) -> str:
    """Rewrite every ``<link rel="alternate" hreflang="…" href="…/">`` so
    the URL points at the per-tag landing for ``slug`` rather than the
    cover. The cover template's hreflang chain ends every locale URL
    with the cover path (``/tags/``, ``/fr/etiquettes/``, …) — we just
    append ``<slug>/`` to keep the chain reciprocal across the locale
    forks of each canonical tag."""
    return _HREFLANG_LINK_RE.sub(rf'\g<1>\g<2>/{slug}/"', html)


def _render_landing_html(
    template: str,
    slug: str,
    entry: dict,
    posts_for_tag: list[tuple[str, str, str, str, list[str], str, str]],
    cooccur: collections.Counter[str],
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
) -> str:
    """Take the /tags/index.html cover as the shell skeleton, swap the
    <main> body, title, description, canonical, og:* meta, and inject
    the per-tag JSON-LD before </head>. Hreflang alternates are
    re-pointed at the per-tag landing of each locale so reciprocity
    holds across the 28-locale chain."""
    url = f"{_BASE_URL}/tags/{slug}/"
    title = f'{entry["name"]} — Articles by topic'
    desc = entry["description"].strip()
    body = _render_landing_body(slug, entry, posts_for_tag, cooccur, taxonomy, posts)
    out = template
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{url}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(
        f'<meta property="og:title" content="{_esc(title)}"', out, count=1
    )
    out = _OG_DESC_RE.sub(
        f'<meta property="og:description" content="{_esc(desc)}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{url}"', out, count=1
    )
    out = _append_slug_to_hreflang(out, slug)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    jsonld = _render_jsonld(slug, entry, posts_for_tag)
    out = out.replace("</head>", f"{jsonld}</head>", 1)
    return out


def _load_locale_article_slugs(lang: str) -> dict[str, str]:
    """Return {en-slug: locale-slug} from ``_data/i18n/<lang>/slugs.json``.
    Returns {} when the file is missing — locale forks then keep the
    EN article links rather than 404 silently."""
    import json

    path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    arts = data.get("articles") or {}
    return {k: v for k, v in arts.items() if isinstance(v, str) and v}


def _load_fr_to_en_slug_map(lang: str) -> dict[str, str]:
    """Return ``{locale_slug: en_slug}`` from
    ``_data/i18n/<lang>/slugs.json``. Returns {} on missing/malformed
    file."""
    import json

    slugs_path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    if not slugs_path.is_file():
        return {}
    try:
        data = json.loads(slugs_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {
        locale_slug: en_slug
        for en_slug, locale_slug in (data.get("articles") or {}).items()
        if isinstance(locale_slug, str) and locale_slug
    }


def _locale_post_card_fields(path: Path) -> tuple[str, str, str, str] | None:
    """Extract (stem, title, excerpt, banner) from one locale post.
    Returns None when the post has no `title:` frontmatter."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    title_m = _TITLE_FM_RE.search(text)
    if not title_m:
        return None
    excerpt_m = _EXCERPT_FM_RE.search(text)
    desc_m = _DESC_FM_RE.search(text)
    banner_m = _BANNER_FM_RE.search(text)
    title = title_m.group(1)
    excerpt = (
        excerpt_m.group(1)
        if excerpt_m
        else (desc_m.group(1) if desc_m else "")
    )
    banner = banner_m.group(1) if banner_m else _DEFAULT_BANNER
    return path.stem, title, excerpt, banner


def _load_locale_post_index(lang: str) -> dict[str, tuple[str, str, str, str]]:
    """Return ``{en_slug: (locale_slug, locale_title, locale_excerpt,
    locale_banner)}`` for every dated post in ``_posts/<lang>/``. Same
    contract as build_listings._load_locale_post_index — duplicated
    here to keep build_tag_landings importable without forcing a
    cross-module import. Posts present only in EN fall back to the
    EN card content at render time."""
    src = ROOT / "_posts" / lang
    if not src.is_dir():
        return {}
    fr_to_en = _load_fr_to_en_slug_map(lang)
    out: dict[str, tuple[str, str, str, str]] = {}
    for path in sorted(src.glob("*.md")):
        fields = _locale_post_card_fields(path)
        if fields is None:
            continue
        stem, title, excerpt, banner = fields
        en_slug = fr_to_en.get(stem, stem)
        out[en_slug] = (stem, title, excerpt, banner)
    return out


def _localise_posts_for_tag(
    posts_for_tag: list[tuple[str, str, str, str, list[str], str, str]],
    locale_index: dict[str, tuple[str, str, str, str]],
) -> list[tuple[str, str, str, str, list[str], str, str]]:
    """Return a list with locale-translated title/excerpt/banner where
    the EN slug maps to a locale post; pass-through otherwise."""
    out: list[tuple[str, str, str, str, list[str], str, str]] = []
    for title, iso_date, slug, excerpt, pillars, banner, banner_alt in posts_for_tag:
        entry = locale_index.get(slug)
        if entry is not None:
            _locale_slug, locale_title, locale_excerpt, locale_banner = entry
            title = locale_title
            excerpt = locale_excerpt or excerpt
            banner = locale_banner or banner
        out.append((title, iso_date, slug, excerpt, pillars, banner, banner_alt))
    return out


_LANDING_LIST_SECTION_RE = re.compile(
    r'(<section class="tag-landing-list"[^>]*>)([\s\S]*?)(</section>)',
    re.IGNORECASE,
)


def _swap_landing_cards(
    html: str,
    posts_for_tag: list[tuple[str, str, str, str, list[str], str, str]],
    locale_index: dict[str, tuple[str, str, str, str]],
    article_map: dict[str, str],
    lang: str,
) -> str:
    """Replace the EN card grid inside the per-tag landing's
    ``<section class="tag-landing-list">`` with locale-translated
    cards pointing at ``/<lang>/<locale-slug>/`` URLs."""
    locale_posts = _localise_posts_for_tag(posts_for_tag, locale_index)
    href_overrides = {
        p[2]: f"/{lang}/{article_map.get(p[2], p[2])}/" for p in posts_for_tag
    }
    body = _render_article_cards(locale_posts, href_overrides=href_overrides)
    return _LANDING_LIST_SECTION_RE.sub(rf"\1{body}\3", html, count=1)


_HREFLANG_ARTICLE_RE = re.compile(r'href="/(\d{4}-\d{2}-\d{2}-[^/"]+)/"')
# JSON-LD "inLanguage":"en" / "en-GB" strings sprinkled across the EN
# template. validate_jsonld.py flags them when the <html lang> base
# doesn't match — see the build's JSON-LD validation step. Update in
# place for each locale fork.
_INLANG_RE = re.compile(r'"inLanguage":\s*"(?:en|en-GB|en-US)"')


def _localise_html_links(
    en_html: str,
    lang: str,
    slug: str,
    article_map: dict[str, str],
) -> str:
    """Rewrite the EN landing HTML into one locale variant: <html lang>,
    canonical, og:url, internal article links, related-tag chip hrefs."""
    locale_tags = LOCALE_TAGS_PATH[lang]
    locale_root = f"/{lang}"
    out = en_html
    out = _HTML_LANG_RE.sub(f'<html lang="{lang}"', out, count=1)
    canonical = f"{_BASE_URL}{locale_root}/{locale_tags}/{slug}/"
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{canonical}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{canonical}"', out, count=1
    )
    # Article slug remap — strict {en-slug} matches only so we don't
    # silently rewrite unrelated hrefs.
    def _swap_article(m: re.Match[str]) -> str:
        en_slug = m.group(1)
        locale_slug = article_map.get(en_slug, en_slug)
        return f'href="{locale_root}/{locale_slug}/"'

    out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
    # Related-tag chips: /tags/<canonical>/ → /<lang>/<locale-tags>/<canonical>/
    out = out.replace('href="/tags/', f'href="{locale_root}/{locale_tags}/')
    # Update JSON-LD inLanguage so validate_jsonld doesn't warn.
    out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
    return out


def _translate_chrome_for(lang: str, html: str) -> str:
    """Run the EN shell through ``build_translations.translate_chrome``
    bound to ``lang`` — translates nav, footer, search labels, aria
    attributes, language menu, dates. Keeps the body content (which
    is generator-emitted EN text) untouched. Raises ``RuntimeError`` if
    the package isn't importable so silent EN-chrome leaks don't ship."""
    # Ensure repo root is on sys.path even when this module is invoked
    # as a script (`python3 scripts/generators/build_tag_landings.py`) —
    # otherwise the `scripts.generators...` package path won't resolve
    # and the import would have to fall back to untranslated chrome.
    import sys as _sys
    if str(ROOT) not in _sys.path:
        _sys.path.insert(0, str(ROOT))
    from scripts.generators.build_translations import _state as _bt_state
    from scripts.generators.build_translations._chrome import translate_chrome
    _bt_state.bind_lang(lang)
    return translate_chrome(html)


def _write_locale_landings(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    en_pages: dict[str, str],
) -> int:
    written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    locale_indexes = {lang: _load_locale_post_index(lang) for lang in LOCALES_NON_EN}
    for slug in en_pages:
        if len(posts.get(slug, [])) < _LANDING_THRESHOLD:
            continue
        en_html = en_pages[slug]
        posts_for_tag = posts.get(slug, [])
        for lang in LOCALES_NON_EN:
            locale_html = _localise_html_links(en_html, lang, slug, article_maps[lang])
            locale_html = _swap_landing_cards(
                locale_html, posts_for_tag, locale_indexes[lang],
                article_maps[lang], lang,
            )
            locale_html = _translate_chrome_for(lang, locale_html)
            out_path = (
                PUBLIC / lang / LOCALE_TAGS_PATH[lang] / slug / "index.html"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(locale_html, encoding="utf-8")
            written += 1
    return written


def _render_category_tag_item(
    slug: str,
    entry: dict,
    n: int,
) -> str:
    """One ``<li>`` for the category page's tag list.

    Tags below the landing threshold are listed (with count + deck) but
    not linked — their ``/tags/<slug>/`` page is not emitted, so a link
    would 404 and fail audit_links --strict-internal."""
    meta = f' <span class="meta">— {n} article{"s" if n != 1 else ""}</span>'
    head = f'<strong>{_esc(entry["name"])}</strong>{meta}'
    if n >= _LANDING_THRESHOLD:
        head = f'<a href="/tags/{slug}/">{head}</a>'
    return f"<li>{head}<p>{_esc(entry['description'].strip())}</p></li>"


def _category_recent_posts(
    pillar_slugs: list[str],
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    n: int = 12,
) -> list[tuple[str, str, str, str, list[str], str, str]]:
    """Collect recent posts across every canonical in the pillar,
    dedupe by slug, return the newest ``n``."""
    seen: set[str] = set()
    recent: list[tuple[str, str, str, str, list[str], str, str]] = []
    for slug in pillar_slugs:
        for entry in posts.get(slug, []):
            if entry[2] in seen:
                continue
            seen.add(entry[2])
            recent.append(entry)
    recent.sort(key=lambda p: p[1] or "0000", reverse=True)
    return recent[:n]


def _render_category_body(
    pillar: str,
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
) -> str:
    """Render the body of a /categories/<pillar>/ landing — a hero
    with the pillar deck, the canonical tags belonging to the pillar
    (each linked to /tags/<slug>/ when landing-eligible, with article
    count), and a "recent across this pillar" card list."""
    pillar_slugs = [
        slug for slug, e in taxonomy.items() if e.get("category") == pillar
    ]
    pillar_slugs.sort(key=lambda s: -len(posts.get(s, [])))
    tag_items = [
        _render_category_tag_item(slug, taxonomy[slug], len(posts.get(slug, [])))
        for slug in pillar_slugs
        if len(posts.get(slug, [])) >= 1
    ]
    recent = _category_recent_posts(pillar_slugs, posts)
    return (
        f'<div class="wrap report-wrap">'
        f'<header class="tag-landing-hero">'
        f'<p class="eyebrow">CATEGORY</p>'
        f"<h1>{_esc(PILLAR_LABELS[pillar])}</h1>"
        f'<p class="deck">{_esc(PILLAR_DECKS[pillar])}</p>'
        f'<p class="tag-landing-meta">{len(tag_items)} tags</p>'
        f"</header>"
        f'<section aria-label="Tags under {_esc(PILLAR_LABELS[pillar])}">'
        f'<h2>Tags in this category</h2>'
        f'<ul class="tag-list">' + "".join(tag_items) + "</ul>"
        f"</section>"
        f'<section class="tag-landing-list" aria-label="Recent articles">'
        f'<h2>Recent articles in {_esc(PILLAR_LABELS[pillar])}</h2>'
        f"{_render_article_cards(recent)}"
        f"</section>"
        f"</div>"
    )


def _rewrite_hreflang_to_category(html: str, pillar: str) -> str:
    """Rewrite the cover template's hreflang chain so every locale URL
    points at ``/categories/<pillar>/`` (EN) or ``/<lang>/categories/
    <pillar>/`` (non-EN). The cover template's chain ends with each
    locale's tags-cover path (``/fr/etiquettes/``, ``/ar/wusum/``, …);
    we swap that segment out for the unified ``/categories/<pillar>/``
    pattern so the reciprocity checker can pair every category page
    across the 28-locale matrix."""
    cover_path = f"/categories/{pillar}/"

    def _swap(m: re.Match[str]) -> str:
        prefix, href = m.group(1), m.group(2)
        # Check locale-prefixed forms first (e.g. /ha/tags, /zh-hans/biaoqian)
        # so we don't mistake them for the bare-EN /tags pattern.
        for lang, locale_tags in LOCALE_TAGS_PATH.items():
            tail = f"/{lang}/{locale_tags}"
            if href.endswith(tail):
                return f'{prefix}{_BASE_URL}/{lang}{cover_path}"'
        # Bare EN cover: href ends with /tags (no locale prefix).
        if href.endswith("/tags"):
            return f'{prefix}{_BASE_URL}{cover_path}"'
        return m.group(0)

    return _HREFLANG_LINK_RE.sub(_swap, html)


def _render_category_html(
    template: str,
    pillar: str,
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
) -> str:
    url = f"{_BASE_URL}/categories/{pillar}/"
    title = f"{PILLAR_LABELS[pillar]} — Editorial pillar"
    desc = PILLAR_DECKS[pillar]
    out = template
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", out, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{url}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(
        f'<meta property="og:title" content="{_esc(title)}"', out, count=1
    )
    out = _OG_DESC_RE.sub(
        f'<meta property="og:description" content="{_esc(desc)}"', out, count=1
    )
    out = _OG_URL_RE.sub(
        f'<meta property="og:url" content="{url}"', out, count=1
    )
    out = _rewrite_hreflang_to_category(out, pillar)
    body = _render_category_body(pillar, taxonomy, posts)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    return out


def _write_category_pages(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
) -> tuple[int, int]:
    """Generate /categories/<pillar>/index.html for each of the 6
    pillars + locale forks. Reuses the /tags/index.html cover as a
    template skeleton."""
    if not TEMPLATE_PATH.is_file():
        return 0, 0
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    en_pages: dict[str, tuple[str, list[tuple[str, str, str, str, list[str], str, str]]]] = {}
    for pillar in PILLAR_ORDER:
        page_html = _render_category_html(template, pillar, taxonomy, posts)
        out_path = PUBLIC / "categories" / pillar / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        pillar_slugs = [
            slug for slug, e in taxonomy.items() if e.get("category") == pillar
        ]
        pillar_slugs.sort(key=lambda s: -len(posts.get(s, [])))
        recent = _category_recent_posts(pillar_slugs, posts)
        en_pages[pillar] = (page_html, recent)
    locale_written = _write_category_locale_forks(en_pages)
    return len(en_pages), locale_written


def _write_category_locale_forks(
    en_pages: dict[str, tuple[str, list[tuple[str, str, str, str, list[str], str, str]]]],
) -> int:
    """Same lang/canonical/links rewrite as tag-landing locales. The
    /categories/ path stays English across all locales (no localised
    segment for this round — a future polish can add per-locale
    "catégories" / "categorías" / etc.).

    Cards inside the "Recent articles" rail get re-rendered with
    locale-translated title/excerpt/banner + URL via the per-locale
    post index (frontmatter from ``_posts/<lang>/``)."""
    written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    locale_indexes = {lang: _load_locale_post_index(lang) for lang in LOCALES_NON_EN}
    for pillar, (en_html, recent) in en_pages.items():
        for lang in LOCALES_NON_EN:
            locale_tags = LOCALE_TAGS_PATH[lang]
            out = en_html
            out = _HTML_LANG_RE.sub(f'<html lang="{lang}"', out, count=1)
            canonical = f"{_BASE_URL}/{lang}/categories/{pillar}/"
            out = _CANONICAL_RE.sub(
                f'<link rel="canonical" href="{canonical}"', out, count=1
            )
            out = _OG_URL_RE.sub(
                f'<meta property="og:url" content="{canonical}"', out, count=1
            )
            amap = article_maps[lang]

            def _swap_article(m: re.Match[str], _lang: str = lang, _amap: dict = amap) -> str:
                en_slug = m.group(1)
                return f'href="/{_lang}/{_amap.get(en_slug, en_slug)}/"'

            out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
            out = out.replace('href="/tags/', f'href="/{lang}/{locale_tags}/')
            out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
            out = _swap_landing_cards(out, recent, locale_indexes[lang], amap, lang)
            out = _translate_chrome_for(lang, out)
            out_path = (
                PUBLIC / lang / "categories" / pillar / "index.html"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(out, encoding="utf-8")
            written += 1
    return written


def _write_landings(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str, list[str], str, str]]],
    cooccur: dict[str, collections.Counter[str]],
) -> tuple[int, int]:
    if not TEMPLATE_PATH.is_file():
        print(
            f"build_tag_landings: missing template {TEMPLATE_PATH}",
            file=sys.stderr,
        )
        return 0, 0
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    en_pages: dict[str, str] = {}
    for slug, entry in taxonomy.items():
        ps = posts.get(slug, [])
        if len(ps) < _LANDING_THRESHOLD:
            continue
        page_html = _render_landing_html(
            template, slug, entry, ps,
            cooccur.get(slug, collections.Counter()), taxonomy, posts,
        )
        out_path = PUBLIC / "tags" / slug / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        en_pages[slug] = page_html
    locale_written = _write_locale_landings(taxonomy, posts, en_pages)
    return len(en_pages), locale_written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not TAXONOMY.is_file():
        print(
            f"build_tag_landings: no taxonomy at {TAXONOMY}, skipping",
            file=sys.stderr,
        )
        return 0
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8")) or {}
    posts, cooccur = _walk(taxonomy)
    en_written, locale_written = _write_landings(taxonomy, posts, cooccur)
    cat_en, cat_locale = _write_category_pages(taxonomy, posts)
    print(
        f"build_tag_landings: wrote {en_written} EN tag landing(s) + "
        f"{locale_written} locale fork(s); {cat_en} EN category landing(s) + "
        f"{cat_locale} locale fork(s) "
        f"across {len(LOCALES_NON_EN)} non-EN locales."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
