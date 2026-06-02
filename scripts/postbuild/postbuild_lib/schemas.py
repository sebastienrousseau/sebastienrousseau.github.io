"""Additional Schema.org JSON-LD passes — TechArticle / ScholarlyArticle
+ SoftwareSourceCode.

The site already emits BlogPosting for every dated article and an ItemList
for /articles/, /papers/, /projects/. This module layers two more types:

* :func:`inject_tech_article` — adds a richer Article subtype block on
  every dated post. The type is chosen at runtime:

  - **ScholarlyArticle** when the article cites at least
    :data:`SCHOLARLY_CITATION_THRESHOLD` distinct primary-source
    authorities (NIST, ISO, BIS, IETF, …). Carries the citation array
    natively so AI engines walking the JSON-LD see a peer-reviewable
    document graph.
  - **TechArticle** otherwise. Carries ``programmingLanguage`` and
    ``dependencies`` when the keyword set names them.

  Both inherit from ``Article`` and AI Overview / Google Search pick
  the more specific subtype when present. The existing BlogPosting
  block remains untouched so the postbuild gates (``article_furniture``,
  ``seo``, ``build_translations``) keep matching their substrings.

* :func:`inject_software_source_code` — for /projects/index.html only,
  replaces the plain ListItem entries (already injected by
  postbuild.inject_itemlist) with ``SoftwareSourceCode``-typed items
  carrying ``programmingLanguage``, ``codeRepository``, and
  ``applicationCategory``. Parses the rendered card markup —
  no separate source-of-truth maintenance.

Both functions are pure ``(html) -> html``. Insertion happens before
``</body>`` so the existing CSP-hash pass in postbuild captures the
new blocks.
"""
from __future__ import annotations

import datetime as _dt
import html as _html
import json as _json
import re
from pathlib import Path

PUBLIC = Path("public")
SITE = "https://sebastienrousseau.com"


# ---------------------------------------------------------------------------
# TechArticle — adds a richer Article subtype on technical posts.
# ---------------------------------------------------------------------------

# Map keyword tokens (lowercased) → programming language label.
_LANG_TOKENS: dict[str, str] = {
    "rust": "Rust",
    "python": "Python",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "go": "Go",
    "wasm": "WebAssembly",
    "webassembly": "WebAssembly",
    "solidity": "Solidity",
}

# Keyword tokens → domain dependency label that goes into
# TechArticle.dependencies (a free-text list per schema.org).
_DEP_TOKENS: dict[str, str] = {
    "iso 20022":          "ISO 20022",
    "pain.001":           "ISO 20022 pain.001",
    "pacs.008":           "ISO 20022 pacs.008",
    "post-quantum":       "Post-Quantum Cryptography",
    "post quantum":       "Post-Quantum Cryptography",
    "pqc":                "Post-Quantum Cryptography",
    "crystals-kyber":     "CRYSTALS-Kyber (NIST FIPS 203)",
    "kyber":              "CRYSTALS-Kyber",
    "nist":               "NIST",
    "fips 203":           "NIST FIPS 203",
    "swift gpi":          "SWIFT gpi",
    "sepa":               "SEPA Instant Payments",
    "blockchain":         "Blockchain",
    "ethereum":           "Ethereum",
    "erc-20":             "ERC-20",
    "stablecoin":         "Stablecoin",
}

_keywords_meta_re = re.compile(
    r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_title_re = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
_canonical_re = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_html_lang_re = re.compile(r'<html\b[^>]*\blang=["\']?([a-zA-Z-]+)', re.IGNORECASE)
_dated_stem_re = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def _parse_keywords(html: str) -> list[str]:
    m = _keywords_meta_re.search(html)
    if not m:
        return []
    raw = _html.unescape(m.group(1))
    return [k.strip() for k in raw.split(",") if k.strip()]


def _detect_languages(keywords_lower: str) -> list[str]:
    seen: list[str] = []
    for token, label in _LANG_TOKENS.items():
        if (
            re.search(rf"(?<![A-Za-z]){re.escape(token)}(?![A-Za-z])", keywords_lower)
            and label not in seen
        ):
            seen.append(label)
    return seen


def _detect_dependencies(keywords_lower: str) -> list[str]:
    seen: list[str] = []
    for token, label in _DEP_TOKENS.items():
        if token in keywords_lower and label not in seen:
            seen.append(label)
    return seen


def _is_dated_article(page: Path) -> bool:
    """Dated post pages live at ``public/YYYY-MM-DD-slug/index.html`` for
    English; localized copies live at ``public/<lang>/YYYY-MM-DD-slug/``.
    We accept both — the URL we report comes from <link rel="canonical">.
    """
    parts = page.relative_to(PUBLIC).parts
    if not parts or parts[-1] != "index.html":
        return False
    parent = parts[-2] if len(parts) >= 2 else ""
    return bool(_dated_stem_re.match(parent))


def _page_lang(html: str) -> str:
    m = _html_lang_re.search(html)
    return (m.group(1) if m else "en-GB")


# A page with at least this many distinct primary-source citations
# (NIST / ISO / BIS / IETF / …) earns the ScholarlyArticle subtype.
# Below the threshold we still emit TechArticle. Six is the heuristic
# used by the BIS Working Paper style sheet — fewer than six and the
# piece reads as commentary; six or more and it reads as research.
SCHOLARLY_CITATION_THRESHOLD = 6

# Google News Top Stories carousel admits articles published within
# the last 48 hours. Above this cutoff a NewsArticle block has no
# practical effect — the article is still discoverable via TechArticle
# / ScholarlyArticle / BlogPosting, but the carousel slot has passed.
NEWS_FRESHNESS_HOURS = 48


_blogposting_dates_re = re.compile(
    r'"datePublished":"([^"]+)"[^"]*"dateModified":"([^"]+)"',
)
_blogposting_image_re = re.compile(
    r'"@type":"BlogPosting"[\s\S]*?'
    r'"image":\{[^{}]*?"url":"([^"]+)"',
)
_blogposting_section_re = re.compile(
    r'"@type":"BlogPosting"[\s\S]*?"articleSection":"([^"]+)"',
)


def _parse_iso_date(s: str) -> _dt.datetime | None:
    """Liberal ISO 8601 parser. Accepts ``YYYY-MM-DD``, full timestamps
    with ``+HH:MM`` offsets, and the ``Z`` shorthand. Returns a
    timezone-aware datetime or None."""
    s = s.strip().replace("Z", "+00:00")
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M%z",
        "%Y-%m-%d",
    ):
        try:
            dt = _dt.datetime.strptime(s, fmt)
        except ValueError:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=_dt.UTC)
        return dt
    return None


def _is_fresh_for_news(
    date_pub: str, now: _dt.datetime,
) -> bool:
    """True iff ``date_pub`` is within :data:`NEWS_FRESHNESS_HOURS` of ``now``.

    Posts older than the window stay indexed via TechArticle /
    ScholarlyArticle / BlogPosting; we just stop emitting the NewsArticle
    carousel signal because Google News won't slot it anyway."""
    parsed = _parse_iso_date(date_pub)
    if parsed is None:
        return False
    delta = now - parsed
    return _dt.timedelta(0) <= delta <= _dt.timedelta(hours=NEWS_FRESHNESS_HOURS)


def _tech_payload(
    languages: list[str], dependencies: list[str],
) -> dict[str, object]:
    """TechArticle-specific developer hints."""
    payload: dict[str, object] = {"proficiencyLevel": "Expert"}
    if languages:
        payload["programmingLanguage"] = (
            languages if len(languages) > 1 else languages[0]
        )
    if dependencies:
        payload["dependencies"] = dependencies
    return payload


def _detect_kw_signals(html: str) -> tuple[list[str], list[str], list[str]]:
    """Return (keywords, languages, dependencies) for the page."""
    keywords = _parse_keywords(html)
    if not keywords:
        return [], [], []
    kw_lower = ", ".join(keywords).lower()
    return keywords, _detect_languages(kw_lower), _detect_dependencies(kw_lower)


def _tech_article_graph(
    html: str, page: Path,
) -> dict[str, object] | None:
    """Build the richer Article-subtype JSON-LD payload for a dated post.

    Returns ``None`` only when the page is missing the structural anchors
    we need (title, canonical URL). For every other dated post the
    function returns:

    * ``ScholarlyArticle`` when the rendered body cites
      ``SCHOLARLY_CITATION_THRESHOLD`` or more distinct authority-domain
      URLs (the same set ``inject_citations`` writes into BlogPosting).
      The citation array is duplicated into the new block so AI engines
      and academic-graph crawlers walking just the ScholarlyArticle node
      still see the full provenance chain.
    * ``TechArticle`` otherwise — with ``programmingLanguage`` and
      ``dependencies`` populated when the keyword set names them.
    """
    title_m = _title_re.search(html)
    canon_m = _canonical_re.search(html)
    if not title_m or not canon_m:
        return None

    # Late import to avoid a circular at module load — article_furniture
    # already imports from postbuild_lib.seo, so going the other way
    # via top-level import would close the loop.
    from postbuild_lib.article_furniture import _extract_citations
    citations = _extract_citations(html)
    is_scholarly = len(citations) >= SCHOLARLY_CITATION_THRESHOLD
    keywords, languages, dependencies = _detect_kw_signals(html)

    headline = _html.unescape(title_m.group(1)).split(" — ")[0].strip()
    url = _html.unescape(canon_m.group(1))
    graph: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle" if is_scholarly else "TechArticle",
        "headline": headline,
        "url": url,
        "inLanguage": _page_lang(html),
        "isAccessibleForFree": True,
        "author": {"@id": "https://sebastienrousseau.com/#person"},
        "publisher": {"@id": "https://sebastienrousseau.com/#organization"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }
    if keywords:
        graph["keywords"] = ", ".join(keywords)
    if is_scholarly:
        graph["citation"] = citations
    else:
        graph.update(_tech_payload(languages, dependencies))
    return graph


def inject_tech_article(page: Path, html: str) -> str:
    """Add a TechArticle (or ScholarlyArticle, when citation-heavy)
    JSON-LD block to every dated post page. Idempotent — skipped if a
    TechArticle or ScholarlyArticle block already exists on the page,
    or if the page isn't a dated post."""
    if not _is_dated_article(page):
        return html
    if (
        '"@type":"TechArticle"' in html or '"@type": "TechArticle"' in html
        or '"@type":"ScholarlyArticle"' in html
        or '"@type": "ScholarlyArticle"' in html
    ):
        return html
    graph = _tech_article_graph(html, page)
    if graph is None:
        return html
    payload = _json.dumps(graph, separators=(",", ":"), ensure_ascii=False)
    block = f'<script type="application/ld+json">{payload}</script>'
    return re.sub(r"(?i)</body>", block + "</body>", html, count=1)


# ---------------------------------------------------------------------------
# NewsArticle — Google News Top Stories carousel signal for fresh posts.
# ---------------------------------------------------------------------------


def _news_article_graph(
    html: str, page: Path, now: _dt.datetime,
) -> dict[str, object] | None:
    """Build the NewsArticle JSON-LD payload, or return None when the
    page isn't a fresh dated post.

    Reads the canonical URL, headline, datePublished + dateModified,
    keywords, articleSection, and banner image URL from the existing
    BlogPosting graph the SSG already emits, then re-shapes them into
    a Google-News-spec-compliant NewsArticle node with author /
    publisher refs pointing at the identity graph #person and
    #organization @ids.
    """
    canon_m = _canonical_re.search(html)
    title_m = _title_re.search(html)
    dates_m = _blogposting_dates_re.search(html)
    if not canon_m or not title_m or not dates_m:
        return None
    date_pub, date_mod = dates_m.group(1), dates_m.group(2)
    if not _is_fresh_for_news(date_pub, now):
        return None

    headline = _html.unescape(title_m.group(1)).split(" — ")[0].strip()
    url = _html.unescape(canon_m.group(1))
    graph: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": headline,
        "url": url,
        "datePublished": date_pub,
        "dateModified": date_mod,
        "inLanguage": _page_lang(html),
        "isAccessibleForFree": True,
        "author": [{"@id": "https://sebastienrousseau.com/#person"}],
        "publisher": {"@id": "https://sebastienrousseau.com/#organization"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [
                ".post-lead", ".post-lead-tldr", ".post-lead-takeaways",
            ],
        },
    }
    image_m = _blogposting_image_re.search(html)
    if image_m:
        graph["image"] = [_html.unescape(image_m.group(1))]
    section_m = _blogposting_section_re.search(html)
    if section_m:
        graph["articleSection"] = _html.unescape(section_m.group(1))
    keywords, *_ = _detect_kw_signals(html)
    if keywords:
        graph["keywords"] = ", ".join(keywords)
    return graph


def inject_news_article(
    page: Path, html: str, now: _dt.datetime | None = None,
) -> str:
    """Add a NewsArticle JSON-LD block to dated post pages published
    within the Google News Top Stories carousel window.

    Skipped when:
      - the page isn't a dated post,
      - the article is older than :data:`NEWS_FRESHNESS_HOURS`,
      - a NewsArticle block already exists on the page (idempotent),
      - the page lacks a canonical URL, title, or BlogPosting graph
        (no source to project from).

    ``now`` defaults to the wall-clock time; tests pass a fixed value
    so the freshness check is deterministic.
    """
    if not _is_dated_article(page):
        return html
    if '"@type":"NewsArticle"' in html or '"@type": "NewsArticle"' in html:
        return html
    if now is None:
        now = _dt.datetime.now(_dt.UTC)
    graph = _news_article_graph(html, page, now)
    if graph is None:
        return html
    payload = _json.dumps(graph, separators=(",", ":"), ensure_ascii=False)
    block = f'<script type="application/ld+json">{payload}</script>'
    return re.sub(r"(?i)</body>", block + "</body>", html, count=1)


# ---------------------------------------------------------------------------
# SoftwareSourceCode — projects listing only.
# ---------------------------------------------------------------------------

_card_re = re.compile(
    r'<article\b[^>]*\bclass="([^"]*newsroom-card[^"]*)"[^>]*>([\s\S]*?)</article>',
    re.IGNORECASE,
)
_eyebrow_re = re.compile(
    r'<span\b[^>]*class="newsroom-eyebrow"[^>]*>([^<]+)</span>',
    re.IGNORECASE,
)
_h3_link_re = re.compile(
    r'<h3>\s*<a\b[^>]*\bhref="([^"]+)"[^>]*>([\s\S]*?)</a>',
    re.IGNORECASE,
)
_excerpt_re = re.compile(
    r'<p\b[^>]*class="newsroom-excerpt"[^>]*>([\s\S]*?)</p>',
    re.IGNORECASE,
)
_strip_tags_re = re.compile(r"<[^>]+>")
_ws_re = re.compile(r"\s+")
_section_re = re.compile(
    r'<h2\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)</h2>([\s\S]*?)'
    r'(?=<h2\b[^>]*\bid=|</main>)',
    re.IGNORECASE,
)


def _strip(s: str) -> str:
    return _ws_re.sub(" ", _strip_tags_re.sub("", s)).strip()


def _category_label(section_title: str) -> str:
    """Coarse mapping from a /projects/ section heading to a Schema.org
    applicationCategory value. Keep these short — they're consumed by
    AI agents, not displayed to humans."""
    t = section_title.lower()
    if "payment" in t:
        return "Finance — Payments"
    if "quantum" in t or "pqc" in t:
        return "Cryptography — Post-Quantum"
    if "ai" in t:
        return "Artificial Intelligence"
    if "rust" in t:
        return "Developer Tools — Rust"
    if "web" in t or "css" in t:
        return "Developer Tools — Web"
    return "Software Library"


def _languages_from_eyebrow(eyebrow_text: str) -> list[str]:
    """The eyebrow has the shape ``Featured · Python · ISO 20022``. Split
    on '·' and pick tokens that match the language vocabulary. ``go`` is
    too generic — only an exact match counts; other keys accept substring
    so eyebrow ``JS`` matches the canonical ``JavaScript`` label."""
    languages: list[str] = []
    for tok in (t.strip() for t in eyebrow_text.split("·")):
        lc = tok.lower()
        for k, label in _LANG_TOKENS.items():
            if (k == lc or (k != "go" and k in lc)) and label not in languages:
                languages.append(label)
    return languages


def _parse_card(card_body: str) -> tuple[str, str, str, list[str]] | None:
    """Return ``(name, href, description, languages)`` for one project card,
    or None if the card lacks a title+href."""
    h3 = _h3_link_re.search(card_body)
    if not h3:
        return None
    name = _strip(h3.group(2))
    if not name:
        return None
    href = _html.unescape(h3.group(1))
    eyebrow = _eyebrow_re.search(card_body)
    eyebrow_text = _strip(eyebrow.group(1)) if eyebrow else ""
    excerpt = _excerpt_re.search(card_body)
    description = _strip(excerpt.group(1)) if excerpt else ""
    return name, href, description, _languages_from_eyebrow(eyebrow_text)


def _build_software_source_code(
    card_body: str, section_title: str, position: int,
) -> dict[str, object] | None:
    parsed = _parse_card(card_body)
    if parsed is None:
        return None
    name, href, description, languages = parsed
    if href.startswith("/"):
        href = SITE + href
    record: dict[str, object] = {
        "@type": "SoftwareSourceCode",
        "position": position,
        "name": name,
        "url": href,
        "applicationCategory": _category_label(section_title),
    }
    if description:
        record["description"] = description
    if languages:
        record["programmingLanguage"] = (
            languages if len(languages) > 1 else languages[0]
        )
    if "github.com/sebastienrousseau/" in href:
        record["codeRepository"] = href
    elif href.startswith("https://") and "github" not in href:
        # Project sites (pain001.com, kyberlib.com, …) — link the
        # canonical sebastienrousseau GitHub org as the repo holder.
        slug = name.lower().replace(" ", "-")
        record["codeRepository"] = f"https://github.com/sebastienrousseau/{slug}"
    record["author"] = {
        "@type": "Person",
        "name": "Sebastien Rousseau",
        "url": f"{SITE}/about/index.html",
    }
    return record


def _collect_cards_by_section(html: str) -> list[dict[str, object]]:
    """Walk every <section> chunk and apply its category to each card.
    Returns the records in document order with ``position`` already set."""
    items: list[dict[str, object]] = []
    position = 0
    for section_m in _section_re.finditer(html):
        section_title = _strip(section_m.group(2))
        for card_m in _card_re.finditer(section_m.group(3)):
            position += 1
            rec = _build_software_source_code(card_m.group(2), section_title, position)
            if rec is not None:
                items.append(rec)
    return items


def _collect_cards_flat(html: str) -> list[dict[str, object]]:
    """Fallback for pages without ``<section><h2 id=…>`` structure. Walk
    every card with the generic ``Software Library`` category."""
    items: list[dict[str, object]] = []
    for position, card_m in enumerate(_card_re.finditer(html), start=1):
        rec = _build_software_source_code(card_m.group(2), "", position)
        if rec is not None:
            items.append(rec)
    return items


def build_projects_source_code(html: str) -> str | None:
    """Walk /projects/ markup section-by-section. Each
    ``<section><h2 id=…>category</h2>…cards…</section>`` chunk feeds
    its cards into one batch with the section's applicationCategory.
    Falls back to a flat scan when no sectioning is present."""
    items = _collect_cards_by_section(html) or _collect_cards_flat(html)
    if not items:
        return None
    graph = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "url": f"{SITE}/projects/",
        "name": "Open-source projects by Sebastien Rousseau",
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": rec["position"],
                # `name` is required on ListItem itself by the Schema.org
                # validator — we mirror the inner item's name on the
                # ListItem so both the wrapper and `item` carry it.
                "name": rec["name"],
                "item": {k: v for k, v in rec.items() if k != "position"},
            }
            for rec in items
        ],
    }
    return _json.dumps(graph, separators=(",", ":"), ensure_ascii=False)


def inject_software_source_code(page: Path, html: str) -> str:
    """Emit a SoftwareSourceCode-typed ItemList on /projects/index.html.

    Does NOT replace the existing plain ItemList that inject_itemlist
    already emits — the two are complementary (one is generic page-card
    enumeration, the other is the rich software graph). Search engines
    pick the more specific type.
    """
    rel = page.relative_to(PUBLIC).as_posix()
    if rel != "projects/index.html":
        return html
    payload = build_projects_source_code(html)
    if payload is None:
        return html
    block = f'<script type="application/ld+json">{payload}</script>'
    return re.sub(r"(?i)</body>", block + "</body>", html, count=1)
