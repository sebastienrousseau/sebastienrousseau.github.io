"""Tag/category landing rendering (leaf): landing + category HTML, article
cards, related tags, JSON-LD, hreflang rewriting, and locale card localisation.

Split from build_tag_landings (Phase 4.1). Imports shared frontmatter constants
from listing_common, share glyphs from _svg_icons, and stdlib only —
build_tag_landings imports the render entry points + shared constants back
(one-directional, no cycle).
"""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from _svg_icons import (
    _CARD_SVG_EMAIL,
    _CARD_SVG_FB,
    _CARD_SVG_LI,
    _CARD_SVG_LINK,
    _CARD_SVG_WA,
    _CARD_SVG_X,
)
from listing_common import (
    _BANNER_FM_RE,
    _DEFAULT_BANNER,
    _DESC_FM_RE,
    _EXCERPT_FM_RE,
    _TITLE_FM_RE,
    _strip_fm_quotes,
)

ROOT = Path(__file__).resolve().parents[2]

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
_LANDING_THRESHOLD = 3
_BASE_URL = "https://sebastienrousseau.com"
_MAIN_RE = re.compile(
    r"(<main\b[^>]*>)([\s\S]*?)(</main>)",
    re.IGNORECASE,
)
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(r'<meta name="description" content="[^"]*"', re.IGNORECASE)
_CANONICAL_RE = re.compile(r'<link rel="canonical" href="[^"]*"', re.IGNORECASE)
_OG_TITLE_RE = re.compile(r'<meta property="og:title" content="[^"]*"', re.IGNORECASE)
_OG_DESC_RE = re.compile(r'<meta property="og:description" content="[^"]*"', re.IGNORECASE)
_OG_URL_RE = re.compile(r'<meta property="og:url" content="[^"]*"', re.IGNORECASE)
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
        eyebrow_label = eyebrow_override or (PILLAR_LABELS[pillars[0]] if pillars else "Editorial")
        eyebrow_html = f'<p class="eyebrow card-eyebrow">{_esc(eyebrow_label).upper()}</p>'
        date_html = (
            f'<time datetime="{iso_date}" class="card-date">{iso_date}</time>' if iso_date else ""
        )
        excerpt_html = f'<p class="card-excerpt">{_esc(excerpt)}</p>' if excerpt else ""
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
    # `most_common()` breaks ties by INSERTION order, and the counter is built
    # by iterating a set — whose order Python randomises per process. Tied
    # co-occurrence counts are the common case, so the chips came out in a
    # different order on every build and the page was not reproducible.
    # Sorting by (-count, slug) is a total order over distinct slugs, so the
    # result no longer depends on how the counter was populated.
    eligible = [
        (other, cnt)
        for other, cnt in sorted(cooccur.items(), key=lambda kv: (-kv[1], kv[0]))
        if len(posts.get(other, [])) >= _LANDING_THRESHOLD
    ][:n]
    if not eligible:
        return ""
    chips = "".join(
        f'<a href="/tags/{other}/" class="related-tag-chip">'
        f"{_esc(taxonomy[other]['name'])} "
        f'<span class="meta">{cnt}</span></a>'
        for other, cnt in eligible
    )
    return (
        f'<nav aria-labelledby="related-tags-h2-{slug}" class="related-tags">'
        f'<h2 id="related-tags-h2-{slug}">Related tags</h2>'
        f"<p>Topics this tag most often appears with.</p>"
        f'<div class="related-tags-grid">{chips}</div>'
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
                "name": f"{entry['name']} — Articles",
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
        f"</section>" + _render_related_tags(cooccur, taxonomy, slug, posts) + "</div>"
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
    title = f"{entry['name']} — Articles by topic"
    desc = entry["description"].strip()
    body = _render_landing_body(slug, entry, posts_for_tag, cooccur, taxonomy, posts)
    out = template
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", out, count=1)
    out = _DESC_RE.sub(f'<meta name="description" content="{_esc(desc)}"', out, count=1)
    out = _CANONICAL_RE.sub(f'<link rel="canonical" href="{url}"', out, count=1)
    out = _OG_TITLE_RE.sub(f'<meta property="og:title" content="{_esc(title)}"', out, count=1)
    out = _OG_DESC_RE.sub(f'<meta property="og:description" content="{_esc(desc)}"', out, count=1)
    out = _OG_URL_RE.sub(f'<meta property="og:url" content="{url}"', out, count=1)
    out = _append_slug_to_hreflang(out, slug)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    jsonld = _render_jsonld(slug, entry, posts_for_tag)
    out = out.replace("</head>", f"{jsonld}</head>", 1)
    return out


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
    title = _strip_fm_quotes(title_m.group(1))
    excerpt = _strip_fm_quotes(
        excerpt_m.group(1) if excerpt_m else (desc_m.group(1) if desc_m else "")
    )
    banner = _strip_fm_quotes(banner_m.group(1)) if banner_m else _DEFAULT_BANNER
    return path.stem, title, excerpt, banner


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
    href_overrides = {p[2]: f"/{lang}/{article_map.get(p[2], p[2])}/" for p in posts_for_tag}
    body = _render_article_cards(locale_posts, href_overrides=href_overrides)
    return _LANDING_LIST_SECTION_RE.sub(rf"\1{body}\3", html, count=1)


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
    head = f"<strong>{_esc(entry['name'])}</strong>{meta}"
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
    pillar_slugs = [slug for slug, e in taxonomy.items() if e.get("category") == pillar]
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
        f"<h2>Tags in this category</h2>"
        f'<ul class="tag-list">' + "".join(tag_items) + "</ul>"
        f"</section>"
        f'<section class="tag-landing-list" aria-label="Recent articles">'
        f"<h2>Recent articles in {_esc(PILLAR_LABELS[pillar])}</h2>"
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
    out = _DESC_RE.sub(f'<meta name="description" content="{_esc(desc)}"', out, count=1)
    out = _CANONICAL_RE.sub(f'<link rel="canonical" href="{url}"', out, count=1)
    out = _OG_TITLE_RE.sub(f'<meta property="og:title" content="{_esc(title)}"', out, count=1)
    out = _OG_DESC_RE.sub(f'<meta property="og:description" content="{_esc(desc)}"', out, count=1)
    out = _OG_URL_RE.sub(f'<meta property="og:url" content="{url}"', out, count=1)
    out = _rewrite_hreflang_to_category(out, pillar)
    body = _render_category_body(pillar, taxonomy, posts)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    return out
