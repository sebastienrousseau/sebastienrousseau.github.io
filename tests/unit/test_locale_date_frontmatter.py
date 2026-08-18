"""Every locale post's `date:` must equal its English counterpart's.

An earlier translation pass localised the field ("28 juin 2026",
"2026年6月27日"). Three consumers parse it and all three failed silently:
ssg's news-sitemap generator and build_lang_feeds.parse_date both stamped the
build time, and feeds.py's last-modified map skipped the post. The result was
467 posts advertising themselves as published at build time across 27 locale
RSS feeds, invisible because a <pubDate> was always present and plausible.

The assertion is against the English counterpart rather than mere
parseability: `date` is not in the translation allow-list, so the English
value is what the locale file was scaffolded from, and a divergence means
something rewrote it. Compared as a resolved calendar date, not as a string —
parts of the corpus legitimately differ in format ("January 1, 2018" vs
"Jan 01, 2018"), which is a cosmetic difference, not a wrong date.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def _field(text: str, name: str) -> str | None:
    # Frontmatter uses both quote styles; parts of the corpus are
    # single-quoted (date: 'January 1, 2018'). Stripping only double quotes
    # leaves the value unparseable and invents a defect that is not there.
    m = re.search(rf"^{name}:\s*(.*?)\s*$", text, re.M)
    if not m:
        return None
    v = m.group(1)
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def _to_date(v: str):
    from datetime import datetime

    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def _en_counterpart(p: Path) -> Path:
    reg = ROOT / "_data" / "i18n" / p.parent.name / "slugs.json"
    stem = p.stem
    if reg.is_file():
        articles = json.loads(reg.read_text(encoding="utf-8")).get("articles", {})
        stem = {v: k for k, v in articles.items()}.get(p.stem, p.stem)
    return ROOT / "_posts" / f"{stem}.md"


def test_every_locale_date_is_parseable():
    """The invariant that prevents the defect: no consumer may have to guess.

    Asserted as parseability rather than equality with the English original.
    Equality is not a true invariant of this corpus — 92 locale posts already
    differ from their English counterpart, and in 46 of those the locale date
    matches its own slug while the English one does not. Those are a real
    pre-existing discrepancy (tracked in #433), not something this guard
    should coerce: overwriting them would destroy the more plausible date.
    """
    bad = []
    for p in sorted((ROOT / "_posts").glob("*/*.md")):
        if not DATED.match(p.stem):
            continue
        v = _field(p.read_text(encoding="utf-8"), "date")
        if v is None:
            continue
        if _to_date(v) is None:
            bad.append(f"{p.parent.name}/{p.stem}: {v!r}")
    assert not bad, (
        f"{len(bad)} locale post(s) with a date no consumer can parse. "
        "ssg's news sitemap and build_lang_feeds both fall back to the build "
        "time, which looks plausible and is wrong. Run "
        "scripts/maintenance/fix_locale_date_frontmatter.py\n" + "\n".join(bad[:10])
    )


def test_parse_date_raises_rather_than_stamping_build_time():
    """Regression: the old fallback returned datetime.now() silently."""
    import sys

    sys.path[:0] = [
        str(ROOT / "scripts"),
        str(ROOT / "scripts" / "lib"),
        str(ROOT / "scripts" / "generators"),
    ]
    import build_lang_feeds

    assert build_lang_feeds.parse_date("2026-06-28").date().isoformat() == "2026-06-28"
    assert build_lang_feeds.parse_date("June 28, 2026").date().isoformat() == "2026-06-28"
    for bad in ("28 juin 2026", "2026年6月27日", ""):
        try:
            build_lang_feeds.parse_date(bad)
        except ValueError:
            continue
        raise AssertionError(f"parse_date({bad!r}) should raise, not invent a date")
