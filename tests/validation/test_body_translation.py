#!/usr/bin/env python3
"""Localized static pages must not ship the English ``<main>`` body.

``test_lang_no_leakage`` deliberately scopes to chrome — everything
*outside* ``<main>`` — so that an article legitimately quoting English
does not trip it. That carve-out is a blind spot: /playlists/ shipped its
entire body in English on all 34 locales (39 cards, a featured band, five
lane heads, a seven-question FAQ, a device aside) under a localized
``<title>``, and no gate could see it.

Extending the chrome gate to ``<main>`` does not work. Measured across
680 localized static pages it yields five distinct hits, and every one is
noise: ``navigate`` from a ``data-filter-mode`` attribute, ``Status``
inside German prose, ``Boards``/``Regulators`` from article excerpts that
are English by design (only ~105 of 3,675 articles are translated).
Individual UI words are the wrong unit.

What both bugs actually looked like is a *body that is still the English
body*. So this gate measures that directly: the share of the English
page's word 5-grams that reappear verbatim in the localized page's
``<main>``. A translated page scores near zero; an untranslated one
scores 1.0. The measured distribution is sharply bimodal — 398 of 680
pages below 0.10, 78 at 1.0 — so the threshold sits in a wide empty band
rather than being tuned.

Some pages legitimately score in between: /topics/ and /tags/ are built
largely from article titles that are English by design. Hence the
ratchet.

Ratchet: each page's current worst-locale score is recorded as a
baseline and the gate FAILS only if a page goes backwards. The remaining
backlog prints every run — visible, not silently permanent. Same
mechanism as the slug policy, the mypy tier and the complexity allowlist.
``--strict`` fails on the backlog too, for when it has been worked
through.

That backlog is now empty. /speaking/, /suite/, /articles/, /library/,
/projects/, /topics/ and /case-studies/ all shipped an English ``<main>``
when this gate was written — 1.000 on the worst locale for the first
three — and all seven are now under 0.12, the worst page on the site
being /tags/ at 0.427 against a 0.60 threshold. So ``--strict`` is on in
build.sh and the Makefile, which is what turns "no page ships an English
body" from an observation that happens to hold into an invariant.

Usage:  python3 tests/validation/test_body_translation.py [--strict]
        python3 tests/validation/test_body_translation.py --update-baseline
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import _lang_registry  # type: ignore[import-not-found]

PUBLIC = ROOT / "public"
BASELINE = Path(__file__).with_name("body-translation-baseline.json")

# A page scoring at or above this shares most of its English wording and is
# treated as untranslated. The observed distribution is bimodal with almost
# nothing between 0.20 and 0.30, so the exact value is not load-bearing.
THRESHOLD = 0.60

# Shorter n-grams match incidental phrasing; longer ones miss reordered
# sentences. Five words is long enough that a genuine translation cannot
# hit it by accident.
NGRAM = 5

# Below this many n-grams the English page has too little prose for the
# ratio to mean anything (a redirect stub, a bare listing).
MIN_NGRAMS = 20

# Drift a page may accumulate before the ratchet calls it a regression.
#
# The floor absorbs a card being added to a listing page. It is not enough
# on its own: pages built largely from article titles carry English that is
# English by design, and their score creeps upward as English articles are
# published. Measured over one build cycle with no work done on either
# page, /tags/ moved +0.006 and /research/ +0.001 — against a flat 0.02
# that is a handful of cycles before a spurious failure.
#
# So the band scales with the recorded value. A page already at 0.4 is one
# whose content churns; a page at 0.0 is not, and stays on the floor. Even
# at the widest this leaves the gate's actual signal untouched: a body
# reverting to English moves the score to ~1.0, tenths above any band here.
TOLERANCE_FLOOR = 0.02
TOLERANCE_FRACTION = 0.15


def tolerance(recorded: float) -> float:
    """Drift allowed for a page recorded at ``recorded``."""
    return max(TOLERANCE_FLOOR, TOLERANCE_FRACTION * recorded)


_MAIN_RE = re.compile(r"<main\b[\s\S]*?</main\s*>", re.IGNORECASE)
_SCRIPT_RE = re.compile(r"<script\b[\s\S]*?</script(?:[\s/][^>]*)?>", re.IGNORECASE)
_STYLE_RE = re.compile(r"<style\b[\s\S]*?</style(?:[\s/][^>]*)?>", re.IGNORECASE)
_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def main_text(path: Path) -> str | None:
    """Visible text of a page's ``<main>``, or None when it has none."""
    html = path.read_text(encoding="utf-8", errors="ignore")
    m = _MAIN_RE.search(html)
    if not m:
        return None
    body = _SCRIPT_RE.sub(" ", m.group(0))
    body = _STYLE_RE.sub(" ", body)
    body = _COMMENT_RE.sub(" ", body)
    body = _TAG_RE.sub(" ", body)
    return _WS_RE.sub(" ", body).strip()


def ngrams(text: str, n: int = NGRAM) -> set[tuple[str, ...]]:
    words = text.split()
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def english_share(en_text: str, loc_text: str) -> float | None:
    """Share of the English page's n-grams reappearing verbatim."""
    en_grams = ngrams(en_text)
    if len(en_grams) < MIN_NGRAMS:
        return None
    return len(en_grams & ngrams(loc_text)) / len(en_grams)


def report() -> dict[str, dict[str, float]]:
    """Per EN static-page slug: worst and median score across locales."""
    scores: dict[str, list[float]] = {}
    for lang in _lang_registry.active():
        if lang.code == "en":
            continue
        for en_slug, native in _lang_registry.load_slugs(lang.code)["static"].items():
            if en_slug.startswith("_"):
                continue
            loc_page = PUBLIC / lang.code / native / "index.html"
            en_page = PUBLIC / en_slug / "index.html"
            if not (loc_page.is_file() and en_page.is_file()):
                continue
            en_text, loc_text = main_text(en_page), main_text(loc_page)
            if not en_text or not loc_text:
                continue
            share = english_share(en_text, loc_text)
            if share is not None:
                scores.setdefault(en_slug, []).append(share)
    return {
        slug: {"worst": max(v), "median": statistics.median(v), "locales": len(v)}
        for slug, v in scores.items()
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="fail on the backlog too")
    ap.add_argument("--update-baseline", action="store_true")
    args = ap.parse_args()

    if not PUBLIC.is_dir():
        print("public/ not built — run ./build.sh first", file=sys.stderr)
        return 0

    current = report()
    if not current:
        print("warn: no localized static pages found", file=sys.stderr)
        return 0

    if args.update_baseline:
        BASELINE.write_text(
            json.dumps({k: round(v["worst"], 3) for k, v in sorted(current.items())}, indent=0)
            + "\n",
            encoding="utf-8",
        )
        print(f"baseline written: {BASELINE.name} ({len(current)} page(s))")
        return 0

    baseline: dict[str, float] = (
        json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.is_file() else {}
    )

    regressions: list[str] = []
    backlog: list[str] = []
    for slug, v in sorted(current.items()):
        worst = v["worst"]
        recorded = baseline.get(slug)
        if recorded is not None and worst > recorded + tolerance(recorded):
            regressions.append(
                f"  {slug}: worst-locale English share {worst:.3f} "
                f"(baseline {recorded:.3f} +{tolerance(recorded):.3f}) "
                f"— a localized <main> reverted to English"
            )
        if worst >= THRESHOLD:
            backlog.append(
                f"  backlog: {slug}: {worst:.3f} worst / {v['median']:.3f} median "
                f"across {v['locales']} locales"
            )

    if regressions:
        print("localized <main> bodies reverted to English:", file=sys.stderr)
        for line in regressions:
            print(line, file=sys.stderr)
        print(
            "\nIf this is intentional, re-record with --update-baseline.",
            file=sys.stderr,
        )
        return 1

    for line in backlog:
        print(line)

    if backlog and args.strict:
        print(
            f"body-translation: {len(backlog)} page(s) still ship an English <main>",
            file=sys.stderr,
        )
        return 1

    print(
        f"body-translation: OK — no page regressed against baseline "
        f"({len(current)} page(s) checked, {len(backlog)} still in backlog)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
