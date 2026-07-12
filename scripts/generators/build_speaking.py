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
_MONO_RE = re.compile("|".join(re.escape(t) for t in _MONO_TERMS))


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
    except (OSError, ValueError):
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


def _unescape_head_metas(html_text: str) -> str:
    """Repair entity-escaped ``<meta>`` / ``<link>`` tags some local SSG builds
    emit in the shell's <head>. No-op on CI (tags are already real there)."""
    return re.sub(
        r"&lt;(?:meta|link)\b.*?&gt;",
        lambda m: _html.unescape(m.group(0)),
        html_text,
        flags=re.DOTALL,
    )


def _mark_nav_active(html_text: str) -> str:
    """Move the primary-nav active state from Articles onto Speaking."""
    out = html_text.replace(
        '<a href="/articles/index.html" aria-current="page" class="active">Articles</a>',
        '<a href="/articles/index.html">Articles</a>',
        1,
    )
    return out.replace(
        '<a href="/speaking/index.html">Speaking</a>',
        '<a href="/speaking/index.html" aria-current="page" class="active">Speaking</a>',
        1,
    )


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


def _hero(d: dict, booking: str) -> str:
    h = d.get("hero", {}) or {}
    micro = " · ".join(
        f"<strong>{_esc(m.split(' ', 1)[0])}</strong> {_esc(m.split(' ', 1)[1])}"
        if " " in m else _esc(m)
        for m in (h.get("microproof") or [])
    )
    bio = d.get("biography", {}) or {}
    portrait = bio.get("portrait", "")
    photo = (
        f'<div class="spk-hero-photo"><img src="{_esc(portrait)}" '
        f'alt="{_esc(bio.get("portrait_alt", ""))}" width="440" height="550" '
        'fetchpriority="high" decoding="async" /></div>'
        if portrait else ""
    )
    return (
        '<header class="spk-hero" id="spk-top"><div class="spk-hero-grid"><div>'
        f'<span class="spk-eyebrow">{_esc(h.get("eyebrow", ""))}</span>'
        f'<h1>{_esc(h.get("headline", ""))}</h1>'
        f'<p class="spk-lede">{_esc(h.get("lede", ""))}</p>'
        '<div class="spk-cta-row">'
        f'<a href="{_esc(booking)}" class="spk-btn spk-btn-primary">'
        f'{_esc(h.get("primary_cta", "Invite me to speak"))} <span class="spk-arw">&#8594;</span></a>'
        f'<a href="#spk-keynotes" class="spk-btn spk-btn-ghost">{_esc(h.get("secondary_cta", "Explore keynotes"))}</a>'
        "</div>"
        f'<p class="spk-press-nudge">{_esc(h.get("press_nudge", ""))} '
        f'<a href="#spk-media" class="spk-textlink">{_esc(h.get("press_nudge_cta", ""))} &#8594;</a></p>'
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
    cells = "".join(
        f'<div class="spk-stat"><div class="spk-num">{_esc(metrics[r["kpi"]])}</div>'
        f'<div class="spk-lbl">{_esc(r.get("label", ""))}</div></div>'
        for r in rows
        if r.get("kpi") in metrics
    )
    if not cells:
        return ""
    foot = d.get("stats_foot", "")
    foot_html = f'<p class="spk-stats-foot">{_rich(foot)}</p>' if foot else ""
    return (
        '<section class="spk-band"><div class="spk-wrap">'
        f'<div class="spk-stats">{cells}</div>{foot_html}</div></section>'
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
            f'<div class="spk-audience">For: {_esc(t.get("audience", ""))}</div>'
            "</div></article>"
        )
    custom = k.get("custom", {}) or {}
    if custom.get("title"):
        cards.append(
            '<article class="spk-talk spk-talk-cta">'
            f'<h3>{_esc(custom.get("title", ""))}</h3>'
            f'<p class="spk-desc">{_esc(custom.get("body", ""))}</p>'
            f'<a href="{_esc(booking)}" class="spk-btn spk-btn-primary">'
            f'{_esc(custom.get("cta_label", ""))} <span class="spk-arw">&#8594;</span></a>'
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
    cards = []
    for it in items:
        length = it.get("length", "")
        bid = f"spk-bio-{length.lower()}"
        cards.append(
            '<div class="spk-biocard">'
            f'<div class="spk-len">{_esc(length)}</div>'
            f'<button type="button" class="spk-copybtn copy-btn" data-copy="#{bid}" '
            f'aria-label="{_esc(length)} bio, copy">{_esc(copy_label)}</button>'
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
        f'{_esc(it.get("q", ""))} <span class="spk-ic">+</span></summary>'
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
        f'{_esc(b.get("cta_label", "Invite me to speak"))} <span class="spk-arw">&#8594;</span></a>'
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
        f'{_esc(c.get("primary_cta", ""))} <span class="spk-arw">&#8594;</span></a>'
        f'<a href="#spk-media" class="spk-btn spk-btn-ghost">{_esc(c.get("secondary_cta", ""))}</a>'
        "</div></div></section>"
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
    payload = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Speaking topics by Sebastien Rousseau",
        "itemListElement": items,
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )


def _render_body(d: dict, bio_html: str) -> str:
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
    ]
    return '<div class="speaking-page">' + "".join(s for s in sections if s) + "</div>"


def _parse_source() -> tuple[dict, str]:
    """Split ``speaking.md`` into (frontmatter dict, rendered biography HTML).

    Splits on the ``---`` *delimiter lines* only (not substrings, so ``# --- Hero``
    section comments inside the frontmatter don't break the parse)."""
    raw = SPEAKING_MD.read_text(encoding="utf-8")
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n(.*)$", raw, re.DOTALL)
    if not m:
        return {}, ""
    data = yaml.safe_load(m.group(1)) or {}
    bio_html = render_markdown(m.group(2).strip())
    return data, bio_html


def _load_overlay(lang: str, data: dict, bio_html: str) -> tuple[dict, str]:
    """Per-locale content overlay. If ``_data/proof/i18n/<lang>/speaking.md``
    exists, parse it and use its (frontmatter, body); otherwise fall back to
    English. This is the progressive-backfill hook: locales without an overlay
    ship the English body under a localised chrome (nav / footer / lang tag)."""
    overlay = ROOT / "_data" / "proof" / "i18n" / lang / "speaking.md"
    if not overlay.is_file():
        return data, bio_html
    raw = overlay.read_text(encoding="utf-8")
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n(.*)$", raw, re.DOTALL)
    if not m:
        return data, bio_html
    loc = {**data, **(yaml.safe_load(m.group(1)) or {})}
    loc_bio = render_markdown(m.group(2).strip()) or bio_html
    return loc, loc_bio


def _emit_one_locale(active_shell: str, data: dict, bio_html: str, lang: str, segment: str) -> None:
    """Render and write the speaking page for one locale. ``active_shell`` is the
    EN articles shell with the Speaking nav item already marked active (and, for
    non-EN, already run through translate_chrome)."""
    body = _render_body(data, bio_html)
    title = data.get("meta_title") or "Speaking & advisory: Sebastien Rousseau"
    desc = (data.get("meta_description") or "").strip()[:200]
    url = URL if lang == "en" else f"{BASE_URL}/{lang}/{segment}/"
    out = _swap_into_shell(active_shell, body, title, desc, url)
    out = _unescape_head_metas(out)
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
        segment = _lang_registry.load_slugs(lang.code).get("static", {}).get("speaking", "speaking")
        _st.bind_lang(lang.code)
        loc_shell = _ch._set_html_lang(active_shell)
        loc_shell = _ch.translate_chrome(loc_shell)
        loc_shell = _ch._localize_inlanguage_globally(loc_shell, lang.code)
        loc_data, loc_bio = _load_overlay(lang.code, data, bio_html)
        _emit_one_locale(loc_shell, loc_data, loc_bio, lang.code, segment)
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
