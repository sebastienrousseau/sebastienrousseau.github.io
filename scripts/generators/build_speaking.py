#!/usr/bin/env python3
"""Generate the ``/speaking/`` authority hub from ``speaking.yml``.

The speaking kit — bios, outcome-framed talk topics, and an invite CTA —
already lives in ``_data/proof/speaking.yml`` but nothing rendered it.
This generator forks the FT-tier ``/articles/index.html`` shell (so the
typography, CSP, SRI, and accessibility profile stay identical to the
rest of the site) and swaps in a body composed only of existing utility
classes, then relies on the postbuild passes for SEO / CSP / JSON-LD
hashing.

Runs from ``build.sh`` AFTER ``build_translations`` (so it lands only on
the English tree, like ``build_changelog``) and BEFORE ``postbuild`` (so
the sitemap-augment pass adds it and its inline JSON-LD is CSP-hashed).

Output: ``public/speaking/index.html``
Input:  ``_data/proof/speaking.yml``   (single source of truth)
        ``public/articles/index.html`` (shell template)
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
from case_studies_components import _esc

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SPEAKING_YML = ROOT / "_data" / "proof" / "speaking.yml"
SHELL_SRC = PUBLIC / "articles" / "index.html"
METRICS_JSON = ROOT / "_data" / "proof" / "metrics.json"
BASE_URL = "https://sebastienrousseau.com"
URL = f"{BASE_URL}/speaking/"

# Portrait + the brand logos already served for the homepage credibility
# strip. Reusing them keeps the CDN + CSP surface unchanged.
PORTRAIT = "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
_LOGO_BASE = "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos"
_BRANDS = [
    ("HSBC", "hsbc"),
    ("PayPal", "paypal"),
    ("Barclays", "barclays"),
    ("Shazam", "shazam"),
    ("AKQA", "akqa"),
    ("Virgin", "virgin"),
]


def _brands_block() -> str:
    """Where-I've-shipped logo strip — the same `.brands`/`.brand-logo`
    markup the homepage uses, so the articles shell already styles it."""
    imgs = "".join(
        f'<img alt="{name} logo" src="{_LOGO_BASE}/{slug}.webp" '
        'class="brand-logo" loading="lazy" decoding="async" '
        'width="120" height="32" />'
        for name, slug in _BRANDS
    )
    return f'<div class="brands">{imgs}</div>'


def _fmt_metric(value: object, fmt: str) -> str:
    if not isinstance(value, (int, float)):
        return str(value)
    if fmt == "compact":
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        if value >= 1_000:
            return f"{value / 1_000:.1f}K"
    return str(int(value))


def _proof_rail() -> str:
    """Authority proof rail, baked from metrics.json at build time (this
    generator runs after fetch_metrics, so the numbers are fresh). Uses
    the shell's `.proof-rail`/`.kpi-cell` styling."""
    try:
        stats = {
            s["key"]: _fmt_metric(s.get("value"), s.get("format", "plain"))
            for s in json.loads(METRICS_JSON.read_text(encoding="utf-8")).get("stats", [])
            if s.get("key")
        }
    except (OSError, ValueError):
        return ""
    cells = [
        ("years_payments", "Years in banking &amp; payments"),
        ("downloads_total", "Open-source downloads"),
        ("articles_signed", "Signed, dated articles"),
        ("github_stars", "GitHub stars"),
    ]
    rendered = "".join(
        f'<div class="kpi-cell"><span class="kpi-cell-value">{stats[key]}</span>'
        f'<span class="kpi-cell-label">{label}</span></div>'
        for key, label in cells
        if key in stats
    )
    if not rendered:
        return ""
    return f'<section class="proof-rail" aria-label="Speaking credibility by the numbers">{rendered}</section>'


def _split_paragraphs(text: str, groups: int = 2) -> list[str]:
    """Split a folded one-line bio into `groups` prose paragraphs on sentence
    boundaries, so the biography reads like an Apple leadership page rather
    than one dense block."""
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
    if len(sentences) <= 1:
        return sentences
    per = max(1, -(-len(sentences) // groups))  # ceil
    return [" ".join(sentences[i : i + per]) for i in range(0, len(sentences), per)]


def _unescape_head_metas(html_text: str) -> str:
    """Repair entity-escaped `<meta>` / `<link>` tags that some local SSG
    builds emit in the shell's <head> (`&lt;meta …&gt;`). Left unrepaired the
    browser spills them into the body as visible text. On CI the tags are
    already real, so this is a no-op."""
    return re.sub(
        r"&lt;(?:meta|link)\b.*?&gt;",
        lambda m: _html.unescape(m.group(0)),
        html_text,
        flags=re.DOTALL,
    )


def _mark_nav_active(html_text: str) -> str:
    """Move the primary-nav active state onto the Speaking link. The forked
    /articles/ shell marks Articles as `aria-current="page" class="active"`;
    swap that onto /speaking/ so the current page is correctly highlighted."""
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


def _bio_block(key: str, label: str, value: str) -> str:
    bid = f"bio-{key}"
    return (
        '<div class="cite-format">'
        f'<p class="cite-format-label">{_esc(label)}</p>'
        f'<p id="{bid}">{_esc(value.strip())}</p>'
        f'<button type="button" class="copy-btn" data-copy="#{bid}" '
        f'aria-label="{_esc(label)} — Copy">Copy</button>'
        "</div>"
    )


def _topics_jsonld(topics: list[dict]) -> str:
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": t.get("title", ""),
            "description": t.get("summary", "").strip(),
        }
        for i, t in enumerate(topics)
        if t.get("title")
    ]
    payload = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Speaking topics — Sebastien Rousseau",
        "itemListElement": items,
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )


def _format_card(fmt: str) -> str:
    """One format card, e.g. 'Keynote (30-45 min)' -> title + detail."""
    if "(" in fmt:
        title, detail = fmt.split("(", 1)
        return (
            f'<div class="speaking-format"><h3>{_esc(title.strip())}</h3>'
            f'<p>{_esc(detail.rstrip(")").strip())}</p></div>'
        )
    return f'<div class="speaking-format"><h3>{_esc(fmt.strip())}</h3></div>'


def _secondary_cta(logistics: dict) -> str:
    """Secondary CTA: the media kit if its PDF exists, else an in-page jump to
    the keynotes — never a broken link."""
    media_kit = logistics.get("media_kit_pdf", "")
    if media_kit and (PUBLIC / media_kit.lstrip("/")).is_file():
        return f'<a class="pill ghost" href="{_esc(media_kit)}">Download media kit</a>'
    return '<a class="pill ghost" href="#speaking-keynotes">Explore keynotes</a>'


def _hero_section(booking: str, secondary: str) -> str:
    """Benefit-led, two-column hero (portrait right), dual CTA, then the
    "where I've shipped" logo strip. Positions the value, not the name."""
    return (
        '<section class="feat speaking-hero-band" aria-labelledby="speaking-h1">'
        '<div class="wrap">'
        '<div class="speaking-hero"><div>'
        '<p class="feat-eyebrow">Keynotes &middot; Panels &middot; Advisory</p>'
        '<h1 id="speaking-h1" class="feat-headline">The technologies reshaping '
        "banking, explained to the people who have to act.</h1>"
        '<p class="ap-hero-deck">Sebastien Rousseau is a senior banking '
        "technologist with 20+ years across HSBC, PayPal, and Barclays. He turns "
        "payments modernisation, post-quantum cryptography, and applied AI from "
        "policy paper into inspectable code, and into keynotes a board can act "
        "on.</p>"
        f'<div class="speaking-cta-row"><a class="pill" href="{_esc(booking)}">'
        f"Invite me to speak</a>{secondary}</div>"
        "</div>"
        f'<img class="speaking-hero-photo" src="{PORTRAIT}" '
        'alt="Sebastien Rousseau" width="300" height="375" '
        'fetchpriority="high" decoding="async" />'
        "</div>"
        f"{_brands_block()}"
        "</div></section>"
    )


def _keynote_card(topic: dict) -> str:
    """One signature-keynote card with an optional audience chip."""
    chip = (
        f'<span class="talk-audience">For: {_esc(topic["audience"])}</span>'
        if topic.get("audience")
        else ""
    )
    return (
        '<article class="offer-card">'
        f"<h3>{_esc(topic.get('title', ''))}</h3>"
        f"<p>{_esc(topic.get('summary', '').strip())}</p>"
        f"{chip}</article>"
    )


def _keynotes_section(topics: list) -> str:
    """Signature keynotes — each with an audience chip so an organiser can place
    the talk against their room. Empty string when there are no titled topics."""
    cards = "".join(_keynote_card(t) for t in topics if t.get("title"))
    if not cards:
        return ""
    return (
        '<section class="feat alt" aria-labelledby="speaking-keynotes">'
        '<div class="wrap">'
        '<p class="feat-eyebrow">Signature keynotes</p>'
        '<h2 id="speaking-keynotes" class="feat-headline">'
        "Talks built for the boardroom.</h2>"
        f'<div class="offer-cards">{cards}</div>'
        "</div></section>"
    )


def _formats_section(logistics: dict) -> str:
    """Formats & regions — the practical answers an organiser needs."""
    formats = logistics.get("formats", []) or []
    regions = logistics.get("regions", []) or []
    if not (formats or regions):
        return ""
    fmt_cards = "".join(_format_card(f) for f in formats)
    region_spans = "".join(f"<span>{_esc(r)}</span>" for r in regions)
    regions_html = (
        f'<div class="speaking-regions">{region_spans}</div>' if regions else ""
    )
    return (
        '<section class="feat" aria-labelledby="speaking-formats">'
        '<div class="wrap">'
        '<p class="feat-eyebrow">For organisers</p>'
        '<h2 id="speaking-formats" class="feat-headline">How I work.</h2>'
        f'<div class="speaking-formats">{fmt_cards}</div>'
        f"{regions_html}"
        "</div></section>"
    )


def _biography_section(bio: dict) -> str:
    """Flowing-prose biography for programme pages and introductions."""
    bio_prose = (bio.get("long", "") or "").strip()
    bio_prose = bio_prose or (bio.get("short", "") or "").strip()
    if not bio_prose:
        return ""
    body = "".join(f"<p>{_esc(p)}</p>" for p in _split_paragraphs(bio_prose))
    return (
        '<section class="feat" aria-labelledby="speaking-about">'
        '<div class="wrap">'
        '<p class="feat-eyebrow">Biography</p>'
        '<h2 id="speaking-about" class="feat-headline">About Sebastien.</h2>'
        f"{body}"
        "</div></section>"
    )


def _press_bios_section(bio: dict) -> str:
    """Ready-to-use press bios (short/medium/long) with copy-to-clipboard."""
    bio_blocks = [
        _bio_block(k, label, bio[k])
        for k, label in (("short", "Short"), ("medium", "Medium"), ("long", "Long"))
        if bio.get(k)
    ]
    if not bio_blocks:
        return ""
    return (
        '<section class="feat" aria-labelledby="speaking-bio"><div class="wrap">'
        '<p class="feat-eyebrow">Press &amp; media</p>'
        '<h2 id="speaking-bio" class="feat-headline">Ready-to-use bio.</h2>'
        + "".join(bio_blocks)
        + "</div></section>"
    )


def _closing_cta(booking: str, secondary: str) -> str:
    """Closing "book me" CTA band."""
    return (
        '<section class="feat"><div class="wrap"><div class="speaking-cta">'
        '<p class="feat-eyebrow">Book a keynote</p>'
        '<h2 class="feat-headline">Bring this to your stage.</h2>'
        '<p class="ap-hero-deck">Keynotes, panels, and advisory for boards, '
        "conferences, and executive teams navigating payments, post-quantum "
        "cryptography, and applied AI. In London, across Europe, or remote.</p>"
        f'<div class="cta-actions"><a class="pill" href="{_esc(booking)}">'
        f"Invite me to speak</a>{secondary}</div>"
        "</div></div></section>"
    )


def _render_body(data: dict) -> str:
    """Assemble the speaking page body from its sections (empties dropped)."""
    bio = data.get("bio", {}) or {}
    topics = data.get("topics", []) or []
    logistics = data.get("logistics", {}) or {}
    booking = logistics.get("booking_url") or "/contact/index.html"
    secondary = _secondary_cta(logistics)

    sections = [
        _hero_section(booking, secondary),
        _proof_rail(),
        _keynotes_section(topics),
        _formats_section(logistics),
        _biography_section(bio),
        _press_bios_section(bio),
        _closing_cta(booking, secondary),
        _topics_jsonld(topics),
    ]
    return "".join(s for s in sections if s)


def main() -> int:
    if not SHELL_SRC.is_file():
        print(f"build_speaking: shell missing at {SHELL_SRC}", file=sys.stderr)
        return 1
    if not SPEAKING_YML.is_file():
        print(f"build_speaking: {SPEAKING_YML} missing", file=sys.stderr)
        return 1

    data = yaml.safe_load(SPEAKING_YML.read_text(encoding="utf-8")) or {}
    shell = SHELL_SRC.read_text(encoding="utf-8")
    body = _render_body(data)
    title = "Speaking & advisory — Sebastien Rousseau"
    desc = (data.get("bio", {}).get("short", "") or "").strip()[:155]
    out = _swap_into_shell(shell, body, title, desc, URL)
    out = _unescape_head_metas(out)
    out = _mark_nav_active(out)

    target = PUBLIC / "speaking" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_speaking: wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
