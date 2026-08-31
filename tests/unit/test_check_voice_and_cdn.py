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


# ---------------------------------------------------------------------------
# check_voice — structure, the gate that differs by language
# ---------------------------------------------------------------------------


_CITE = '[source](https://example.com/a "Title")'


def _en_article(**drop: bool) -> str:
    """A structurally complete EN article; pass e.g. faq=False to break one."""
    parts = ["<!-- lead-start -->\n"]
    if drop.get("summary", True):
        parts.append("> **Executive Summary** the summary.\n\n")
    parts.append("## One\ntext\n\n## Two\ntext\n\n")
    if drop.get("faq", True):
        parts.append("## Frequently Asked Questions\n\n**A question?**\n\n")
    if drop.get("refs", True):
        parts.append(f"## References\n\n{_CITE}\n")
    else:
        parts.append(f"{_CITE}\n")
    return "".join(parts)


def test_structure_accepts_a_complete_english_article() -> None:
    assert cv.check_structure(_en_article(), lang="en") == []


def test_structure_requires_the_lead_marker() -> None:
    body = _en_article().replace("<!-- lead-start -->", "")
    assert any("lead-start" in d for d in cv.check_structure(body, lang="en"))


def test_structure_accepts_the_manual_lead_opt_out() -> None:
    """A hand-curated lead tells post_enrich to leave it alone; still valid."""
    body = _en_article().replace("<!-- lead-start -->", "<!-- lead-start: manual -->")
    assert cv.check_structure(body, lang="en") == []


def test_structure_requires_three_h2_sections() -> None:
    body = "<!-- lead-start -->\n> **Executive Summary** s.\n\n## One\n" + _CITE
    assert any("H2 section" in d for d in cv.check_structure(body, lang="en"))


def test_structure_requires_a_titled_citation_link() -> None:
    """A bare markdown link is not a citation; the title attribute is the point."""
    body = _en_article().replace(_CITE, "[source](https://example.com/a)")
    assert any("citation links" in d for d in cv.check_structure(body, lang="en"))


def test_structure_names_each_missing_english_section() -> None:
    for key, needle in (("summary", "Executive Summary"), ("faq", "FAQ"), ("refs", "References")):
        defects = cv.check_structure(_en_article(**{key: False}), lang="en")
        assert any(needle in d for d in defects), f"{key} not reported"


def test_structure_does_not_apply_english_heading_text_to_a_locale() -> None:
    """A German article carries '## Häufige Fragen', not '## FAQ' — matching
    on English heading text would fail every translated file."""
    body = (
        "<!-- lead-start -->\n"
        "> **Zusammenfassung** der Text.\n\n"
        "## Einleitung\ntext\n\n"
        "## Häufige Fragen\n\n"
        "**Eine Frage?**\n\n**Noch eine?**\n\n**Und eine dritte?**\n\n"
        "## Referenzen\n\n"
        f"{_CITE}\n{_CITE.replace('/a', '/b')}\n{_CITE.replace('/a', '/c')}\n"
    )
    assert cv.check_structure(body, lang="de") == []


def test_locale_structure_wants_a_bold_led_blockquote() -> None:
    body = "## Eins\ntext\n\n## Zwei\ntext\n"
    assert any("blockquote" in d for d in cv._check_locale_structure(body))


def test_locale_structure_needs_three_question_shaped_paragraphs() -> None:
    """Two is not a FAQ section; the shape check is a count, not a keyword."""
    body = (
        "> **Zusammenfassung** text.\n\n## Eins\n\n**Frage eins?**\n\n**Frage zwei?**\n\n"
        "## Zwei\ntext\n"
    )
    assert any("FAQ" in d for d in cv._check_locale_structure(body))


def test_locale_structure_stops_early_with_fewer_than_two_h2() -> None:
    """Too few sections to judge shape — report only what is knowable."""
    defects = cv._check_locale_structure("> **Zusammenfassung** text.\n\n## Nur eins\n")
    assert not any("FAQ" in d or "References" in d for d in defects)


# ---------------------------------------------------------------------------
# check_voice — external link probing
# ---------------------------------------------------------------------------


def test_external_links_is_empty_when_there_are_none() -> None:
    assert cv.check_external_links("no links here") == []


def test_external_links_reports_a_dead_citation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cv.urllib.request, "urlopen", lambda *a, **k: _Resp(404))
    defects = cv.check_external_links(f"see {_CITE}")
    assert len(defects) == 1
    assert "link-rot" in defects[0]


def test_external_links_accepts_a_partial_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """The probe is a Range GET, so 206 is the expected success code."""
    monkeypatch.setattr(cv.urllib.request, "urlopen", lambda *a, **k: _Resp(206))
    assert cv.check_external_links(f"see {_CITE}") == []


def test_external_links_reports_an_unreachable_host(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_a, **_k):
        raise OSError("no route")

    monkeypatch.setattr(cv.urllib.request, "urlopen", boom)
    assert cv.check_external_links(f"see {_CITE}")


def test_external_links_deduplicates_repeated_urls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[str] = []

    def record(req, **_k):
        seen.append(req.full_url)
        return _Resp(200)

    monkeypatch.setattr(cv.urllib.request, "urlopen", record)
    cv.check_external_links(f"{_CITE} and again {_CITE}")
    assert len(seen) == 1


# ---------------------------------------------------------------------------
# check_voice — the orchestrator
# ---------------------------------------------------------------------------


def _write(tmp_path: Path, body: str, **fm_over: str) -> Path:
    fm = dict.fromkeys(cv._REQUIRED_FM, "value")
    # `date` is a required field AND is parsed; a placeholder would be
    # reported as malformed and mask whatever the test is really asserting.
    fm["date"] = dt.datetime.now(dt.UTC).strftime("%B %d, %Y")
    fm.update(fm_over)
    head = "".join(f'{k}: "{v}"\n' for k, v in fm.items())
    today = _today()
    p = tmp_path / f"{today}-a-post.md"
    p.write_text(f"---\n{head}---\n\n# Title\n\n{body}", encoding="utf-8")
    return p


def test_check_article_is_clean_on_a_complete_post(tmp_path: Path) -> None:
    p = _write(tmp_path, _en_article())
    assert cv.check_article(p, skip_network=True) == []


def test_check_article_skips_the_banner_probe_when_asked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """skip_network must mean no socket is opened at all."""

    def fail(*_a, **_k):
        raise AssertionError("network was used despite skip_network")

    monkeypatch.setattr(cv.urllib.request, "urlopen", fail)
    cv.check_article(_write(tmp_path, _en_article()), skip_network=True)


def test_check_article_reports_a_date_mismatch(tmp_path: Path) -> None:
    p = _write(tmp_path, _en_article())
    stale = p.with_name("2020-01-01-a-post.md")
    p.rename(stale)
    assert any("date:" in d for d in cv.check_article(stale, skip_network=True))


def test_check_article_skips_dates_when_asked(tmp_path: Path) -> None:
    p = _write(tmp_path, _en_article())
    stale = p.with_name("2020-01-01-a-post.md")
    p.rename(stale)
    assert cv.check_article(stale, skip_network=True, skip_date=True) == []


def test_check_article_picks_the_locale_from_frontmatter(tmp_path: Path) -> None:
    """A German post must be judged by locale shape, not English headings."""
    body = (
        "> **Zusammenfassung** der Text.\n\n"
        "## Einleitung\ntext\n\n"
        "## Häufige Fragen\n\n**Eins?**\n\n**Zwei?**\n\n**Drei?**\n\n"
        "## Referenzen\n\n"
        f"{_CITE}\n{_CITE.replace('/a', '/b')}\n{_CITE.replace('/a', '/c')}\n"
    )
    p = _write(tmp_path, "<!-- lead-start -->\n" + body, hreflang="de")
    assert cv.check_article(p, skip_network=True, skip_date=True) == []
