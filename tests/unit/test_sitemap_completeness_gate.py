"""Unit tests for tests/validation/test_sitemap_completeness.py.

The gate reads the *root* sitemap and follows sitemap indexes. It must not
walk the tree: ssg drops a full copy of the sitemap into every output
directory, and each copy prefixes its URLs with the containing directory,
producing malformed double-slash entries. On this site that is thousands
of files and gigabytes of duplicated junk, which turned a one-second gate
into a multi-minute one without adding a single URL the root sitemap did
not already list.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "sitemap_completeness_gate",
    ROOT / "tests" / "validation" / "test_sitemap_completeness.py",
)
gate = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gate
_SPEC.loader.exec_module(gate)

SITE = gate.SITE


def _urlset(*urls: str) -> str:
    locs = "".join(f"<loc>{u}</loc>" for u in urls)
    return f'<?xml version="1.0"?><urlset xmlns="x">{locs}</urlset>'


def _sitemapindex(*urls: str) -> str:
    locs = "".join(f"<sitemap><loc>{u}</loc></sitemap>" for u in urls)
    return f'<?xml version="1.0"?><sitemapindex xmlns="x">{locs}</sitemapindex>'


def _public(tmp_path: Path, monkeypatch) -> Path:
    pub = tmp_path / "public"
    pub.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(gate, "PUBLIC", pub)
    return pub


# ---------------------------------------------------------------------------
# collect_sitemap_urls
# ---------------------------------------------------------------------------


def test_reads_root_sitemap(tmp_path, monkeypatch):
    pub = _public(tmp_path, monkeypatch)
    (pub / "sitemap.xml").write_text(_urlset(f"{SITE}/a/", f"{SITE}/b/"), encoding="utf-8")
    assert gate.collect_sitemap_urls() == {f"{SITE}/a", f"{SITE}/b"}


def test_ignores_per_directory_duplicate_sitemaps(tmp_path, monkeypatch):
    """The regression: nested copies carry directory-prefixed junk URLs."""
    pub = _public(tmp_path, monkeypatch)
    (pub / "sitemap.xml").write_text(_urlset(f"{SITE}/a/"), encoding="utf-8")
    nested = pub / "some-article"
    nested.mkdir()
    (nested / "sitemap.xml").write_text(
        _urlset(f"{SITE}/some-article//a/", f"{SITE}/some-article//b/"),
        encoding="utf-8",
    )
    urls = gate.collect_sitemap_urls()
    assert urls == {f"{SITE}/a"}
    assert not any("//a" in u or "some-article" in u for u in urls)


def test_follows_sitemap_index(tmp_path, monkeypatch):
    pub = _public(tmp_path, monkeypatch)
    (pub / "sitemap.xml").write_text(_sitemapindex(f"{SITE}/sitemap-fr.xml"), encoding="utf-8")
    (pub / "sitemap-fr.xml").write_text(_urlset(f"{SITE}/fr/a/"), encoding="utf-8")
    assert gate.collect_sitemap_urls() == {f"{SITE}/fr/a"}


def test_index_pointing_at_missing_file_is_ignored(tmp_path, monkeypatch):
    pub = _public(tmp_path, monkeypatch)
    (pub / "sitemap.xml").write_text(_sitemapindex(f"{SITE}/nope.xml"), encoding="utf-8")
    assert gate.collect_sitemap_urls() == set()


def test_index_cycle_terminates(tmp_path, monkeypatch):
    """A self-referential index must not spin forever."""
    pub = _public(tmp_path, monkeypatch)
    (pub / "sitemap.xml").write_text(_sitemapindex(f"{SITE}/sitemap.xml"), encoding="utf-8")
    assert gate.collect_sitemap_urls() == set()


def test_missing_root_sitemap_yields_empty_set(tmp_path, monkeypatch):
    _public(tmp_path, monkeypatch)
    assert gate.collect_sitemap_urls() == set()


# ---------------------------------------------------------------------------
# _is_redirect_page — bounded read
# ---------------------------------------------------------------------------


def test_redirect_page_detected(tmp_path):
    p = tmp_path / "index.html"
    p.write_text('<head><meta http-equiv="refresh" content="0"></head>', encoding="utf-8")
    assert gate._is_redirect_page(p) is True


def test_non_redirect_page_not_detected(tmp_path):
    p = tmp_path / "index.html"
    p.write_text("<head><title>x</title></head><body>hi</body>", encoding="utf-8")
    assert gate._is_redirect_page(p) is False


def test_redirect_sniff_reads_only_the_head(tmp_path):
    """Only the first 4 KB is consulted, so a refresh buried past that
    boundary is deliberately not treated as a redirect — and, more to the
    point, whole pages are never pulled into memory."""
    p = tmp_path / "index.html"
    p.write_text(
        "<head>" + ("x" * 5000) + '<meta http-equiv="refresh" content="0"></head>',
        encoding="utf-8",
    )
    assert gate._is_redirect_page(p) is False
