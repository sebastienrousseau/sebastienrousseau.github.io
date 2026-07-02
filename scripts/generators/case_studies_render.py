"""Case-study HTML rendering (hero, stages, body, index, share, rails).

Leaf render module split from build_case_studies (Phase 4.1). Imports the URL +
JSON-LD helpers from case_studies_schema, share glyphs from _svg_icons, and
stdlib only — build_case_studies imports the render entry points back with no
cycle.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from case_studies_components import (
    _LINK_LABELS,
    _LINK_ORDER,
    _collect_categories,
    _contact_slug,
    _deck_html,
    _esc,
    _filter_dropdown_html,
    _json_ld_block,
    _prose_body_for,
    _prose_section,
    _related_article_href,
    _render_breadcrumb,
    _render_side_panel,
    _stage_n,
    _stage_no,
)
from case_studies_schema import (
    _build_article_jsonld,
    _build_breadcrumb_jsonld,
    _build_collection_jsonld,
    _study_url,
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
