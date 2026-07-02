"""Case-study render components (leaf): reusable sub-renderers — breadcrumb,
meta bars, side panels, share rail, inline outcome/rigour/validation blocks,
pull-quotes, related-article links, and the _esc/_json_ld_block helpers.

Split from case_studies_render (Phase 4.1). Imports schema + share glyphs +
stdlib only; case_studies_render imports these components back (one-directional).
"""

from __future__ import annotations

import html as _html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from _svg_icons import _CARD_SVG_EMAIL, _CARD_SVG_FB, _CARD_SVG_LI, _CARD_SVG_X
from case_studies_schema import (
    _BASE_URL,
    _hub_url,
    _study_url,
)

ROOT = Path(__file__).resolve().parents[2]
def _esc(s: str) -> str:
    return _html.escape(str(s or ""), quote=True)
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
def _stage_no(n: int, label: str) -> str:
    """Numbered stage eyebrow — '01 — THE PROBLEM' style."""
    return (
        f'<p class="cs-stage-no">'
        f'<span aria-hidden="true">{n:02d} — </span>'
        f'{_esc(label.upper())}</p>'
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
_CONTACT_SLUG_CACHE: dict[str, str] = {}
def _contact_slug(lang: str) -> str:
    """Resolve the localised /contact/ URL segment from slugs.json. Falls
    back to 'contact' when the file or key is missing (EN + dev paths)."""
    if lang in _CONTACT_SLUG_CACHE:
        return _CONTACT_SLUG_CACHE[lang]
    slug_path = ROOT / "_data" / "i18n" / lang / "slugs.json"
    try:
        slug = json.loads(slug_path.read_text()).get("static", {}).get("contact", "contact")
    except (OSError, ValueError):
        slug = "contact"
    _CONTACT_SLUG_CACHE[lang] = slug
    return slug
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
def _stage_n(n: int) -> str:
    return f'<span aria-hidden="true">{n:02d} — </span>'
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
