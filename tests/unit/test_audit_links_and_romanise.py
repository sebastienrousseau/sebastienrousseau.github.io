# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The link auditor's resolution rules, and the Indic/Hangul romanisers.

audit_links gates every internal link on the site. Four separate accuracy
bugs were fixed in it recently — a dropped query string, share endpoints
reported as broken, an InvalidURL that aborted the whole external pass, and
HEAD-only checking against hosts that answer HEAD with 403. What none of
those fixes had was a test, so the same class of over-reporting could return
and would look like a real finding.

_romanise turns a translated title into a URL slug. Its length cap exists
because coverage-guided fuzzing found a real defect here: a repeated-hangul
title produced a 180-character slug, since dropping words cannot go below the
minimum word count and the survivors can exceed the bound on their own. That
hard cap now has a direct test rather than only a fuzzer that might not
rediscover it.
"""

from __future__ import annotations

import urllib.error
from pathlib import Path

import audit_links as al
import pytest
from _romanise import _MAX_SLUG, derive_slug, indic_romanise

# ---------------------------------------------------------------------------
# Internal link resolution
# ---------------------------------------------------------------------------


def test_a_relative_href_is_left_alone(tmp_path: Path) -> None:
    """This pass only owns absolute paths; relative ones are another concern."""
    assert al.check_internal("../sibling/", tmp_path) is True


def test_a_file_that_exists_resolves(tmp_path: Path) -> None:
    (tmp_path / "robots.txt").write_text("x", encoding="utf-8")
    assert al.check_internal("/robots.txt", tmp_path) is True


def test_a_directory_resolves_through_its_index(tmp_path: Path) -> None:
    """The static-site convention: /foo/ is served by /foo/index.html."""
    (tmp_path / "foo").mkdir()
    (tmp_path / "foo" / "index.html").write_text("x", encoding="utf-8")
    assert al.check_internal("/foo/", tmp_path) is True


def test_an_extensionless_path_resolves_through_the_html_file(tmp_path: Path) -> None:
    (tmp_path / "about.html").write_text("x", encoding="utf-8")
    assert al.check_internal("/about", tmp_path) is True


def test_a_genuinely_missing_path_does_not_resolve(tmp_path: Path) -> None:
    assert al.check_internal("/nope/", tmp_path) is False


def test_the_query_string_is_stripped_before_resolution(tmp_path: Path) -> None:
    """A static file is found by path, not query — one of the four accuracy
    bugs fixed here was reporting every ?-carrying link as broken."""
    (tmp_path / "search.html").write_text("x", encoding="utf-8")
    assert al.check_internal("/search?q=payments", tmp_path) is True


def test_a_worker_route_resolves_without_a_file(tmp_path: Path) -> None:
    """Worker routes are served at request time and have no file on disk;
    treating them as broken would fail the build on working links."""
    route = next(iter(al.WORKER_ROUTES))
    assert al.check_internal(route, tmp_path) is True


# ---------------------------------------------------------------------------
# Host and share-endpoint classification
# ---------------------------------------------------------------------------


def test_host_extracts_the_authority() -> None:
    assert al.host("https://example.com/a/b") == "example.com"
    assert al.host("http://sub.example.com:8080/x") == "sub.example.com:8080"


def test_host_of_a_bare_authority() -> None:
    assert al.host("example.com") == "example.com"


def test_share_endpoints_are_recognised() -> None:
    """An intent URL is a button, not a link to a page — probing it returns
    a code that says nothing about the site."""
    for marker in list(al.SHARE_ENDPOINTS)[:3]:
        assert al.is_share_endpoint(f"https://{marker}whatever")


def test_an_ordinary_url_is_not_a_share_endpoint() -> None:
    assert not al.is_share_endpoint("https://example.com/an/article/")


# ---------------------------------------------------------------------------
# External checking — every call stubbed, no socket opened
# ---------------------------------------------------------------------------


def test_a_4xx_from_head_is_retried_with_get(monkeypatch: pytest.MonkeyPatch) -> None:
    """Plenty of servers answer HEAD with 4xx and GET with 200. Reporting
    those as broken is how a link checker loses the reader's trust."""
    seen: list[str] = []

    def fake(url: str, method: str):
        seen.append(method)
        if method == "HEAD":
            raise urllib.error.HTTPError(url, 403, "Forbidden", {}, None)
        return url, 200

    monkeypatch.setattr(al, "_fetch", fake)
    assert al.check_external("https://x/")[1] == 200
    assert seen == ["HEAD", "GET"]


def test_a_5xx_from_head_is_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    """A server error will repeat; retrying only doubles the wait."""
    seen: list[str] = []

    def fake(url: str, method: str):
        seen.append(method)
        raise urllib.error.HTTPError(url, 503, "Unavailable", {}, None)

    monkeypatch.setattr(al, "_fetch", fake)
    assert al.check_external("https://x/")[1] == 503
    assert seen == ["HEAD"]


def test_a_malformed_url_is_reported_not_raised(monkeypatch: pytest.MonkeyPatch) -> None:
    """http.client.InvalidURL derives from HTTPException, not OSError, so it
    once escaped the handler and aborted the entire external pass — every
    link after it went unchecked, which is the opposite of an audit."""
    import http.client

    def fake(url: str, method: str):
        raise http.client.InvalidURL("space in path")

    monkeypatch.setattr(al, "_fetch", fake)
    url, code = al.check_external("https://x/a b")
    assert isinstance(code, str)
    assert "InvalidURL" in code


@pytest.mark.parametrize(
    "exc", [urllib.error.URLError("down"), TimeoutError("slow"), ValueError("bad")]
)
def test_every_transport_failure_degrades_to_a_string_code(
    monkeypatch: pytest.MonkeyPatch, exc: Exception
) -> None:
    def fake(url: str, method: str):
        raise exc

    monkeypatch.setattr(al, "_fetch", fake)
    assert isinstance(al.check_external("https://x/")[1], str)


def test_bot_blocked_hosts_are_skipped_not_reported(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A 403 from a host that blocks every automated client says nothing
    about the link, so it is counted separately rather than called broken."""
    blocked = next(iter(al.HEAD_BLOCKED))

    def must_not_check(url: str):
        raise AssertionError(f"checked a bot-blocked host: {url}")

    monkeypatch.setattr(al, "check_external", must_not_check)
    broken = al._audit_external([f"https://{blocked}/a"])
    assert broken == []
    assert "skipped 1 bot-blocked" in capsys.readouterr().out


def test_report_external_lists_only_genuine_failures(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(al, "check_external", lambda u: (u, 404 if "bad" in u else 200))
    broken = al._audit_external(["https://x/good", "https://x/bad"])
    assert [u for u, _ in broken] == ["https://x/bad"]
    capsys.readouterr()


def test_a_3xx_is_not_broken(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """A redirect resolves for a reader; only >=400 is a broken link."""
    monkeypatch.setattr(al, "check_external", lambda u: (u, 301))
    assert al._audit_external(["https://x/moved"]) == []
    capsys.readouterr()


# ---------------------------------------------------------------------------
# Slug length — the defect coverage-guided fuzzing found
# ---------------------------------------------------------------------------


def test_a_long_hangul_title_is_capped(monkeypatch: pytest.MonkeyPatch) -> None:
    """The fuzzer's find: dropping words cannot go below the minimum word
    count, so a single unbroken run can exceed the bound on its own. The
    hard cap is the backstop."""
    slug = derive_slug("가" * 60, "ko")
    assert len(slug) <= _MAX_SLUG


def test_a_long_cjk_title_is_capped() -> None:
    assert len(derive_slug("测" * 80, "zh-hans")) <= _MAX_SLUG


def test_a_capped_slug_never_ends_in_a_separator() -> None:
    """A trailing hyphen would produce /a-slug--/ once joined into a URL."""
    for n in (40, 60, 80):
        slug = derive_slug("가" * n, "ko")
        assert not slug.endswith("-"), slug


def test_an_ordinary_title_is_not_truncated() -> None:
    slug = derive_slug("Le système de paiement", "fr")
    assert 0 < len(slug) <= _MAX_SLUG
    assert not slug.endswith("-")


# ---------------------------------------------------------------------------
# Indic romanisation — the inherent-vowel rule
# ---------------------------------------------------------------------------


def test_indic_romanise_appends_the_inherent_vowel() -> None:
    """A bare consonant carries an inherent 'a' unless a virama or matra
    cancels it — dropping that turns 'prathama' into 'prthm'."""
    out = indic_romanise("नम", "hi")
    assert "a" in out


def test_a_medial_virama_suppresses_the_inherent_vowel() -> None:
    """नमस्ते is "namaste", not "namasate" — the virama after स cancels the
    schwa that a bare consonant would otherwise carry."""
    assert indic_romanise("नमस्ते", "hi") == "namaste"
    assert indic_romanise("नमसते", "hi") == "namasate"


def test_the_final_schwa_is_dropped_for_the_locales_that_drop_it() -> None:
    """Hindi, Bengali and Marathi drop the word-final inherent vowel, so
    नम is "nam" rather than "nama". Emitting the schwa would put a spurious
    trailing vowel on the end of every slug in those three locales."""
    from _romanise import _FINAL_SCHWA_DROP

    assert {"hi", "bn", "mr"} <= set(_FINAL_SCHWA_DROP)
    assert indic_romanise("नम", "hi") == "nam"


def test_the_virama_itself_is_not_transliterated() -> None:
    assert "्" not in indic_romanise("नमस्ते", "hi")


def test_an_unmapped_character_passes_through() -> None:
    assert "7" in indic_romanise("न7", "hi")
