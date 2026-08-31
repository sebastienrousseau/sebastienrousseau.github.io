# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The taxonomy gate and the post-deploy verifier.

check_taxonomy guards the canonical tag vocabulary the whole site is organised
by: an alias colliding across two canonicals silently reroutes every post
carrying it. verify_deploy runs against the live origin after a deploy and is
the only check that the thing actually serving traffic matches what was built.

Neither had its predicates tested. verify_deploy in particular cannot be
smoke-tested — it needs a live origin — so every HTTP call here is stubbed and
no test opens a socket.
"""

from __future__ import annotations

import urllib.error

import check_taxonomy as ct
import pytest
import verify_deploy as vd

# ---------------------------------------------------------------------------
# Taxonomy entry validation
# ---------------------------------------------------------------------------


def _entry(**over) -> dict:
    base = dict.fromkeys(ct._REQUIRED_FIELDS, "value")
    base["category"] = ct._PILLARS[0]
    base.update(over)
    return base


def test_entry_that_is_not_a_mapping_is_rejected() -> None:
    assert ct._validate_entry("slug", ["not", "a", "dict"]) == ["slug: entry is not a mapping"]


def test_entry_missing_a_required_field_is_reported() -> None:
    e = _entry()
    field = ct._REQUIRED_FIELDS[0]
    del e[field]
    problems = ct._validate_entry("slug", e)
    assert any(field in p for p in problems)


def test_entry_with_an_unknown_category_is_reported() -> None:
    """The pillar set is closed; an unknown one would orphan the tag."""
    problems = ct._validate_entry("slug", _entry(category="not-a-pillar"))
    assert any("not in allowed pillars" in p for p in problems)


def test_a_complete_entry_is_clean() -> None:
    assert ct._validate_entry("slug", _entry()) == []


# ---------------------------------------------------------------------------
# Alias collisions — the failure that silently reroutes posts
# ---------------------------------------------------------------------------


def test_alias_colliding_across_two_canonicals_is_reported() -> None:
    seen: dict[str, str] = {}
    ct._check_alias_collisions("first", {"aliases": ["shared"]}, seen)
    problems = ct._check_alias_collisions("second", {"aliases": ["shared"]}, seen)
    assert any("already maps to 'first'" in p for p in problems)


def test_alias_matching_is_case_and_whitespace_insensitive() -> None:
    seen: dict[str, str] = {}
    ct._check_alias_collisions("first", {"aliases": ["Shared Tag"]}, seen)
    problems = ct._check_alias_collisions("second", {"aliases": ["  shared tag  "]}, seen)
    assert problems, "a collision differing only in case must still be caught"


def test_a_slug_colliding_with_another_entrys_alias_is_reported() -> None:
    """The slug itself is an alias of the canonical, so it collides too."""
    seen: dict[str, str] = {}
    ct._check_alias_collisions("first", {"aliases": ["second"]}, seen)
    problems = ct._check_alias_collisions("second", {}, seen)
    assert problems


def test_repeating_an_alias_within_one_entry_is_not_a_collision() -> None:
    seen: dict[str, str] = {}
    assert ct._check_alias_collisions("only", {"aliases": ["a", "a"]}, seen) == []


def test_entry_without_aliases_is_clean() -> None:
    assert ct._check_alias_collisions("slug", {}, {}) == []


def test_null_aliases_are_treated_as_none() -> None:
    """`aliases:` with no value parses to None, not an empty list."""
    assert ct._check_alias_collisions("slug", {"aliases": None}, {}) == []


# ---------------------------------------------------------------------------
# Whole-taxonomy validation and the alias map
# ---------------------------------------------------------------------------


def test_validate_taxonomy_aggregates_every_problem() -> None:
    tax = {"a": _entry(category="bogus"), "b": "not a dict"}
    problems = ct.validate_taxonomy(tax)
    assert any("bogus" in p for p in problems)
    assert any("not a mapping" in p for p in problems)


def test_validate_taxonomy_is_clean_for_a_well_formed_vocabulary() -> None:
    assert ct.validate_taxonomy({"a": _entry(), "b": _entry()}) == []


def test_alias_map_includes_the_slug_itself() -> None:
    amap = ct.alias_map({"payments": _entry(aliases=["pay"])})
    assert amap["payments"] == "payments"
    assert amap["pay"] == "payments"


def test_alias_map_lowercases_its_keys() -> None:
    amap = ct.alias_map({"payments": _entry(aliases=["ISO 20022"])})
    assert "iso 20022" in amap


def test_alias_map_tolerates_null_aliases() -> None:
    assert ct.alias_map({"a": _entry(aliases=None)}) == {"a": "a"}


# ---------------------------------------------------------------------------
# Post walking
# ---------------------------------------------------------------------------


def _post(tmp_path, name: str, tags: str) -> None:
    (tmp_path / name).write_text(f'---\ntags: "{tags}"\n---\nbody\n', encoding="utf-8")


def test_walk_posts_separates_resolved_from_orphan_tags(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _post(tmp_path, "2026-01-01-a.md", "payments, not-a-known-tag")
    monkeypatch.setattr(ct, "POSTS", tmp_path)
    resolved, orphan = ct.walk_posts({"payments": "payments"})
    assert resolved["payments"] == 1
    assert orphan["not-a-known-tag"] == 1


def test_walk_posts_resolves_through_an_alias(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    _post(tmp_path, "2026-01-01-a.md", "ISO 20022")
    monkeypatch.setattr(ct, "POSTS", tmp_path)
    resolved, orphan = ct.walk_posts({"iso 20022": "iso-20022"})
    assert resolved["iso-20022"] == 1
    assert orphan == {}


def test_walk_posts_skips_a_file_without_tags(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "2026-01-01-a.md").write_text('---\ntitle: "T"\n---\nbody\n', encoding="utf-8")
    monkeypatch.setattr(ct, "POSTS", tmp_path)
    assert ct.walk_posts({}) == ({}, {})


def test_walk_posts_ignores_empty_tag_entries(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    _post(tmp_path, "2026-01-01-a.md", "payments, , ")
    monkeypatch.setattr(ct, "POSTS", tmp_path)
    resolved, orphan = ct.walk_posts({"payments": "payments"})
    assert sum(orphan.values()) == 0
    assert resolved["payments"] == 1


# ---------------------------------------------------------------------------
# verify_deploy — HTTP fetch
# ---------------------------------------------------------------------------


class _Resp:
    def __init__(self, status=200, body="", headers=None):
        self.status = status
        self._b = body.encode()
        self.headers = headers or {}

    def read(self):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False


def test_fetch_returns_status_body_and_lowercased_headers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        vd.urllib.request,
        "urlopen",
        lambda *a, **k: _Resp(200, "hello", {"Content-Security-Policy": "x"}),
    )
    status, body, headers = vd.fetch("https://x/")
    assert status == 200
    assert body == "hello"
    assert "content-security-policy" in headers, "headers must be case-normalised"


def test_fetch_returns_the_code_for_an_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """A 404 is data — the point of the check — not an exception."""

    def raise_404(*_a, **_k):
        raise urllib.error.HTTPError("u", 404, "nf", {}, None)

    monkeypatch.setattr(vd.urllib.request, "urlopen", raise_404)
    assert vd.fetch("https://x/")[0] == 404


def test_fetch_raises_failure_when_unreachable(monkeypatch: pytest.MonkeyPatch) -> None:
    """An unreachable origin is a deploy failure, not a per-URL problem."""

    def boom(*_a, **_k):
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(vd.urllib.request, "urlopen", boom)
    with pytest.raises(vd.Failure, match="unreachable"):
        vd.fetch("https://x/")


# ---------------------------------------------------------------------------
# verify_deploy — advertised paths
# ---------------------------------------------------------------------------


BASE = "https://sebastienrousseau.com"


def _serve(monkeypatch, pages: dict) -> None:
    def fake(url):
        for suffix, (status, body) in pages.items():
            if url.endswith(suffix):
                return status, body, {}
        return 200, "", {}

    monkeypatch.setattr(vd, "fetch", fake)


def test_advertised_paths_collects_sitemaps_from_robots(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _serve(
        monkeypatch,
        {
            "/robots.txt": (200, f"Sitemap: {BASE}/sitemap.xml\n"),
            "/llms.txt": (200, ""),
        },
    )
    assert f"{BASE}/sitemap.xml" in vd.advertised_paths(BASE)


def test_advertised_paths_includes_commented_pointers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A documented 404 is still a broken promise to a crawler."""
    _serve(
        monkeypatch,
        {"/robots.txt": (200, f"# see {BASE}/humans.txt\n"), "/llms.txt": (200, "")},
    )
    assert f"{BASE}/humans.txt" in vd.advertised_paths(BASE)


def test_advertised_paths_excludes_off_origin_urls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Third-party URLs are not ours to guarantee."""
    _serve(
        monkeypatch,
        {
            "/robots.txt": (200, "Sitemap: https://example.com/sitemap.xml\n"),
            "/llms.txt": (200, ""),
        },
    )
    assert vd.advertised_paths(BASE) == set()


def test_advertised_paths_raises_when_robots_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _serve(monkeypatch, {"/robots.txt": (404, "")})
    with pytest.raises(vd.Failure, match=r"robots\.txt"):
        vd.advertised_paths(BASE)


def test_check_paths_reports_each_non_200(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(vd, "fetch", lambda url: (404, "", {}) if "bad" in url else (200, "", {}))
    problems = vd.check_paths(BASE, {f"{BASE}/bad", f"{BASE}/good"})
    assert len(problems) == 1
    assert "bad" in problems[0]


# ---------------------------------------------------------------------------
# verify_deploy — home description
# ---------------------------------------------------------------------------


def _home(monkeypatch, body: str, status: int = 200, headers=None) -> None:
    monkeypatch.setattr(vd, "fetch", lambda _u: (status, body, headers or {}))


def test_home_description_missing_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    _home(monkeypatch, "<html><head></head></html>")
    assert vd.check_home_description(BASE) == ['home page has no <meta name="description">']


def test_home_description_too_short_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    _home(monkeypatch, '<meta name="description" content="too short">')
    assert any("only" in p for p in vd.check_home_description(BASE))


def test_home_description_ending_mid_sentence_is_reported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A truncated description is how a build bug reaches search results."""
    desc = "A" * 60 + ","
    _home(monkeypatch, f'<meta name="description" content="{desc}">')
    assert any("mid-sentence" in p for p in vd.check_home_description(BASE))


def test_a_good_home_description_is_clean(monkeypatch: pytest.MonkeyPatch) -> None:
    _home(monkeypatch, f'<meta name="description" content="{"A" * 80}.">')
    assert vd.check_home_description(BASE) == []


def test_home_description_non_200_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    _home(monkeypatch, "", status=503)
    assert vd.check_home_description(BASE) == ["home page -> HTTP 503"]


# ---------------------------------------------------------------------------
# verify_deploy — CSP at the edge
# ---------------------------------------------------------------------------


def test_csp_absent_entirely_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    _home(monkeypatch, "<html></html>")
    assert vd.check_csp(BASE) == ["no Content-Security-Policy delivered by header or meta"]


def test_csp_header_with_unsafe_inline_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    _home(
        monkeypatch,
        "<html></html>",
        headers={"content-security-policy": "script-src 'self' 'unsafe-inline'"},
    )
    assert any("edge CSP header" in p for p in vd.check_csp(BASE))


def test_csp_meta_with_unsafe_inline_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    body = (
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"script-src 'self' 'unsafe-inline'\">"
    )
    _home(monkeypatch, body)
    assert any("meta CSP" in p for p in vd.check_csp(BASE))


def test_a_hash_pinned_meta_csp_is_clean(monkeypatch: pytest.MonkeyPatch) -> None:
    body = "<meta http-equiv=\"Content-Security-Policy\" content=\"script-src 'self' 'sha256-x'\">"
    _home(monkeypatch, body)
    assert vd.check_csp(BASE) == []


def test_a_header_csp_alone_satisfies_the_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """Meta is absent but the edge sets one — that is a valid deployment."""
    _home(monkeypatch, "<html></html>", headers={"content-security-policy": "script-src 'self'"})
    assert vd.check_csp(BASE) == []
