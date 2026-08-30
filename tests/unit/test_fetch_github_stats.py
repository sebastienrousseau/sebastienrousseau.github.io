# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The GitHub stats fetcher — stale-data retention is the behaviour that matters.

These figures feed the KPI numbers on the home page, /about/ and /projects/.
The interesting logic is not the HTTP call but what happens when it fails:
the previous value is kept and marked stale, so a rate-limited or offline
build publishes last-known numbers rather than dropping a repo silently. A
missing repo would quietly shrink the totals, and nothing downstream would
notice a smaller number.

Only fetch_repo is stubbed — the merge, the stale marking, the ordering and
the file write all run for real against a tmp path. No socket is opened.
"""

from __future__ import annotations

import json
from pathlib import Path

import fetch_github_stats as gh
import pytest


@pytest.fixture(autouse=True)
def _no_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)


def _out(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    p = tmp_path / "_data" / "gh-stats.json"
    monkeypatch.setattr(gh, "OUTPUT", p)
    return p


def _repo(slug: str, stars: int = 1, forks: int = 2) -> dict:
    return {"slug": slug, "stars": stars, "forks": forks}


# ---------------------------------------------------------------------------
# load_existing
# ---------------------------------------------------------------------------


def test_load_existing_is_empty_without_a_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _out(tmp_path, monkeypatch)
    assert gh.load_existing() == {}


def test_load_existing_indexes_by_slug(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = _out(tmp_path, monkeypatch)
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps({"repos": [_repo("a/b", stars=9)]}), encoding="utf-8")
    assert gh.load_existing()["a/b"]["stars"] == 9


def test_load_existing_degrades_on_malformed_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A corrupt cache must not stop the build; it just has nothing to keep."""
    p = _out(tmp_path, monkeypatch)
    p.parent.mkdir(parents=True)
    p.write_text("{not json", encoding="utf-8")
    assert gh.load_existing() == {}


# ---------------------------------------------------------------------------
# main — the merge and stale-retention path
# ---------------------------------------------------------------------------


def test_main_writes_every_repo_that_fetched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    p = _out(tmp_path, monkeypatch)
    monkeypatch.setattr(gh, "fetch_repo", lambda slug, token: _repo(slug))
    assert gh.main() == 0
    payload = json.loads(p.read_text(encoding="utf-8"))
    assert len(payload["repos"]) == len(gh.REPOS)
    capsys.readouterr()


def test_main_keeps_last_known_data_and_marks_it_stale(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The point of the whole module: a failed fetch must not shrink the
    totals. The previous value is kept and flagged, not dropped."""
    p = _out(tmp_path, monkeypatch)
    p.parent.mkdir(parents=True)
    p.write_text(
        json.dumps({"repos": [_repo(slug, stars=7) for slug in gh.REPOS]}), encoding="utf-8"
    )
    monkeypatch.setattr(gh, "fetch_repo", lambda slug, token: None)  # every fetch fails
    assert gh.main() == 0
    payload = json.loads(p.read_text(encoding="utf-8"))
    assert len(payload["repos"]) == len(gh.REPOS), "no repo may be dropped"
    assert all(r["stale"] is True for r in payload["repos"])
    assert all(r["stars"] == 7 for r in payload["repos"]), "last-known values retained"
    capsys.readouterr()


def test_main_omits_a_repo_that_failed_and_has_no_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Nothing to fall back on — better absent than invented."""
    p = _out(tmp_path, monkeypatch)
    first = gh.REPOS[0]
    monkeypatch.setattr(
        gh, "fetch_repo", lambda slug, token: None if slug == first else _repo(slug)
    )
    assert gh.main() == 0
    slugs = {r["slug"] for r in json.loads(p.read_text(encoding="utf-8"))["repos"]}
    assert first not in slugs
    assert len(slugs) == len(gh.REPOS) - 1
    capsys.readouterr()


def test_main_preserves_the_declared_repo_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Output order follows REPOS, not thread-pool completion order — the
    file is committed, so a shuffling order would churn the diff every run."""
    p = _out(tmp_path, monkeypatch)
    monkeypatch.setattr(gh, "fetch_repo", lambda slug, token: _repo(slug))
    gh.main()
    written = [r["slug"] for r in json.loads(p.read_text(encoding="utf-8"))["repos"]]
    assert written == list(gh.REPOS)
    capsys.readouterr()


def test_main_totals_stars_and_forks_in_its_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _out(tmp_path, monkeypatch)
    monkeypatch.setattr(gh, "fetch_repo", lambda slug, token: _repo(slug, stars=2, forks=3))
    gh.main()
    out = capsys.readouterr().out
    assert f"{2 * len(gh.REPOS)} stars" in out
    assert f"{3 * len(gh.REPOS)} forks" in out


def test_main_warns_when_no_token_is_present(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Unauthenticated is 60 requests/hour — worth saying out loud."""
    _out(tmp_path, monkeypatch)
    monkeypatch.setattr(gh, "fetch_repo", lambda slug, token: _repo(slug))
    gh.main()
    assert "no GH_TOKEN" in capsys.readouterr().err


def test_main_passes_the_token_through_when_set(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _out(tmp_path, monkeypatch)
    monkeypatch.setenv("GH_TOKEN", "secret")
    seen: list[str | None] = []

    def record(slug: str, token: str | None) -> dict:
        seen.append(token)
        return _repo(slug)

    monkeypatch.setattr(gh, "fetch_repo", record)
    gh.main()
    assert set(seen) == {"secret"}
    assert "no GH_TOKEN" not in capsys.readouterr().err


def test_main_creates_the_output_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    p = _out(tmp_path, monkeypatch)
    assert not p.parent.exists()
    monkeypatch.setattr(gh, "fetch_repo", lambda slug, token: _repo(slug))
    gh.main()
    assert p.is_file()
    capsys.readouterr()


def test_main_stamps_a_generated_at_timestamp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    p = _out(tmp_path, monkeypatch)
    monkeypatch.setattr(gh, "fetch_repo", lambda slug, token: _repo(slug))
    gh.main()
    assert "generated_at" in json.loads(p.read_text(encoding="utf-8"))
    capsys.readouterr()


# ---------------------------------------------------------------------------
# fetch_repo — the HTTP boundary. urlopen is stubbed; no socket is opened.
# ---------------------------------------------------------------------------


class _Resp:
    def __init__(self, payload: dict) -> None:
        self._b = json.dumps(payload).encode()

    def read(self) -> bytes:
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False


def test_fetch_repo_maps_the_api_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {
        "name": "kyberlib",
        "description": "A library",
        "stargazers_count": 42,
        "forks_count": 7,
        "subscribers_count": 3,
        "open_issues_count": 1,
        "language": "Rust",
        "license": {"spdx_id": "MIT"},
        "default_branch": "trunk",
        "archived": True,
        "html_url": "https://github.com/o/kyberlib",
    }
    monkeypatch.setattr(gh.urllib.request, "urlopen", lambda *a, **k: _Resp(payload))
    out = gh.fetch_repo("o/kyberlib", None)
    assert out["stars"] == 42
    assert out["forks"] == 7
    assert out["license"] == "MIT"
    assert out["default_branch"] == "trunk"
    assert out["archived"] is True


def test_fetch_repo_defaults_every_absent_field(monkeypatch: pytest.MonkeyPatch) -> None:
    """A sparse payload must yield zeros and empty strings, never None —
    these values are summed and rendered straight into the page."""
    monkeypatch.setattr(gh.urllib.request, "urlopen", lambda *a, **k: _Resp({}))
    out = gh.fetch_repo("o/n", None)
    assert out["stars"] == 0
    assert out["forks"] == 0
    assert out["description"] == ""
    assert out["license"] == ""
    assert out["default_branch"] == "main"
    assert out["html_url"] == "https://github.com/o/n"


def test_fetch_repo_coerces_explicit_nulls_to_empty_strings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The API sends `null`, not a missing key, for an unset description or
    licence — `.get(k, "")` alone would let None through into the page."""
    monkeypatch.setattr(
        gh.urllib.request,
        "urlopen",
        lambda *a, **k: _Resp({"description": None, "homepage": None, "license": None}),
    )
    out = gh.fetch_repo("o/n", None)
    assert out["description"] == ""
    assert out["homepage"] == ""
    assert out["license"] == ""


def test_fetch_repo_sends_the_bearer_token_when_given(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: dict[str, str] = {}

    def record(req, **_k):
        seen.update({k.lower(): v for k, v in req.headers.items()})
        return _Resp({})

    monkeypatch.setattr(gh.urllib.request, "urlopen", record)
    gh.fetch_repo("o/n", "secret")
    assert seen.get("Authorization".lower()) == "Bearer secret"


def test_fetch_repo_omits_the_auth_header_without_a_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: dict[str, str] = {}

    def record(req, **_k):
        seen.update({k.lower(): v for k, v in req.headers.items()})
        return _Resp({})

    monkeypatch.setattr(gh.urllib.request, "urlopen", record)
    gh.fetch_repo("o/n", None)
    assert "authorization" not in seen


@pytest.mark.parametrize(
    "exc",
    [
        gh.urllib.error.HTTPError("u", 404, "Not Found", {}, None),
        gh.urllib.error.URLError("no route to host"),
        ValueError("malformed json"),
    ],
)
def test_fetch_repo_returns_none_on_any_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], exc: Exception
) -> None:
    """Every failure mode degrades to None so main() can fall back to the
    last-known value; none of them may abort the build."""

    def boom(*_a, **_k):
        raise exc

    monkeypatch.setattr(gh.urllib.request, "urlopen", boom)
    assert gh.fetch_repo("o/n", None) is None
    assert "o/n" in capsys.readouterr().err
