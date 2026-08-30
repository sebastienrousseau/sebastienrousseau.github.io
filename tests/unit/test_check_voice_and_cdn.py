# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The editorial gate and the CDN URL repairer.

check_voice is the gate a new article must pass before publication. It is the
last thing between a draft and the live site, so a check that silently stops
detecting is worse than no check: the article ships and nobody looks again.

fix_cdn_urls rewrites asset URLs to their current CDN locations. Its candidate
ordering is load-bearing — the unmodified path is tried first so an
already-correct URL is never rewritten — and that ordering had no test.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import check_voice as cv
import fix_cdn_urls as cdn
import pytest

# ---------------------------------------------------------------------------
# check_voice — front matter
# ---------------------------------------------------------------------------


def test_frontmatter_reports_one_defect_per_missing_field() -> None:
    defects = cv.check_frontmatter({})
    assert len(defects) == len(cv._REQUIRED_FM)
    assert all("missing or empty" in d for d in defects)


def test_frontmatter_treats_an_empty_value_as_missing() -> None:
    """A present-but-empty field is not a filled field."""
    field = cv._REQUIRED_FM[0]
    assert cv.check_frontmatter({field: ""})


def test_frontmatter_is_clean_when_every_field_is_filled() -> None:
    assert cv.check_frontmatter({k: "value" for k in cv._REQUIRED_FM}) == []


# ---------------------------------------------------------------------------
# check_voice — filler
# ---------------------------------------------------------------------------


def test_filler_detects_a_banned_phrase_case_insensitively() -> None:
    phrase = cv._BANNED_FILLER[0]
    assert cv.check_filler(f"Text {phrase.upper()} more text")


def test_filler_is_clean_on_ordinary_prose() -> None:
    assert cv.check_filler("A plain sentence about payments.") == []


def test_filler_reports_each_distinct_phrase() -> None:
    if len(cv._BANNED_FILLER) < 2:
        pytest.skip("needs at least two banned phrases")
    a, b = cv._BANNED_FILLER[0], cv._BANNED_FILLER[1]
    assert len(cv.check_filler(f"{a} and also {b}")) == 2


# ---------------------------------------------------------------------------
# check_voice — markdown discipline
# ---------------------------------------------------------------------------


def test_markdown_requires_exactly_one_h1() -> None:
    assert cv.check_markdown_discipline("# One\n\ntext\n") == []


def test_markdown_flags_a_missing_h1() -> None:
    assert any("H1 appears 0" in d for d in cv.check_markdown_discipline("no heading\n"))


def test_markdown_flags_a_second_h1() -> None:
    assert any("H1 appears 2" in d for d in cv.check_markdown_discipline("# A\n# B\n"))


def test_markdown_does_not_count_an_h2_as_an_h1() -> None:
    assert cv.check_markdown_discipline("# A\n## B\n") == []


def test_markdown_detects_a_broken_citation_link() -> None:
    assert any("](]" in d for d in cv.check_markdown_discipline("# A\n[text](]\n"))


# ---------------------------------------------------------------------------
# check_voice — dates
# ---------------------------------------------------------------------------


def _today() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")


def test_date_flags_a_filename_without_a_date() -> None:
    defects = cv.check_date_consistency(Path("glossary.md"), {})
    assert any("does not begin with YYYY-MM-DD" in d for d in defects)


def test_date_is_clean_when_filename_and_frontmatter_agree_with_today() -> None:
    today = _today()
    human = dt.datetime.strptime(today, "%Y-%m-%d").strftime("%B %d, %Y")
    assert cv.check_date_consistency(Path(f"{today}-a-post.md"), {"date": human}) == []


def test_date_flags_a_filename_that_is_not_today() -> None:
    defects = cv.check_date_consistency(Path("2020-01-01-old.md"), {})
    assert any("!= today UTC" in d for d in defects)


def test_date_flags_frontmatter_disagreeing_with_the_filename() -> None:
    today = _today()
    defects = cv.check_date_consistency(Path(f"{today}-a.md"), {"date": "January 01, 2020"})
    assert any("but filename says" in d for d in defects)


def test_date_flags_an_unparseable_frontmatter_date() -> None:
    today = _today()
    defects = cv.check_date_consistency(Path(f"{today}-a.md"), {"date": "2026-01-01"})
    assert any("not in" in d for d in defects)


def test_date_ignores_an_absent_frontmatter_date() -> None:
    """Missing is check_frontmatter's business, not this check's."""
    today = _today()
    assert cv.check_date_consistency(Path(f"{today}-a.md"), {}) == []


# ---------------------------------------------------------------------------
# check_voice — banner reachability
# ---------------------------------------------------------------------------


def test_banner_empty_is_a_defect() -> None:
    assert cv.check_banner_reachable("") == ["banner: empty"]


def test_banner_unreachable_is_reported_not_raised(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_a, **_k):
        raise OSError("no route to host")

    monkeypatch.setattr(cv.urllib.request, "urlopen", boom)
    defects = cv.check_banner_reachable("https://cdn/x.webp")
    assert len(defects) == 1
    assert "unreachable" in defects[0]


class _Resp:
    def __init__(self, status: int) -> None:
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False


@pytest.mark.parametrize("status", [200, 206])
def test_banner_accepts_ok_and_partial_content(
    monkeypatch: pytest.MonkeyPatch, status: int
) -> None:
    """A Range GET answers 206; treating that as failure would flag every banner."""
    monkeypatch.setattr(cv.urllib.request, "urlopen", lambda *a, **k: _Resp(status))
    assert cv.check_banner_reachable("https://cdn/x.webp") == []


def test_banner_non_2xx_is_a_defect(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cv.urllib.request, "urlopen", lambda *a, **k: _Resp(404))
    assert "HTTP 404" in cv.check_banner_reachable("https://cdn/x.webp")[0]


# ---------------------------------------------------------------------------
# fix_cdn_urls — candidate generation
# ---------------------------------------------------------------------------


def test_candidates_start_with_the_unmodified_path() -> None:
    """Order is load-bearing: an already-correct URL must never be rewritten."""
    cands = cdn.candidate_paths("https://cloudcdn.pro/stocks/images/a.webp")
    assert cands[0] == "stocks/images/a.webp"


def test_candidates_strip_either_cdn_host() -> None:
    for host in ("kura.pro", "cloudcdn.pro"):
        assert cdn.candidate_paths(f"https://{host}/stocks/x.webp")[0] == "stocks/x.webp"


def test_candidates_are_deduplicated_preserving_order() -> None:
    cands = cdn.candidate_paths("https://cloudcdn.pro/stock/images/a.webp")
    assert len(cands) == len(dict.fromkeys(cands))


def test_stock_rewrite_renames_the_legacy_bucket() -> None:
    assert "stocks/images/a.webp" in cdn._stock_rewrites("stock/images/a.webp")


def test_stock_rewrite_flattens_the_unsplash_banners_path() -> None:
    assert "stocks/images/a.webp" in cdn._stock_rewrites("unsplash/images/banners/a.webp")


def test_stock_rewrite_handles_plain_unsplash_images() -> None:
    assert "stocks/images/a.webp" in cdn._stock_rewrites("unsplash/images/a.webp")


def test_stock_rewrite_leaves_an_unrelated_path_alone() -> None:
    assert cdn._stock_rewrites("something/else.webp") == []


def test_client_rewrite_maps_a_known_brand_logo_to_svg() -> None:
    brand = next(iter(cdn.BRAND_LOGOS))
    out = cdn._client_rewrites(f"logos/{brand}.png")
    assert f"clients/sebastienrousseau/v1/logos/{brand}.svg" in out


def test_client_rewrite_ignores_an_unknown_brand() -> None:
    assert cdn._client_rewrites("logos/not-a-known-brand.png") == []


def test_client_rewrite_maps_a_project_images_path() -> None:
    project = next(iter(cdn.PROJECT_PREFIXES))
    assert f"clients/{project}/v1/a.webp" in cdn._client_rewrites(f"{project}/images/a.webp")


def test_client_rewrite_preserves_an_explicit_version() -> None:
    project = next(iter(cdn.PROJECT_PREFIXES))
    assert f"clients/{project}/v3/a.webp" in cdn._client_rewrites(f"{project}/v3/a.webp")


def test_client_rewrite_ignores_an_unknown_project() -> None:
    assert cdn._client_rewrites("not-a-project/images/a.webp") == []


# ---------------------------------------------------------------------------
# fix_cdn_urls — resolution against disk
# ---------------------------------------------------------------------------


def _cdn_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *rels: str) -> None:
    for rel in rels:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"x")
    monkeypatch.setattr(cdn, "CDN_ROOT", tmp_path)


def test_try_ext_variants_returns_the_path_when_it_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _cdn_root(tmp_path, monkeypatch, "stocks/a.webp")
    assert cdn.try_ext_variants("stocks/a.webp") == "stocks/a.webp"


def test_try_ext_variants_swaps_the_extension(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ext = cdn.EXT_FALLBACKS[0]
    _cdn_root(tmp_path, monkeypatch, f"stocks/a{ext}")
    assert cdn.try_ext_variants("stocks/a.jpg") == f"stocks/a{ext}"


def test_try_ext_variants_returns_none_when_nothing_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _cdn_root(tmp_path, monkeypatch)
    assert cdn.try_ext_variants("stocks/missing.webp") is None


def test_resolve_returns_none_for_an_already_correct_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No rewrite needed means None, not the same URL back."""
    _cdn_root(tmp_path, monkeypatch, "stocks/images/a.webp")
    assert cdn.resolve("https://cloudcdn.pro/stocks/images/a.webp") is None


def test_resolve_rewrites_a_legacy_bucket(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _cdn_root(tmp_path, monkeypatch, "stocks/images/a.webp")
    out = cdn.resolve("https://cloudcdn.pro/stock/images/a.webp")
    assert out == "https://cloudcdn.pro/stocks/images/a.webp"


def test_resolve_rewrites_the_host_even_when_the_path_is_right(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _cdn_root(tmp_path, monkeypatch, "stocks/images/a.webp")
    out = cdn.resolve("https://kura.pro/stocks/images/a.webp")
    assert out == "https://cloudcdn.pro/stocks/images/a.webp"


def test_resolve_returns_none_when_nothing_resolves(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _cdn_root(tmp_path, monkeypatch)
    assert cdn.resolve("https://cloudcdn.pro/stocks/images/gone.webp") is None
