# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Build-output gates for the SEO recovery work (v0.0.30).

Each test reads the built ``public/`` (skipped when it is absent) and
checks one property search engines were penalising:

* locale indexing (``_data/seo/locale-indexing.json``): every page of a
  noindex locale says ``noindex``, no indexed page does unless it is a
  utility page, the sitemap lists only indexed locales, and no hreflang
  alternate anywhere targets a noindex locale;
* every page carries at most one robots meta;
* titles and meta descriptions are unique among indexable pages;
* sitemap ``<lastmod>`` dates are real: no single date covers more than 5%
  of URLs unless every URL carrying it is dated by its own source front
  matter;
* every meta-refresh stub is in ``worker-assets/redirects.json`` with its
  final target, and that map has no chains, loops or dead targets.
"""

from __future__ import annotations

import html as _html
import json
import re
import sys
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "postbuild"))
sys.path.insert(0, str(ROOT / "scripts"))

import _lang_registry as _lr
import _locale_indexing as _li
import build_worker_assets as bwa
from postbuild_lib.indexability import UTILITY_KEYS
from postbuild_lib.sitemap_lastmod import linked_article_dates, source_date, split_locale, url_path
from postbuild_transforms import build_comprehensive_lastmod_index

pytestmark = pytest.mark.skipif(
    not (PUBLIC / "index.html").is_file(), reason="public/ not built: run ./build.sh first"
)

SITE = "https://sebastienrousseau.com"
CODES = frozenset(lang.code for lang in _lr.active())
_ROBOTS_RE = re.compile(r'<meta\s+(?=[^>]*\bname=["\']?robots["\']?[\s/>])[^>]*>', re.I)
_REFRESH_RE = re.compile(r'http-equiv=["\']?refresh', re.I)
_HREFLANG_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']?alternate)(?=[^>]*\bhreflang=["\']?([^"\'\s>]+))'
    r'(?=[^>]*\bhref=["\']?([^"\'\s>]+))[^>]*>',
    re.I,
)
_CANON_RE = re.compile(
    r'<link\b[^>]*\brel=["\']?canonical["\']?[^>]*\bhref=["\']?([^"\'\s>]+)', re.I
)
_TITLE_RE = re.compile(r"<title>([\s\S]*?)</title>", re.I)
_DESC_RE = re.compile(
    r'<meta\s+(?=[^>]*\bname=["\']?description["\']?[\s/>])[^>]*\bcontent=(?:"([^"]*)"|\'([^\']*)\')',
    re.I,
)


def _locale(rel: str) -> str:
    first = rel.split("/", 1)[0]
    return first if "/" in rel and first in CODES else "en"


@cache
def _pages() -> list[tuple[str, str, str]]:
    """``(rel, locale, head)`` for every HTML page, labs demos excluded."""
    out = []
    for page in sorted(PUBLIC.rglob("*.html")):
        rel = page.relative_to(PUBLIC).as_posix()
        if rel.startswith("labs/"):
            continue
        with page.open(encoding="utf-8", errors="ignore") as fh:
            out.append((rel, _locale(rel), fh.read(65536)))
    return out


def _is_noindex(head: str) -> bool:
    return any("noindex" in tag.lower() for tag in _ROBOTS_RE.findall(head))


def _is_utility(rel: str, locale: str) -> bool:
    statics = {} if locale == "en" else _lr.load_slugs(locale).get("static", {})
    prefix = "" if locale == "en" else f"{locale}/"
    return any(rel == f"{prefix}{statics.get(k, k)}/index.html" for k in UTILITY_KEYS)


def _sitemap_locs() -> list[str]:
    return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", (PUBLIC / "sitemap.xml").read_text())


# -- Locale indexing --------------------------------------------------------


def test_every_noindex_locale_page_is_noindex() -> None:
    dropped = set(_li.noindex_codes())
    missing = [rel for rel, loc, head in _pages() if loc in dropped and not _is_noindex(head)]
    assert not missing, f"{len(missing)} noindex-locale page(s) indexable, e.g. {missing[:5]}"


def test_no_indexed_locale_page_is_noindex_except_utility_and_stubs() -> None:
    bad = [
        rel
        for rel, loc, head in _pages()
        if _li.is_indexed(loc)
        and _is_noindex(head)
        and not _is_utility(rel, loc)
        and not _REFRESH_RE.search(head)
    ]
    assert not bad, f"{len(bad)} indexed-locale page(s) carry noindex, e.g. {bad[:5]}"


def test_at_most_one_robots_meta_per_page() -> None:
    multi = [rel for rel, _loc, head in _pages() if len(_ROBOTS_RE.findall(head)) > 1]
    assert not multi, f"{len(multi)} page(s) with several robots metas, e.g. {multi[:5]}"


def test_sitemap_lists_only_indexed_locales() -> None:
    locales = Counter(split_locale(url_path(loc) or "/", CODES)[0] for loc in _sitemap_locs())
    assert set(locales) <= _li.indexed_codes(), sorted(set(locales) - _li.indexed_codes())
    assert set(locales) == _li.indexed_codes(), "an indexed locale vanished from the sitemap"


def test_no_hreflang_targets_a_noindex_locale() -> None:
    dropped = set(_li.noindex_codes())
    bad_values = _li.noindex_hreflangs()
    hits = []
    for rel, loc, head in _pages():
        for value, href in _HREFLANG_RE.findall(head):
            target = split_locale(url_path(href) or "/", CODES)[0]
            if loc in dropped or value.lower() in bad_values or target in dropped:
                hits.append(f"{rel} -> {value} {href}")
    assert not hits, f"{len(hits)} hreflang link(s) involve a noindex locale, e.g. {hits[:5]}"


# -- Unique titles and descriptions -----------------------------------------


def _indexable_heads() -> list[tuple[str, str]]:
    out = []
    for rel, _loc, head in _pages():
        if not rel.endswith("index.html") or _is_noindex(head) or _REFRESH_RE.search(head):
            continue
        canon = _CANON_RE.search(head)
        url = f"{SITE}/{rel.removesuffix('index.html')}"
        if canon and canon.group(1).rstrip("/") != url.rstrip("/"):
            continue
        out.append((rel, head))
    return out


def _duplicates(values: dict[str, list[str]]) -> dict[str, list[str]]:
    return {v: rels for v, rels in values.items() if v and len(rels) > 1}


def test_titles_unique_among_indexable_pages() -> None:
    seen: dict[str, list[str]] = defaultdict(list)
    for rel, head in _indexable_heads():
        m = _TITLE_RE.search(head)
        seen[_html.unescape(m.group(1).strip()) if m else ""].append(rel)
    dup = _duplicates(seen)
    assert not dup, f"{len(dup)} duplicate title(s): {list(dup.items())[:3]}"


def test_descriptions_unique_among_indexable_pages() -> None:
    seen: dict[str, list[str]] = defaultdict(list)
    for rel, head in _indexable_heads():
        m = _DESC_RE.search(head)
        seen[_html.unescape(m.group(1) or m.group(2) or "") if m else ""].append(rel)
    dup = _duplicates(seen)
    assert not dup, f"{len(dup)} duplicate description(s): {list(dup.items())[:3]}"


# -- Sitemap lastmod ----------------------------------------------------------


def _sitemap_dates() -> dict[str, str]:
    text = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
    out = {}
    for block in re.findall(r"<url>[\s\S]*?</url>", text):
        lm = re.search(r"<lastmod>([^<]+)</lastmod>", block)
        loc = re.search(r"<loc>\s*([^<\s]+)", block)
        if lm and loc:
            out[url_path(loc.group(1)) or "/"] = lm.group(1)
    return out


def _backed(path: str, date: str, index: dict[str, str], dates: dict[str, str]) -> bool:
    """True when ``date`` is the page's own source date, or the date of an
    article page it links to (how a listing page is dated)."""
    if source_date(path, index, CODES) == date:
        return True
    page = PUBLIC / path.lstrip("/") / "index.html"
    html = page.read_text(encoding="utf-8", errors="ignore") if page.is_file() else ""
    return date in linked_article_dates(html, dates)


def test_no_lastmod_date_dominates_unless_sourced() -> None:
    # A date may legitimately cover many URLs: 31 articles were reviewed on
    # 2026-05-11 (341 locale URLs), and every listing that shows the newest
    # article shares its date. What must never dominate is a date with no
    # source behind it, which is what the old build-date stamp was.
    dates = _sitemap_dates()
    total = len(_sitemap_locs())
    index = build_comprehensive_lastmod_index()
    by_date: dict[str, list[str]] = defaultdict(list)
    for path, date in dates.items():
        by_date[date].append(path)
    for date, paths in by_date.items():
        if len(paths) <= 0.05 * total:
            continue
        unbacked = [p for p in paths if not _backed(p, date, index, dates)]
        assert not unbacked, (
            f"lastmod {date} covers {len(paths)}/{total} URLs; {len(unbacked)} have no "
            f"source or linked article with that date, e.g. {unbacked[:5]}"
        )


def test_nearly_every_sitemap_url_has_a_real_lastmod() -> None:
    text = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
    dated = len(re.findall(r"<lastmod>", text))
    assert dated >= 0.9 * len(_sitemap_locs()), f"only {dated} URLs dated"


# -- Worker redirect map ------------------------------------------------------


def _committed_map() -> dict[str, str]:
    payload = json.loads((ROOT / "worker-assets" / "redirects.json").read_text(encoding="utf-8"))
    return payload["redirects"]


def test_every_stub_has_its_final_target_in_the_worker_map() -> None:
    expected = bwa.collapse_chains(bwa.stub_redirects(PUBLIC))
    committed = _committed_map()
    missing = sorted(set(expected) - set(committed))
    wrong = sorted(k for k in expected if k in committed and committed[k] != expected[k])
    extra = sorted(set(committed) - set(expected))
    assert not missing, f"{len(missing)} stub(s) not in redirects.json, e.g. {missing[:5]}"
    assert not wrong, f"{len(wrong)} stub(s) map elsewhere, e.g. {wrong[:5]}"
    assert not extra, f"{len(extra)} map entrie(s) with no stub, e.g. {extra[:5]}"


def test_worker_map_has_no_chain_loop_or_dead_target() -> None:
    committed = _committed_map()
    assert committed, "redirects.json is empty"
    for source, target in committed.items():
        assert source != target, f"self-redirect {source}"
        assert target not in committed, f"chain {source} -> {target} -> {committed[target]}"
        page = PUBLIC / target.lstrip("/") / "index.html"
        assert page.is_file(), f"{source} -> {target}: target does not render"
        head = page.read_text(encoding="utf-8", errors="ignore")[:16384]
        assert not _REFRESH_RE.search(head), f"{source} -> {target}: target is itself a stub"
