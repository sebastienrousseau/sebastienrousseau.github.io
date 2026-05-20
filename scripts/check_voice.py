#!/usr/bin/env python3
"""Tone-of-voice + style + structure gate for daily-publishing articles.

Run against `_posts/<today>-*.md` *before* the translation + build
pipeline kicks off. Fails fast with a clear list of defects so the
daily-publishing routine doesn't ship a draft that violates the
house editorial rules.

Checks (in order):

  1. Frontmatter completeness — title, subtitle, description, banner,
     banner_alt, tags, twitter_*, excerpt, date, keywords are all
     present and non-empty.
  2. Banner reachability — the `banner:` URL must return HTTP 200
     from the CDN (no broken images cascading through 28 locales).
  3. Banned filler — phrases that mark hype rather than executive
     register: "delve into", "embark on", "in conclusion", "let's
     explore", "it is worth noting", "in today's fast-paced world",
     "in this article", etc.
  4. Structural shape — must have a lead aside block, an executive
     summary blockquote, at least 3 H2 sections, at least one
     citation link with title attribute, an FAQ section, and a
     References section.
  5. Markdown discipline — H1 appears exactly once; no broken
     citation links (`[text](]` patterns).
  6. Date sanity — frontmatter `date:` matches the YYYY-MM-DD in
     the filename, and filename date is today's UTC date.

Usage:
    python3 scripts/check_voice.py _posts/2026-05-20-*.md
    python3 scripts/check_voice.py --today          # auto-pick today's article

Exit codes: 0 clean, 1 defects found.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
import urllib.request
from pathlib import Path

from _core import ROOT, parse_frontmatter  # shared with gen_articles, build_topics

# ---------------------------------------------------------------------------
# Banned phrases — hype filler that mark non-executive register
# ---------------------------------------------------------------------------

_BANNED_FILLER = (
    "delve into",
    "embark on",
    "in conclusion,",
    "let's explore",
    "let us explore",
    "it is worth noting",
    "in today's fast-paced",
    "in this article",
    "this article will",
    "we will see",
    "as we have seen",
    "without further ado",
    "the world of",
    "navigate the",
    "harness the power",
    "unlock the potential",
    "game-changer",
    "paradigm shift",
    "synergy",
    "leverage cutting-edge",
    "revolutionise the way",
    "transformative journey",
    "unprecedented",
)

# Required frontmatter keys for a publishable article
_REQUIRED_FM = (
    "title", "subtitle", "description", "banner", "banner_alt",
    "tags", "excerpt", "date", "keywords",
    "twitter_title", "twitter_description",
)

# Frontmatter parser is imported from _core — single canonical impl.


# ---------------------------------------------------------------------------
# Individual checks — each returns list[str] of defects
# ---------------------------------------------------------------------------


def check_frontmatter(fm: dict[str, str]) -> list[str]:
    return [
        f"frontmatter: missing or empty `{k}`"
        for k in _REQUIRED_FM
        if not fm.get(k)
    ]


def check_banner_reachable(banner: str, timeout: float = 10.0) -> list[str]:
    """GET the banner URL with Range: bytes=0-0 and a browser-style
    User-Agent; defect if non-2xx or unreachable. (HEAD is refused by
    some CDN edges with 403, so a tiny Range GET is the portable form.)"""
    if not banner:
        return ["banner: empty"]
    try:
        req = urllib.request.Request(
            banner,
            headers={
                "Range": "bytes=0-0",
                "User-Agent": "sebastienrousseau.com-voice-check/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if r.status not in (200, 206):
                return [f"banner: {banner} returned HTTP {r.status}"]
    except Exception as exc:
        return [f"banner: {banner} unreachable ({exc})"]
    return []


def check_filler(body: str) -> list[str]:
    """Return one defect per banned phrase found (case-insensitive)."""
    lower = body.lower()
    return [f"voice: banned filler — {p!r}" for p in _BANNED_FILLER if p in lower]


def check_structure(body: str) -> list[str]:
    """Hard structural requirements for a publishable article."""
    defects: list[str] = []
    if "<!-- lead-start -->" not in body:
        defects.append("structure: missing <!-- lead-start --> lead aside")
    if not re.search(r'>\s*\*\*Executive Summary', body):
        defects.append("structure: missing > **Executive Summary blockquote")
    h2s = re.findall(r'^## ', body, re.MULTILINE)
    if len(h2s) < 3:
        defects.append(f"structure: only {len(h2s)} H2 section(s), need ≥3")
    citations = re.findall(r'\[[^\]]+\]\(https?://[^)]+ "[^"]+"\)', body)
    if not citations:
        defects.append("structure: no citation links with title attribute")
    if not re.search(r'^## (?:Frequently Asked Questions|FAQ)', body, re.MULTILINE):
        defects.append("structure: missing FAQ section")
    if not re.search(r'^## References', body, re.MULTILINE):
        defects.append("structure: missing References section")
    return defects


def check_markdown_discipline(body: str) -> list[str]:
    defects: list[str] = []
    h1_count = len(re.findall(r'^# ', body, re.MULTILINE))
    if h1_count != 1:
        defects.append(f"markdown: H1 appears {h1_count}× — should be exactly 1")
    if re.search(r'\]\(\]', body):
        defects.append("markdown: broken citation link `](]` detected")
    return defects


def check_date_consistency(path: Path, fm: dict[str, str]) -> list[str]:
    """Filename date should match today (UTC) and frontmatter date."""
    defects: list[str] = []
    m = re.match(r'^(\d{4}-\d{2}-\d{2})-', path.stem)
    if not m:
        return [f"date: filename {path.name} does not begin with YYYY-MM-DD"]
    file_date = m.group(1)
    today = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d")
    if file_date != today:
        defects.append(
            f"date: filename {file_date} != today UTC {today} "
            f"(skip with --no-date-check if intentional)"
        )
    fm_date = fm.get("date", "")
    if fm_date:
        # Best-effort YYYY-MM-DD extraction from "Month DD, YYYY"
        try:
            dt = _dt.datetime.strptime(fm_date, "%B %d, %Y")
            fm_iso = dt.strftime("%Y-%m-%d")
            if fm_iso != file_date:
                defects.append(
                    f"date: frontmatter `date: \"{fm_date}\"` → "
                    f"{fm_iso}, but filename says {file_date}"
                )
        except ValueError:
            defects.append(
                f"date: frontmatter `date: \"{fm_date}\"` is not in "
                f'"Month DD, YYYY" form'
            )
    return defects


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def check_external_links(body: str, timeout: float = 10.0) -> list[str]:
    """Probe every external citation URL with a ranged GET; defect for
    each one returning a non-2xx code. Run concurrently with a small
    thread pool so the link-rot pass stays in seconds, not minutes."""
    from concurrent.futures import ThreadPoolExecutor

    urls = sorted({
        m.group(1)
        for m in re.finditer(r'\]\((https?://[^)\s]+)', body)
    })
    if not urls:
        return []

    def probe(url: str) -> str | None:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Range": "bytes=0-0",
                    "User-Agent": "sebastienrousseau.com-link-check/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.status not in (200, 206):
                    return f"link-rot: {url} → HTTP {r.status}"
        except Exception as exc:
            return f"link-rot: {url} → {exc}"
        return None

    with ThreadPoolExecutor(max_workers=8) as pool:
        return [d for d in pool.map(probe, urls) if d]


def check_article(path: Path, *, skip_date: bool = False,
                  skip_network: bool = False,
                  check_links: bool = False) -> list[str]:
    """Run every gate against ``path``. Returns a flat list of defect
    strings. Empty list = clean.

    Flags:
      ``skip_date``     — disable filename/today/frontmatter date checks
                          (useful for backfills + dry-run drafting)
      ``skip_network``  — disable banner-reachability HEAD/Range GET
                          (useful for offline drafting)
      ``check_links``   — additionally probe every external citation URL
                          with a Range GET, surface 404s as defects
    """
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    defects: list[str] = []
    defects.extend(check_frontmatter(fm))
    if not skip_network:
        defects.extend(check_banner_reachable(fm.get("banner", "")))
    defects.extend(check_filler(body))
    defects.extend(check_structure(body))
    defects.extend(check_markdown_discipline(body))
    if not skip_date:
        defects.extend(check_date_consistency(path, fm))
    if check_links and not skip_network:
        defects.extend(check_external_links(body))
    return defects


def _today_article() -> Path | None:
    today = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d")
    matches = sorted((ROOT / "_posts").glob(f"{today}-*.md"))
    return matches[0] if matches else None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", type=Path, nargs="?", help="article markdown path")
    p.add_argument("--today", action="store_true",
                   help="auto-pick _posts/<today>-*.md")
    p.add_argument("--no-date-check", action="store_true",
                   help="skip filename-date-vs-today gate (useful for backfills)")
    p.add_argument("--no-network", "--bypass-network", action="store_true",
                   help="skip banner-reachability + external-link probes "
                        "(useful for offline drafting)")
    p.add_argument("--check-links", action="store_true",
                   help="additionally probe every external citation URL "
                        "for link rot; surfaces 404s as defects")
    args = p.parse_args()

    if args.today:
        path = _today_article()
        if not path:
            today = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d")
            print(f"check_voice: no _posts/{today}-*.md found", file=sys.stderr)
            return 1
    elif args.path:
        path = args.path
    else:
        p.print_help(sys.stderr)
        return 2

    if not path.is_file():
        print(f"check_voice: {path} does not exist", file=sys.stderr)
        return 1

    defects = check_article(
        path,
        skip_date=args.no_date_check,
        skip_network=args.no_network,
        check_links=args.check_links,
    )
    if defects:
        print(f"check_voice: {len(defects)} defect(s) in {path}:", file=sys.stderr)
        for d in defects:
            print(f"  - {d}", file=sys.stderr)
        return 1
    print(f"check_voice: {path.name} — OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
