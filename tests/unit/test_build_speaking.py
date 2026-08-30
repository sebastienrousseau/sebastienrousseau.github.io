# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The /speaking/ page generator — the largest untested file in the tree.

scripts/generators/build_speaking.py had 295 uncovered statements. It renders
a public page section by section from front matter, so the properties that
matter are the ones that fail quietly: escaping (the front matter is
hand-authored prose), the empty-input contract (an absent section must render
nothing rather than an empty shell), and the JSON-LD escaping that stops a
payload terminating its own <script> element.

The stats renderer is covered specifically because it drops rows whose KPI is
not in metrics.json. Silently emitting a stat with no number behind it would
be worse than emitting nothing.
"""

from __future__ import annotations

import json
from pathlib import Path

import build_speaking as bs
import pytest

# ---------------------------------------------------------------------------
# Text treatment
# ---------------------------------------------------------------------------


def test_rich_escapes_prose() -> None:
    assert "<script>" not in bs._rich("<script>alert(1)</script>")


def test_rich_marks_up_a_standards_identifier() -> None:
    """Standards terms get the monospace treatment; prose does not."""
    out = bs._rich("Migrating to ISO 20022 this year")
    assert "spk-mono" in out


def test_rich_leaves_ordinary_prose_unmarked() -> None:
    assert "spk-mono" not in bs._rich("A talk about payments and people")


def test_mono_wraps_each_identifier_once_per_pass() -> None:
    """_rich applies _mono exactly once per field; one wrap per identifier."""
    out = bs._rich("ISO 20022 and ISO 20022 again")
    assert out.count("spk-mono") == 2


# ---------------------------------------------------------------------------
# Microproof items
# ---------------------------------------------------------------------------


def test_micro_item_bolds_the_leading_word() -> None:
    assert bs._micro_item("20 years experience") == "<strong>20</strong> years experience"


def test_micro_item_keeps_trailing_punctuation_outside_the_bold() -> None:
    """`<strong>20,</strong>` would bold the comma; it belongs outside."""
    out = bs._micro_item("20, years experience")
    assert "<strong>20</strong>," in out


def test_micro_item_handles_a_single_word() -> None:
    assert bs._micro_item("Solo") == "Solo"


def test_micro_item_escapes_its_input() -> None:
    assert "<b>" not in bs._micro_item("<b>bold</b> attempt")


# ---------------------------------------------------------------------------
# Section head
# ---------------------------------------------------------------------------


def test_section_head_omits_the_lede_when_empty() -> None:
    assert "spk-lede" not in bs._section_head("Eyebrow", "Headline")


def test_section_head_includes_the_lede_when_given() -> None:
    out = bs._section_head("Eyebrow", "Headline", "A lede.")
    assert "spk-lede" in out
    assert "A lede." in out


def test_section_head_escapes_all_three_fields() -> None:
    out = bs._section_head("<e>", "<h>", "<l>")
    assert "<e>" not in out and "<h>" not in out and "<l>" not in out


def test_arrow_is_hidden_from_screen_readers() -> None:
    assert 'aria-hidden="true"' in bs._arrow()


# ---------------------------------------------------------------------------
# Empty-input contract — an absent section renders nothing at all
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fn",
    [bs._employers, bs._stats],
)
def test_section_renders_empty_string_when_its_data_is_absent(fn) -> None:
    assert fn({}) == ""


def test_paths_renders_empty_without_items() -> None:
    assert bs._paths({}, "/contact/") == ""
    assert bs._paths({"paths": {"items": []}}, "/contact/") == ""


def test_employers_renders_each_name_escaped() -> None:
    out = bs._employers({"employers": ["Bank & Co", "Other"], "employers_label": "Worked at"})
    assert "Bank &amp; Co" in out
    assert "Worked at" in out


# ---------------------------------------------------------------------------
# Stats — the KPI guard
# ---------------------------------------------------------------------------


def _with_metrics(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, stats: list[dict]) -> None:
    f = tmp_path / "metrics.json"
    f.write_text(json.dumps({"stats": stats}), encoding="utf-8")
    monkeypatch.setattr(bs, "METRICS_JSON", f)


def test_stats_drops_a_row_whose_kpi_is_unknown(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A stat with no number behind it must not be rendered with a blank."""
    _with_metrics(monkeypatch, tmp_path, [])
    out = bs._stats({"stats": [{"kpi": "no_such_kpi", "label": "Nope"}]})
    assert out == ""
    assert "unknown kpi" in capsys.readouterr().err


def test_stats_renders_a_known_kpi(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _with_metrics(monkeypatch, tmp_path, [{"key": "articles", "value": 1234, "format": "plain"}])
    out = bs._stats({"stats": [{"kpi": "articles", "label": "Articles"}]})
    assert "Articles" in out
    assert "1234" in out
    assert "spk-stat" in out


@pytest.mark.parametrize(
    ("value", "fmt", "expected"),
    [
        (39_600_000, "compact", "39.6M"),
        (2_000_000, "compact", "2M"),
        (1_500, "compact", "1.5K"),
        (2_000, "compact", "2K"),
        (999, "compact", "999"),
        (1234, "plain", "1234"),
    ],
)
def test_metrics_formats_numbers_the_same_way_the_rest_of_the_site_does(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, value: int, fmt: str, expected: str
) -> None:
    """Trailing .0 is dropped so 2.0M reads 2M, matching fetch_metrics."""
    _with_metrics(monkeypatch, tmp_path, [{"key": "k", "value": value, "format": fmt}])
    assert bs._metrics()["k"] == expected


def test_metrics_skips_a_row_with_no_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _with_metrics(monkeypatch, tmp_path, [{"value": 1}, {"key": "ok", "value": 2}])
    assert bs._metrics() == {"ok": "2"}


def test_metrics_stringifies_a_non_numeric_value(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _with_metrics(monkeypatch, tmp_path, [{"key": "k", "value": "n/a"}])
    assert bs._metrics()["k"] == "n/a"


def test_metrics_degrades_on_malformed_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    f = tmp_path / "metrics.json"
    f.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(bs, "METRICS_JSON", f)
    assert bs._metrics() == {}
    assert "could not read" in capsys.readouterr().err


def test_metrics_degrades_to_empty_when_the_file_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A missing metrics file must warn and return nothing, never crash."""
    monkeypatch.setattr(bs, "METRICS_JSON", tmp_path / "absent.json")
    assert bs._metrics() == {}
    capsys.readouterr()


# ---------------------------------------------------------------------------
# Navigation state
# ---------------------------------------------------------------------------


def test_mark_nav_active_fails_loudly_when_the_nav_is_missing() -> None:
    """A nav markup change must not silently ship broken chrome."""
    with pytest.raises(SystemExit):
        bs._mark_nav_active("<html><body>no nav here</body></html>")


def test_mark_nav_active_strips_a_stale_articles_marker() -> None:
    html = (
        '<ul class="ap-menu">'
        '<a href="/articles/index.html" aria-current="page" class="active">Articles</a>'
        "</ul>"
    )
    out = bs._mark_nav_active(html)
    assert 'aria-current="page"' not in out
    assert '<a href="/articles/index.html">Articles</a>' in out


def test_mark_nav_active_is_a_no_op_without_a_stale_marker() -> None:
    html = '<ul class="ap-menu"><a href="/articles/index.html">Articles</a></ul>'
    assert bs._mark_nav_active(html) == html


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------


def test_jsonld_script_escapes_a_closing_tag_sequence() -> None:
    """`</script>` inside the payload would end the element early."""
    out = bs._jsonld_script({"name": "</script><img onerror=x>"})
    assert "</script><img" not in out
    assert "<\\/script>" in out


def test_jsonld_script_is_valid_json_once_unescaped() -> None:
    out = bs._jsonld_script({"a": "b</c"})
    blob = out.split(">", 1)[1].rsplit("</script>", 1)[0]
    assert json.loads(blob.replace("<\\/", "</")) == {"a": "b</c"}


def test_topics_jsonld_is_empty_without_talks() -> None:
    assert bs._topics_jsonld({}) == ""
    assert bs._topics_jsonld({"keynotes": {"talks": []}}) == ""


def test_topics_jsonld_skips_a_talk_with_no_title() -> None:
    d = {"keynotes": {"talks": [{"title": "", "desc": "x"}, {"title": "Real", "desc": "y"}]}}
    out = bs._topics_jsonld(d)
    payload = json.loads(out.split(">", 1)[1].rsplit("</script>", 1)[0])
    assert [i["name"] for i in payload["itemListElement"]] == ["Real"]


def test_topics_jsonld_numbers_positions_from_one() -> None:
    d = {"keynotes": {"talks": [{"title": "A"}, {"title": "B"}]}}
    payload = json.loads(bs._topics_jsonld(d).split(">", 1)[1].rsplit("</script>", 1)[0])
    assert [i["position"] for i in payload["itemListElement"]] == [1, 2]


def test_breadcrumbs_jsonld_is_well_formed() -> None:
    out = bs._breadcrumbs_jsonld({}, "https://sebastienrousseau.com/speaking/")
    payload = json.loads(out.split(">", 1)[1].rsplit("</script>", 1)[0])
    assert payload["@type"] == "BreadcrumbList"
    assert len(payload["itemListElement"]) >= 2


# ---------------------------------------------------------------------------
# The empty-section contract, for the stages not already covered above.
#
# Same rule as the case-study stages: absent data renders nothing. A section
# with a heading and no content reads as missing data rather than data that
# does not apply.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "call"),
    [
        ("work", lambda: bs._work({})),
        ("media", lambda: bs._media({}, "/contact/")),
        ("bios", lambda: bs._bios({})),
        ("faq", lambda: bs._faq({})),
        ("keynotes", lambda: bs._keynotes({}, "/contact/")),
        ("final_cta", lambda: bs._final_cta({}, "/contact/")),
    ],
)
def test_every_remaining_section_renders_nothing_when_its_data_is_absent(name, call) -> None:
    """Each call is written out rather than guessed from the signature.

    A first version caught TypeError and retried with an extra argument,
    which fed "/contact/" to _biography as its BODY HTML — the section then
    rendered, and the test failed for a reason that had nothing to do with
    the contract it was checking.
    """
    assert call() == "", name


def test_booking_renders_nothing_without_its_block() -> None:
    assert bs._booking({}, "/contact/") == ""


def test_biography_renders_nothing_without_body_html() -> None:
    assert bs._biography({}, "") == ""


# ---------------------------------------------------------------------------
# Head patching — every mutation verifies it matched, and fails the build if
# not. These guards exist because the shell is a fork of the articles hub: if
# that markup changes, the page would otherwise ship with the articles hub's
# title and social copy and nothing would say so.
# ---------------------------------------------------------------------------


_SHELL_HEAD = (
    "<html><head>"
    "<title>Articles</title>"
    '<meta name="description" content="old">'
    '<meta name="viewport" content="width=device-width">'
    '<meta name="twitter:title" content="Articles">'
    '<meta name="twitter:description" content="old">'
    '<meta name="apple-mobile-web-app-title" content="Articles">'
    "</head><body>b</body></html>"
)


def test_patch_head_rewrites_title_and_social_copy() -> None:
    out = bs._patch_head(_SHELL_HEAD, "Speaking", "Speaking — SEO", "A description")
    assert "<title>Speaking</title>" in out
    assert 'content="Speaking — SEO"' in out
    assert "A description" in out
    assert "<body>b</body>" in out, "the body must be returned untouched"


def test_patch_head_fails_loudly_without_a_head() -> None:
    with pytest.raises(SystemExit, match="no </head>"):
        bs._patch_head("<html><body>b</body></html>", "T", "S", "D")


def test_patch_head_fails_loudly_without_a_title() -> None:
    shell = _SHELL_HEAD.replace("<title>Articles</title>", "")
    with pytest.raises(SystemExit, match="<title> not found"):
        bs._patch_head(shell, "T", "S", "D")


def test_patch_head_fails_loudly_without_twitter_title() -> None:
    shell = _SHELL_HEAD.replace('<meta name="twitter:title" content="Articles">', "")
    with pytest.raises(SystemExit, match="twitter:title not found"):
        bs._patch_head(shell, "T", "S", "D")


def test_patch_head_fails_loudly_without_twitter_description() -> None:
    shell = _SHELL_HEAD.replace('<meta name="twitter:description" content="old">', "")
    with pytest.raises(SystemExit, match="twitter:description not found"):
        bs._patch_head(shell, "T", "S", "D")


def test_patch_head_fails_loudly_if_stale_articles_copy_survives() -> None:
    """The last-resort check: if the hub's marketing line is still in the
    head after every rewrite, something upstream changed and the page would
    ship advertising the wrong thing."""
    shell = _SHELL_HEAD.replace(
        "</head>", '<meta name="x" content="Discover How Technology"></head>'
    )
    with pytest.raises(SystemExit, match="stale articles copy"):
        bs._patch_head(shell, "T", "S", "D")


def test_patch_head_replaces_the_stale_web_app_title() -> None:
    out = bs._patch_head(_SHELL_HEAD, "T", "S", "D")
    assert 'name="apple-mobile-web-app-title" content="Sebastien Rousseau"' in out


def test_patch_head_tolerates_an_absent_web_app_title() -> None:
    """Absence means nothing stale to fix — not a reason to fail the build."""
    shell = _SHELL_HEAD.replace('<meta name="apple-mobile-web-app-title" content="Articles">', "")
    assert bs._patch_head(shell, "T", "S", "D")


def test_patch_head_leaves_exactly_one_description_and_viewport() -> None:
    shell = _SHELL_HEAD.replace(
        "</head>",
        '<meta name="description" content="dupe"><meta name="viewport" content="dupe"></head>',
    )
    out = bs._patch_head(shell, "T", "S", "D")
    head = out[: out.find("</head>")]
    assert head.count('name="description"') == 1
    assert head.count('name="viewport"') == 1


def test_patch_head_keeps_one_theme_color_per_media_condition() -> None:
    """The light/dark pair is one set, not a duplicate — collapsing it to a
    single tag would break the dark-mode colour."""
    shell = _SHELL_HEAD.replace(
        "</head>",
        '<meta name="theme-color" content="#fff" media="(prefers-color-scheme: light)">'
        '<meta name="theme-color" content="#000" media="(prefers-color-scheme: dark)">'
        '<meta name="theme-color" content="#fff" media="(prefers-color-scheme: light)">'
        "</head>",
    )
    out = bs._patch_head(shell, "T", "S", "D")
    head = out[: out.find("</head>")]
    assert head.count('name="theme-color"') == 2
