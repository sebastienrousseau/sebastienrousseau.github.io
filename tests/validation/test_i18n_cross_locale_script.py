#!/usr/bin/env python3
"""A localized page must not carry another language's script.

_data/i18n/fil/ and _data/i18n/he/ were forked from _data/i18n/ar/ and
only partly localized: 198 of 290 static_patches replacements were still
Arabic, some mangled by what looks like a word-level find/replace over
the Arabic text (``ملاحظات Maghanapية``, ``>צור קשר معنا<``). The result
shipped: five Filipino and four Hebrew static pages carried Arabic inside
``<main>``, the topic hub and the tags page among them. ``cs``, ``sv`` and
``th`` carried fourteen Spanish FAQ headings each from a similar fork.

No gate could see it. ``test_lang_no_leakage`` looks for English words;
``test_body_translation`` measures the share of the ENGLISH body that
survives, and Arabic text on a Filipino page scores zero there — it looks
perfectly translated, just into the wrong language.

So this gate asks a different question: does any page contain a writing
system that neither its own locale nor English uses? Scripts partition
cleanly, which is what makes the check exact rather than heuristic — a
Devanagari run on a Swedish page is never a false positive.

Latin-script pairs (Spanish inside Swedish) share an alphabet and cannot
be separated this way; ``_MARKERS`` covers the orthographic giveaways
(``¿``, ``¡``) and the rest is left to review.

Ratcheted, like ``test_body_translation`` and the slug policy: the pages
still affected are recorded in a baseline and the gate FAILS only when a
NEW page starts carrying a foreign script. The backlog prints every run,
so it stays visible rather than silently permanent. ``--strict`` fails on
the backlog too, for when it has been worked through.

The recorded backlog has one cause: 34 of the 105 files in ``_posts/fil/``
are Arabic articles, front matter and body alike (~39,000 Arabic runs) —
that directory was forked from ``_posts/ar/`` and never translated. The
titles surface on the Filipino tag index and research listing, which is
what the two baselined pages are.

Usage:  python3 tests/validation/test_i18n_cross_locale_script.py [--strict]
        python3 tests/validation/test_i18n_cross_locale_script.py --update-baseline
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry  # type: ignore[import-not-found]

PUBLIC = ROOT / "public"
BASELINE = Path(__file__).with_name("cross-locale-script-baseline.json")

# script name -> (character class, the locales entitled to write in it)
SCRIPTS: dict[str, tuple[re.Pattern[str], frozenset[str]]] = {
    "arabic": (re.compile(r"[؀-ۿ]"), frozenset({"ar", "fa"})),
    "hebrew": (re.compile(r"[֐-׿]"), frozenset({"he"})),
    "cyrillic": (re.compile(r"[Ѐ-ӿ]"), frozenset({"ru", "uk"})),
    "greek": (re.compile(r"[Ͱ-Ͽ]"), frozenset({"el"})),
    # U+0964/U+0965 (danda) sit in the Devanagari block but are shared
    # punctuation that Bengali and others use too.
    "devanagari": (re.compile(r"[ऀ-ॣ०-ॿ]"), frozenset({"hi", "mr"})),
    "bengali": (re.compile(r"[ঀ-৿]"), frozenset({"bn"})),
    "tamil": (re.compile(r"[஀-௿]"), frozenset({"ta"})),
    "telugu": (re.compile(r"[ఀ-౿]"), frozenset({"te"})),
    "thai": (re.compile(r"[฀-๿]"), frozenset({"th"})),
    "hangul": (re.compile(r"[가-힯ᄀ-ᇿ]"), frozenset({"ko"})),
    "kana": (re.compile(r"[぀-ヿ]"), frozenset({"ja"})),
    "han": (re.compile(r"[一-鿿]"), frozenset({"ja", "ko", "zh-hans", "zh-hant"})),
}

# Latin-script languages share an alphabet, so only orthography gives them
# away. Spanish inverted punctuation is the marker that actually shipped.
_MARKERS: dict[str, tuple[re.Pattern[str], frozenset[str]]] = {
    "spanish": (re.compile(r"[¿¡]"), frozenset({"es"})),
}

# Runs shorter than this are single stray glyphs — a maths symbol, a
# transliteration aid — not a sentence in the wrong language.
MIN_RUN = 3

_MAIN_RE = re.compile(r"<main\b[\s\S]*?</main\s*>", re.IGNORECASE)
_SCRIPT_TAG_RE = re.compile(r"<script\b[\s\S]*?</script(?:[\s/][^>]*)?>", re.IGNORECASE)
_STYLE_RE = re.compile(r"<style\b[\s\S]*?</style(?:[\s/][^>]*)?>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")


def visible_main(path: Path) -> str | None:
    html = path.read_text(encoding="utf-8", errors="ignore")
    m = _MAIN_RE.search(html)
    if not m:
        return None
    body = _SCRIPT_TAG_RE.sub(" ", m.group(0))
    body = _STYLE_RE.sub(" ", body)
    return _TAG_RE.sub(" ", body)


def foreign_runs(code: str, text: str) -> list[tuple[str, str]]:
    """(script, sample) for every writing system this locale must not use."""
    out: list[tuple[str, str]] = []
    for name, (pattern, owners) in SCRIPTS.items():
        if code in owners:
            continue
        runs = re.findall(f"{pattern.pattern}{{{MIN_RUN},}}", text)
        if runs:
            out.append((name, runs[0][:60]))
    for name, (pattern, owners) in _MARKERS.items():
        if code in owners:
            continue
        found = pattern.findall(text)
        if found:
            out.append((name, "".join(found[:10])))
    return out


def _locale_pages() -> Iterator[tuple[str, str, Path]]:
    """(code, native slug, path) for every built localized static page."""
    for lang in _lang_registry.active():
        if lang.code == "en":
            continue
        for en_slug, native in _lang_registry.load_slugs(lang.code)["static"].items():
            if en_slug.startswith("_"):
                continue
            page = PUBLIC / lang.code / native / "index.html"
            if page.is_file():
                yield lang.code, native, page


def scan() -> tuple[dict[str, list[str]], int]:
    """Per page URL, the foreign scripts it carries; plus the page count."""
    found: dict[str, list[str]] = {}
    checked = 0
    for code, native, page in _locale_pages():
        text = visible_main(page)
        if text is None:
            continue
        checked += 1
        scripts = sorted({s for s, _ in foreign_runs(code, text)})
        if scripts:
            found[f"/{code}/{native}/"] = scripts
    return found, checked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="fail on the recorded backlog too")
    ap.add_argument("--update-baseline", action="store_true")
    args = ap.parse_args()

    if not PUBLIC.is_dir():
        print("public/ not built — run ./build.sh first", file=sys.stderr)
        return 0

    found, checked = scan()

    if args.update_baseline:
        BASELINE.write_text(
            json.dumps(dict(sorted(found.items())), indent=0) + "\n", encoding="utf-8"
        )
        print(f"baseline written: {BASELINE.name} ({len(found)} page(s))")
        return 0

    baseline: dict[str, list[str]] = (
        json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.is_file() else {}
    )

    regressions = [
        f"  {page} carries {', '.join(scripts)}"
        for page, scripts in sorted(found.items())
        if sorted(baseline.get(page, [])) != scripts
    ]
    if regressions:
        print("localized pages newly carrying another language's script:", file=sys.stderr)
        for line in regressions:
            print(line, file=sys.stderr)
        print(
            "\nA locale file forked from another locale and left partly translated is "
            "the usual cause; check its static_patches.json and _posts/<code>/.\n"
            "If this is intentional, re-record with --update-baseline.",
            file=sys.stderr,
        )
        return 1

    for page, scripts in sorted(found.items()):
        print(f"  backlog: {page} carries {', '.join(scripts)}")

    if found and args.strict:
        print(
            f"cross-locale script: {len(found)} page(s) still carry a foreign script",
            file=sys.stderr,
        )
        return 1

    print(
        f"cross-locale script: OK — no new page regressed "
        f"({checked} page(s) checked, {len(found)} in backlog)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
