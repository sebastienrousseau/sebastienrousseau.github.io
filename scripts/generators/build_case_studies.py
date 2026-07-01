#!/usr/bin/env python3
"""Generate outcome-led case-study pages under ``public/case-studies/``.

Phase 1 of the Authority Playbook (see plan §1). Each case study is a
data file in ``_data/proof/case-studies/<slug>.yml`` rendered into a
standalone HTML document sharing the FT-tier ``/articles/`` shell — so
the typography, accessibility, and CSP profile stay identical to the
rest of the site.

The page structure follows the plan's exact order:
    Problem → Role → What I built → Outcomes / Engineering rigour →
    External validation → Standards → Links → Related articles

Outputs:
    public/case-studies/index.html            hub listing every study
    public/case-studies/<slug>/index.html    one per data file

Inputs:
    _data/proof/case-studies/*.yml           case-study data (source of truth)
    _data/proof/metrics.json                 build-time metrics (optional)
    public/articles/index.html               FT-tier shell template

Runs in ``build.sh`` after ``ssg`` has emitted the articles shell, and
before ``build_translations`` so the locale-fork pass can pick the
case-study pages up.
"""

from __future__ import annotations

import argparse
import html as _html
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    print("error: PyYAML not installed (see requirements.txt)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
DATA_DIR = ROOT / "_data" / "proof" / "case-studies"
METRICS_PATH = ROOT / "_data" / "proof" / "metrics.json"
SHELL_SRC = PUBLIC / "articles" / "index.html"
OUT_DIR = PUBLIC / "case-studies"

# Per-locale case-study UI labels live in _data/proof/case-studies-i18n.json,
# extracted from three inline dicts for data/code separation (Phase 4.1).
# v1 = base section labels, v2 = Bloomberg-tier elevation, v3 = staged layout;
# _lbl() merges v3 over v2 over v1 with EN fallback.
_CS_I18N = json.loads(
    (ROOT / "_data" / "proof" / "case-studies-i18n.json").read_text(encoding="utf-8")
)
_CS_LABELS: dict[str, dict[str, str]] = _CS_I18N["v1"]
_CS_LABELS_V2: dict[str, dict[str, str]] = _CS_I18N["v2"]
_CS_LABELS_V3: dict[str, dict[str, str]] = _CS_I18N["v3"]


def _lbl(lang: str) -> dict[str, str]:
    """Merged label set for ``lang`` — V3 keys layered on V2 on V1, with
    EN as the fallback for any missing key across all dicts."""
    base = {**_CS_LABELS["en"], **_CS_LABELS_V2["en"], **_CS_LABELS_V3["en"]}
    v1 = _CS_LABELS.get(lang, _CS_LABELS["en"])
    v2 = _CS_LABELS_V2.get(lang, _CS_LABELS_V2["en"])
    v3 = _CS_LABELS_V3.get(lang, _CS_LABELS_V3["en"])
    return {**base, **v1, **v2, **v3}

_BASE_URL = "https://sebastienrousseau.com"
_TITLE_RE = re.compile(r"<title>[^<]*</title>", re.IGNORECASE)
_DESC_RE = re.compile(
    r'<meta name="description" content="[^"]*"', re.IGNORECASE
)
_CANONICAL_RE = re.compile(
    r'<link rel="canonical" href="[^"]*"', re.IGNORECASE
)
_OG_TITLE_RE = re.compile(
    r'(<meta property="og:title" content=")[^"]*(")', re.IGNORECASE
)
_OG_DESC_RE = re.compile(
    r'(<meta property="og:description" content=")[^"]*(")', re.IGNORECASE
)
_OG_URL_RE = re.compile(
    r'(<meta property="og:url" content=")[^"]*(")', re.IGNORECASE
)
_MAIN_WRAP_RE = re.compile(
    r'(<main\b[^>]*>\s*)<div class="wrap[^"]*">[\s\S]*?</div>(\s*</main>)',
    re.IGNORECASE,
)
_AP_HERO_BLOCK_RE = re.compile(
    r'<section class="ap-hero">[\s\S]*?</section>', re.IGNORECASE
)


def _esc(s: str) -> str:
    return _html.escape(str(s or ""), quote=True)


def _load_studies() -> list[dict]:
    """Load every YAML file under ``_data/proof/case-studies/`` and
    return them as dicts. Empty list if the directory is missing.
    Per-locale overlays under ``i18n/<lang>/<slug>.yml`` are loaded
    separately and merged at render time via ``_localised_study``."""
    if not DATA_DIR.is_dir():
        return []
    studies = []
    for path in sorted(DATA_DIR.glob("*.yml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            print(f"build_case_studies: skip {path.name} — {exc}", file=sys.stderr)
            continue
        if not data.get("slug"):
            print(f"build_case_studies: skip {path.name} — missing slug", file=sys.stderr)
            continue
        studies.append(data)
    return studies


def _load_overlay(lang: str, slug: str) -> dict:
    """Load a per-locale overlay YAML if it exists. Returns {} if missing
    or unreadable — caller falls back to EN content."""
    if lang == "en":
        return {}
    path = DATA_DIR / "i18n" / lang / f"{slug}.yml"
    if not path.is_file():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        print(f"build_case_studies: overlay parse failed {path} — {exc}", file=sys.stderr)
        return {}


_OVERLAY_KEEP_EN = frozenset({
    "slug", "banner", "category_slug", "links",
    "related_articles", "signed", "period",
    "outcome_highlights_keep_values", "standards",
})
_OVERLAY_LIST_FIELDS = frozenset({"outcome_highlights", "rigour"})


def _merge_list_of_dicts(base: list, overlay_rows: list) -> list[dict]:
    """Zip overlay rows over base rows so a translator can override
    just the prose ``label`` / ``metric`` keys without restating
    ``value``."""
    merged: list[dict] = []
    for i, base_row in enumerate(list(base) or []):
        row = dict(base_row) if isinstance(base_row, dict) else {}
        if i < len(overlay_rows) and isinstance(overlay_rows[i], dict):
            row.update(overlay_rows[i])
        merged.append(row)
    return merged


def _merge_overlay(study: dict, overlay: dict) -> dict:
    """Return a copy of ``study`` with fields from ``overlay`` substituted.
    List-of-dicts fields (outcome_highlights, rigour) are zipped index-by-
    index so partial overlays still work. Scalar / list-of-string fields
    are simple replacements. URLs, slugs, banner image, signed flag, and
    related_articles stay EN-canonical."""
    if not overlay:
        return study
    out = dict(study)
    for key, val in overlay.items():
        if key in _OVERLAY_KEEP_EN:
            continue
        if key in _OVERLAY_LIST_FIELDS and isinstance(val, list):
            out[key] = _merge_list_of_dicts(study.get(key) or [], val)
        else:
            out[key] = val
    return out


def _localised_study(study: dict, lang: str) -> dict:
    """Return ``study`` merged with its per-locale overlay (if any)."""
    return _merge_overlay(study, _load_overlay(lang, study["slug"]))


def _load_metrics() -> dict:
    if not METRICS_PATH.is_file():
        return {}
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _hub_url(lang: str, url_segment: str) -> str:
    return "/case-studies/" if lang == "en" else f"/{lang}/{url_segment}/"


def _study_url(lang: str, url_segment: str, slug: str) -> str:
    return (
        f"/case-studies/{slug}/"
        if lang == "en"
        else f"/{lang}/{url_segment}/{slug}/"
    )


def _related_article_href(slug: str, lang: str, article_slug_map: dict[str, str]) -> str:
    target_slug = article_slug_map.get(slug, slug) if lang != "en" else slug
    return f"/{slug}/" if lang == "en" else f"/{lang}/{target_slug}/"


def _render_breadcrumb(
    lbl: dict[str, str], lang: str, url_segment: str, current: str | None = None
) -> str:
    sep = '<span aria-hidden="true"> › </span>'
    home_href = "/" if lang == "en" else f"/{lang}/"
    hub_href = _hub_url(lang, url_segment)
    parts = [
        f'<a href="{home_href}">{_esc(lbl["Home"])}</a>{sep}',
        f'<a href="{hub_href}">{_esc(lbl["Case studies"])}</a>',
    ]
    if current:
        parts.append(f'{sep}<span aria-current="page">{_esc(current)}</span>')
    return (
        f'<nav class="cs-breadcrumb" aria-label="{_esc(lbl["Home"])}">'
        + "".join(parts) + "</nav>"
    )


def _render_outcomes(outcomes: list[dict], lbl: dict[str, str]) -> str:
    if not outcomes:
        return ""
    items = "".join(
        '<div class="cs-outcomes-item">'
        f'<dt>{_esc(o.get("value",""))}</dt>'
        f'<dd>{_esc(o.get("label",""))}</dd>'
        "</div>"
        for o in outcomes
    )
    return (
        f'<section class="cs-outcomes" aria-label="{_esc(lbl["By the numbers"])}">'
        f'<h2>{_esc(lbl["By the numbers"])}</h2>'
        f'<dl>{items}</dl></section>'
    )


def _render_pullquote(quote: str) -> str:
    if not quote or not quote.strip():
        return ""
    return f'<aside class="cs-pullquote"><p>{_esc(quote.strip().strip(chr(34)))}</p></aside>'


def _render_meta_strip(study: dict, lbl: dict[str, str]) -> str:
    pieces: list[str] = []
    fields = [
        ("Role", study.get("role", "")),
        ("Period", study.get("period", "")),
        ("Status", study.get("status", "")),
        ("Sector", study.get("sector", "")),
    ]
    for key, val in fields:
        if val:
            pieces.append(
                f'<li><strong>{_esc(lbl[key])}</strong> {_esc(val)}</li>'
            )
    if not pieces:
        return ""
    return f'<ul class="cs-meta-strip" role="list">{"".join(pieces)}</ul>'


def _render_rigour_table(rigour: list[dict], lbl: dict[str, str]) -> str:
    if not rigour:
        return ""
    rows = "".join(
        f'<tr><th scope="row">{_esc(r.get("metric",""))}</th>'
        f'<td>{_esc(r.get("value",""))}</td></tr>'
        for r in rigour
    )
    return (
        '<section class="cs-rigour"><h2>'
        f'{_esc(lbl["Engineering rigour"])}</h2>'
        '<table class="case-study-rigour">'
        f'<caption>{_esc(lbl["Engineering rigour"])}</caption>'
        f'<thead><tr><th scope="col">{_esc(lbl["Signal"])}</th>'
        f'<th scope="col">{_esc(lbl["Evidence"])}</th></tr></thead>'
        f"<tbody>{rows}</tbody></table></section>"
    )


def _render_list_section(heading: str, items: list[str], css_class: str) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{_esc(item)}</li>" for item in items)
    return f'<section class="{css_class}"><h2>{_esc(heading)}</h2><ul>{lis}</ul></section>'


_LINK_LABELS = {
    "repo": "GitHub repository",
    "site": "Project site",
    "pypi": "PyPI",
    "crates": "crates.io",
    "docs": "Docs.rs",
    "stats": "PyPI download stats",
    "qtonic_evaluation": "Qtonic Quantum Lab — independent evaluation",
    "qgram_adopter": "QGram (Quantum2pi) — KyberLib adopter",
    "bank": "HSBC",
    "linkedin": "LinkedIn",
}
_LINK_ORDER = (
    "repo", "site", "pypi", "crates", "docs", "stats",
    "qtonic_evaluation", "qgram_adopter", "bank", "linkedin",
)


def _render_rail_links(links: dict[str, str], lbl: dict[str, str]) -> str:
    if not links:
        return ""
    rows: list[str] = []
    seen: set[str] = set()
    for key in _LINK_ORDER:
        if key in links and key not in seen:
            seen.add(key)
            rows.append(
                f'<li><a href="{_esc(links[key])}" rel="noopener noreferrer">'
                f'{_esc(_LINK_LABELS.get(key, key))}</a></li>'
            )
    for key, val in links.items():
        if key not in seen:
            rows.append(
                f'<li><a href="{_esc(val)}" rel="noopener noreferrer">{_esc(key)}</a></li>'
            )
    return (
        '<div class="cs-rail-links">'
        f'<p class="cs-side-heading">{_esc(lbl["Verifiable links"])}</p>'
        f'<ul>{"".join(rows)}</ul></div>'
    )


def _render_share_rail(url: str, title: str, lbl: dict[str, str]) -> str:
    import urllib.parse as _up

    full_url = url if url.startswith("http") else f"{_BASE_URL}{url}"
    enc_url = _up.quote(full_url, safe="")
    enc_title = _up.quote(title, safe="")
    x_href = f"https://twitter.com/intent/tweet?url={enc_url}&text={enc_title}"
    li_href = f"https://www.linkedin.com/sharing/share-offsite/?url={enc_url}"
    return (
        '<div class="cs-rail-share-block">'
        f'<p class="cs-side-heading">{_esc(lbl["Share"])}</p>'
        '<div class="cs-rail-share">'
        f'<a href="{x_href}" rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on X"])}" title="{_esc(lbl["Share on X"])}">X</a>'
        f'<a href="{li_href}" rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on LinkedIn"])}" title="{_esc(lbl["Share on LinkedIn"])}">in</a>'
        '</div>'
        '</div>'
    )


def _render_related_articles_section(
    slugs: list[str], lbl: dict[str, str], lang: str, article_slug_map: dict[str, str]
) -> str:
    if not slugs:
        return ""
    items = []
    for slug in slugs:
        href = _related_article_href(slug, lang, article_slug_map)
        # Strip date prefix for display; keep underscores → spaces fallback.
        display = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug).replace("-", " ").capitalize()
        items.append(f'<li><a href="{href}">{_esc(display)}</a></li>')
    return (
        '<section class="cs-related-articles">'
        f'<h2>{_esc(lbl["Related articles"])}</h2>'
        f'<ul>{"".join(items)}</ul></section>'
    )


def _render_more_case_studies(
    current: dict, all_studies: list[dict], lbl: dict[str, str],
    lang: str, url_segment: str,
) -> str:
    others = [s for s in all_studies if s["slug"] != current["slug"]][:4]
    if not others:
        return ""
    cards = []
    for s in others:
        slug = s["slug"]
        title = s.get("title", slug)
        kicker = s.get("kicker", lbl["eyebrow"])
        banner = s.get("banner", "")
        banner_alt = s.get("banner_alt", title)
        href = _study_url(lang, url_segment, slug)
        media = ""
        if banner:
            media = (
                f'<a href="{href}" class="cs-card-media">'
                f'<img alt="{_esc(banner_alt)}" src="{_esc(banner)}" '
                'loading="lazy" decoding="async" width="600" height="338">'
                f'<span class="cs-card-kicker">{_esc(kicker)}</span></a>'
            )
        cards.append(
            f'<article data-category="{_esc(s.get("category_slug",""))}">'
            f'{media}'
            '<div class="cs-card-body">'
            f'<h3><a href="{href}">{_esc(title)}</a></h3>'
            '</div></article>'
        )
    return (
        '<section class="cs-related">'
        f'<h2>{_esc(lbl["More case studies"])}</h2>'
        '<div class="cs-related-grid" role="list">'
        + "".join(cards) +
        '</div></section>'
    )


def _json_ld_block(payload: dict) -> str:
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
        + '</script>'
    )


def _build_breadcrumb_jsonld(
    lbl: dict[str, str], lang: str, url_segment: str,
    study: dict | None = None,
) -> dict:
    bcp47 = {
        "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
        "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
    }.get(lang, lang)
    home_url = _BASE_URL + ("/" if lang == "en" else f"/{lang}/")
    hub_url = _BASE_URL + _hub_url(lang, url_segment)
    items = [
        {"@type": "ListItem", "position": 1, "name": lbl["Home"], "item": home_url},
        {"@type": "ListItem", "position": 2, "name": lbl["Case studies"], "item": hub_url},
    ]
    if study is not None:
        items.append({
            "@type": "ListItem", "position": 3,
            "name": study.get("title", study["slug"]),
            "item": _BASE_URL + _study_url(lang, url_segment, study["slug"]),
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
        "inLanguage": bcp47,
    }


_BCP47_OVERRIDES = {
    "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
    "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
}


def _source_code_entity(study: dict, links: dict, person_id: str) -> dict | None:
    """Schema.org SoftwareSourceCode node for a repo-linked study."""
    if not (links.get("repo") or links.get("crates") or links.get("pypi")):
        return None
    language = "Rust" if links.get("crates") else ("Python" if links.get("pypi") else None)
    entity = {
        "@type": "SoftwareSourceCode",
        "name": study.get("title", study["slug"]),
        "codeRepository": links.get("repo"),
        "programmingLanguage": language,
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "author": {"@type": "Person", "@id": person_id},
    }
    return {k: v for k, v in entity.items() if v is not None}


def _build_article_jsonld(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
) -> dict:
    bcp47 = _BCP47_OVERRIDES.get(lang, lang)
    url = _BASE_URL + _study_url(lang, url_segment, study["slug"])
    person_id = f"{_BASE_URL}/#person"
    links = study.get("links", {}) or {}
    main_entity = _source_code_entity(study, links, person_id)
    about = [{
        "@type": "Organization",
        "name": "HSBC Holdings plc",
        "url": links["bank"],
    }] if "bank" in links else []
    # Collapse YAML folded-scalar newlines so JSON-LD stays a single
    # logical line. Postbuild HTML transforms apply unescape passes that
    # turn json.dumps's \n back into a literal newline, which breaks
    # test_page_inline_jsonld_is_valid_json.
    description = " ".join((study.get("problem", "") or "").split())[:200]
    # Schema.org Article requires datePublished. Case studies don't carry
    # a single launch date so derive one from the YAML ``period`` start
    # year (e.g. "2023 – present" → "2023-01-01"). Falls back to the
    # case-studies hub launch date when period is non-numeric.
    period = str(study.get("period", "")).strip()
    period_year_match = re.match(r"\s*(\d{4})", period)
    date_published = (
        f"{period_year_match.group(1)}-01-01" if period_year_match else "2025-09-01"
    )
    article: dict = {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": url + "#article",
        "headline": study.get("title", study["slug"]),
        "description": description,
        "url": url,
        "articleSection": lbl["Case study"],
        "inLanguage": bcp47,
        "datePublished": date_published,
        "dateModified": "2026-06-17",
        "isPartOf": {
            "@type": "CollectionPage",
            "@id": _BASE_URL + _hub_url(lang, url_segment) + "#collection",
        },
        "author": {"@type": "Person", "@id": person_id},
        "creator": {"@type": "Person", "@id": person_id},
        "publisher": {"@type": "Person", "@id": person_id},
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }
    if study.get("banner"):
        article["image"] = study["banner"]
    if main_entity:
        article["mainEntity"] = main_entity
    if about:
        article["about"] = about
    return article


def _build_collection_jsonld(
    studies: list[dict], lbl: dict[str, str], lang: str, url_segment: str,
) -> dict:
    bcp47 = {
        "en": "en-GB", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
        "it": "it-IT", "ja": "ja-JP", "ko": "ko-KR", "ru": "ru-RU",
    }.get(lang, lang)
    hub_url = _BASE_URL + _hub_url(lang, url_segment)
    items = []
    for i, study in enumerate(studies, start=1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": _BASE_URL + _study_url(lang, url_segment, study["slug"]),
            "name": study.get("title", study["slug"]),
        })
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": hub_url + "#collection",
        "name": lbl["Case studies"],
        "description": lbl["deck"],
        "url": hub_url,
        "inLanguage": bcp47,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(studies),
            "itemListElement": items,
        },
    }


def _hero_variant(slug: str) -> str:
    """Rotate hero composition across 5 studies so each feels distinct.
    Stable per slug — same slug always gets the same variant."""
    return ("centre", "left", "split")[sum(ord(c) for c in slug) % 3]


def _stage_no(n: int, label: str) -> str:
    """Numbered stage eyebrow — '01 — THE PROBLEM' style."""
    return (
        f'<p class="cs-stage-no">'
        f'<span aria-hidden="true">{n:02d} — </span>'
        f'{_esc(label.upper())}</p>'
    )


def _render_hero_stage(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
) -> str:
    """FT customer-stories hero — full-bleed photo with overlay text + CTA."""
    title = study.get("title", study.get("slug", ""))
    kicker = study.get("kicker", lbl["eyebrow"])
    deck = study.get("pull_quote", "").strip()
    if deck.startswith('"') and deck.endswith('"'):
        deck = deck[1:-1]
    # Per-study hero may override the card thumbnail via `hero_banner`.
    # Falls through to the standard `banner` field when unset.
    banner = study.get("hero_banner") or study.get("banner", "")
    breadcrumb = _render_breadcrumb(lbl, lang, url_segment, title)

    media_html = ""
    if banner:
        media_html = (
            '<figure class="cs-hero-media" aria-hidden="true">'
            f'<img alt="" src="{_esc(banner)}" '
            'loading="eager" fetchpriority="high" decoding="async" '
            'width="1600" height="900">'
            '</figure>'
        )

    return (
        '<section class="cs-stage cs-hero" data-stage>'
        + media_html
        + '<div class="cs-stage-row">'
        + '<div class="cs-hero-text">'
        + breadcrumb
        + f'<p class="cs-kicker">{_esc(kicker)}</p>'
        + f'<h1>{_esc(title)}</h1>'
        + (f'<p class="cs-deck">{_esc(deck)}</p>' if deck else '')
        + f'<a class="cs-hero-cta" href="#story">{_esc(lbl.get("Read case study", "Read more"))}</a>'
        + '</div>'
        + '</div>'
        + '</section>'
    )


def _render_meta_bar(study: dict, lbl: dict[str, str]) -> str:
    """Compact meta strip below hero — role / period / status / sector."""
    pieces: list[str] = []
    fields = [
        ("Role", study.get("role", "")),
        ("Period", study.get("period", "")),
        ("Status", study.get("status", "")),
        ("Sector", study.get("sector", "")),
    ]
    for key, val in fields:
        if val:
            pieces.append(
                f'<li><strong>{_esc(lbl[key])}</strong> {_esc(val)}</li>'
            )
    if not pieces:
        return ""
    return (
        '<section class="cs-stage cs-meta-bar" data-stage>'
        '<div class="cs-stage-row">'
        f'<ul role="list">{"".join(pieces)}</ul>'
        '</div></section>'
    )


def _render_outcomes_stage(outcomes: list[dict], lbl: dict[str, str]) -> str:
    if not outcomes:
        return ""
    items = "".join(
        '<div class="cs-outcome">'
        f'<dt>{_esc(o.get("value",""))}</dt>'
        f'<dd>{_esc(o.get("label",""))}</dd>'
        "</div>"
        for o in outcomes
    )
    return (
        '<section class="cs-stage cs-outcomes" data-stage '
        f'aria-label="{_esc(lbl["By the numbers"])}">'
        '<div class="cs-stage-row">'
        + _stage_no(0, lbl["By the numbers"]).replace(
            '<span aria-hidden="true">00 — </span>', ''
        )
        + f'<dl>{items}</dl>'
        '</div></section>'
    )


def _render_quote_stage(quote: str) -> str:
    """Full-bleed italic serif pull quote."""
    q = (quote or "").strip().strip('"').strip("“").strip("”")
    if not q:
        return ""
    return (
        '<section class="cs-stage cs-quote" data-stage>'
        '<div class="cs-stage-row">'
        f'<blockquote><p>{_esc(q)}</p>'
        '<cite>— from the case-study brief</cite></blockquote>'
        '</div></section>'
    )


def _render_story_stage(n: int, label: str, body_text: str, anchor: str = "") -> str:
    if not body_text:
        return ""
    anchor_attr = f' id="{anchor}"' if anchor else ""
    return (
        f'<section class="cs-stage cs-story" data-stage{anchor_attr}>'
        '<div class="cs-stage-row">'
        f'<div class="cs-stage-head">{_stage_no(n, label)}'
        f'<h2>{_esc(label)}</h2></div>'
        '<div class="cs-stage-body">'
        f'<p>{_esc(body_text)}</p>'
        '</div></div></section>'
    )


def _render_rigour_stage(rigour: list[dict], lbl: dict[str, str], n: int) -> str:
    if not rigour:
        return ""
    cards = "".join(
        '<li class="cs-rigour-card">'
        f'<p class="cs-rigour-card-signal">{_esc(r.get("metric",""))}</p>'
        f'<p class="cs-rigour-card-value">{_esc(r.get("value",""))}</p>'
        '</li>'
        for r in rigour
    )
    return (
        '<section class="cs-stage cs-rigour" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Engineering rigour"])
        + f'<h2>{_esc(lbl["Engineering rigour"])}</h2>'
        + f'<ul class="cs-rigour-grid" role="list">{cards}</ul>'
        '</div></section>'
    )


def _render_validation_stage(items: list[str], lbl: dict[str, str], n: int) -> str:
    if not items:
        return ""
    lis = "".join(f'<li>{_esc(i)}</li>' for i in items)
    return (
        '<section class="cs-stage cs-validation" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Independently verified"])
        + f'<h2>{_esc(lbl["Independently verified"])}</h2>'
        + f'<ul>{lis}</ul>'
        '</div></section>'
    )


def _render_standards_stage(items: list[str], lbl: dict[str, str], n: int) -> str:
    if not items:
        return ""
    pills = "".join(f'<li>{_esc(i)}</li>' for i in items)
    return (
        '<section class="cs-stage cs-standards" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Aligned standards"])
        + f'<h2>{_esc(lbl["Aligned standards"])}</h2>'
        + f'<ul class="cs-standards-pills" role="list">{pills}</ul>'
        '</div></section>'
    )


def _render_links_stage(links: dict[str, str], lbl: dict[str, str], n: int) -> str:
    if not links:
        return ""
    rows: list[str] = []
    seen: set[str] = set()
    for key in _LINK_ORDER:
        if key in links and key not in seen:
            seen.add(key)
            rows.append(
                f'<li><a href="{_esc(links[key])}" rel="noopener noreferrer">'
                f'{_esc(_LINK_LABELS.get(key, key))}</a></li>'
            )
    for key, val in links.items():
        if key not in seen:
            rows.append(
                f'<li><a href="{_esc(val)}" rel="noopener noreferrer">{_esc(key)}</a></li>'
            )
    return (
        '<section class="cs-stage cs-stage--wash cs-links" data-stage>'
        '<div class="cs-stage-row">'
        + _stage_no(n, lbl["Verifiable links"])
        + f'<h2>{_esc(lbl["Verifiable links"])}</h2>'
        + f'<ul class="cs-links-grid" role="list">{"".join(rows)}</ul>'
        '</div></section>'
    )


def _render_related_articles_stage(
    slugs: list[str], lbl: dict[str, str], lang: str, article_slug_map: dict[str, str]
) -> str:
    if not slugs:
        return ""
    items = []
    for slug in slugs:
        href = _related_article_href(slug, lang, article_slug_map)
        display = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug).replace("-", " ").capitalize()
        items.append(f'<li><a href="{href}">{_esc(display)}</a></li>')
    return (
        '<section class="cs-stage cs-related" data-stage>'
        '<div class="cs-stage-row cs-stage-row--mid">'
        f'<p class="cs-stage-no">{_esc(lbl["Related articles"]).upper()}</p>'
        f'<h2>{_esc(lbl["Related articles"])}</h2>'
        f'<ul class="cs-links-grid" role="list">{"".join(items)}</ul>'
        '</div></section>'
    )


_CONTACT_SLUG_CACHE: dict[str, str] = {}


def _contact_slug(lang: str) -> str:
    """Resolve the localised /contact/ URL segment from slugs.json. Falls
    back to 'contact' when the file or key is missing (EN + dev paths)."""
    if lang in _CONTACT_SLUG_CACHE:
        return _CONTACT_SLUG_CACHE[lang]
    slug_path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    slug = "contact"
    import contextlib

    with contextlib.suppress(OSError, ValueError):
        slug = json.loads(slug_path.read_text()).get("static", {}).get("contact", "contact")
    _CONTACT_SLUG_CACHE[lang] = slug
    return slug


def _render_cta_stage(lbl: dict[str, str], lang: str) -> str:
    contact = "/contact/" if lang == "en" else f"/{lang}/{_contact_slug(lang)}/"
    return (
        '<section class="cs-stage cs-cta" data-stage>'
        '<div class="cs-stage-row">'
        f'<p class="cs-stage-no">{_esc(lbl.get("Next", "Next")).upper()}</p>'
        f'<h2>{_esc(lbl.get("CTA headline", "Want this kind of evidence in your bank?"))}</h2>'
        f'<p>{_esc(lbl.get("CTA body", "Architecture reviews, post-quantum migration plans, treasury-API programmes — all signed, all verifiable."))}</p>'
        f'<a class="cs-cta-btn" href="{contact}">'
        f'{_esc(lbl.get("Get in touch", "Get in touch"))}'
        '</a>'
        '</div></section>'
    )


def _render_more_studies_stage(
    current: dict, all_studies: list[dict], lbl: dict[str, str],
    lang: str, url_segment: str,
) -> str:
    others = [s for s in all_studies if s["slug"] != current["slug"]][:4]
    if not others:
        return ""
    cards = []
    for s in others:
        slug = s["slug"]
        title = s.get("title", slug)
        kicker = s.get("kicker", lbl["eyebrow"])
        banner = s.get("banner", "")
        href = _study_url(lang, url_segment, slug)
        media_html = ""
        if banner:
            media_html = (
                '<span class="cs-more-card-media" aria-hidden="true">'
                f'<img class="cs-more-card-bg" alt="" src="{_esc(banner)}" '
                'loading="lazy" decoding="async" width="600" height="375">'
                '</span>'
            )
        cards.append(
            '<article class="cs-more-card">'
            + media_html
            + '<div class="cs-more-card-body">'
            + f'<p class="cs-more-card-kicker">{_esc(kicker)}</p>'
            + f'<h3 class="cs-more-card-title"><a href="{href}">{_esc(title)}</a></h3>'
            + '</div></article>'
        )
    return (
        '<section class="cs-stage cs-more" data-stage>'
        '<div class="cs-stage-row">'
        f'<p class="cs-stage-no">{_esc(lbl["More case studies"]).upper()}</p>'
        f'<h2>{_esc(lbl["More case studies"])}</h2>'
        f'<div class="cs-more-grid" role="list">{"".join(cards)}</div>'
        '</div></section>'
    )


sys.path.insert(0, str(ROOT / "scripts" / "lib"))
from _svg_icons import (  # shared share-rail glyphs (Phase 4.2 dedup)
    _CARD_SVG_EMAIL,
    _CARD_SVG_FB,
    _CARD_SVG_LI,
    _CARD_SVG_X,
)

_SHARE_SVG = {
    "x": _CARD_SVG_X,
    "li": _CARD_SVG_LI,
    "fb": _CARD_SVG_FB,
    "mail": _CARD_SVG_EMAIL,
}


def _render_side_meta(study: dict, lbl: dict[str, str]) -> str:
    """Role / Period / Status / Sector dt-dd rows for the sidebar."""
    rows = []
    for field, label_key in (("role", "Role"), ("period", "Period"),
                              ("status", "Status"), ("sector", "Sector")):
        value = study.get(field, "")
        if value:
            rows.append(
                '<div class="cs-side-section">'
                f'<dt>{_esc(lbl[label_key])}</dt>'
                f'<dd>{_esc(value)}</dd></div>'
            )
    return f'<dl class="cs-side-meta">{"".join(rows)}</dl>' if rows else ""


def _render_side_links(links: dict, lbl: dict[str, str]) -> str:
    """Verifiable-links block — _LINK_ORDER first, remainder appended."""
    if not links:
        return ""
    link_rows: list[str] = []
    seen: set[str] = set()
    for key in _LINK_ORDER:
        if key in links and key not in seen:
            seen.add(key)
            link_rows.append(
                f'<li><a href="{_esc(links[key])}" rel="noopener noreferrer">'
                f'{_esc(_LINK_LABELS.get(key, key))}</a></li>'
            )
    for key, val in links.items():
        if key not in seen:
            link_rows.append(
                f'<li><a href="{_esc(val)}" rel="noopener noreferrer">{_esc(key)}</a></li>'
            )
    return (
        '<div class="cs-side-section cs-side-links">'
        f'<p class="cs-side-heading">{_esc(lbl["Verifiable links"])}</p>'
        f'<ul>{"".join(link_rows)}</ul></div>'
    )


def _render_share_block(study: dict, lbl: dict[str, str], lang: str) -> str:
    """Article-style share rail (44×44 circular SVG icons)."""
    import urllib.parse as _up

    full_url = f"{_BASE_URL}{_study_url(lang, '', study['slug'])}"
    enc_url = _up.quote(full_url, safe="")
    enc_title = _up.quote(study.get("title", study["slug"]), safe="")
    enc_mail_body = _up.quote(f"Read more: {full_url}", safe="")
    return (
        '<div class="cs-side-section cs-side-share-block">'
        f'<p class="cs-side-heading">{_esc(lbl["Share"])}</p>'
        '<nav class="share-rail" aria-label="Share">'
        '<ul>'
        f'<li><a href="https://twitter.com/intent/tweet?url={enc_url}&amp;text={enc_title}" '
        f'rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on X"])}">{_SHARE_SVG["x"]}</a></li>'
        f'<li><a href="https://www.linkedin.com/sharing/share-offsite/?url={enc_url}" '
        f'rel="noopener noreferrer" target="_blank" '
        f'aria-label="{_esc(lbl["Share on LinkedIn"])}">{_SHARE_SVG["li"]}</a></li>'
        f'<li><a href="https://www.facebook.com/sharer/sharer.php?u={enc_url}" '
        f'rel="noopener noreferrer" target="_blank" '
        f'aria-label="Share on Facebook">{_SHARE_SVG["fb"]}</a></li>'
        f'<li><a href="mailto:?subject={enc_title}&amp;body={enc_mail_body}" '
        f'rel="noopener noreferrer" '
        f'aria-label="Share by email">{_SHARE_SVG["mail"]}</a></li>'
        '</ul></nav>'
        '</div>'
    )


def _render_side_panel(study: dict, lbl: dict[str, str], lang: str) -> str:
    """FT-style left rail: meta dl + standards + verifiable links + share."""
    standards = study.get("standards", []) or []
    standards_block = ""
    if standards:
        pills = "".join(f"<li>{_esc(s)}</li>" for s in standards)
        standards_block = (
            '<div class="cs-side-section cs-side-standards">'
            f'<p class="cs-side-heading">{_esc(lbl["Aligned standards"])}</p>'
            f'<ul>{pills}</ul></div>'
        )
    return (
        '<aside class="cs-side" aria-label="Story details">'
        + _render_side_meta(study, lbl)
        + standards_block
        + _render_side_links(study.get("links", {}) or {}, lbl)
        + _render_share_block(study, lbl, lang)
        + '</aside>'
    )


def _render_inline_outcomes(outcomes: list[dict]) -> str:
    if not outcomes:
        return ""
    items = "".join(
        '<div>'
        f'<dt>{_esc(o.get("value",""))}</dt>'
        f'<dd>{_esc(o.get("label",""))}</dd>'
        '</div>'
        for o in outcomes
    )
    return f'<dl class="cs-outcomes-inline">{items}</dl>'


def _render_inline_pull_quote(quote: str) -> str:
    q = (quote or "").strip().strip('"').strip("“").strip("”")
    if not q:
        return ""
    return (
        '<aside class="cs-pull-inline">'
        f'<p>{_esc(q)}</p>'
        f'<cite>— from the case-study brief</cite>'
        '</aside>'
    )


def _render_inline_rigour(rigour: list[dict], lbl: dict[str, str]) -> str:
    if not rigour:
        return ""
    items = "".join(
        '<li>'
        f'<p class="cs-rigour-signal">{_esc(r.get("metric",""))}</p>'
        f'<p class="cs-rigour-value">{_esc(r.get("value",""))}</p>'
        '</li>'
        for r in rigour
    )
    return f'<ul class="cs-rigour-rows" role="list">{items}</ul>'


def _render_inline_validation(items: list[str]) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{_esc(i)}</li>" for i in items)
    return f'<ul class="cs-validation-inline" role="list">{lis}</ul>'


def _render_inline_related_articles(
    slugs: list[str], lbl: dict[str, str], lang: str, article_slug_map: dict[str, str]
) -> str:
    if not slugs:
        return ""
    items: list[str] = []
    for slug in slugs:
        href = _related_article_href(slug, lang, article_slug_map)
        display = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug).replace("-", " ").capitalize()
        items.append(f'<li><a href="{href}">{_esc(display)}</a></li>')
    return f'<ul class="cs-side-links cs-related-rows" role="list">{"".join(items)}</ul>'


def _prose_section(headline_html: str, body_html: str, anchor: str = "") -> str:
    """Emit one <section> with a stage-headline + body HTML."""
    open_tag = f'<section id="{anchor}">' if anchor else "<section>"
    return f'{open_tag}<h2 class="cs-stage-headline">{headline_html}</h2>{body_html}</section>'


def _deck_html(study: dict) -> str:
    """Pull-quote deck used as standfirst above the numbered sections."""
    deck = (study.get("pull_quote", "") or "").strip().strip('"').strip("“").strip("”")
    return f'<p class="cs-deck-intro">{_esc(deck)}</p>' if deck else ""


def _prose_body_for(study: dict, lbl: dict[str, str], lang: str,
                    article_slug_map: dict[str, str], field: str) -> str:
    """Render the body HTML for one of the named sections.

    The keys mirror the YAML field names so the section table below can
    drive the whole render with one lookup per row."""
    value = study.get(field)
    if not value:
        return ""
    if field in ("problem", "what_i_built"):
        return f'<p>{_esc(value)}</p>'
    if field == "outcome_highlights":
        return _render_inline_outcomes(value)
    if field == "rigour":
        return _render_inline_rigour(value, lbl)
    if field == "validation":
        return _render_inline_validation(value)
    if field == "related_articles":
        return _render_inline_related_articles(value, lbl, lang, article_slug_map)
    return ""


# Ordered (field, label-key, stage-number-or-zero, anchor) tuples driving
# the right-column section render. Stage number 0 means "no NN — prefix".
_MAIN_SECTIONS: tuple[tuple[str, str, int, str], ...] = (
    ("problem", "Problem", 1, "story"),
    ("what_i_built", "What I built", 2, ""),
    ("outcome_highlights", "By the numbers", 0, ""),
    ("rigour", "Engineering rigour", 3, ""),
    ("validation", "Independently verified", 4, ""),
    ("related_articles", "Related articles", 0, ""),
)


def _render_main_body_parts(
    study: dict, lbl: dict[str, str], lang: str, article_slug_map: dict[str, str],
) -> list[str]:
    """Build the ordered narrative sections for the right column."""
    parts: list[str] = []
    deck = _deck_html(study)
    if deck:
        parts.append(deck)
    for field, label_key, stage, anchor in _MAIN_SECTIONS:
        body = _prose_body_for(study, lbl, lang, article_slug_map, field)
        if not body:
            continue
        prefix = _stage_n(stage) if stage else ""
        parts.append(_prose_section(f'{prefix}{_esc(lbl[label_key])}', body, anchor=anchor))
    return parts


def _render_body_two_col(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
    article_slug_map: dict[str, str],
) -> str:
    """FT customer-story two-column body: sticky left rail + right prose column."""
    side = _render_side_panel(study, lbl, lang)
    main_parts = _render_main_body_parts(study, lbl, lang, article_slug_map)
    main_body = f'<div class="cs-body-main">{"".join(main_parts)}</div>'
    return (
        '<section class="cs-stage cs-body-stage" data-stage>'
        '<div class="cs-stage-row cs-body-grid">'
        + side + main_body
        + '</div></section>'
    )


def _stage_n(n: int) -> str:
    return f'<span aria-hidden="true">{n:02d} — </span>'


def _render_body(
    study: dict, lbl: dict[str, str], lang: str, url_segment: str,
    article_slug_map: dict[str, str], all_studies: list[dict],
) -> str:
    """Per-study page — FT customer-stories pattern:
       hero (full-bleed photo) → 2-col body (sticky meta rail + prose) →
       CTA closer → more case studies → JSON-LD."""

    article_jsonld = _json_ld_block(_build_article_jsonld(study, lbl, lang, url_segment))
    breadcrumb_jsonld = _json_ld_block(_build_breadcrumb_jsonld(lbl, lang, url_segment, study))

    return (
        '<div class="case-study-wrap">'
        + _render_hero_stage(study, lbl, lang, url_segment)
        + _render_body_two_col(study, lbl, lang, url_segment, article_slug_map)
        + _render_cta_stage(lbl, lang)
        + _render_more_studies_stage(study, all_studies, lbl, lang, url_segment)
        + breadcrumb_jsonld
        + article_jsonld
        + '</div>'
    )


def _collect_categories(studies: list[dict]) -> list[tuple[str, str]]:
    """Unique (slug, display-name) pairs over the studies, preserving order."""
    categories: list[tuple[str, str]] = []
    seen: set[str] = set()
    for s in studies:
        slug = s.get("category_slug", "")
        if slug and slug not in seen:
            seen.add(slug)
            categories.append((slug, s.get("category", "") or slug))
    return categories


def _filter_dropdown_html(
    categories: list[tuple[str, str]], lbl: dict[str, str],
) -> tuple[str, str]:
    """Return (summary_swap_spans, radio_input_block) for the CSS-only
    category filter."""
    summary_swaps = (
        f'<span class="cs-dd-label cs-dd-label--all">{_esc(lbl["All categories"])}</span>'
        + "".join(
            f'<span class="cs-dd-label cs-dd-label--{_esc(slug)}">{_esc(name)}</span>'
            for slug, name in categories
        )
    )
    radio_options = (
        '<input type="radio" id="csf-all" name="csfilter" value="" checked>'
        f'<label for="csf-all">{_esc(lbl["All categories"])}</label>'
        + "".join(
            f'<input type="radio" id="csf-{_esc(slug)}" name="csfilter" value="{_esc(slug)}">'
            f'<label for="csf-{_esc(slug)}">{_esc(name)}</label>'
            for slug, name in categories
        )
    )
    return summary_swaps, radio_options


def _render_index_body(
    studies: list[dict], lbl: dict[str, str], lang: str, url_segment: str,
) -> str:
    """Hub page — full-bleed hero (uses first study's banner as bg),
    metrics-bar stage, filter-bar stage, banner-card grid stage, CTA."""
    breadcrumb = _render_breadcrumb(lbl, lang, url_segment)

    if not studies:
        return (
            '<div class="case-study-wrap">'
            '<section class="cs-stage cs-hero cs-hub-hero" data-stage>'
            '<div class="cs-stage-row">'
            + breadcrumb
            + f'<p class="cs-kicker">{_esc(lbl["eyebrow_plural"])}</p>'
            + f'<h1>{_esc(lbl["Case studies"])}</h1>'
            + f'<p class="cs-deck">{_esc(lbl["deck"])}</p>'
            + '</div></section></div>'
        )

    # Pick a hero banner from the first study so the hub feels editorial.
    hero_banner = studies[0].get("banner", "")

    categories = _collect_categories(studies)
    summary_swaps, radio_options = _filter_dropdown_html(categories, lbl)

    metric_items = "".join(
        '<div class="cs-hub-metric">'
        f'<dt>{_esc(label)}</dt>'
        f'<dd>{_esc(value)}</dd>'
        '</div>'
        for value, label in (
            (str(len(studies)), lbl["Case studies"]),
            (str(len(categories)), lbl["Categories"]),
            ("19 yrs", lbl.get("Years banking", "Banking + payments")),
            ("100%", lbl.get("No fabrication", "Verifiable — no fabrication")),
        )
    )

    hero_media = ""
    if hero_banner:
        hero_media = (
            '<figure class="cs-hero-media" aria-hidden="true">'
            f'<img alt="" src="{_esc(hero_banner)}" '
            'loading="eager" fetchpriority="high" decoding="async" '
            'width="1600" height="900">'
            '</figure>'
        )
    hero_stage = (
        '<section class="cs-stage cs-hero cs-hub-hero" data-stage>'
        + hero_media
        + '<div class="cs-stage-row">'
        '<div class="cs-hero-text">'
        + breadcrumb
        + f'<p class="cs-kicker">{_esc(lbl["eyebrow_plural"])}</p>'
        + f'<h1>{_esc(lbl["Case studies"])}</h1>'
        + f'<p class="cs-deck">{_esc(lbl["deck"])}</p>'
        + f'<a class="cs-hero-cta" href="#hub-grid">{_esc(lbl.get("Read case study", "Browse"))}</a>'
        + '</div></div>'
        + '</section>'
    )

    metrics_stage = (
        '<section class="cs-stage cs-hub-metrics-bar" data-stage '
        f'aria-label="{_esc(lbl["By the numbers"])}">'
        '<div class="cs-stage-row">'
        f'<dl class="cs-hub-metrics">{metric_items}</dl>'
        '</div></section>'
    )

    filter_bar = (
        '<section class="cs-stage cs-hub-filter" data-stage id="hub-grid">'
        '<div class="cs-stage-row">'
        # Filter is CSS-only via radio inputs + :has() — no form submission.
        # Using <form> here trips pa11y's H32.2 (no submit button); a
        # <div role="search"> carries the same semantics for AT users.
        '<div class="cs-filter-bar" role="search">'
        '<details class="cs-dropdown">'
        '<summary class="cs-dropdown-summary" '
        f'aria-label="{_esc(lbl["Filter by category"])}">'
        '<span class="cs-dd-prefix">' + _esc(lbl["Filter by category"]) + ':</span> '
        + summary_swaps
        + '</summary>'
        '<fieldset class="cs-dropdown-menu" role="radiogroup" '
        f'aria-label="{_esc(lbl["Filter by category"])}">'
        '<legend class="visually-hidden">'
        + _esc(lbl["Filter by category"]) +
        '</legend>'
        + radio_options
        + '</fieldset>'
        '</details>'
        + f'<span class="cs-filter-meta">{_esc(lbl["count"].format(n=len(studies)))}</span>'
        '</div>'
    )

    cards: list[str] = []
    for s in studies:
        slug = s["slug"]
        title = s.get("title", slug)
        kicker = s.get("kicker", lbl["eyebrow"])
        cat_slug = s.get("category_slug", "")
        problem = s.get("problem", "")
        excerpt = (problem.strip()[:200].rstrip() + "…") if problem else ""
        banner = s.get("banner", "")
        banner_alt = s.get("banner_alt", title)
        href = _study_url(lang, url_segment, slug)

        media_html = ""
        if banner:
            media_html = (
                f'<a class="cs-card-media" href="{href}" tabindex="-1" aria-hidden="true">'
                f'<img alt="{_esc(banner_alt)}" src="{_esc(banner)}" '
                'loading="lazy" decoding="async" width="800" height="500">'
                '</a>'
            )

        cards.append(
            f'<article data-category="{_esc(cat_slug)}">'
            + media_html
            + '<div class="cs-card-body">'
            + f'<p class="cs-card-kicker">{_esc(kicker)}</p>'
            + f'<h2 class="cs-card-title"><a href="{href}">{_esc(title)}</a></h2>'
            + f'<p class="cs-card-excerpt">{_esc(excerpt)}</p>'
            + '</div></article>'
        )

    # Close the filter section, then open a sibling grid stage so the
    # CSS :has() ~ filter selector can reach it without inline JS.
    grid = (
        '</div></section>'
        '<section class="cs-stage cs-grid-stage" data-stage>'
        '<div class="cs-stage-row">'
        f'<section class="cs-grid" aria-label="{_esc(lbl["Case studies"])}">'
        + "".join(cards) + '</section>'
        '</div></section>'
    )

    cta_stage = _render_cta_stage(lbl, lang)

    collection_jsonld = _json_ld_block(_build_collection_jsonld(studies, lbl, lang, url_segment))
    breadcrumb_jsonld = _json_ld_block(_build_breadcrumb_jsonld(lbl, lang, url_segment, None))

    return (
        '<div class="case-study-wrap">'
        + hero_stage
        + metrics_stage
        + filter_bar + grid
        + cta_stage
        + breadcrumb_jsonld
        + collection_jsonld
        + '</div>'
    )


def _swap_into_shell(shell: str, body: str, title: str, desc: str, url: str) -> str:
    out = _TITLE_RE.sub(f"<title>{_esc(title)}</title>", shell, count=1)
    out = _DESC_RE.sub(
        f'<meta name="description" content="{_esc(desc)}"', out, count=1
    )
    out = _CANONICAL_RE.sub(
        f'<link rel="canonical" href="{_esc(url)}"', out, count=1
    )
    out = _OG_TITLE_RE.sub(rf'\1{_esc(title)}\2', out, count=1)
    out = _OG_DESC_RE.sub(rf'\1{_esc(desc)}\2', out, count=1)
    out = _OG_URL_RE.sub(rf'\1{_esc(url)}\2', out, count=1)
    out = _AP_HERO_BLOCK_RE.sub("", out, count=1)
    out = _MAIN_WRAP_RE.sub(rf'\1{body}\2', out, count=1)
    return out


def _write_study(
    shell: str, study: dict, lang: str, url_segment: str,
    lbl: dict[str, str], out_dir: Path, article_slug_map: dict[str, str],
    all_studies: list[dict],
) -> Path:
    slug = study["slug"]
    title = study.get("title", slug)
    desc = (study.get("problem", "") or "")[:155]
    url = (
        f"{_BASE_URL}/case-studies/{slug}/"
        if lang == "en"
        else f"{_BASE_URL}/{lang}/{url_segment}/{slug}/"
    )
    body = _render_body(study, lbl, lang, url_segment, article_slug_map, all_studies)
    out = _swap_into_shell(shell, body, title, desc, url)
    target = out_dir / slug / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def _write_index(
    shell: str, studies: list[dict], lang: str, url_segment: str,
    lbl: dict[str, str], out_dir: Path,
) -> Path:
    body = _render_index_body(studies, lbl, lang, url_segment)
    url = (
        f"{_BASE_URL}/case-studies/"
        if lang == "en"
        else f"{_BASE_URL}/{lang}/{url_segment}/"
    )
    out = _swap_into_shell(
        shell, body,
        f"{lbl['Case studies']} — Sebastien Rousseau",
        lbl["deck"],
        url,
    )
    target = out_dir / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def _emit_one_locale(
    shell: str, studies: list[dict], lang: str, url_segment: str,
    lbl: dict[str, str], article_slug_map: dict[str, str],
) -> int:
    out_dir = OUT_DIR if lang == "en" else (PUBLIC / lang / url_segment)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Apply per-locale overlay to each study before rendering. EN passes
    # through unchanged (overlay loader returns {} for lang == 'en').
    localised_studies = [_localised_study(s, lang) for s in studies]
    for study in localised_studies:
        _write_study(shell, study, lang, url_segment, lbl, out_dir, article_slug_map, localised_studies)
    _write_index(shell, localised_studies, lang, url_segment, lbl, out_dir)
    return len(localised_studies) + 1


def _emit_locale_forks(studies: list[dict]) -> int:
    """For each active non-EN locale, fork the EN locale shell + run
    translate_chrome to localise nav / footer / search aria / lang switch
    on the case-study pages. Body text is rendered from the per-locale
    label table; YAML body content (Problem prose etc.) stays in EN."""
    sys.path.insert(0, str(ROOT / "scripts" / "lib"))
    sys.path.insert(0, str(ROOT / "scripts" / "generators"))
    try:
        import _lang_registry  # type: ignore[import-not-found]
        from build_translations import _chrome as _ch  # type: ignore[import-not-found]
        from build_translations import _state as _st  # type: ignore[import-not-found]
    except ImportError as exc:
        print(f"build_case_studies: skip locale forks — {exc}", file=sys.stderr)
        return 0

    en_shell = SHELL_SRC.read_text(encoding="utf-8")
    total = 0
    for lang in _lang_registry.active():
        if lang.code == "en":
            continue
        lbl = _lbl(lang.code)
        slugs_map = _lang_registry.load_slugs(lang.code)
        url_segment = slugs_map.get("static", {}).get("case-studies", "case-studies")
        article_slug_map = slugs_map.get("articles", {})
        _st.bind_lang(lang.code)
        # Render the case-study body in this locale (uses per-locale labels)
        # then run the same chrome translator the rest of the locale forks
        # use — nav, footer, search aria, lang switcher all localise.
        localised_shell = _ch._set_html_lang(en_shell)
        localised_shell = _ch.translate_chrome(localised_shell)
        # Rewrite every JSON-LD inLanguage="en"/"en-GB" → this locale's
        # BCP-47 tag so test_jsonld_localized.py passes for the locale forks.
        localised_shell = _ch._localize_inlanguage_globally(localised_shell, lang.code)
        total += _emit_one_locale(
            localised_shell, studies, lang.code, url_segment, lbl, article_slug_map
        )
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not SHELL_SRC.is_file():
        print(f"build_case_studies: missing shell {SHELL_SRC}", file=sys.stderr)
        return 0
    studies = _load_studies()
    shell = SHELL_SRC.read_text(encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    en_lbl = _lbl("en")
    en_count = _emit_one_locale(shell, studies, "en", "case-studies", en_lbl, {})
    locale_count = _emit_locale_forks(studies)
    print(
        f"build_case_studies: wrote {len(studies)} case studies + 1 index in EN "
        f"({en_count} files); {locale_count} files across 27 locale forks"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
