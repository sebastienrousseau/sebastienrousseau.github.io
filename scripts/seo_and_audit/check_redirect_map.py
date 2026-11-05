#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Fail when the committed Worker redirect map disagrees with the build.

``scripts/build_worker_assets.py`` derives ``worker-assets/redirects.json``
from the meta-refresh stubs in the built ``public/`` and keeps the committed
file when ``public/`` is not built. The lang-router Worker serves that
committed file, so nothing stopped it drifting from the site: a renamed URL
missing from the map answers with a stub page instead of a 301, and a stale
entry 301s a reader away from a page that now exists. ``build.sh`` rewrites
the file in the working tree, so comparing against the working tree after a
build proves nothing; this compares against git ``HEAD``.

Checks, each against a freshly built ``public/``:

1. the map regenerated from the build (written to a temporary path) is
   byte-identical to the committed one;
2. every target is a real page in ``public/``, not a stub;
3. no source is a real page (the Worker would redirect live content);
4. no chains and no loops (``collapse_chains`` raises on a build loop);
5. every ``_data/redirects/articles.json`` entry in a kept locale
   (``_data/seo/locale-indexing.json``) is in the map, or is listed with
   its reason in ``_data/redirects/map-exemptions.json``. A listed entry
   that is in the map after all, or no longer in ``articles.json``, fails
   too, so the list cannot go stale.

Usage: ``./build.sh && python3 scripts/seo_and_audit/check_redirect_map.py``
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import build_worker_assets as bwa
from _locale_indexing import indexed_codes

MAP_REL = "worker-assets/redirects.json"
PUBLIC = ROOT / "public"
ARTICLES = ROOT / "_data" / "redirects" / "articles.json"
EXEMPTIONS = ROOT / "_data" / "redirects" / "map-exemptions.json"
SHOWN = 20


def committed_text(path: Path | None) -> str:
    """The committed map: ``path`` if given, else ``git show HEAD:<map>``."""
    if path is not None:
        return path.read_text(encoding="utf-8")
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{MAP_REL}"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def regenerate(public: Path) -> tuple[str, Path]:
    """Rebuild the map from ``public/`` into a temp file; ``(text, path)``.

    Raises ``RedirectMapError`` on a loop or an off-site stub target.
    """
    text = bwa.render_redirects(bwa.collapse_chains(bwa.stub_redirects(public)))
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", prefix="redirects-", suffix=".json", delete=False
    ) as fh:
        fh.write(text)
    return text, Path(fh.name)


def _entries(text: str) -> dict[str, str]:
    redirects: dict[str, str] = json.loads(text)["redirects"]
    return redirects


def check_drift(committed: str, built: str) -> list[str]:
    """Check 1: one problem summarising any difference, else none."""
    if committed == built:
        return []
    old, new = _entries(committed), _entries(built)
    added = len(new.keys() - old.keys())
    removed = len(old.keys() - new.keys())
    changed = sum(1 for k in old.keys() & new.keys() if old[k] != new[k])
    return [
        f"{MAP_REL} differs from the build: {added} added, {removed} removed, "
        f"{changed} changed. Run ./build.sh (it regenerates the map) and "
        f"commit {MAP_REL}."
    ]


def _page_kind(public: Path, path: str) -> str:
    """``missing``, ``stub`` or ``page`` for a site path such as ``/fr/x/``."""
    page = public / path.strip("/") / "index.html"
    if not page.is_file():
        return "missing"
    return "stub" if bwa.refresh_url(page) else "page"


def check_targets(public: Path, redirects: dict[str, str]) -> list[str]:
    """Check 2: every target renders and is not itself a stub."""
    reasons = {"missing": "target does not render", "stub": "target is itself a redirect stub"}
    problems = []
    for source, target in redirects.items():
        kind = _page_kind(public, target)
        if kind != "page":
            problems.append(f"{source} -> {target}: {reasons[kind]}")
    return problems


def check_sources(public: Path, redirects: dict[str, str]) -> list[str]:
    """Check 3: no source is a live page."""
    return [
        f"{source} is a live page but the map redirects it"
        for source in redirects
        if _page_kind(public, source) == "page"
    ]


def check_chains(redirects: dict[str, str]) -> list[str]:
    """Check 4: every entry is one hop to a path that is not a source."""
    problems = []
    for source, target in redirects.items():
        if source == target:
            problems.append(f"loop {source} -> {target}")
        elif target in redirects:
            problems.append(f"chain {source} -> {target} -> {redirects[target]}")
    return problems


def load_articles(path: Path) -> dict[str, dict[str, str]]:
    """``{locale: {old slug: new slug}}`` from ``articles.json``."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return {code: mapping for code, mapping in data.items() if not code.startswith("_")}


def load_exemptions(path: Path) -> dict[str, str]:
    """``{source path: reason}`` for article redirects absent on purpose."""
    if not path.is_file():
        return {}
    absent: dict[str, str] = json.loads(path.read_text(encoding="utf-8"))["absent"]
    return absent


def _article_sources(articles: dict[str, dict[str, str]], kept: set[str]) -> list[tuple[str, str]]:
    """``(source path, locale)`` of every article redirect in a kept locale."""
    out: list[tuple[str, str]] = []
    for code, mapping in articles.items():
        if code in kept:
            prefix = "/" if code == "en" else f"/{code}/"
            out.extend((f"{prefix}{dead}/", code) for dead in mapping)
    return out


def check_articles(
    redirects: dict[str, str],
    articles: dict[str, dict[str, str]],
    reasons: dict[str, str],
    kept: set[str],
) -> list[str]:
    """Check 5: kept-locale article redirects are mapped or explained."""
    sources = _article_sources(articles, kept)
    problems = [
        f"{src} (articles.json, {code}) is not in the map and has no listed reason"
        for src, code in sources
        if src not in redirects and src not in reasons
    ]
    known = {src for src, _ in sources}
    for src in sorted(reasons):
        if src in redirects:
            problems.append(f"{src} is listed as absent but is in the map")
        elif src not in known:
            problems.append(
                f"{src} is listed as absent but is not in articles.json for a kept locale"
            )
    return problems


def parse_kept(value: str | None) -> set[str]:
    """Kept locales: ``--kept a,b`` or the locale-indexing policy."""
    if value:
        return {code.strip() for code in value.split(",") if code.strip()}
    return set(indexed_codes())


def report(name: str, problems: list[str]) -> None:
    """Print one check's problems to stderr, at most ``SHOWN`` of them."""
    print(f"check_redirect_map: {name}: {len(problems)} problem(s)", file=sys.stderr)
    for line in problems[:SHOWN]:
        print(f"  ::error::{line}", file=sys.stderr)
    if len(problems) > SHOWN:
        print(f"  ... and {len(problems) - SHOWN} more", file=sys.stderr)


def _parse(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--public", type=Path, default=PUBLIC)
    parser.add_argument("--committed", type=Path, help=f"map file (default: git HEAD:{MAP_REL})")
    parser.add_argument("--articles", type=Path, default=ARTICLES)
    parser.add_argument("--exemptions", type=Path, default=EXEMPTIONS)
    parser.add_argument("--kept", help="comma-separated kept locales (default: the policy)")
    return parser.parse_args(argv)


def run_checks(args: argparse.Namespace) -> dict[str, list[str]]:
    """Every check's problems, keyed by check name."""
    committed = committed_text(args.committed)
    redirects = _entries(committed)
    results: dict[str, list[str]] = {}
    try:
        built, tmp = regenerate(args.public)
        results["drift"] = check_drift(committed, built)
        tmp.unlink()
    except bwa.RedirectMapError as exc:
        results["drift"] = [f"the build's stubs cannot form a map: {exc}"]
    results["targets"] = check_targets(args.public, redirects)
    results["sources"] = check_sources(args.public, redirects)
    results["chains"] = check_chains(redirects)
    results["articles"] = check_articles(
        redirects,
        load_articles(args.articles),
        load_exemptions(args.exemptions),
        parse_kept(args.kept),
    )
    return results


def main(argv: list[str] | None = None) -> int:
    args = _parse(argv)
    if not (args.public / "index.html").is_file():
        print(f"check_redirect_map: {args.public} is not built; run ./build.sh", file=sys.stderr)
        return 2
    results = run_checks(args)
    failed = {name: problems for name, problems in results.items() if problems}
    for name, problems in failed.items():
        report(name, problems)
    if failed:
        return 1
    count = len(_entries(committed_text(args.committed)))
    print(f"check_redirect_map: OK, {count} redirects match the build")
    return 0


if __name__ == "__main__":
    sys.exit(main())
