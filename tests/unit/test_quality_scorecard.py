# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The scorecard reports quality, so a wrong number here is worse than none.

scripts/seo_and_audit/quality_scorecard.py had no test at all — 305 statements
at 0% coverage — while producing the figures the project quotes about itself.
Its own header says "every figure below is measured, not asserted"; nothing
checked that the measuring worked.

These tests pin the behaviour that would silently corrupt a published score:
the unmeasured sentinel never scoring, a broken scorer degrading to None rather
than to a number, the weighted overall ignoring unscored categories, and the
English/locale split in the internal-link count that a previous single-median
measurement got badly wrong.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import quality_scorecard as qs

# ---------------------------------------------------------------------------
# Scoring primitives
# ---------------------------------------------------------------------------


def test_band_higher_is_better_picks_first_threshold_met() -> None:
    score = qs.band([(90, 10.0), (75, 7.0), (50, 4.0)])
    assert score(95) == 10.0
    assert score(90) == 10.0  # boundary is inclusive
    assert score(80) == 7.0
    assert score(50) == 4.0
    assert score(49) == 0.0  # nothing met -> zero, never a guess


def test_band_lower_is_better_inverts_the_comparison() -> None:
    score = qs.band([(0, 10.0), (5, 7.0), (20, 3.0)], higher_is_better=False)
    assert score(0) == 10.0
    assert score(3) == 7.0
    assert score(20) == 3.0
    assert score(21) == 0.0


def test_boolean_scorer() -> None:
    assert qs.boolean()(True) == 10.0
    assert qs.boolean()(False) == 0.0
    assert qs.boolean(points_true=6.0, points_false=1.0)(True) == 6.0


# ---------------------------------------------------------------------------
# Metric / Category — the sentinel is the whole point
# ---------------------------------------------------------------------------


def _metric(value: object = qs.UNMEASURED, fn=None) -> qs.Metric:
    return qs.Metric(key="k", label="l", how="h", score_fn=fn or float, value=value)


def test_unmeasured_never_scores() -> None:
    """'unmeasured' means exactly that; it must not become a number."""
    assert _metric().score is None
    assert _metric(value=None).score is None


def test_measured_value_scores() -> None:
    assert _metric(value=7).score == 7.0


def test_a_broken_scorer_yields_none_not_a_fake_number() -> None:
    def explode(_v: object) -> float:
        raise ZeroDivisionError("scorer is wrong")

    assert _metric(value=1, fn=explode).score is None


def test_category_score_is_the_mean_of_scored_metrics_only() -> None:
    cat = qs.Category(key="c", label="C", weight=0.5)
    cat.metrics = [_metric(value=10), _metric(value=5), _metric()]
    assert cat.score == 7.5  # the unmeasured one is excluded, not counted as 0
    assert cat.coverage == "2/3"


def test_category_with_nothing_measured_scores_none() -> None:
    cat = qs.Category(key="c", label="C", weight=0.5)
    cat.metrics = [_metric(), _metric()]
    assert cat.score is None
    assert cat.coverage == "0/2"


# ---------------------------------------------------------------------------
# Weighted overall
# ---------------------------------------------------------------------------


def _cat(key: str, weight: float, values: list[object]) -> qs.Category:
    c = qs.Category(key=key, label=key, weight=weight)
    c.metrics = [_metric(value=v) for v in values]
    return c


def test_overall_weights_categories() -> None:
    cats = [_cat("a", 0.75, [10]), _cat("b", 0.25, [2])]
    assert qs.overall(cats) == 8.0


def test_overall_renormalises_over_scored_categories_only() -> None:
    """An unscored category must not drag the mean toward zero."""
    cats = [_cat("a", 0.5, [8]), _cat("b", 0.5, [])]
    assert qs.overall(cats) == 8.0


def test_overall_is_none_when_nothing_scored() -> None:
    assert qs.overall([_cat("a", 1.0, [])]) is None


# ---------------------------------------------------------------------------
# Filesystem-backed measurements
# ---------------------------------------------------------------------------


def test_pages_is_empty_without_a_build(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path / "absent")
    assert qs.pages() == []


def test_pages_finds_index_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "index.html").write_text("<html></html>", encoding="utf-8")
    (tmp_path / "a" / "other.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    assert [p.name for p in qs.pages()] == ["index.html"]


def test_duplicate_asset_count_unmeasured_without_the_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    assert qs._duplicate_asset_count() == qs.UNMEASURED


def test_duplicate_asset_count_counts_byte_identical_extras(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    csp = tmp_path / "_csp"
    csp.mkdir()
    (csp / "a.css").write_text("body{}", encoding="utf-8")
    (csp / "b.css").write_text("body{}", encoding="utf-8")  # duplicate of a
    (csp / "c.css").write_text("main{}", encoding="utf-8")  # unique
    (csp / "d.txt").write_text("body{}", encoding="utf-8")  # ignored: not css/js
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    assert qs._duplicate_asset_count() == 1


def test_allowlisted_complexity_skips_comments_and_blanks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dev = tmp_path / "scripts" / "dev"
    dev.mkdir(parents=True)
    (dev / "complexity-allowlist.txt").write_text(
        "# a comment\n\nfoo.py:bar\n  # indented comment\nbaz.py:qux\n", encoding="utf-8"
    )
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    assert qs._allowlisted_complexity() == 2


def test_allowlisted_complexity_unmeasured_when_file_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    assert qs._allowlisted_complexity() == qs.UNMEASURED


# ---------------------------------------------------------------------------
# HTML measurements
# ---------------------------------------------------------------------------


def _page(tmp: Path, rel: str, html: str) -> Path:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    return p


def test_meta_coverage_percentages_and_placeholders(tmp_path: Path) -> None:
    good = (
        '<meta name="description" content="'
        + "x" * 30
        + '"><link rel="canonical" href="/"><meta property="og:title" content="t">'
    )
    a = _page(tmp_path, "a/index.html", good)
    b = _page(tmp_path, "b/index.html", "<html>My SSG Site</html>")
    desc, canon, og, placeholder = qs._meta_coverage([a, b])
    assert (desc, canon, og, placeholder) == (50.0, 50.0, 50.0, 1)


def test_meta_coverage_ignores_a_too_short_description(tmp_path: Path) -> None:
    """A 19-character description is a stub, not a description."""
    p = _page(tmp_path, "a/index.html", '<meta name="description" content="short">')
    desc, _, _, _ = qs._meta_coverage([p])
    assert desc == 0.0


def test_internal_link_counts_splits_english_from_locale(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The split is the point: a single median over both hides the shape."""
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    en = _page(
        tmp_path,
        "2026-01-01-english/index.html",
        '<main><a href="/2026-02-02-other/">x</a>'
        '<a href="https://sebastienrousseau.com/2026-03-03-third/">y</a></main>',
    )
    fr = _page(
        tmp_path,
        "fr/2026-01-01-francais/index.html",
        '<main><a href="/fr/2026-02-02-autre/">x</a></main>',
    )
    _page(tmp_path, "about/index.html", '<main><a href="/2026-02-02-other/">x</a></main>')
    english, locale = qs._internal_link_counts([en, fr, tmp_path / "about" / "index.html"])
    assert english == [2]
    assert locale == [1]  # a locale article is counted, and counted separately


def test_internal_link_counts_ignores_links_outside_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    p = _page(
        tmp_path,
        "2026-01-01-x/index.html",
        '<nav><a href="/2026-09-09-nav/">nav</a></nav><main></main>',
    )
    assert qs._internal_link_counts([p]) == ([0], [])


def test_internal_link_counts_deduplicates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    p = _page(
        tmp_path,
        "2026-01-01-x/index.html",
        '<main><a href="/2026-02-02-same/">a</a><a href="/2026-02-02-same/">b</a></main>',
    )
    assert qs._internal_link_counts([p]) == ([1], [])


# ---------------------------------------------------------------------------
# JSON reading
# ---------------------------------------------------------------------------


def test_read_json_missing_invalid_and_non_dict(tmp_path: Path) -> None:
    assert qs._read_json(tmp_path / "nope.json") is None

    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert qs._read_json(bad) is None

    arr = tmp_path / "arr.json"
    arr.write_text("[1, 2]", encoding="utf-8")
    assert qs._read_json(arr) is None  # a list is not a report


def test_read_json_valid(tmp_path: Path) -> None:
    ok = tmp_path / "ok.json"
    ok.write_text(json.dumps({"total_issues": 3}), encoding="utf-8")
    assert qs._read_json(ok) == {"total_issues": 3}


# ---------------------------------------------------------------------------
# WCAG verification routes
# ---------------------------------------------------------------------------


CRITERIA = [
    {"status": "runtime"},
    {"status": "runtime"},
    {"status": "manual"},
    {"status": "not-applicable"},
]


def test_unverified_wcag_counts_runtime_when_no_pa11y_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))  # manual gate passes
    count, detail = qs._unverified_wcag_criteria(CRITERIA)
    assert count == 2
    assert "NO" in detail and "pass" in detail


def test_unverified_wcag_counts_manual_when_the_gate_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "accessibility-report.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (1, ""))  # manual gate fails
    count, detail = qs._unverified_wcag_criteria(CRITERIA)
    assert count == 1
    assert "yes" in detail and "FAIL" in detail


def test_unverified_wcag_is_zero_when_both_routes_hold(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "accessibility-report.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    assert qs._unverified_wcag_criteria(CRITERIA)[0] == 0


# ---------------------------------------------------------------------------
# Subprocess wrapper
# ---------------------------------------------------------------------------


def test_run_returns_output_and_code() -> None:
    rc, out = qs.run(["python3", "-c", "import sys; print('hi'); sys.exit(3)"])
    assert rc == 3
    assert "hi" in out


def test_run_degrades_to_minus_one_on_a_missing_binary() -> None:
    rc, out = qs.run(["definitely-not-a-real-binary-xyzzy"])
    assert rc == -1
    assert out == ""


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def test_render_marks_unmeasured_and_counts_them() -> None:
    cats = [_cat("code", 1.0, [10, qs.UNMEASURED])]
    out = qs.render(cats)
    assert "unmeasured" in out
    assert "1/2 metrics measured" in out
    assert "1 unmeasured and excluded" in out


def test_render_shows_n_a_when_nothing_is_measurable() -> None:
    out = qs.render([_cat("code", 1.0, [])])
    assert "n/a" in out


def test_rubric_categories_have_weights_that_sum_to_one() -> None:
    total = sum(c.weight for c in qs.rubric())
    assert round(total, 6) == 1.0, f"weights sum to {total}, so 'weighted' would be a lie"


def test_rubric_keys_are_unique() -> None:
    keys = [c.key for c in qs.rubric()]
    assert len(keys) == len(set(keys))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_main_json_emits_the_overall_score(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(qs, "collect", lambda: [_cat("code", 1.0, [8])])
    assert qs.main(["--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["overall"] == 8.0


def test_main_fail_under_exits_nonzero_below_the_threshold(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(qs, "collect", lambda: [_cat("code", 1.0, [4])])
    assert qs.main(["--fail-under", "7"]) == 1
    capsys.readouterr()


def test_main_fail_under_passes_at_or_above_the_threshold(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(qs, "collect", lambda: [_cat("code", 1.0, [7])])
    assert qs.main(["--fail-under", "7"]) == 0
    capsys.readouterr()


def test_main_without_arguments_renders_and_succeeds(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(qs, "collect", lambda: [_cat("code", 1.0, [9])])
    assert qs.main([]) == 0
    assert "WEIGHTED OVERALL" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# measure_* — each populates one category from the environment. Every external
# call is stubbed so these assert the mapping, not the tools.
# ---------------------------------------------------------------------------


def _by_key(key: str) -> qs.Category:
    return next(c for c in qs.rubric() if c.key == key)


def test_measure_code_maps_exit_codes_to_booleans(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
        calls.append(cmd)
        if cmd[0] == "ruff":
            return 0, ""
        if cmd[0] == "bash":
            return 1, ""  # typecheck fails
        return 0, "1234 tests collected"

    monkeypatch.setattr(qs, "run", fake_run)
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    monkeypatch.setattr(qs, "PUBLIC", tmp_path / "public")
    cat = _by_key("code")
    qs.measure_code(cat)

    assert cat.metrics[0].value is True  # ruff clean
    assert cat.metrics[1].value is False  # typecheck failed
    assert cat.metrics[2].value == qs.UNMEASURED  # no allowlist file
    assert cat.metrics[3].value == 1234  # parsed from pytest output
    assert any(c[0] == "ruff" for c in calls)


def test_measure_code_records_the_allowlist_detail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dev = tmp_path / "scripts" / "dev"
    dev.mkdir(parents=True)
    (dev / "complexity-allowlist.txt").write_text("a.py:f\n", encoding="utf-8")
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    monkeypatch.setattr(qs, "PUBLIC", tmp_path / "public")
    cat = _by_key("code")
    qs.measure_code(cat)
    assert cat.metrics[2].value == 1
    assert "enumerated" in cat.metrics[2].detail


def test_measure_code_leaves_test_count_unmeasured_when_unparseable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A changed pytest output format must not invent a number."""
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, "no count here"))
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    monkeypatch.setattr(qs, "PUBLIC", tmp_path / "public")
    cat = _by_key("code")
    qs.measure_code(cat)
    assert cat.metrics[3].value == qs.UNMEASURED


def test_measure_a11y_reads_both_reports(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "accessibility-report.json").write_text(
        json.dumps({"total_issues": 4, "pages_scanned": 3697}), encoding="utf-8"
    )
    (tmp_path / "wcag-compliance.json").write_text(
        json.dumps(
            {
                "criteria": [
                    {"status": "automated", "all_pages_pass": True},
                    {"status": "automated", "all_pages_pass": False},
                    {"status": "runtime"},
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    cat = _by_key("a11y")
    qs.measure_a11y(cat)
    assert cat.metrics[0].value == 4
    assert cat.metrics[1].value == 3697
    assert cat.metrics[2].value == 50.0
    assert cat.metrics[2].detail == "1/2 automated criteria"


def test_measure_a11y_without_reports_leaves_everything_unmeasured(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    cat = _by_key("a11y")
    qs.measure_a11y(cat)
    assert all(m.value == qs.UNMEASURED for m in cat.metrics)


def test_measure_i18n_counts_locale_directories(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    posts = tmp_path / "_posts"
    for name in ("fr", "zh-hant", "de"):
        (posts / name).mkdir(parents=True)
    (posts / "a-very-long-directory-name").mkdir()  # not a locale
    monkeypatch.setattr(qs, "POSTS", posts)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    cat = _by_key("i18n")
    qs.measure_i18n(cat)
    assert cat.metrics[0].value is True
    assert cat.metrics[3].value == 3


def test_measure_ops_reads_workflow_features_and_adr_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text(
        "jobs:\n"
        "  a:\n    timeout-minutes: 30\n    steps: []\n"
        "  b:\n    steps: []\n"
        "name: Reproducible build\n",
        encoding="utf-8",
    )
    adr = tmp_path / "project-docs" / "adr"
    adr.mkdir(parents=True)
    (adr / "0001-x.md").write_text("x", encoding="utf-8")
    (adr / "0002-y.md").write_text("y", encoding="utf-8")
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    cat = _by_key("ops")
    qs.measure_ops(cat)
    assert cat.metrics[0].value is True  # "Reproducible build" present
    assert cat.metrics[1].value is False  # verify_deploy.py absent
    assert cat.metrics[3].value == 50.0  # 1 of 2 jobs bounded
    assert cat.metrics[3].detail == "1/2 CI jobs bounded"
    assert cat.metrics[4].value == 2


def test_measure_ops_timeout_ratio_is_unmeasured_on_unparseable_yaml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A broken workflow must not score; it must decline to answer."""
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text("jobs: [unclosed\n", encoding="utf-8")
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    cat = _by_key("ops")
    qs.measure_ops(cat)
    assert cat.metrics[3].value == qs.UNMEASURED


def test_measure_seo_and_ux_decline_without_pages() -> None:
    """No build, no measurement — never a zero."""
    seo, ux = _by_key("seo"), _by_key("ux")
    qs.measure_seo(seo, [])
    qs.measure_ux(ux, [])
    assert all(m.value == qs.UNMEASURED for m in seo.metrics)
    assert all(m.value == qs.UNMEASURED for m in ux.metrics)


def test_measure_security_declines_without_pages() -> None:
    sec = _by_key("security")
    qs.measure_security(sec, [])
    assert all(m.value == qs.UNMEASURED for m in sec.metrics)


def test_collect_returns_every_rubric_category(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(qs, "pages", lambda: [])
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    cats = qs.collect()
    assert [c.key for c in cats] == [c.key for c in qs.rubric()]


# ---------------------------------------------------------------------------
# measure_seo / measure_ux / measure_security — the page-walking measurements.
#
# These take a page list, so synthetic pages are enough; no build required.
# Every subprocess is stubbed, including npm audit, so nothing shells out.
# ---------------------------------------------------------------------------


def _html(tmp: Path, rel: str, body: str) -> Path:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


GOOD_META = (
    '<meta name="description" content="'
    + "d" * 40
    + '"><link rel="canonical" href="/"><meta property="og:title" content="t">'
)


def test_measure_seo_records_meta_coverage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    pages = [_html(tmp_path, "a/index.html", GOOD_META), _html(tmp_path, "b/index.html", "<html>")]
    cat = _by_key("seo")
    qs.measure_seo(cat, pages)
    assert cat.metrics[0].value == 50.0  # description
    assert cat.metrics[1].value == 50.0  # canonical
    assert cat.metrics[2].value == 50.0  # og:title


def test_measure_seo_parses_the_validator_and_link_audit_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Both figures come from another tool's stdout, so the parse is the risk."""

    def fake_run(cmd, cwd=None):
        if "validate_jsonld.py" in " ".join(cmd):
            return 0, "7 with structured-data errors"
        return 0, "1234 checked, 5 broken"

    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", fake_run)
    cat = _by_key("seo")
    qs.measure_seo(cat, [_html(tmp_path, "a/index.html", GOOD_META)])
    assert cat.metrics[4].value == 7
    assert cat.metrics[6].value == 5


def test_measure_seo_leaves_metrics_unmeasured_when_output_is_unparseable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A changed output format must not invent a number."""
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, "unexpected output"))
    cat = _by_key("seo")
    qs.measure_seo(cat, [_html(tmp_path, "a/index.html", GOOD_META)])
    assert cat.metrics[4].value == qs.UNMEASURED
    assert cat.metrics[6].value == qs.UNMEASURED


def test_measure_seo_reports_the_english_internal_link_median(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    pages = [
        _html(
            tmp_path,
            f"2026-01-0{i}-post/index.html",
            "<main>"
            + "".join(f'<a href="/2026-02-0{j}-other/">x</a>' for j in range(1, 5))
            + "</main>",
        )
        for i in (1, 2)
    ]
    cat = _by_key("seo")
    qs.measure_seo(cat, pages)
    assert cat.metrics[5].value == 4
    assert "EN articles" in cat.metrics[5].detail
    assert cat.metrics[7].value == 100.0  # both reached the >=4 threshold


def test_measure_seo_declines_without_pages() -> None:
    cat = _by_key("seo")
    qs.measure_seo(cat, [])
    assert all(m.value == qs.UNMEASURED for m in cat.metrics)


def test_measure_ux_measures_compressed_not_raw_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Raw bytes are not a quantity any reader experiences — production
    serves gzip, and scoring uncompressed size is actively inverted."""
    import gzip

    body = "<html>" + ("a" * 50_000) + "</html>"
    pages = [_html(tmp_path, f"p{i}/index.html", body) for i in range(3)]
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    cat = _by_key("ux")
    qs.measure_ux(cat, pages)
    gz_kb = round(len(gzip.compress(body.encode(), 6)) / 1024, 1)
    assert cat.metrics[0].value == gz_kb
    assert cat.metrics[0].value < len(body) / 1024, "must be smaller than raw"
    assert "gzip" in cat.metrics[0].detail


def test_measure_ux_is_deterministic_across_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The sample uses a fixed seed so two runs on one tree agree."""
    pages = [
        _html(tmp_path, f"p{i}/index.html", f"<html>{'x' * (i * 100)}</html>") for i in range(20)
    ]
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    first, second = _by_key("ux"), _by_key("ux")
    qs.measure_ux(first, pages)
    qs.measure_ux(second, pages)
    assert first.metrics[0].value == second.metrics[0].value


def test_measure_ux_reports_shared_stylesheet_reach(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pages = [
        _html(tmp_path, "a/index.html", '<link href="/_csp/abc123.css">'),
        _html(tmp_path, "b/index.html", '<link href="/_csp/abc123.css">'),
        _html(tmp_path, "c/index.html", '<link href="/_csp/def456.css">'),
    ]
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    cat = _by_key("ux")
    qs.measure_ux(cat, pages)
    assert cat.metrics[2].value == round(100 * 2 / 3, 1)


def test_measure_ux_checks_the_font_stylesheet(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "fonts").mkdir()
    (tmp_path / "fonts" / "fonts.css").write_text(
        "@font-face{font-display: swap; size-adjust: 100%;}", encoding="utf-8"
    )
    monkeypatch.setattr(qs, "ROOT", tmp_path)
    cat = _by_key("ux")
    qs.measure_ux(cat, [_html(tmp_path, "a/index.html", "<html>")])
    assert cat.metrics[3].value is True


def test_measure_security_counts_unsafe_inline_and_sri(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pages = [
        _html(tmp_path, "a/index.html", "<meta content=\"script-src 'unsafe-inline'\">"),
        _html(tmp_path, "b/index.html", '<link rel="stylesheet" integrity="sha256-x">'),
    ]
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    cat = _by_key("security")
    qs.measure_security(cat, pages)
    assert cat.metrics[0].value == 1  # one page with unsafe-inline
    assert cat.metrics[1].value == 50.0  # one of two carries SRI


def test_measure_security_counts_duplicate_integrity_attributes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A doubled integrity attribute is a real postbuild regression shape."""
    page = _html(tmp_path, "a/index.html", '<link integrity="sha256-a" integrity="sha256-b">')
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    cat = _by_key("security")
    qs.measure_security(cat, [page])
    assert cat.metrics[2].value == 1


def test_measure_security_notes_a_missing_sbom(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda *a, **k: (0, ""))
    cat = _by_key("security")
    qs.measure_security(cat, [_html(tmp_path, "a/index.html", "<html>")])
    assert cat.metrics[3].value is False
    (tmp_path / "sbom.cdx.json").write_text("{}", encoding="utf-8")
    cat2 = _by_key("security")
    qs.measure_security(cat2, [_html(tmp_path, "a/index.html", "<html>")])
    assert cat2.metrics[3].value is True


def test_measure_security_counts_failing_npm_audits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Three ci-tools lockfiles are audited; a non-zero exit counts as one."""
    monkeypatch.setattr(qs, "PUBLIC", tmp_path)
    monkeypatch.setattr(qs, "run", lambda cmd, cwd=None: (1, "") if cmd[0] == "npm" else (0, ""))
    cat = _by_key("security")
    qs.measure_security(cat, [_html(tmp_path, "a/index.html", "<html>")])
    assert cat.metrics[4].value == 3
    assert "npm audit" in cat.metrics[4].detail
