# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""The proof-rail stamp follows metrics.json; tag pills show canonical names."""

from __future__ import annotations

import json

from postbuild_lib import article_furniture as af
from postbuild_lib import seo

STAMP_RAW = (
    '<span class="proof-updated">Updated <time datetime="2026-10-15">15 Oct 2026</time>.</span>'
)


def _metrics(tmp_path, generated_at="2026-10-30T00:20:13+00:00"):
    p = tmp_path / "metrics.json"
    p.write_text(json.dumps({"$generated_at": generated_at, "stats": []}), encoding="utf-8")
    return p


def test_stamp_follows_generated_at(monkeypatch, tmp_path):
    monkeypatch.setattr(seo, "_METRICS_JSON", _metrics(tmp_path))
    monkeypatch.setattr(seo, "_kpi_stamp_cache", None)
    out = seo.inject_kpi_stamp(STAMP_RAW)
    assert 'datetime="2026-10-30"' in out and ">30 Oct 2026</time>" in out
    assert seo.inject_kpi_stamp(out) == out  # idempotent


def test_stamp_survives_escaped_and_minified_forms(monkeypatch, tmp_path):
    monkeypatch.setattr(seo, "_METRICS_JSON", _metrics(tmp_path, "2026-11-02T08:00:00+00:00"))
    monkeypatch.setattr(seo, "_kpi_stamp_cache", None)
    escaped = '&lt;span class="proof-updated">Updated &lt;time datetime="2026-10-15">15 Oct 2026&lt;/time>.&lt;/span>'
    minified = (
        "<span class=proof-updated>Updated <time datetime=2026-10-15>15 Oct 2026</time>.</span>"
    )
    for html in (escaped, minified):
        out = seo.inject_kpi_stamp(html)
        assert "2026-11-02" in out and "2 Nov 2026" in out, out


def test_stamp_untouched_without_metrics_or_marker(monkeypatch, tmp_path):
    monkeypatch.setattr(seo, "_METRICS_JSON", tmp_path / "missing.json")
    monkeypatch.setattr(seo, "_kpi_stamp_cache", None)
    assert seo.inject_kpi_stamp(STAMP_RAW) == STAMP_RAW
    assert seo.inject_kpi_stamp("<p>no stamp</p>") == "<p>no stamp</p>"


def test_tag_pills_show_canonical_names_in_english():
    kw = ["AI", "ai-governance", "operational-resilience", "financial-services"]
    html = af._render_tag_badges(kw, {}, "en")
    assert ">AI governance</a>" in html
    assert ">Operational resilience</a>" in html
    # The keyword resolves to the Banking landing page, so the label says so.
    assert 'href="/tags/banking/" class="article-tag" rel="tag">Banking</a>' in html
    assert ">financial-services<" not in html and ">ai-governance<" not in html


def test_tag_pills_keep_keyword_outside_english():
    html = af._render_tag_badges(["ai-governance"], {}, "fr")
    assert ">ai-governance</a>" in html
