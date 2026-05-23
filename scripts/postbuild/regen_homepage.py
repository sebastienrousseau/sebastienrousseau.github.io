#!/usr/bin/env python3
"""Regenerate the homepage's 6-card "latest news" grid in
``_posts/index.md`` from the top-6 most recent dated EN posts.

Why: each article PR used to commit a hand-edited 6-card rotation in
``_posts/index.md`` — every stacked PR collided on that file. By
deriving the cards from the actual ``_posts/YYYY-MM-DD-*.md`` files at
build time, article PRs become additive-only and the rotation always
reflects the on-disk truth.

Algorithm:
    1. Glob ``_posts/YYYY-MM-DD-*.md``, sort by date descending, take
       the first 6.
    2. For each, parse just enough frontmatter to populate one card:
       title, banner, banner_alt, tags (→ eyebrow), excerpt, date.
    3. Render the canonical ``<article class="newsroom-card">`` block
       used by Sebastien's existing homepage layout.
    4. Find the ``<div class="newsroom-grid feat-latest-grid">`` block
       in ``_posts/index.md`` and replace its inner cards with the
       freshly-rendered set. Outer wrapper + surrounding markup are
       preserved verbatim.

Stable rendering means the diff on a no-op rebuild is empty. Run as
part of ``build.sh`` before ``ssg``.
"""
from __future__ import annotations

import html
import re
import sys
from datetime import date as _date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
INDEX = POSTS / "index.md"

_DATED_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-.+\.md$")
_GRID_RE = re.compile(
    r'(<div class="newsroom-grid feat-latest-grid">)(.*?)(</div>\s*\n\s*<div class="feat-cta-row">)',
    re.DOTALL,
)
_MONTHS = (
    "January February March April May June "
    "July August September October November December"
).split()


def _display_date(y: int, m: int, d: int) -> str:
    return f"{_MONTHS[m - 1]} {d}, {y}"


def _parse_minimal_frontmatter(text: str) -> dict[str, str]:
    """Pick out only the fields we need for the card. Lightweight — no
    YAML library — because the publish flow's check_voice.py already
    validates the frontmatter shape.
    """
    out: dict[str, str] = {}
    in_fm = False
    delim_count = 0
    for line in text.splitlines():
        if line.strip() == "---":
            delim_count += 1
            in_fm = delim_count == 1
            if delim_count == 2:
                break
            continue
        if not in_fm:
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*"?(.*?)"?\s*$', line)
        if m:
            key, val = m.group(1), m.group(2)
            if key in {"title", "banner", "banner_alt", "tags", "excerpt", "subtitle", "description"}:
                out[key] = val
    return out


_ACRONYMS = {
    "AI", "AML", "API", "BIS", "BoE", "CBDC", "CBPR", "CSP", "CTO", "DLT",
    "DORA", "DSS", "ECB", "EU", "EUR", "FCA", "FedNow", "FX", "G20", "G7",
    "GDPR", "GENIUS", "GMT", "GBP", "HMRC", "HMT", "HM", "HSBC", "HSM",
    "ICT", "IETF", "ISO", "JP", "JPM", "KYC", "LLM", "ML", "MPP", "MT",
    "MTS", "MX", "NCSC", "NIS2", "NIST", "PIN", "PISP", "PoC", "PQC",
    "PSP", "PSR", "PSU", "QKD", "RTGS", "RTP", "SaaS", "SEPA", "SFTP",
    "SLA", "SWIFT", "SDX", "TIC", "TMS", "TLS", "T+0", "T+1", "T+2",
    "UK", "UN", "US", "USD", "UX", "VC", "WCAG", "XML", "JSON-LD",
    "PII", "JSON", "YAML", "TOML", "HTML", "CSS", "PWA", "BST", "UTC",
    "USDC", "USDT", "BRSRV", "BSTBL", "MMF",
}


def _smart_title(token: str) -> str:
    """Title-case a token but preserve known acronyms in their canonical
    casing. ``.title()`` would butcher ``UK`` into ``Uk``."""
    if token.upper() in _ACRONYMS:
        return token.upper()
    # If the token already has mixed-case (e.g. "FedNow"), trust it.
    if any(c.isupper() for c in token[1:]):
        return token
    return token.title()


def _eyebrow_from_tags(tags: str) -> str:
    """First three comma-separated tags, smart-cased, joined with ' · '.
    Mirrors gen_articles.py's convention but preserves acronyms (UK, AI,
    UX, BoE, …) instead of butchering them via ``.title()``."""
    parts = [t.strip() for t in tags.split(",") if t.strip()][:3]
    return " · ".join(
        " ".join(_smart_title(w) for w in p.split())
        for p in parts
    )


def _excerpt_for(fm: dict[str, str]) -> str:
    """Excerpt preference order: excerpt → subtitle → description → title."""
    return fm.get("excerpt") or fm.get("subtitle") or fm.get("description") or fm.get("title", "")


def _esc(s: str) -> str:
    """Escape user text for HTML, idempotent w.r.t. already-escaped
    ampersands. Frontmatter is hand-authored Markdown and sometimes
    already contains ``&amp;`` — naive ``html.escape`` would turn that
    into ``&amp;amp;``, which is wrong. Unescape first, then re-escape."""
    return html.escape(html.unescape(s), quote=False)


def _render_card(slug: str, year: int, month: int, day: int, fm: dict[str, str]) -> str:
    date_iso = f"{year:04d}-{month:02d}-{day:02d}"
    href = f"/{slug}/index.html"
    title = fm.get("title", slug)
    banner = fm.get("banner", "")
    banner_alt = fm.get("banner_alt", title)
    eyebrow = _eyebrow_from_tags(fm.get("tags", "")) or "Banking · Technology"
    excerpt = _excerpt_for(fm)
    return (
        f'<article class="newsroom-card">\n'
        f'<a class="newsroom-card-media" href="{href}" title="{_esc(title)}">\n'
        f'<img alt="{_esc(banner_alt)}" src="{banner}" loading="lazy" decoding="async" width="600" height="600" />\n'
        f'</a>\n'
        f'<div class="newsroom-card-body">\n'
        f'<span class="newsroom-eyebrow">{_esc(eyebrow)}</span>\n'
        f'<h3><a href="{href}">{_esc(title)}</a></h3>\n'
        f'<p class="newsroom-meta"><time datetime="{date_iso}">{_display_date(year, month, day)}</time></p>\n'
        f'<p class="newsroom-excerpt">{_esc(excerpt)}</p>\n'
        f'</div>\n'
        f'</article>'
    )


def _collect_top_six() -> list[tuple[str, int, int, int, dict[str, str]]]:
    """Top 6 by date descending. Returns ``(slug, y, m, d, frontmatter)``."""
    rows: list[tuple[str, int, int, int, dict[str, str]]] = []
    for md in POSTS.glob("*.md"):
        m = _DATED_RE.match(md.name)
        if not m:
            continue
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        slug = md.stem
        fm = _parse_minimal_frontmatter(md.read_text(encoding="utf-8"))
        if not fm.get("title"):
            # No title means the article isn't fit to advertise.
            continue
        rows.append((slug, y, mo, d, fm))
    rows.sort(key=lambda r: (r[1], r[2], r[3]), reverse=True)
    return rows[:6]


def main() -> int:
    if not INDEX.exists():
        print("regen_homepage: _posts/index.md not found; nothing to do.")
        return 0
    cards = _collect_top_six()
    if not cards:
        print("regen_homepage: no dated EN posts found; nothing to do.")
        return 0
    rendered = "\n\n" + "\n\n".join(_render_card(*c) for c in cards) + "\n\n\n"
    text = INDEX.read_text(encoding="utf-8")
    if not _GRID_RE.search(text):
        print(
            "regen_homepage: newsroom-grid block not found in _posts/index.md; "
            "nothing replaced. (Layout markup may have changed.)",
            file=sys.stderr,
        )
        return 1
    new_text = _GRID_RE.sub(
        lambda m: m.group(1) + rendered + m.group(3),
        text,
        count=1,
    )
    if new_text == text:
        print(f"regen_homepage: 6 cards rendered, no change.")
        return 0
    INDEX.write_text(new_text, encoding="utf-8")
    top_titles = [c[4].get("title", c[0])[:40] for c in cards]
    print(f"regen_homepage: rewrote 6-card grid with {top_titles[0]} on top")
    return 0


if __name__ == "__main__":
    sys.exit(main())
