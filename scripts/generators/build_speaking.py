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

import json
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


def _bio_block(key: str, label: str, value: str) -> str:
    bid = f"bio-{key}"
    return (
        '<div class="cite-format">'
        f'<p class="cite-format-label">{_esc(label)}</p>'
        f'<pre id="{bid}">{_esc(value.strip())}</pre>'
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


def _render_body(data: dict) -> str:
    bio = data.get("bio", {}) or {}
    topics = data.get("topics", []) or []
    short = bio.get("short", "").strip()

    parts: list[str] = []
    # Photo-led hero: portrait + credibility deck + CTA + a where-I've-shipped
    # logo strip, so the page opens with proof instead of an empty band.
    parts.append(
        '<section class="ap-hero" aria-labelledby="speaking-h1"><div class="wrap">'
        f'<img class="ap-hero-portrait" src="{PORTRAIT}" '
        'alt="Sebastien Rousseau" width="96" height="96" '
        'fetchpriority="high" decoding="async" />'
        '<p class="ap-hero-eyebrow">Speaking &amp; advisory</p>'
        '<h1 id="speaking-h1" class="feat-headline">'
        "Keynotes on the future of banking.</h1>"
        f'<p class="ap-hero-deck">{_esc(short)}</p>'
        '<p><a class="pill" href="/contact/">Invite me to speak</a></p>'
        f"{_brands_block()}"
        "</div></section>"
    )
    parts.append(_proof_rail())

    if topics:
        cards = "".join(
            '<article class="offer-card">'
            f"<h3>{_esc(t.get('title', ''))}</h3>"
            f"<p>{_esc(t.get('summary', '').strip())}</p>"
            "</article>"
            for t in topics
            if t.get("title")
        )
        parts.append(
            '<section class="feat alt" aria-labelledby="speaking-topics">'
            '<div class="wrap">'
            '<p class="feat-eyebrow">Topics</p>'
            '<h2 id="speaking-topics" class="feat-headline">'
            "Talks, framed as outcomes.</h2>"
            f'<div class="offer-cards">{cards}</div>'
            "</div></section>"
        )

    bio_blocks = [
        _bio_block(k, label, bio[k])
        for k, label in (
            ("short", "Short bio"),
            ("medium", "Medium bio"),
            ("long", "Long bio"),
        )
        if bio.get(k)
    ]
    if bio_blocks:
        parts.append(
            '<section class="feat" aria-labelledby="speaking-bio"><div class="wrap">'
            '<p class="feat-eyebrow">Press &amp; media</p>'
            '<h2 id="speaking-bio" class="feat-headline">Ready-to-use bio.</h2>'
            + "".join(bio_blocks)
            + "</div></section>"
        )

    parts.append(_topics_jsonld(topics))
    return "".join(parts)


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

    target = PUBLIC / "speaking" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(f"build_speaking: wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
