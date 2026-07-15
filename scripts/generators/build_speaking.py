#!/usr/bin/env python3
"""Generate the ``/speaking/`` speaker page from ``_data/proof/speaking.md``.

All copy lives in the markdown source (frontmatter for the structured
sections, a markdown body for the biography prose) so it can be edited and
translated without touching Python. This generator forks the built
``/articles/index.html`` shell (so typography, CSP, SRI and the accessibility
profile stay identical to the rest of the site) and swaps in a body composed
of ``spk-``-prefixed sections styled by the layout's speaking CSS. Postbuild
then handles SEO / CSP / JSON-LD hashing.

Design follows the FT/Bloomberg-style speaker template, adapted to the site's
light+dark theme tokens; standards identifiers (ISO 20022, pacs.008, FIPS 203,
...) are set in monospace to enact "policy paper into inspectable code".

Output: ``public/speaking/index.html``
Input:  ``_data/proof/speaking.md``      (single source of truth, markdown)
        ``_data/proof/metrics.json``     (live KPI figures)
        ``public/articles/index.html``   (shell template)
"""

from __future__ import annotations

import html as _html
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    print("build_speaking: pyyaml not installed", file=sys.stderr)
    raise

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from build_case_studies import _swap_into_shell
from build_translations._fm import render_markdown
from case_studies_components import _esc

try:
    # Shared helper (hosted by build_case_studies): unescapes entity-escaped
    # <meta>/<link> tags, bounded to the <head>…</head> slice.
    from build_case_studies import _unescape_head_metas
except ImportError:  # pragma: no cover — local head-bounded copy until shared
    def _unescape_head_metas(html_text: str) -> str:
        """Repair entity-escaped ``<meta>`` / ``<link>`` tags some local SSG
        builds emit in the shell's <head>. No-op on CI (tags are real there).
        Bounded to the <head> slice so body prose is never unescaped."""
        end = html_text.find("</head>")
        if end < 0:
            return html_text
        head = re.sub(
            r"&lt;(?:meta|link)\b.*?&gt;",
            lambda m: _html.unescape(m.group(0)),
            html_text[:end],
            flags=re.DOTALL,
        )
        return head + html_text[end:]

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SPEAKING_MD = ROOT / "_data" / "proof" / "speaking.md"
SHELL_SRC = PUBLIC / "articles" / "index.html"
METRICS_JSON = ROOT / "_data" / "proof" / "metrics.json"
BASE_URL = "https://sebastienrousseau.com"
URL = f"{BASE_URL}/speaking/"

# Standards / regulatory identifiers rendered in monospace wherever they appear
# in prose. Longest-first so multi-token names match before their fragments.
_MONO_TERMS = sorted(
    [
        "ISO 20022", "pacs.008", "pain.001", "head.001", "FIPS 203", "NIST PQC",
        "SR 11-7", "SS1/23", "BIC/IBAN/LEI", "UETR", "WORM", "DORA", "SWIFT",
        "OAuth", "OPA", "BAH",
    ],
    key=len,
    reverse=True,
)
_MONO_RE = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in _MONO_TERMS) + r")\b")


def _mono(escaped: str) -> str:
    """Wrap known standards identifiers (already HTML-escaped) in ``.spk-mono``."""
    return _MONO_RE.sub(lambda m: f'<span class="spk-mono">{m.group(0)}</span>', escaped)


def _rich(text: str) -> str:
    """Escape prose then apply the monospace treatment to standards terms."""
    return _mono(_esc(text))


def _metrics() -> dict[str, str]:
    """Live KPI figures keyed by metric name, formatted for display."""
    try:
        raw = json.loads(METRICS_JSON.read_text(encoding="utf-8")).get("stats", [])
    except (OSError, ValueError) as exc:
        print(
            f"build_speaking: warning — could not read {METRICS_JSON}: {exc}; "
            "stats band will be dropped",
            file=sys.stderr,
        )
        return {}
    out: dict[str, str] = {}
    for s in raw:
        key = s.get("key")
        if not key:
            continue
        val, fmt = s.get("value"), s.get("format", "plain")
        if isinstance(val, (int, float)) and fmt == "compact":
            if val >= 1_000_000:
                out[key] = f"{val / 1_000_000:.0f}M"
            elif val >= 1_000:
                out[key] = f"{val / 1_000:.0f}K"
            else:
                out[key] = str(int(val))
        elif isinstance(val, (int, float)):
            out[key] = str(int(val))
        else:
            out[key] = str(val)
    return out


def _mark_nav_active(html_text: str) -> str:
    """Move the primary-nav active state from Articles onto Speaking.

    Fails loudly (SystemExit) if the Speaking anchor is missing so a
    nav-markup change in the shell can never silently ship a page without
    the active Speaking state. The Articles-deactivation step is optional:
    in a fresh build the raw ssg shell carries no aria-current at all
    (postbuild injects it), so its absence is normal, not an error."""
    out = html_text.replace(
        '<a href="/articles/index.html" aria-current="page" class="active">Articles</a>',
        '<a href="/articles/index.html">Articles</a>',
        1,
    )
    out2 = out.replace(
        '<a href="/speaking/index.html">Speaking</a>',
        '<a href="/speaking/index.html" aria-current="page" class="active">Speaking</a>',
        1,
    )
    if out2 == out:
        raise SystemExit(
            "build_speaking: nav marking failed — Speaking anchor not found "
            "in the shell (nav markup changed?)"
        )
    return out2


# ---------------------------------------------------------------------------
# Section renderers — each reads its slice of the parsed frontmatter (``d``)
# ---------------------------------------------------------------------------


def _section_head(eyebrow: str, headline: str, lede: str = "") -> str:
    lede_html = f'<p class="spk-lede">{_esc(lede)}</p>' if lede else ""
    return (
        '<div class="spk-head spk-center">'
        f'<span class="spk-eyebrow">{_esc(eyebrow)}</span>'
        f"<h2>{_esc(headline)}</h2>{lede_html}</div>"
    )


def _arrow() -> str:
    """Decorative CTA arrow, hidden from screen readers."""
    return '<span class="spk-arw" aria-hidden="true">&#8594;</span>'


def _micro_item(m: str) -> str:
    """Bold the leading word of a microproof item, keeping any trailing
    punctuation ([,.;:]) outside the <strong> wrap."""
    if " " not in m:
        return _esc(m)
    first, rest = m.split(" ", 1)
    punct = re.match(r"^(.*?)([,.;:]+)$", first)
    if punct:
        return f"<strong>{_esc(punct.group(1))}</strong>{_esc(punct.group(2))} {_esc(rest)}"
    return f"<strong>{_esc(first)}</strong> {_esc(rest)}"


def _hero(d: dict, booking: str) -> str:
    h = d.get("hero", {}) or {}
    micro = " · ".join(_micro_item(m) for m in (h.get("microproof") or []))
    bio = d.get("biography", {}) or {}
    portrait = bio.get("portrait", "")
    photo = (
        f'<div class="spk-hero-photo"><img src="{_esc(portrait)}" '
        f'alt="{_esc(bio.get("portrait_alt", ""))}" width="440" height="550" '
        'fetchpriority="high" decoding="async" /></div>'
        if portrait else ""
    )
    nudge_txt = h.get("press_nudge", "")
    nudge_cta = h.get("press_nudge_cta", "")
    nudge_link = (
        f' <a href="#spk-media" class="spk-textlink">{_esc(nudge_cta)} '
        '<span aria-hidden="true">&#8594;</span></a>'
        if nudge_cta else ""
    )
    nudge_html = (
        f'<p class="spk-press-nudge">{_esc(nudge_txt)}{nudge_link}</p>'
        if (nudge_txt or nudge_cta) else ""
    )
    return (
        '<header class="spk-hero" id="spk-top"><div class="spk-hero-grid"><div>'
        f'<span class="spk-eyebrow">{_esc(h.get("eyebrow", ""))}</span>'
        f'<h1>{_esc(h.get("headline", ""))}</h1>'
        f'<p class="spk-lede">{_esc(h.get("lede", ""))}</p>'
        '<div class="spk-cta-row">'
        f'<a href="{_esc(booking)}" class="spk-btn spk-btn-primary">'
        f'{_esc(h.get("primary_cta", "Invite me to speak"))} {_arrow()}</a>'
        f'<a href="#spk-keynotes" class="spk-btn spk-btn-ghost">{_esc(h.get("secondary_cta", "Explore keynotes"))}</a>'
        "</div>"
        f"{nudge_html}"
        f'<p class="spk-microproof">{micro}</p>'
        f"</div>{photo}</div></header>"
    )


def _employers(d: dict) -> str:
    names = d.get("employers") or []
    if not names:
        return ""
    logos = "".join(f"<span>{_esc(n)}</span>" for n in names)
    return (
        '<div class="spk-wrap"><div class="spk-strip">'
        f'<div class="spk-strip-label">{_esc(d.get("employers_label", ""))}</div>'
        f'<div class="spk-logos">{logos}</div></div></div>'
    )


def _stats(d: dict) -> str:
    rows = d.get("stats") or []
    if not rows:
        return ""
    metrics = _metrics()
    parts = []
    for r in rows:
        kpi = r.get("kpi")
        if kpi not in metrics:
            print(
                f"build_speaking: warning — stats row dropped, unknown kpi "
                f"{kpi!r} (label {r.get('label', '')!r}) not in metrics.json",
                file=sys.stderr,
            )
            continue
        parts.append(
            f'<div class="spk-stat"><div class="spk-num">{_esc(metrics[kpi])}</div>'
            f'<div class="spk-lbl">{_esc(r.get("label", ""))}</div></div>'
        )
    cells = "".join(parts)
    if not cells:
        return ""
    eyebrow = d.get("stats_eyebrow", "")
    eyebrow_html = f'<span class="spk-eyebrow">{_esc(eyebrow)}</span>' if eyebrow else ""
    foot = d.get("stats_foot", "")
    foot_html = f'<p class="spk-stats-foot">{_rich(foot)}</p>' if foot else ""
    return (
        '<section class="spk-band"><div class="spk-wrap">'
        f'{eyebrow_html}<div class="spk-stats">{cells}</div>{foot_html}</div></section>'
    )


def _paths(d: dict, booking: str) -> str:
    p = d.get("paths", {}) or {}
    items = p.get("items") or []
    if not items:
        return ""
    targets = {"book": booking, "media": "#spk-media", "keynotes": "#spk-keynotes"}
    cards = []
    for i, it in enumerate(items):
        bullets = "".join(f"<li>{_esc(b)}</li>" for b in (it.get("bullets") or []))
        href = targets.get(it.get("cta_target", ""), booking)
        primary = "spk-btn-primary" if i == 0 else "spk-btn-ghost"
        cards.append(
            '<div class="spk-path">'
            f'<span class="spk-eyebrow">{_esc(it.get("eyebrow", ""))}</span>'
            f'<h3>{_esc(it.get("title", ""))}</h3>'
            f'<p>{_esc(it.get("body", ""))}</p>'
            f"<ul>{bullets}</ul>"
            f'<a href="{_esc(href)}" class="spk-btn {primary}">{_esc(it.get("cta_label", ""))}</a>'
            "</div>"
        )
    return (
        '<section id="spk-paths"><div class="spk-wrap">'
        + _section_head(p.get("eyebrow", ""), p.get("headline", ""), p.get("lede", ""))
        + f'<div class="spk-paths">{"".join(cards)}</div></div></section>'
    )


def _keynotes(d: dict, booking: str) -> str:
    k = d.get("keynotes", {}) or {}
    talks = k.get("talks") or []
    if not talks:
        return ""
    out_label = k.get("outcome_label", "You leave with:")
    audience_label = d.get("audience_label", "For:")
    flag_new, flag_del = k.get("flag_new", "New"), k.get("flag_delivered", "Available now")
    cards = []
    for t in talks:
        is_new = bool(t.get("new"))
        flag_cls = "spk-flag spk-flag-new" if is_new else "spk-flag"
        flag_txt = flag_new if is_new else flag_del
        cards.append(
            '<article class="spk-talk">'
            f'<div class="{flag_cls}">{_esc(flag_txt)}</div>'
            f'<h3>{_esc(t.get("title", ""))}</h3>'
            f'<p class="spk-desc">{_rich(t.get("desc", ""))}</p>'
            f'<p class="spk-outcome"><b>{_esc(out_label)}</b> {_rich(t.get("outcome", ""))}</p>'
            '<div class="spk-talk-foot">'
            f'<div class="spk-audience">{_esc(audience_label)} {_esc(t.get("audience", ""))}</div>'
            "</div></article>"
        )
    custom = k.get("custom", {}) or {}
    if custom.get("title"):
        cards.append(
            '<article class="spk-talk spk-talk-cta">'
            f'<h3>{_esc(custom.get("title", ""))}</h3>'
            f'<p class="spk-desc">{_esc(custom.get("body", ""))}</p>'
            f'<a href="{_esc(booking)}" class="spk-btn spk-btn-primary">'
            f'{_esc(custom.get("cta_label", ""))} {_arrow()}</a>'
            "</article>"
        )
    return (
        '<section class="spk-band" id="spk-keynotes"><div class="spk-wrap">'
        + _section_head(k.get("eyebrow", ""), k.get("headline", ""), k.get("lede", ""))
        + f'<div class="spk-talks">{"".join(cards)}</div></div></section>'
    )


def _work(d: dict) -> str:
    w = d.get("work", {}) or {}
    formats = w.get("formats") or []
    if not formats:
        return ""
    fmt_cards = "".join(
        '<div class="spk-format">'
        f'<h3>{_esc(f.get("name", ""))}</h3>'
        f'<div class="spk-dur">{_esc(f.get("duration", ""))}</div>'
        f'<p>{_esc(f.get("body", ""))}</p></div>'
        for f in formats
    )
    reach = "".join(f'<span class="spk-chip">{_esc(r)}</span>' for r in (w.get("reach") or []))
    reach_html = f'<div class="spk-locs">{reach}</div>' if reach else ""
    return (
        '<section id="spk-work"><div class="spk-wrap">'
        + _section_head(w.get("eyebrow", ""), w.get("headline", ""))
        + f'<div class="spk-formats">{fmt_cards}</div>{reach_html}</div></section>'
    )


def _media(d: dict, booking: str) -> str:
    m = d.get("media", {}) or {}
    topics = m.get("topics") or []
    if not topics:
        return ""
    spec = "<br>".join(f"// {_esc(s)}" for s in (m.get("spec") or []))
    spec_html = f'<div class="spk-spec">{spec}</div>' if spec else ""
    topic_items = "".join(
        f'<li><span class="spk-tag">{_esc(t.get("tag", ""))}</span>{_rich(t.get("text", ""))}</li>'
        for t in topics
    )
    return (
        '<section id="spk-media"><div class="spk-wrap"><div class="spk-media">'
        f'<span class="spk-eyebrow">{_esc(m.get("eyebrow", ""))}</span>'
        f'<h2>{_esc(m.get("headline", ""))}</h2>'
        '<div class="spk-media-grid"><div>'
        f'<span class="spk-avail"><span class="spk-dot"></span>{_esc(m.get("availability", ""))}</span>'
        f'<p>{_esc(m.get("body", ""))}</p>{spec_html}'
        '<div class="spk-media-actions">'
        f'<a href="{_esc(booking)}" class="spk-btn spk-btn-onblue">{_esc(m.get("cta_label", "Book expert comment"))}</a>'
        "</div></div>"
        f'<div><ul class="spk-media-topics">{topic_items}</ul></div>'
        "</div></div></div></section>"
    )


def _biography(d: dict, bio_html: str) -> str:
    b = d.get("biography", {}) or {}
    if not bio_html.strip():
        return ""
    portrait = b.get("portrait", "")
    photo = (
        f'<div class="spk-bio-photo"><img src="{_esc(portrait)}" '
        f'alt="{_esc(b.get("portrait_alt", ""))}" width="220" height="220" '
        'loading="lazy" decoding="async" /></div>'
        if portrait else ""
    )
    return (
        '<section class="spk-band" id="spk-bio"><div class="spk-wrap">'
        + _section_head(b.get("eyebrow", ""), b.get("headline", ""))
        + f'<div class="spk-bio-grid">{photo}<div class="spk-bio-body">{bio_html}</div></div>'
        "</div></section>"
    )


def _bios(d: dict) -> str:
    b = d.get("bios", {}) or {}
    items = b.get("items") or []
    if not items:
        return ""
    copy_label = b.get("copy_label", "Copy")
    aria_tpl = d.get("bio_copy_aria", "{length} bio, copy")
    cards = []
    for i, it in enumerate(items, 1):
        length = it.get("length", "")
        # Index-based id: stable and valid whatever the localised label is
        # (spaces / non-ASCII / duplicates would break an id derived from it).
        bid = f"spk-bio-{i}"
        aria = aria_tpl.replace("{length}", length)
        cards.append(
            '<div class="spk-biocard">'
            f'<div class="spk-len">{_esc(length)}</div>'
            f'<button type="button" class="spk-copybtn copy-btn" data-copy="#{bid}" '
            f'aria-label="{_esc(aria)}">{_esc(copy_label)}</button>'
            f'<p id="{bid}">{_esc(it.get("text", ""))}</p>'
            "</div>"
        )
    return (
        '<section id="spk-readybio"><div class="spk-wrap">'
        + _section_head(b.get("eyebrow", ""), b.get("headline", ""), b.get("lede", ""))
        + f'<div class="spk-bios">{"".join(cards)}</div></div></section>'
    )


def _faq(d: dict) -> str:
    f = d.get("faq", {}) or {}
    items = f.get("items") or []
    if not items:
        return ""
    rows = "".join(
        "<details><summary>"
        f'{_esc(it.get("q", ""))} <span class="spk-ic" aria-hidden="true">+</span></summary>'
        f'<div class="spk-ans">{_rich(it.get("a", ""))}</div></details>'
        for it in items
    )
    return (
        '<section class="spk-band" id="spk-faq"><div class="spk-wrap">'
        + _section_head(f.get("eyebrow", ""), f.get("headline", ""))
        + f'<div class="spk-faq">{rows}</div></div></section>'
    )


def _booking(d: dict, booking: str) -> str:
    b = d.get("book", {}) or {}
    if not b:
        return ""
    facts = "".join(
        f'<li><span>{_esc(x.get("k", ""))}</span><b>{_esc(x.get("v", ""))}</b></li>'
        for x in (b.get("aside_facts") or [])
    )
    aside = (
        '<aside class="spk-book-aside">'
        f'<span class="spk-eyebrow">{_esc(b.get("aside_eyebrow", ""))}</span>'
        f'<h3>{_esc(b.get("aside_title", ""))}</h3>'
        f'<p>{_esc(b.get("aside_body", ""))}</p>'
        f'<span class="spk-avail"><span class="spk-dot spk-dot-static"></span>{_esc(b.get("aside_availability", ""))}</span>'
        f'<ul class="spk-aside-list">{facts}</ul></aside>'
    )
    intro = (
        '<div class="spk-book-intro">'
        f'<span class="spk-eyebrow">{_esc(b.get("eyebrow", ""))}</span>'
        f'<h2>{_esc(b.get("headline", ""))}</h2>'
        f'<p class="spk-lede">{_esc(b.get("lede", ""))}</p>'
        f'<a href="{_esc(booking)}" class="spk-btn spk-btn-primary">'
        f'{_esc(b.get("cta_label", "Invite me to speak"))} {_arrow()}</a>'
        "</div>"
    )
    return (
        '<section id="spk-book"><div class="spk-wrap">'
        f'<div class="spk-booking-grid">{intro}{aside}</div></div></section>'
    )


def _final_cta(d: dict, booking: str) -> str:
    c = d.get("final_cta", {}) or {}
    if not c:
        return ""
    return (
        '<section class="spk-band spk-finalcta"><div class="spk-wrap">'
        f'<h2>{_esc(c.get("headline", ""))}</h2>'
        f'<p class="spk-lede">{_esc(c.get("lede", ""))}</p>'
        '<div class="spk-cta-row">'
        f'<a href="{_esc(booking)}" class="spk-btn spk-btn-primary">'
        f'{_esc(c.get("primary_cta", ""))} {_arrow()}</a>'
        f'<a href="#spk-media" class="spk-btn spk-btn-ghost">{_esc(c.get("secondary_cta", ""))}</a>'
        "</div></div></section>"
    )


def _jsonld_script(payload: dict) -> str:
    """Serialise ``payload`` into a JSON-LD <script>, escaping ``</`` so the
    JSON can never terminate the script element early."""
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (
        '<script type="application/ld+json">'
        + blob.replace("</", "<\\/")
        + "</script>"
    )


def _topics_jsonld(d: dict) -> str:
    talks = (d.get("keynotes", {}) or {}).get("talks") or []
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": t.get("title", ""),
            "description": t.get("desc", "").strip(),
        }
        for i, t in enumerate(talks)
        if t.get("title")
    ]
    if not items:
        return ""
    payload = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": d.get("topics_jsonld_name", "Speaking topics by Sebastien Rousseau"),
        "itemListElement": items,
    }
    return _jsonld_script(payload)


def _breadcrumbs_jsonld(d: dict, url: str) -> str:
    """Home > Speaking breadcrumb trail for this page (replaces the articles
    hub's stale CollectionPage/BreadcrumbList graph, which is stripped)."""
    payload = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": d.get("breadcrumb_home", "Home"),
                "item": f"{BASE_URL}/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": d.get("title") or "Speaking",
                "item": url,
            },
        ],
    }
    return _jsonld_script(payload)


def _render_body(d: dict, bio_html: str, url: str) -> str:
    """Assemble the speaking page body from its sections (empties dropped)."""
    booking = d.get("booking_url") or "/contact/index.html"
    sections = [
        _hero(d, booking),
        _employers(d),
        _stats(d),
        _paths(d, booking),
        _keynotes(d, booking),
        _work(d),
        _media(d, booking),
        _biography(d, bio_html),
        _bios(d),
        _faq(d),
        _booking(d, booking),
        _final_cta(d, booking),
        _topics_jsonld(d),
        _breadcrumbs_jsonld(d, url),
    ]
    return '<div class="speaking-page">' + "".join(s for s in sections if s) + "</div>"


# Frontmatter split on ``---`` *delimiter lines* only (not substrings, so
# ``# --- Hero`` section comments inside the frontmatter don't break the
# parse). Tolerates a leading BOM and CRLF line endings.
_FM_RE = re.compile(
    "^\ufeff?" + r"---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n(.*)$", re.DOTALL
)


def _parse_source() -> tuple[dict, str]:
    """Split ``speaking.md`` into (frontmatter dict, rendered biography HTML).

    Fails loudly (SystemExit) on a malformed source rather than shipping a
    hollow page: a missed frontmatter split or empty markdown body would
    otherwise render an empty shell and exit 0."""
    raw = SPEAKING_MD.read_text(encoding="utf-8")
    m = _FM_RE.match(raw)
    if not m:
        raise SystemExit(
            f"build_speaking: cannot parse {SPEAKING_MD} — frontmatter "
            "delimiters ('---' lines) not found"
        )
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        raise SystemExit(
            f"build_speaking: invalid YAML in {SPEAKING_MD}: {exc}"
        ) from exc
    body_md = m.group(2).strip()
    if not data or not body_md:
        raise SystemExit(
            f"build_speaking: {SPEAKING_MD} parsed to an empty "
            f"{'frontmatter' if not data else 'markdown body'} — refusing to "
            "ship a hollow page"
        )
    return data, render_markdown(body_md)


def _load_overlay(lang: str, data: dict, bio_html: str) -> tuple[dict, str]:
    """Per-locale content overlay. If ``_data/proof/i18n/<lang>/speaking.md``
    exists, parse it and use its (frontmatter, body); otherwise fall back to
    English. This is the progressive-backfill hook: locales without an overlay
    ship the English body under a localised chrome (nav / footer / lang tag).
    A malformed overlay warns loudly and falls back to English (not fatal:
    progressive backfill is by design)."""
    overlay = ROOT / "_data" / "proof" / "i18n" / lang / "speaking.md"
    if not overlay.is_file():
        return data, bio_html
    raw = overlay.read_text(encoding="utf-8")
    m = _FM_RE.match(raw)
    if not m:
        print(
            f"build_speaking: warning — malformed overlay {overlay} "
            "(frontmatter delimiters not found); shipping English content "
            f"for '{lang}'",
            file=sys.stderr,
        )
        return data, bio_html
    try:
        overlay_data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        print(
            f"build_speaking: warning — invalid YAML in overlay {overlay} "
            f"({exc}); shipping English content for '{lang}'",
            file=sys.stderr,
        )
        return data, bio_html
    loc = {**data, **overlay_data}
    loc_bio = render_markdown(m.group(2).strip()) or bio_html
    return loc, loc_bio


def _meta_description(text: str, limit: int = 200) -> str:
    """Meta description trimmed to ``limit`` chars at a word boundary, with
    trailing punctuation / whitespace stripped from a truncated result."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" \t,.;:!?")


def _localize_static_hrefs(body: str, lang: str, static_slugs: dict[str, str]) -> str:
    """Rewrite body links to top-level EN static pages (``/contact/index.html``)
    onto the locale's slugged path (``/ar/ittisal/index.html``) using the
    locale's ``slugs.json`` "static" map. Links not in the map pass through."""
    def repl(m: re.Match) -> str:
        slug = static_slugs.get(m.group(1))
        return f'href="/{lang}/{slug}/index.html"' if slug else m.group(0)

    return re.sub(r'href="/([a-z0-9-]+)/index\.html"', repl, body)


def _dedupe_named_meta(head: str, name: str, replacement: str | None) -> str:
    """Keep exactly one ``<meta name=...>`` in the head slice: the first
    occurrence (rewritten to ``replacement`` when given, kept verbatim when
    ``None``); every later duplicate is dropped. Fails loudly if absent."""
    matches = list(re.finditer(rf'<meta name="{re.escape(name)}"[^>]*>', head))
    if not matches:
        raise SystemExit(
            f'build_speaking: head patch failed — no <meta name="{name}"> in shell head'
        )
    parts, last = [], 0
    for i, m in enumerate(matches):
        parts.append(head[last:m.start()])
        if i == 0:
            parts.append(replacement if replacement is not None else m.group(0))
        last = m.end()
    parts.append(head[last:])
    return "".join(parts)


def _patch_head(out: str, doc_title: str, seo_title: str, desc: str) -> str:
    """Repair the forked articles-shell <head> for the speaking page: dedupe
    description / viewport / theme-color metas, retitle the document from the
    frontmatter ``title``, and replace the stale articles twitter / Apple
    web-app copy. Every mutation verifies it matched, raising SystemExit."""
    end = out.find("</head>")
    if end == -1:
        raise SystemExit("build_speaking: head patch failed — no </head> in shell")
    head, rest = out[:end], out[end:]

    head, n = re.subn(
        r"<title>.*?</title>",
        lambda _m: f"<title>{_esc(doc_title)}</title>",
        head,
        count=1,
        flags=re.DOTALL,
    )
    if not n:
        raise SystemExit("build_speaking: head patch failed — <title> not found")

    # Exactly one description (the speaking one) and one viewport; the
    # theme-color light/dark pair is one *set*, deduped per media condition.
    head = _dedupe_named_meta(
        head, "description", f'<meta name="description" content="{_esc(desc)}">'
    )
    head = _dedupe_named_meta(head, "viewport", None)
    seen_theme: set[str] = set()

    def _theme_once(m: re.Match) -> str:
        tag = m.group(0)
        if tag in seen_theme:
            return ""
        seen_theme.add(tag)
        return tag

    head = re.sub(r'<meta name="theme-color"[^>]*>', _theme_once, head)

    head, n = re.subn(
        r'(<meta name="twitter:title" content=")[^"]*(")',
        lambda m: m.group(1) + _esc(seo_title) + m.group(2),
        head,
        count=1,
    )
    if not n:
        raise SystemExit("build_speaking: head patch failed — twitter:title not found")
    head, n = re.subn(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        lambda m: m.group(1) + _esc(desc) + m.group(2),
        head,
        count=1,
    )
    if not n:
        raise SystemExit(
            "build_speaking: head patch failed — twitter:description not found"
        )
    # Stale articles-hub web-app title; tolerate absence (nothing stale then).
    head = re.sub(
        r'(<meta name="apple-mobile-web-app-title" content=")[^"]*(")',
        lambda m: m.group(1) + "Sebastien Rousseau" + m.group(2),
        head,
        count=1,
    )
    if "Discover How Technology" in head:
        raise SystemExit(
            "build_speaking: head patch failed — stale articles copy left in <head>"
        )
    return head + rest


# The articles hub ships a CollectionPage + BreadcrumbList @graph that is
# wrong for /speaking/; it is removed and replaced by the page's own
# BreadcrumbList (see _breadcrumbs_jsonld). Tempered dot so the match can
# never run past this script element; tolerates minified or pretty JSON.
_ARTICLES_JSONLD_RE = re.compile(
    r'[ \t]*<script type="application/ld\+json">'
    r'(?:(?!</script>).)*?"@type":\s*"CollectionPage"(?:(?!</script>).)*?'
    r"</script>\n?",
    re.DOTALL,
)


def _strip_articles_jsonld(out: str) -> str:
    new, n = _ARTICLES_JSONLD_RE.subn("", out)
    if not n:
        raise SystemExit(
            "build_speaking: articles CollectionPage JSON-LD not found — "
            "shell layout changed?"
        )
    return new


def _emit_one_locale(
    active_shell: str,
    data: dict,
    bio_html: str,
    lang: str,
    segment: str,
    static_slugs: dict[str, str] | None = None,
) -> None:
    """Render and write the speaking page for one locale. ``active_shell`` is the
    EN articles shell with the Speaking nav item already marked active (and, for
    non-EN, already run through translate_chrome)."""
    url = URL if lang == "en" else f"{BASE_URL}/{lang}/{segment}/"
    body = _render_body(data, bio_html, url)
    if lang != "en" and static_slugs:
        body = _localize_static_hrefs(body, lang, static_slugs)
    seo_title = data.get("meta_title") or "Speaking & advisory: Sebastien Rousseau"
    doc_title = data.get("title") or seo_title
    desc = _meta_description(data.get("meta_description") or "")

    out = _swap_into_shell(active_shell, body, seo_title, desc, url)
    if '<div class="speaking-page">' not in out:
        raise SystemExit(
            f"build_speaking: body swap failed for '{lang}' — speaking body "
            "missing from output (shell <main> markup changed?)"
        )
    out = _unescape_head_metas(out)  # head-bounded by the shared helper
    out = _patch_head(out, doc_title, seo_title, desc)
    out = _strip_articles_jsonld(out)
    if "Discover How Technology" in out:
        raise SystemExit(
            f"build_speaking: stale articles copy remains in the '{lang}' page"
        )

    target = (PUBLIC / "speaking" if lang == "en" else PUBLIC / lang / segment) / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")


def _emit_locale_forks(active_shell: str, data: dict, bio_html: str) -> int:
    """For each active non-EN locale, fork the nav-active EN shell, localise its
    chrome (nav / footer / search aria / lang switch / JSON-LD inLanguage), and
    write the speaking page under ``/<lang>/<segment>/``. Body content is the
    per-locale overlay when present, else English (progressive backfill)."""
    sys.path.insert(0, str(ROOT / "scripts" / "lib"))
    try:
        import _lang_registry  # type: ignore[import-not-found]
        from build_translations import _chrome as _ch  # type: ignore[import-not-found]
        from build_translations import _state as _st  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        print(f"build_speaking: skip locale forks — {exc}", file=sys.stderr)
        return 0

    total = 0
    for lang in _lang_registry.active():
        if lang.code == "en":
            continue
        static_slugs = _lang_registry.load_slugs(lang.code).get("static", {})
        segment = static_slugs.get("speaking", "speaking")
        _st.bind_lang(lang.code)
        loc_shell = _ch._set_html_lang(active_shell)
        loc_shell = _ch.translate_chrome(loc_shell)
        loc_shell = _ch._localize_inlanguage_globally(loc_shell, lang.code)
        loc_data, loc_bio = _load_overlay(lang.code, data, bio_html)
        _emit_one_locale(loc_shell, loc_data, loc_bio, lang.code, segment, static_slugs)
        total += 1
    return total


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_speaking: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    if not SPEAKING_MD.is_file():
        print(f"build_speaking: {SPEAKING_MD} missing", file=sys.stderr)
        return 1

    data, bio_html = _parse_source()
    # Mark the Speaking nav item active once on the EN shell; translate_chrome
    # then localises the href/label per locale while preserving the active state.
    active_shell = _mark_nav_active(SHELL_SRC.read_text(encoding="utf-8"))
    _emit_one_locale(active_shell, data, bio_html, "en", "speaking")
    locales = _emit_locale_forks(active_shell, data, bio_html)
    print(f"build_speaking: wrote public/speaking/index.html + {locales} locale forks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
