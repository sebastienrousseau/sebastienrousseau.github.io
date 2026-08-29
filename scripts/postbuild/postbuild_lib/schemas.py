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
    "iso 20022": "ISO 20022",
    "pain.001": "ISO 20022 pain.001",
    "pacs.008": "ISO 20022 pacs.008",
    "post-quantum": "Post-Quantum Cryptography",
    "post quantum": "Post-Quantum Cryptography",
    "pqc": "Post-Quantum Cryptography",
    "crystals-kyber": "CRYSTALS-Kyber (NIST FIPS 203)",
    "kyber": "CRYSTALS-Kyber",
    "nist": "NIST",
    "fips 203": "NIST FIPS 203",
    "swift gpi": "SWIFT gpi",
    "sepa": "SEPA Instant Payments",
    "blockchain": "Blockchain",
    "ethereum": "Ethereum",
    "erc-20": "ERC-20",
    "stablecoin": "Stablecoin",
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
    return m.group(1) if m else "en-GB"


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
    r'"@type":"BlogPosting"[\s\S]*?' r'"image":\{[^{}]*?"url":"([^"]+)"',
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
    date_pub: str,
    now: _dt.datetime,
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
    languages: list[str],
    dependencies: list[str],
) -> dict[str, object]:
    """TechArticle-specific developer hints."""
    payload: dict[str, object] = {"proficiencyLevel": "Expert"}
    if languages:
        payload["programmingLanguage"] = languages if len(languages) > 1 else languages[0]
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
    html: str,
    page: Path,
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
    from postbuild_lib.citations import _extract_citations

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
        '"@type":"TechArticle"' in html
        or '"@type": "TechArticle"' in html
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
    html: str,
    page: Path,
    now: _dt.datetime,
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
                ".post-lead",
                ".post-lead-tldr",
                ".post-lead-takeaways",
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
    page: Path,
    html: str,
    now: _dt.datetime | None = None,
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
    r'<h2\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)</h2>([\s\S]*?)' r"(?=<h2\b[^>]*\bid=|</main>)",
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
        return "Finance and payments"
    if "quantum" in t or "pqc" in t:
        return "Post-quantum cryptography"
    if "ai" in t:
        return "Artificial Intelligence"
    if "rust" in t:
        return "Developer tools, Rust"
    if "web" in t or "css" in t:
        return "Developer tools, web"
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
    card_body: str,
    section_title: str,
    position: int,
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
        record["programmingLanguage"] = languages if len(languages) > 1 else languages[0]
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


# ---------------------------------------------------------------------------
# Article identity — one page, one entity
# ---------------------------------------------------------------------------
#
# A dated post carried two Article-family nodes that disagreed about which
# URL they described:
#
#   <link rel="canonical">        .../2026-08-04-slug/     (trailing slash)
#   BlogPosting.url               .../2026-08-04-slug      (ssg, no slash)
#   BlogPosting.mainEntityOfPage  .../2026-08-04-slug      (no slash)
#   TechArticle.mainEntityOfPage  .../2026-08-04-slug/     (slash)
#
# Search engines treat the slashed and unslashed forms as distinct URLs, so
# the richer of the two nodes described a URL that was not the canonical one,
# and the page presented two competing article entities instead of one.
# Agreeing on `mainEntityOfPage` is what merges them: same @id, same entity.
#
# Two smaller inconsistencies on the same nodes are fixed here too, because
# they have the same cause (each writer minted its own value):
#   * inLanguage was "en" on BlogPosting and "en-GB" on TechArticle;
#   * dateModified was date-only ("2026-08-04") while datePublished was a
#     full ISO-8601 timestamp.
#
# Pure (html) -> html and idempotent: a second pass is a no-op.

_ARTICLE_FAMILY = (
    "Article",
    "BlogPosting",
    "NewsArticle",
    "ScholarlyArticle",
    "TechArticle",
    "Report",
)
_DATE_ONLY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_LDJSON_BLOCK_RE = re.compile(
    r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',
    re.IGNORECASE | re.DOTALL,
)


def _is_article_node(node: object) -> bool:
    if not isinstance(node, dict):
        return False
    raw = node.get("@type", "")
    types = raw if isinstance(raw, list) else [raw]
    return any(str(t) in _ARTICLE_FAMILY for t in types)


def _align_main_entity(node: dict, canonical: str) -> bool:
    meop = node.get("mainEntityOfPage")
    if isinstance(meop, dict):
        if meop.get("@id") == canonical:
            return False
        meop["@id"] = canonical
        return True
    if isinstance(meop, str) and meop != canonical:
        node["mainEntityOfPage"] = {"@type": "WebPage", "@id": canonical}
        return True
    return False


def _align_dates(node: dict) -> bool:
    """Give a date-only ``dateModified`` the same shape as ``datePublished``
    so the two are comparable — it shipped as "2026-08-04" beside a full
    ISO-8601 ``datePublished``."""
    modified = node.get("dateModified")
    if not isinstance(modified, str) or not _DATE_ONLY_RE.match(modified):
        return False
    published = node.get("datePublished")
    suffix = "T00:00:00+00:00"
    if isinstance(published, str) and "T" in published:
        suffix = "T" + published.split("T", 1)[1]
    node["dateModified"] = modified + suffix
    return True


def _align_node(node: dict, canonical: str, lang: str) -> bool:
    """Point one Article node at *canonical* and normalise its language and
    dateModified. Returns True when anything changed."""
    changed = False
    if node.get("url") != canonical:
        node["url"] = canonical
        changed = True
    changed |= _align_main_entity(node, canonical)
    if "inLanguage" in node and node["inLanguage"] != lang:
        node["inLanguage"] = lang
        changed = True
    changed |= _align_dates(node)
    return changed


def _walk_align(data: object, canonical: str, lang: str) -> bool:
    changed = False
    if isinstance(data, dict):
        if _is_article_node(data):
            changed |= _align_node(data, canonical, lang)
        for value in data.values():
            changed |= _walk_align(value, canonical, lang)
    elif isinstance(data, list):
        for item in data:
            changed |= _walk_align(item, canonical, lang)
    return changed


def align_article_identity(html: str) -> str:
    """Bind every Article-family JSON-LD node on the page to the canonical URL.

    No-op when the page has no canonical link or no Article node, so listing,
    topic and identity-only pages pass through untouched."""
    canon_m = _canonical_re.search(html)
    if not canon_m:
        return html
    canonical = _html.unescape(canon_m.group(1))
    lang = _page_lang(html)

    def _patch(m: re.Match[str]) -> str:
        body = m.group(2)
        try:
            data = _json.loads(body)
        except ValueError:
            return m.group(0)
        if not _walk_align(data, canonical, lang):
            return m.group(0)
        # Match the separator style the block already uses so a rebuild of an
        # untouched page stays byte-identical.
        separators = (",", ":") if '", "' not in body[:200] else (", ", ": ")
        return (
            m.group(1) + _json.dumps(data, separators=separators, ensure_ascii=False) + m.group(3)
        )

    return _LDJSON_BLOCK_RE.sub(_patch, html)


# ---------------------------------------------------------------------------
# FAQPage — mark up the answers that are already written
# ---------------------------------------------------------------------------
#
# Articles carry a real "Frequently Asked Questions" section with genuine
# question-and-answer prose, and none of it was ever expressed as structured
# data. Google retired FAQ rich results for most sites, so this is not about
# the classic SERP payoff; explicit Question/Answer entities are the cleanest
# signal available to a retrieval system about which span of text answers
# which question, and answer-block extractability is what AI answer engines
# select on.
#
# Three renderings of the same section exist in the tree and all are handled:
#
#   1. <p><strong>Q?</strong><br />A</p>          — what dated articles ship
#   2. <p><strong>Q?</strong></p><p>A</p>         — the shape _convert_faq_to_qa
#                                                   expects (it never matched 1)
#   3. <details class="qa-item"><summary class="qa-q">Q</summary>
#        <div class="qa-a">A</div></details>      — /projects/, /papers/
#
# Only the FAQ section is read: matching starts at the FAQ <h2> and stops at
# the next <h2> or the end of the article, so a bolded lead-in elsewhere in
# the body can never be mistaken for a question.

_FAQ_HEADING_RE = re.compile(
    r'<h2\b[^>]*\bid="(?:frequently-asked-questions|faq|questions?)"[^>]*>.*?</h2>',
    re.IGNORECASE | re.DOTALL,
)
_NEXT_H2_RE = re.compile(r"<h2\b", re.IGNORECASE)
_TAG_STRIP_RE = re.compile(r"<[^>]+>")
_WS_COLLAPSE_RE = re.compile(r"\s+")

# 1 + 2: a <p> opening with <strong>…</strong>. The remainder of that <p> is
# the answer when non-empty (shape 1); otherwise the following <p>s are
# (shape 2).
_FAQ_P_RE = re.compile(
    r"<p\b[^>]*>\s*<strong>(?P<q>.*?)</strong>\s*(?:<br\s*/?>)?(?P<a>.*?)</p>",
    re.IGNORECASE | re.DOTALL,
)
_PLAIN_P_RE = re.compile(r"<p\b[^>]*>(?P<a>.*?)</p>", re.IGNORECASE | re.DOTALL)
# 3: the collapsible rendering.
_FAQ_DETAILS_RE = re.compile(
    r'<details\b[^>]*class="[^"]*qa-item[^"]*"[^>]*>\s*'
    r"<summary\b[^>]*>(?P<q>.*?)</summary>\s*"
    r'<div\b[^>]*class="[^"]*qa-a[^"]*"[^>]*>(?P<a>.*?)</div>\s*</details>',
    re.IGNORECASE | re.DOTALL,
)

# Below this an "answer" is a stray bold run, not prose.
_MIN_ANSWER_CHARS = 20


def _plain_text(fragment: str) -> str:
    return _WS_COLLAPSE_RE.sub(" ", _html.unescape(_TAG_STRIP_RE.sub(" ", fragment))).strip()


def _faq_section(html: str) -> str | None:
    """The FAQ section body: from its <h2> to the next <h2> (or end)."""
    heading = _FAQ_HEADING_RE.search(html)
    if not heading:
        return None
    rest = html[heading.end() :]
    nxt = _NEXT_H2_RE.search(rest)
    return rest[: nxt.start()] if nxt else rest


def _pairs_from_details(section: str) -> list[tuple[str, str]]:
    """Shape 3: the collapsible <details class="qa-item"> rendering."""
    pairs: list[tuple[str, str]] = []
    for m in _FAQ_DETAILS_RE.finditer(section):
        q, a = _plain_text(m.group("q")), _plain_text(m.group("a"))
        if q and len(a) >= _MIN_ANSWER_CHARS:
            pairs.append((q, a))
    return pairs


def _following_paragraphs(tail: str) -> str:
    """Shape 2: the answer is the plain <p>s after the question paragraph,
    up to the next question."""
    chunks: list[str] = []
    for pm in _PLAIN_P_RE.finditer(tail):
        body = pm.group("a")
        if re.match(r"\s*<strong>", body, re.IGNORECASE):
            break
        chunks.append(_plain_text(body))
        if len(chunks) >= 4:
            break
    return " ".join(c for c in chunks if c).strip()


def _pairs_from_paragraphs(section: str) -> list[tuple[str, str]]:
    """Shapes 1 and 2: <p><strong>Q?</strong><br />A</p> and
    <p><strong>Q?</strong></p><p>A</p>."""
    pairs: list[tuple[str, str]] = []
    for m in _FAQ_P_RE.finditer(section):
        question = _plain_text(m.group("q"))
        answer = _plain_text(m.group("a")) or _following_paragraphs(section[m.end() :])
        if question and len(answer) >= _MIN_ANSWER_CHARS:
            pairs.append((question, answer))
    return pairs


def _extract_qa_pairs(section: str) -> list[tuple[str, str]]:
    return _pairs_from_details(section) or _pairs_from_paragraphs(section)


def inject_faq_schema(page: Path, html: str) -> str:
    """Emit ``FAQPage`` JSON-LD for a page whose FAQ section has real Q&A.

    Idempotent — a page that already carries a FAQPage node is left alone.
    No-op when there is no FAQ section or no pair clears the minimum answer
    length, so listing and identity-only pages pass through untouched."""
    if "FAQPage" in html:
        return html
    section = _faq_section(html)
    if not section:
        return html
    pairs = _extract_qa_pairs(section)
    if not pairs:
        return html
    canon_m = _canonical_re.search(html)
    base = _html.unescape(canon_m.group(1)) if canon_m else ""
    graph: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": _page_lang(html),
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }
    if base:
        graph["@id"] = base.rstrip("/") + "/#faq"
        graph["isPartOf"] = {"@id": base}
    payload = _json.dumps(graph, separators=(",", ":"), ensure_ascii=False)
    block = f'<script type="application/ld+json">{payload}</script>'
    return re.sub(r"(?i)</body>", block + "</body>", html, count=1)


# ---------------------------------------------------------------------------
# Dataset — the index and scorecard articles carry the scoring framework that
# earns the name, and it lived in HTML tables only. Dataset is the type Google
# Dataset Search indexes and the one an answer engine can attribute, so
# publishing it is what makes the index citable rather than merely readable.
# ---------------------------------------------------------------------------

_DATASETS_PATH = Path("_data") / "datasets.json"
_DATASETS: dict[str, dict] | None = None


def _datasets() -> dict[str, dict]:
    """Manifest written by scripts/generators/build_datasets.py, by slug."""
    global _DATASETS
    if _DATASETS is None:
        if _DATASETS_PATH.is_file():
            raw = _json.loads(_DATASETS_PATH.read_text(encoding="utf-8"))
            _DATASETS = {d["slug"]: d for d in raw.get("datasets", [])}
        else:
            _DATASETS = {}
    return _DATASETS


def _dataset_graph(entry: dict) -> dict:
    slug = entry["slug"]
    page = f"{SITE}/{slug}"
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": f"{page}#dataset",
        "name": entry["name"],
        "description": entry["description"],
        "url": page,
        "isAccessibleForFree": True,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@id": f"{SITE}/#person"},
        "publisher": {"@id": f"{SITE}/#organization"},
        "isPartOf": {"@id": f"{page}#article"},
        "keywords": [k.strip() for k in entry.get("keywords", "").split(",") if k.strip()],
        "temporalCoverage": entry.get("date", ""),
        # The frameworks are qualitative, so what the index *measures* is the
        # honest representation. A ranked ItemList would assert a leaderboard
        # the articles do not publish.
        "variableMeasured": [
            {"@type": "PropertyValue", "name": v["name"], "description": v["description"]}
            for v in entry["variables"]
        ],
        "distribution": [
            {
                "@type": "DataDownload",
                "encodingFormat": fmt,
                "contentUrl": f"{SITE}/data/{slug}.{ext}",
            }
            for ext, fmt in (("json", "application/json"), ("csv", "text/csv"))
        ],
    }


def inject_dataset(page: Path, html: str) -> str:
    """Add a Dataset block to an article that declares an index table.

    Idempotent — skipped when the page already carries one, or when the slug
    is not in the manifest.
    """
    if '"@type":"Dataset"' in html or '"@type": "Dataset"' in html:
        return html
    entry = _datasets().get(page.parent.name)
    if entry is None:
        return html
    payload = _json.dumps(_dataset_graph(entry), separators=(",", ":"), ensure_ascii=False)
    block = f'<script type="application/ld+json">{payload}</script>'
    return re.sub(r"(?i)</body>", block + "</body>", html, count=1)
