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
_DATED_SLUG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
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


def _post_meta(path: Path) -> tuple[str, str, str, str, list[str]] | None:
    """Return (title, iso-date, slug, excerpt, [raw tag strings]) or None."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    tags_m = _TAG_FM_RE.search(text)
    if not tags_m:
        return None
    title_m = _TITLE_FM_RE.search(text)
    title = title_m.group(1) if title_m else path.stem
    excerpt_m = _EXCERPT_FM_RE.search(text)
    excerpt = excerpt_m.group(1) if excerpt_m else ""
    stem_m = _DATED_SLUG_RE.match(path.stem)
    iso_date = stem_m.group(1) if stem_m else ""
    raw_tags = [t.strip().strip('"').strip("'").strip() for t in tags_m.group(1).split(",")]
    return title, iso_date, path.stem, excerpt, [t for t in raw_tags if t]


def _canonical_set(raw_tags: list[str], amap: dict[str, str]) -> set[str]:
    """Resolve a post's raw tag strings to a deduplicated set of
    canonical slugs via the alias map."""
    return {amap[r.lower()] for r in raw_tags if r.lower() in amap}


def _ingest_post(
    path: Path,
    amap: dict[str, str],
    posts: dict[str, list[tuple[str, str, str, str]]],
    cooccur: dict[str, collections.Counter[str]],
) -> None:
    meta = _post_meta(path)
    if not meta:
        return
    title, iso_date, slug, excerpt, raw_tags = meta
    canons = _canonical_set(raw_tags, amap)
    for c in canons:
        posts[c].append((title, iso_date, slug, excerpt))
        for other in canons - {c}:
            cooccur[c][other] += 1


def _walk(taxonomy: dict) -> tuple[
    dict[str, list[tuple[str, str, str, str]]],
    dict[str, collections.Counter[str]],
]:
    """Return:
    * per-canonical [(title, iso-date, slug, excerpt), ...] newest first
    * per-canonical Counter of OTHER canonicals that co-occur on the
      same posts — drives the "related tags" sidebar.
    """
    amap = _alias_map(taxonomy)
    posts: dict[str, list[tuple[str, str, str, str]]] = collections.defaultdict(list)
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
        _ingest_post(path, amap, posts, cooccur)
    for c in posts:
        posts[c].sort(key=lambda p: p[1] or "0000", reverse=True)
    return posts, cooccur


def _render_article_cards(posts_for_tag: list[tuple[str, str, str, str]]) -> str:
    cards = []
    for title, iso_date, slug, excerpt in posts_for_tag:
        date_html = (
            f'<time datetime="{iso_date}" class="card-date">{iso_date}</time>'
            if iso_date
            else ""
        )
        excerpt_html = (
            f'<p class="card-excerpt">{_esc(excerpt)}</p>' if excerpt else ""
        )
        cards.append(
            f'<article class="tag-landing-card">'
            f'<h2><a href="/{slug}/">{_esc(title)}</a></h2>'
            f"{date_html}"
            f"{excerpt_html}"
            f"</article>"
        )
    return "".join(cards)


def _render_related_tags(
    cooccur: collections.Counter[str],
    taxonomy: dict,
    slug: str,
    posts: dict[str, list[tuple[str, str, str, str]]],
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
    posts_for_tag: list[tuple[str, str, str, str]],
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
        for i, (title, _iso, post_slug, _ex) in enumerate(posts_for_tag)
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
    posts_for_tag: list[tuple[str, str, str, str]],
    cooccur: collections.Counter[str],
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str]]],
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


def _render_landing_html(
    template: str,
    slug: str,
    entry: dict,
    posts_for_tag: list[tuple[str, str, str, str]],
    cooccur: collections.Counter[str],
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str]]],
) -> str:
    """Take the /tags/index.html cover as the shell skeleton, swap the
    <main> body, title, description, canonical, og:* meta, and inject
    the per-tag JSON-LD before </head>."""
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
    posts: dict[str, list[tuple[str, str, str, str]]],
    en_pages: dict[str, str],
) -> int:
    written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    for slug in en_pages:
        if len(posts.get(slug, [])) < _LANDING_THRESHOLD:
            continue
        en_html = en_pages[slug]
        for lang in LOCALES_NON_EN:
            locale_html = _localise_html_links(en_html, lang, slug, article_maps[lang])
            locale_html = _translate_chrome_for(lang, locale_html)
            out_path = (
                PUBLIC / lang / LOCALE_TAGS_PATH[lang] / slug / "index.html"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(locale_html, encoding="utf-8")
            written += 1
    return written


def _render_category_body(
    pillar: str,
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str]]],
) -> str:
    """Render the body of a /categories/<pillar>/ landing — a hero
    with the pillar deck, the canonical tags belonging to the pillar
    (each linked to /tags/<slug>/, with article count), and a
    "recent across this pillar" card list."""
    pillar_slugs = [
        slug for slug, e in taxonomy.items() if e.get("category") == pillar
    ]
    pillar_slugs.sort(key=lambda s: -len(posts.get(s, [])))
    tag_items = []
    for slug in pillar_slugs:
        n = len(posts.get(slug, []))
        if n < 1:
            continue
        entry = taxonomy[slug]
        meta = (
            f' <span class="meta">— {n} article{"s" if n != 1 else ""}</span>'
        )
        head = f'<strong>{_esc(entry["name"])}</strong>{meta}'
        # Tags below the landing threshold are listed (with count + deck)
        # but not linked — their `/tags/<slug>/` page is not emitted, so
        # the link would 404 and fail audit_links --strict-internal.
        if n >= _LANDING_THRESHOLD:
            head = f'<a href="/tags/{slug}/">{head}</a>'
        tag_items.append(
            f"<li>{head}<p>{_esc(entry['description'].strip())}</p></li>"
        )
    # Cross-pillar recent posts: collect unique recent posts that
    # touch any canonical in this pillar, dedupe by slug, newest first.
    seen: set[str] = set()
    recent: list[tuple[str, str, str, str]] = []
    for slug in pillar_slugs:
        for entry in posts.get(slug, []):
            if entry[2] in seen:
                continue
            seen.add(entry[2])
            recent.append(entry)
    recent.sort(key=lambda p: p[1] or "0000", reverse=True)
    recent = recent[:12]
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


def _render_category_html(
    template: str,
    pillar: str,
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str]]],
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
    body = _render_category_body(pillar, taxonomy, posts)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_RE.sub(rf"\1{body}\3", out, count=1)
    return out


def _write_category_pages(
    taxonomy: dict,
    posts: dict[str, list[tuple[str, str, str, str]]],
) -> tuple[int, int]:
    """Generate /categories/<pillar>/index.html for each of the 6
    pillars + locale forks. Reuses the /tags/index.html cover as a
    template skeleton."""
    if not TEMPLATE_PATH.is_file():
        return 0, 0
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    en_pages: dict[str, str] = {}
    for pillar in PILLAR_ORDER:
        page_html = _render_category_html(template, pillar, taxonomy, posts)
        out_path = PUBLIC / "categories" / pillar / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page_html, encoding="utf-8")
        en_pages[pillar] = page_html
    locale_written = _write_category_locale_forks(en_pages)
    return len(en_pages), locale_written


def _write_category_locale_forks(en_pages: dict[str, str]) -> int:
    """Same lang/canonical/links rewrite as tag-landing locales. The
    /categories/ path stays English across all locales (no localised
    segment for this round — a future polish can add per-locale
    "catégories" / "categorías" / etc.)."""
    written = 0
    article_maps = {lang: _load_locale_article_slugs(lang) for lang in LOCALES_NON_EN}
    for pillar, en_html in en_pages.items():
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
            # Article links + tags → locale variants.
            amap = article_maps[lang]

            def _swap_article(m: re.Match[str], _lang: str = lang, _amap: dict = amap) -> str:
                en_slug = m.group(1)
                return f'href="/{_lang}/{_amap.get(en_slug, en_slug)}/"'

            out = _HREFLANG_ARTICLE_RE.sub(_swap_article, out)
            out = out.replace('href="/tags/', f'href="/{lang}/{locale_tags}/')
            out = _INLANG_RE.sub(f'"inLanguage":"{lang}"', out)
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
    posts: dict[str, list[tuple[str, str, str, str]]],
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
