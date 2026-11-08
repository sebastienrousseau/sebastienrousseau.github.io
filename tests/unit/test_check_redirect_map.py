# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Offline tests for ``scripts/seo_and_audit/check_redirect_map.py``.

Every case builds a miniature ``public/`` under ``tmp_path``: real pages,
meta-refresh stubs, a committed ``redirects.json`` and an
``articles.json``, then runs one check (or the whole CLI) against it.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import build_worker_assets as bwa
import check_redirect_map as crm
import pytest

SITE = "https://sebastienrousseau.com"


def _page(public: Path, path: str, html: str = "<html><head></head><body>ok</body></html>") -> None:
    page = public / path.strip("/") / "index.html" if path != "/" else public / "index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(html, encoding="utf-8")


def _stub(public: Path, source: str, target: str) -> None:
    _page(
        public,
        source,
        f'<html><head><meta http-equiv="refresh" content="0; url={SITE}{target}" />'
        "</head><body></body></html>",
    )


@pytest.fixture
def site(tmp_path: Path) -> dict[str, Path]:
    """A built tree with two renamed pages and a matching committed map."""
    public = tmp_path / "public"
    _page(public, "/")
    _page(public, "/new-a/")
    _page(public, "/fr/nouveau-b/")
    _stub(public, "/old-a/", "/new-a/")
    _stub(public, "/fr/ancien-b/", "/fr/nouveau-b/")
    committed = tmp_path / "redirects.json"
    committed.write_text(
        bwa.render_redirects({"/old-a/": "/new-a/", "/fr/ancien-b/": "/fr/nouveau-b/"}),
        encoding="utf-8",
    )
    articles = tmp_path / "articles.json"
    articles.write_text(
        json.dumps(
            {
                "_comment": "fixture",
                "en": {"old-a": "new-a"},
                "fr": {"ancien-b": "nouveau-b"},
                "eo": {"malnova": "nova"},
            }
        ),
        encoding="utf-8",
    )
    exemptions = tmp_path / "exemptions.json"
    exemptions.write_text(json.dumps({"_comment": "fixture", "absent": {}}), encoding="utf-8")
    return {
        "root": tmp_path,
        "public": public,
        "committed": committed,
        "articles": articles,
        "exemptions": exemptions,
    }


def _run(site: dict[str, Path], *extra: str) -> int:
    return crm.main(
        [
            "--public",
            str(site["public"]),
            "--committed",
            str(site["committed"]),
            "--articles",
            str(site["articles"]),
            "--exemptions",
            str(site["exemptions"]),
            "--kept",
            "en,fr",
            *extra,
        ]
    )


# -- 1. drift ---------------------------------------------------------------


def test_matching_map_passes(site: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    assert _run(site) == 0
    assert "OK" in capsys.readouterr().out


def test_drifted_map_fails_and_says_to_commit(
    site: dict[str, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    _stub(site["public"], "/older-a/", "/new-a/")  # a new stub the map lacks
    assert _run(site) == 1
    err = capsys.readouterr().err
    assert "1 added" in err
    assert "commit worker-assets/redirects.json" in err


def test_drift_counts_added_removed_changed() -> None:
    committed = {"/a/": "/x/", "/b/": "/y/", "/c/": "/z/"}
    built = {"/a/": "/x/", "/b/": "/other/", "/d/": "/z/"}
    problems = crm.check_drift(bwa.render_redirects(committed), bwa.render_redirects(built))
    assert len(problems) == 1
    assert "1 added, 1 removed, 1 changed" in problems[0]


def test_byte_level_drift_with_equal_entries_still_fails() -> None:
    same = {"/a/": "/x/"}
    pretty = json.dumps({"version": 1, "redirects": same}, indent=2) + "\n"
    problems = crm.check_drift(pretty, bwa.render_redirects(same))
    assert problems and "0 added, 0 removed, 0 changed" in problems[0]


def test_regenerated_map_is_written_to_a_temp_path(site: dict[str, Path]) -> None:
    text, path = crm.regenerate(site["public"])
    assert path.read_text(encoding="utf-8") == text
    assert not path.is_relative_to(site["root"])
    path.unlink()


# -- 2. targets ---------------------------------------------------------------


def test_stub_target_fails(site: dict[str, Path]) -> None:
    redirects = {"/old-a/": "/fr/ancien-b/"}
    problems = crm.check_targets(site["public"], redirects)
    assert problems == ["/old-a/ -> /fr/ancien-b/: target is itself a redirect stub"]


def test_missing_target_fails(site: dict[str, Path]) -> None:
    problems = crm.check_targets(site["public"], {"/old-a/": "/gone/"})
    assert problems == ["/old-a/ -> /gone/: target does not render"]


def test_root_target_resolves(site: dict[str, Path]) -> None:
    assert crm.check_targets(site["public"], {"/old-a/": "/"}) == []


# -- 3. sources ---------------------------------------------------------------


def test_live_page_as_source_fails(site: dict[str, Path]) -> None:
    problems = crm.check_sources(site["public"], {"/new-a/": "/fr/nouveau-b/"})
    assert problems == ["/new-a/ is a live page but the map redirects it"]


def test_stub_or_absent_source_is_fine(site: dict[str, Path]) -> None:
    assert crm.check_sources(site["public"], {"/old-a/": "/new-a/", "/never/": "/new-a/"}) == []


# -- 4. chains and loops ----------------------------------------------------


def test_chain_and_self_loop_fail() -> None:
    problems = crm.check_chains({"/a/": "/b/", "/b/": "/c/", "/s/": "/s/"})
    assert "chain /a/ -> /b/ -> /c/" in problems
    assert "loop /s/ -> /s/" in problems


def test_loop_in_the_build_fails(site: dict[str, Path], capsys: pytest.CaptureFixture[str]) -> None:
    _stub(site["public"], "/loop-1/", "/loop-2/")
    _stub(site["public"], "/loop-2/", "/loop-1/")
    with pytest.raises(bwa.RedirectMapError):
        bwa.collapse_chains(bwa.stub_redirects(site["public"]))
    assert _run(site) == 1
    assert "redirect loop" in capsys.readouterr().err


# -- 5. articles.json coverage ----------------------------------------------


def _articles(site: dict[str, Path], data: dict[str, object]) -> dict[str, dict[str, str]]:
    site["articles"].write_text(json.dumps(data), encoding="utf-8")
    return crm.load_articles(site["articles"])


def test_kept_locale_article_missing_from_map_fails(site: dict[str, Path]) -> None:
    articles = _articles(site, {"fr": {"ancien-b": "nouveau-b", "perdu": "nouveau-b"}})
    problems = crm.check_articles({"/fr/ancien-b/": "/fr/nouveau-b/"}, articles, {}, {"fr"})
    assert problems == ["/fr/perdu/ (articles.json, fr) is not in the map and has no listed reason"]


def test_dropped_locale_article_is_ignored(site: dict[str, Path]) -> None:
    articles = _articles(site, {"eo": {"malnova": "nova"}})
    assert crm.check_articles({}, articles, {}, {"en", "fr"}) == []


def test_listed_absence_passes_and_stale_listing_fails(site: dict[str, Path]) -> None:
    articles = _articles(site, {"en": {"old-a": "new-a", "gone": "new-a"}})
    redirects = {"/old-a/": "/new-a/"}
    reasons = {"/gone/": "source still renders"}
    assert crm.check_articles(redirects, articles, reasons, {"en"}) == []
    stale = {"/gone/": "x", "/old-a/": "now present", "/unknown/": "x"}
    problems = crm.check_articles(redirects, articles, stale, {"en"})
    assert "/old-a/ is listed as absent but is in the map" in problems
    assert "/unknown/ is listed as absent but is not in articles.json for a kept locale" in problems


def test_exemptions_file_missing_means_none(tmp_path: Path) -> None:
    assert crm.load_exemptions(tmp_path / "nope.json") == {}


# -- CLI ------------------------------------------------------------------------


def test_unbuilt_public_exits_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert crm.main(["--public", str(tmp_path / "public")]) == 2
    assert "not built" in capsys.readouterr().err


def test_committed_map_defaults_to_git_head(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[list[str]] = []

    def fake_run(cmd: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        seen.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout='{"version":1,"redirects":{}}\n')

    monkeypatch.setattr(crm.subprocess, "run", fake_run)
    assert crm.committed_text(None) == '{"version":1,"redirects":{}}\n'
    assert seen[0][-1] == "HEAD:worker-assets/redirects.json"


def test_kept_defaults_to_locale_indexing_policy() -> None:
    kept = crm.parse_kept(None)
    assert "en" in kept
    assert kept == set(crm.indexed_codes())


def test_many_problems_are_truncated(capsys: pytest.CaptureFixture[str]) -> None:
    crm.report("targets", [f"p{i}" for i in range(30)])
    err = capsys.readouterr().err
    assert "30 problem(s)" in err
    assert "p19" in err
    assert "p20" not in err
    assert "10 more" in err
