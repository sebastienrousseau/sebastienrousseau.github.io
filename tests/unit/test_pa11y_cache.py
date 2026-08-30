# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Unit tests for the pa11y hash cache."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "seo_and_audit"))
import pa11y_cache as pc


@pytest.fixture
def public_dir(tmp_path: Path) -> Path:
    """Build a tiny synthetic public/ tree with three pages."""
    base = tmp_path / "public"
    (base / "page-a").mkdir(parents=True)
    (base / "page-a" / "index.html").write_text("<html>A</html>", encoding="utf-8")
    (base / "page-b").mkdir(parents=True)
    (base / "page-b" / "index.html").write_text("<html>B</html>", encoding="utf-8")
    (base / "ar" / "page-c").mkdir(parents=True)
    (base / "ar" / "page-c" / "index.html").write_text("<html>C</html>", encoding="utf-8")
    return base


# ---------------------------------------------------------------------------
# Hashing helpers
# ---------------------------------------------------------------------------


def test_compute_page_hash_is_deterministic(tmp_path: Path) -> None:
    p = tmp_path / "x.html"
    p.write_text("hello world", encoding="utf-8")
    h1 = pc.compute_page_hash(p)
    h2 = pc.compute_page_hash(p)
    assert h1 == h2
    assert len(h1) == 64


def test_compute_page_hash_changes_with_content(tmp_path: Path) -> None:
    a = tmp_path / "a.html"
    a.write_text("alpha", encoding="utf-8")
    b = tmp_path / "b.html"
    b.write_text("beta", encoding="utf-8")
    assert pc.compute_page_hash(a) != pc.compute_page_hash(b)


def test_compute_page_hash_normalises_csp_bundle_filename(tmp_path: Path) -> None:
    """The SSG's CSP plugin bundles stylesheets/scripts into
    ``/_csp/<hex>.{css,js}`` files where the hash IS the filename (no
    name prefix). Two pages that reference different bundle hashes
    but are otherwise identical must collapse to the same cache key
    so a layout-only PR doesn't bust the cache for every page."""
    a = tmp_path / "a.html"
    a.write_text(
        "<html><head>"
        '<link rel="stylesheet" href="/_csp/97f63c950cabc48b.css">'
        '<script src="/_csp/3ae64e6558e84d20.js"></script>'
        "</head><body><h1>Hi</h1></body></html>",
        encoding="utf-8",
    )
    b = tmp_path / "b.html"
    b.write_text(
        "<html><head>"
        '<link rel="stylesheet" href="/_csp/46e68e1191726dec.css">'
        '<script src="/_csp/8f94793606401e0a.js"></script>'
        "</head><body><h1>Hi</h1></body></html>",
        encoding="utf-8",
    )
    assert pc.compute_page_hash(a) == pc.compute_page_hash(b)


def test_compute_page_hash_normalises_fingerprinted_assets(tmp_path: Path) -> None:
    """A page whose only diff between two builds is the asset
    fingerprint (``main.<hash>.js``) must produce the same cache key,
    otherwise every layout-touching commit busts the whole cache."""
    a = tmp_path / "a.html"
    a.write_text(
        "<html><head>"
        '<script src="/main.799e2fd8.js"></script>'
        '<link rel="stylesheet" href="/main.799e2fd8.css">'
        "</head><body><h1>Hi</h1></body></html>",
        encoding="utf-8",
    )
    b = tmp_path / "b.html"
    b.write_text(
        "<html><head>"
        '<script src="/main.f085a635.js"></script>'
        '<link rel="stylesheet" href="/main.f085a635.css">'
        "</head><body><h1>Hi</h1></body></html>",
        encoding="utf-8",
    )
    assert pc.compute_page_hash(a) == pc.compute_page_hash(b)


def test_compute_page_hash_normalises_integrity_attribute(tmp_path: Path) -> None:
    """SRI integrity hashes rotate every build; they're not pa11y-
    relevant, so they shouldn't bust the cache."""
    a = tmp_path / "a.html"
    a.write_text(
        '<html><head><link href="/m.css" '
        'integrity="sha256-abc123def456ghi789jkl012mno345pqrs678="></head>'
        "<body>Hi</body></html>",
        encoding="utf-8",
    )
    b = tmp_path / "b.html"
    b.write_text(
        '<html><head><link href="/m.css" '
        'integrity="sha256-zzz999yyy888xxx777www666vvv555uuu444==="></head>'
        "<body>Hi</body></html>",
        encoding="utf-8",
    )
    assert pc.compute_page_hash(a) == pc.compute_page_hash(b)


def test_compute_page_hash_normalises_csp_sha256_hashes(tmp_path: Path) -> None:
    """CSP inline-script/style hashes rotate every build; identical
    rationale to SRI."""
    a = tmp_path / "a.html"
    a.write_text(
        "<html><head>"
        "<meta http-equiv=Content-Security-Policy content=\"script-src 'self' "
        "'sha256-abcdefghij1234567890ABCDEFGH+/=='\"></head>"
        "<body>Hi</body></html>",
        encoding="utf-8",
    )
    b = tmp_path / "b.html"
    b.write_text(
        "<html><head>"
        "<meta http-equiv=Content-Security-Policy content=\"script-src 'self' "
        "'sha256-zzzzzzzzzz9999999999AAAAAAAAA+/=='\"></head>"
        "<body>Hi</body></html>",
        encoding="utf-8",
    )
    assert pc.compute_page_hash(a) == pc.compute_page_hash(b)


def test_compute_page_hash_normalises_query_cache_busters(tmp_path: Path) -> None:
    """``?v=20260618`` style cache-busters on asset hrefs shouldn't
    invalidate the pa11y cache."""
    a = tmp_path / "a.html"
    a.write_text('<link href="/x.css?v=20260618">', encoding="utf-8")
    b = tmp_path / "b.html"
    b.write_text('<link href="/x.css?v=20260601">', encoding="utf-8")
    assert pc.compute_page_hash(a) == pc.compute_page_hash(b)


def test_compute_page_hash_still_changes_on_semantic_diff(tmp_path: Path) -> None:
    """The normaliser must NOT swallow real content changes — a
    different heading text must still produce a different hash."""
    a = tmp_path / "a.html"
    a.write_text(
        '<html><head><script src="/main.aaaaaaaa.js"></script></head>'
        "<body><h1>Original</h1></body></html>",
        encoding="utf-8",
    )
    b = tmp_path / "b.html"
    b.write_text(
        '<html><head><script src="/main.aaaaaaaa.js"></script></head>'
        "<body><h1>Updated</h1></body></html>",
        encoding="utf-8",
    )
    assert pc.compute_page_hash(a) != pc.compute_page_hash(b)


def test_compute_config_hash_ignores_urls() -> None:
    """The config hash MUST be stable across runs even though the URL
    list changes — otherwise the fingerprint would invalidate the cache
    on every run."""
    c1 = pc.build_pa11yci_config(
        urls=["http://x.example/"],
        hide_elements="iframe[src*='x']",
    )
    c2 = pc.build_pa11yci_config(
        urls=["http://y.example/", "http://z.example/"],
        hide_elements="iframe[src*='x']",
    )
    assert pc.compute_config_hash(c1) == pc.compute_config_hash(c2)


def test_compute_config_hash_changes_with_hide_elements() -> None:
    c1 = pc.build_pa11yci_config(urls=[], hide_elements="iframe.a")
    c2 = pc.build_pa11yci_config(urls=[], hide_elements="iframe.b")
    assert pc.compute_config_hash(c1) != pc.compute_config_hash(c2)


# ---------------------------------------------------------------------------
# Cache I/O
# ---------------------------------------------------------------------------


def test_load_cache_missing_returns_skeleton(tmp_path: Path) -> None:
    cache = pc.load_cache(tmp_path / "nope.json")
    assert cache == {"version": pc.CACHE_VERSION, "fingerprint": {}, "pages": {}}


def test_load_cache_invalid_json_returns_skeleton(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("not json{{{", encoding="utf-8")
    cache = pc.load_cache(p)
    assert cache["pages"] == {}


def test_load_cache_old_version_returns_skeleton(tmp_path: Path) -> None:
    """If the schema version drops, the old entries shouldn't be
    trusted — they could be in a different shape."""
    p = tmp_path / "old.json"
    p.write_text(json.dumps({"version": 0, "pages": {"foo/index.html": {}}}), encoding="utf-8")
    cache = pc.load_cache(p)
    assert cache["pages"] == {}


def test_save_then_load_roundtrips(tmp_path: Path) -> None:
    p = tmp_path / "_data" / "pa11y-cache.json"
    payload = {
        "version": pc.CACHE_VERSION,
        "fingerprint": {"pa11y_version": "3.1.0"},
        "pages": {"a/index.html": {"hash": "abc", "status": "pass"}},
    }
    pc.save_cache(p, payload)
    assert p.is_file()
    reloaded = pc.load_cache(p)
    assert reloaded == payload


# ---------------------------------------------------------------------------
# Fingerprint comparison
# ---------------------------------------------------------------------------


def _fp(
    pa11y: str = "3.1.0", chromium: str = "130.0", cfg: str = "abc", std: str = "WCAG2AAA"
) -> dict:
    return {
        "pa11y_version": pa11y,
        "chromium_version": chromium,
        "config_hash": cfg,
        "wcag_standard": std,
    }


def test_fingerprint_matches_full_equality() -> None:
    cache = {"fingerprint": _fp()}
    assert pc.fingerprint_matches(cache, _fp())


@pytest.mark.parametrize(
    "key", ["pa11y_version", "chromium_version", "config_hash", "wcag_standard"]
)
def test_fingerprint_mismatch_on_any_key(key: str) -> None:
    cache = {"fingerprint": _fp()}
    diff = _fp()
    diff[key] = "DIFFERENT"
    assert not pc.fingerprint_matches(cache, diff)


def test_fingerprint_missing_in_cache_is_mismatch() -> None:
    """An empty cache (first ever run) must never report a hit."""
    cache = {"fingerprint": {}}
    assert not pc.fingerprint_matches(cache, _fp())


# ---------------------------------------------------------------------------
# Spotify-iframe detection
# ---------------------------------------------------------------------------


def test_page_is_spotify_iframe_true() -> None:
    html = '<html><body><iframe src="https://open.spotify.com/embed/x"></iframe></body></html>'
    assert pc.page_is_spotify_iframe(html)


def test_page_is_spotify_iframe_false_no_iframe() -> None:
    html = "<html><body>open.spotify.com mentioned in prose</body></html>"
    assert not pc.page_is_spotify_iframe(html)


def test_page_is_spotify_iframe_false_other_iframe() -> None:
    html = '<html><body><iframe src="https://www.youtube.com/embed/y"></iframe></body></html>'
    assert not pc.page_is_spotify_iframe(html)


def test_page_is_spotify_iframe_scdn_variant() -> None:
    html = '<html><body><iframe src="https://i.scdn.co/embed"></iframe></body></html>'
    assert pc.page_is_spotify_iframe(html)


# ---------------------------------------------------------------------------
# page_should_skip — composite skip predicate (zero-value + iframe)
# ---------------------------------------------------------------------------


def test_page_should_skip_made_with_static_site_generator() -> None:
    """The Static Site Generator credit page is generated boilerplate;
    its a11y surface is already exercised by every other page on the
    site, so pa11y can skip it."""
    html = "<html><body><p>Made with Static Site Generator.</p></body></html>"
    assert pc.page_should_skip(html, "made-with-static-site-generator/index.html")


def test_page_should_skip_normal_content_page() -> None:
    """Editorial pages must NOT be on the skip list — they carry
    unique semantic content that pa11y has to validate."""
    html = "<html><body><h1>Real article</h1></body></html>"
    assert not pc.page_should_skip(html, "2026-06-18-real-article/index.html")


def test_page_should_skip_spotify_iframe_via_compound_predicate() -> None:
    """Spotify iframe detection still routes through page_should_skip
    even when the relpath isn't on the explicit zero-value list."""
    html = '<html><body><iframe src="https://open.spotify.com/embed/x"></iframe></body></html>'
    assert pc.page_should_skip(html, "playlists/foo/index.html")


def test_page_should_skip_locale_prefixed_made_with_not_skipped() -> None:
    """The zero-value list is anchored on bare EN slugs — a locale-
    prefixed equivalent (if one ever existed) would NOT be skipped
    until someone explicitly extends the list."""
    html = "<html><body><p>Made with Static Site Generator.</p></body></html>"
    assert not pc.page_should_skip(html, "fr/made-with-static-site-generator/index.html")


# ---------------------------------------------------------------------------
# page_is_redirect_stub - instant meta-refresh redirect stubs
# ---------------------------------------------------------------------------


def test_page_is_redirect_stub_true_for_meta_refresh() -> None:
    """The /papers/ -> /research/ moves ship 29 instant meta-refresh
    stubs. Puppeteer follows the refresh before pa11y evaluates, so the
    sweep would score the (production) redirect target, not the stub."""
    html = (
        '<html lang="en-GB"><head>'
        '<meta http-equiv="refresh" content="0; url=https://example.com/research/" />'
        "<title>Moved</title></head><body><p>This page has moved.</p></body></html>"
    )
    assert pc.page_is_redirect_stub(html)
    assert pc.page_should_skip(html, "papers/index.html")


def test_page_is_redirect_stub_false_for_normal_page() -> None:
    html = '<html lang="en-GB"><head><title>Real</title></head><body><h1>Hi</h1></body></html>'
    assert not pc.page_is_redirect_stub(html)
    assert not pc.page_should_skip(html, "research/index.html")


def test_page_is_redirect_stub_ignores_body_prose_about_meta_refresh() -> None:
    """Only the <head> slice is scanned: an article whose body quotes a
    meta-refresh snippet must still be swept."""
    html = (
        '<html lang="en-GB"><head><title>Article</title></head><body>'
        '<pre>&lt;meta http-equiv="refresh"&gt;</pre>'
        '<p>Raw example: <meta http-equiv="refresh" content="0; url=/x/"></p>'
        "</body></html>"
    )
    assert not pc.page_is_redirect_stub(html)


# ---------------------------------------------------------------------------
# partition_pages — the heart of the cache decision
# ---------------------------------------------------------------------------


def test_partition_empty_cache_sweeps_everything(public_dir: Path) -> None:
    to_sweep, cache_hits, skipped = pc.partition_pages(
        public_dir,
        cache={"fingerprint": {}, "pages": {}},
        current_fingerprint=_fp(),
    )
    assert len(to_sweep) == 3
    assert cache_hits == []
    assert skipped == []


def test_partition_full_cache_hit(public_dir: Path) -> None:
    """When every page's hash is cached at the current fingerprint,
    to_sweep is empty."""
    pages: dict[str, dict] = {}
    for rel_dir in ("page-a", "page-b", "ar/page-c"):
        p = public_dir / rel_dir / "index.html"
        rel = p.relative_to(public_dir).as_posix()
        pages[rel] = {"hash": pc.compute_page_hash(p), "status": "pass"}
    cache = {"version": pc.CACHE_VERSION, "fingerprint": _fp(), "pages": pages}
    to_sweep, cache_hits, _ = pc.partition_pages(public_dir, cache, _fp())
    assert to_sweep == []
    assert len(cache_hits) == 3


def test_partition_one_page_changed(public_dir: Path) -> None:
    """Cache hit on the unchanged page, sweep the changed one."""
    pages = {
        "page-a/index.html": {
            "hash": pc.compute_page_hash(public_dir / "page-a" / "index.html"),
            "status": "pass",
        },
        # page-b stored with a STALE hash (wrong hex) -> must re-sweep.
        "page-b/index.html": {"hash": "0" * 64, "status": "pass"},
        "ar/page-c/index.html": {
            "hash": pc.compute_page_hash(public_dir / "ar" / "page-c" / "index.html"),
            "status": "pass",
        },
    }
    cache = {"version": pc.CACHE_VERSION, "fingerprint": _fp(), "pages": pages}
    to_sweep, cache_hits, _ = pc.partition_pages(public_dir, cache, _fp())
    assert len(to_sweep) == 1
    assert len(cache_hits) == 2
    assert to_sweep[0][0].name == "index.html"
    assert "page-b" in to_sweep[0][0].as_posix()


def test_partition_fingerprint_mismatch_busts_entire_cache(public_dir: Path) -> None:
    """Even with every hash correct, a fingerprint mismatch (e.g.
    Chromium upgrade) forces a full re-sweep."""
    pages = {
        f"{rel}/index.html": {
            "hash": pc.compute_page_hash(public_dir / rel / "index.html"),
            "status": "pass",
        }
        for rel in ("page-a", "page-b", "ar/page-c")
    }
    cache = {"version": pc.CACHE_VERSION, "fingerprint": _fp(chromium="OLD"), "pages": pages}
    to_sweep, cache_hits, _ = pc.partition_pages(public_dir, cache, _fp(chromium="NEW"))
    assert len(to_sweep) == 3
    assert cache_hits == []


def test_partition_skips_spotify_iframe_pages(public_dir: Path) -> None:
    # Replace page-b with a Spotify embed.
    (public_dir / "page-b" / "index.html").write_text(
        '<html><iframe src="https://open.spotify.com/embed/foo"></iframe></html>',
        encoding="utf-8",
    )
    to_sweep, cache_hits, skipped = pc.partition_pages(
        public_dir,
        cache={"fingerprint": {}, "pages": {}},
        current_fingerprint=_fp(),
    )
    assert "page-b/index.html" in skipped
    swept_rels = [p.relative_to(public_dir).as_posix() for p, _ in to_sweep]
    assert "page-b/index.html" not in swept_rels
    assert len(to_sweep) + len(skipped) == 3
    assert cache_hits == []


# ---------------------------------------------------------------------------
# End-to-end: pre then post mirrors the CI workflow
# ---------------------------------------------------------------------------


def test_e2e_first_run_sweeps_all_then_caches_all(
    public_dir: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate the first CI run: cache is empty, all three pages get
    swept, the post-pass marks all three as passing. The next run
    partitioning then reports zero to-sweep."""
    cache_path = tmp_path / "_data" / "pa11y-cache.json"
    pa11yci = tmp_path / ".pa11yci"
    manifest = tmp_path / ".pa11y-cache-manifest.json"

    monkeypatch.setattr(pc, "detect_pa11y_version", lambda: "3.1.0")
    monkeypatch.setattr(pc, "detect_chromium_version", lambda: "130.0.0.0")

    # PRE
    import argparse

    rc = pc.cmd_pre(
        argparse.Namespace(
            public_dir=str(public_dir),
            cache=str(cache_path),
            pa11yci_out=str(pa11yci),
            manifest_out=str(manifest),
            base_url="http://127.0.0.1:8000",
            pa11y_version="",
            chromium_version="",
            hide_elements="",
        )
    )
    assert rc == 0
    assert pa11yci.is_file()
    cfg = json.loads(pa11yci.read_text())
    assert len(cfg["urls"]) == 3  # all pages need sweeping on first run

    # POST (simulate pa11y returning success)
    rc = pc.cmd_post(
        argparse.Namespace(
            public_dir=str(public_dir),
            cache=str(cache_path),
            manifest=str(manifest),
        )
    )
    assert rc == 0
    cache = pc.load_cache(cache_path)
    assert len(cache["pages"]) == 3

    # PRE again — every page is now cache-hit
    rc = pc.cmd_pre(
        argparse.Namespace(
            public_dir=str(public_dir),
            cache=str(cache_path),
            pa11yci_out=str(pa11yci),
            manifest_out=str(manifest),
            base_url="http://127.0.0.1:8000",
            pa11y_version="",
            chromium_version="",
            hide_elements="",
        )
    )
    assert rc == 0
    cfg = json.loads(pa11yci.read_text())
    assert cfg["urls"] == []  # nothing to sweep

    manifest_data = json.loads(manifest.read_text())
    assert len(manifest_data["cache_hit_hashes"]) == 3
    assert manifest_data["to_sweep_hashes"] == {}


def test_e2e_post_drops_stale_pages(
    public_dir: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page that disappears from public/ should be evicted from the
    cache on the next post-pass — otherwise stale entries accumulate."""
    cache_path = tmp_path / "_data" / "pa11y-cache.json"

    # Pre-seed cache with an extra entry that won't exist in public/.
    cache = {
        "version": pc.CACHE_VERSION,
        "fingerprint": _fp(),
        "pages": {
            "page-a/index.html": {"hash": "x" * 64, "status": "pass"},
            "deleted/index.html": {"hash": "y" * 64, "status": "pass"},
        },
    }
    pc.save_cache(cache_path, cache)

    monkeypatch.setattr(pc, "detect_pa11y_version", lambda: "3.1.0")
    monkeypatch.setattr(pc, "detect_chromium_version", lambda: "130.0.0.0")
    monkeypatch.setattr(pc, "compute_config_hash", lambda _: "abc")

    pa11yci = tmp_path / ".pa11yci"
    manifest = tmp_path / ".pa11y-cache-manifest.json"
    import argparse

    pc.cmd_pre(
        argparse.Namespace(
            public_dir=str(public_dir),
            cache=str(cache_path),
            pa11yci_out=str(pa11yci),
            manifest_out=str(manifest),
            base_url="http://127.0.0.1:8000",
            pa11y_version="",
            chromium_version="",
            hide_elements="",
        )
    )
    pc.cmd_post(
        argparse.Namespace(
            public_dir=str(public_dir),
            cache=str(cache_path),
            manifest=str(manifest),
        )
    )

    cache_after = pc.load_cache(cache_path)
    assert "deleted/index.html" not in cache_after["pages"]


def test_e2e_fingerprint_change_resets_cache(
    public_dir: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When pre detects a fingerprint mismatch, post should write the
    new fingerprint and drop every old entry, only keeping the freshly-
    swept set."""
    cache_path = tmp_path / "_data" / "pa11y-cache.json"

    monkeypatch.setattr(pc, "detect_pa11y_version", lambda: "3.1.0")
    monkeypatch.setattr(pc, "detect_chromium_version", lambda: "130.0.0.0")

    # Seed cache at an OLDER chromium version, with bogus hashes
    # to prove they don't survive the fingerprint flip.
    cache = {
        "version": pc.CACHE_VERSION,
        "fingerprint": _fp(chromium="120.0.0.0"),
        "pages": {"page-a/index.html": {"hash": "z" * 64, "status": "pass"}},
    }
    pc.save_cache(cache_path, cache)

    pa11yci = tmp_path / ".pa11yci"
    manifest = tmp_path / ".pa11y-cache-manifest.json"
    import argparse

    pc.cmd_pre(
        argparse.Namespace(
            public_dir=str(public_dir),
            cache=str(cache_path),
            pa11yci_out=str(pa11yci),
            manifest_out=str(manifest),
            base_url="http://127.0.0.1:8000",
            pa11y_version="",
            chromium_version="",
            hide_elements="",
        )
    )
    # Pre should have written a manifest with 3 to-sweep, 0 cache hits.
    m = json.loads(manifest.read_text())
    assert len(m["to_sweep_hashes"]) == 3
    assert m["cache_hit_hashes"] == {}

    pc.cmd_post(
        argparse.Namespace(
            public_dir=str(public_dir),
            cache=str(cache_path),
            manifest=str(manifest),
        )
    )
    cache_after = pc.load_cache(cache_path)
    assert cache_after["fingerprint"]["chromium_version"] == "130.0.0.0"
    assert len(cache_after["pages"]) == 3
    # The stale entry under an old fingerprint shouldn't survive.
    for entry in cache_after["pages"].values():
        assert entry["hash"] != "z" * 64


def test_cmd_post_handles_missing_manifest(tmp_path: Path) -> None:
    """Defensive: if the manifest got lost (e.g. pa11y exited mid-run),
    post should not crash — it should report and exit non-zero."""
    import argparse

    rc = pc.cmd_post(
        argparse.Namespace(
            public_dir="public",
            cache=str(tmp_path / "cache.json"),
            manifest=str(tmp_path / "missing.json"),
        )
    )
    assert rc == 1


# ---------------------------------------------------------------------------
# Partial cache checkpointing (--audited-reports)
#
# A hung pa11y shard used to discard the whole run's cache update, so the
# next run re-swept everything, ran longer, and was likelier to hang again.
# These cover the narrower update: cache what some shard actually audited
# clean, leave everything else out.
# ---------------------------------------------------------------------------

_BASE = "http://127.0.0.1:8000"


def _post_args(tmp_path: Path, public_dir: Path, **kw):
    import argparse

    defaults = dict(
        public_dir=str(public_dir),
        cache=str(tmp_path / "_data" / "pa11y-cache.json"),
        manifest=str(tmp_path / ".pa11y-cache-manifest.json"),
        audited_reports="",
        base_url=_BASE,
    )
    defaults.update(kw)
    return argparse.Namespace(**defaults)


def _seed_manifest(tmp_path: Path, to_sweep: dict[str, str]) -> None:
    (tmp_path / ".pa11y-cache-manifest.json").write_text(
        json.dumps(
            {
                "fingerprint": _fp(),
                "cache_hit_hashes": {},
                "to_sweep_hashes": to_sweep,
            },
        ),
        encoding="utf-8",
    )


def test_audited_clean_reads_only_passing_urls(tmp_path: Path) -> None:
    """A URL is audited-clean only if a report lists it with no issues."""
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "shard-1.json").write_text(
        json.dumps(
            {
                "results": {
                    f"{_BASE}/clean/index.html": [],
                    f"{_BASE}/broken/index.html": [{"code": "WCAG2AA...", "message": "x"}],
                },
            },
        ),
        encoding="utf-8",
    )
    got = pc._audited_clean_relpaths(
        _post_args(tmp_path, tmp_path, audited_reports=str(reports)),
    )
    assert got == {"clean/index.html"}


def test_audited_clean_is_none_without_the_flag(tmp_path: Path) -> None:
    """No flag means the caller is asserting a fully green run."""
    assert pc._audited_clean_relpaths(_post_args(tmp_path, tmp_path)) is None


def test_audited_clean_survives_a_truncated_report(tmp_path: Path) -> None:
    """A shard killed mid-write leaves invalid JSON; skip it, don't crash."""
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "shard-1.json").write_text('{"results": {', encoding="utf-8")
    (reports / "shard-2.json").write_text(
        json.dumps({"results": {f"{_BASE}/ok/index.html": []}}),
        encoding="utf-8",
    )
    got = pc._audited_clean_relpaths(
        _post_args(tmp_path, tmp_path, audited_reports=str(reports)),
    )
    assert got == {"ok/index.html"}


def test_post_caches_only_audited_pages_when_partial(
    public_dir: Path,
    tmp_path: Path,
) -> None:
    """The core guarantee: an unaudited page must not be cached.

    page-a was audited clean by a surviving shard; page-b belonged to the
    shard that hung and was never audited. Only page-a may be
    checkpointed — otherwise the next run would skip a page nothing has
    ever checked.
    """
    cache_path = tmp_path / "_data" / "pa11y-cache.json"
    pc.save_cache(cache_path, {"version": pc.CACHE_VERSION, "fingerprint": _fp(), "pages": {}})
    _seed_manifest(tmp_path, {"page-a/index.html": "a" * 64, "page-b/index.html": "b" * 64})

    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "shard-1.json").write_text(
        json.dumps({"results": {f"{_BASE}/page-a/index.html": []}}),
        encoding="utf-8",
    )

    rc = pc.cmd_post(_post_args(tmp_path, public_dir, audited_reports=str(reports)))
    assert rc == 0
    pages = pc.load_cache(cache_path)["pages"]
    assert "page-a/index.html" in pages
    assert "page-b/index.html" not in pages


def test_post_without_flag_still_caches_whole_delta(
    public_dir: Path,
    tmp_path: Path,
) -> None:
    """Green-run behaviour is unchanged: the full delta is checkpointed."""
    cache_path = tmp_path / "_data" / "pa11y-cache.json"
    pc.save_cache(cache_path, {"version": pc.CACHE_VERSION, "fingerprint": _fp(), "pages": {}})
    _seed_manifest(tmp_path, {"page-a/index.html": "a" * 64, "page-b/index.html": "b" * 64})

    rc = pc.cmd_post(_post_args(tmp_path, public_dir))
    assert rc == 0
    pages = pc.load_cache(cache_path)["pages"]
    assert {"page-a/index.html", "page-b/index.html"} <= set(pages)
