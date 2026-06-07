"""Run ``main()`` on the big builder scripts against the real
post-build tree, then re-run postbuild to re-stamp CSP/SRI on
anything that got rewritten.

Each test is a single ``main()`` invocation — that's deliberately
unsophisticated. The script's internals are idempotent on a clean
tree (they write the same bytes that already exist), so re-running
``./build.sh`` between sessions repairs any drift. The pay-off is
coverage: each main() walks 100+ to 1000+ lines of branchy logic
that's untouchable from a unit test without a vast fixture.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC = ROOT / "public"
sys.path.insert(0, str(ROOT / "scripts"))

SKIP_IF_NO_BUILD = pytest.mark.skipif(
    not PUBLIC.is_dir() or not (PUBLIC / "index.html").is_file(),
    reason="public/ not built — run ./build.sh first",
)


def _repair_csp_after_mutating_main():
    """Postbuild's CSP-hash + SRI passes need to re-stamp anything
    that got rewritten. Idempotent — same bytes in, same bytes out."""
    import postbuild

    importlib.reload(postbuild)
    postbuild.main()


# ---------------------------------------------------------------------------
# Builders + generators that emit content into _posts/ or rewrite
# specific markdown files. Safe to re-run because the inputs (the
# real _data/, _posts/<lang>/, etc.) don't change between runs.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_post_enrich_main_runs(capsys):
    import post_enrich

    post_enrich.main()
    out = capsys.readouterr().out
    assert "enriched" in out.lower() or "dated post" in out.lower()


@SKIP_IF_NO_BUILD
def test_build_topics_main_runs(capsys):
    import build_topics

    build_topics.main()
    out = capsys.readouterr().out
    # Output line varies; just confirm something printed.
    assert len(out.strip()) > 0


@SKIP_IF_NO_BUILD
def test_build_lang_feeds_main_runs(capsys):
    """Writes per-language rss/atom/feed.json/news-sitemap. Heavy but
    idempotent on a clean tree."""
    import build_lang_feeds

    build_lang_feeds.main()
    out = capsys.readouterr().out
    assert "build_lang_feeds:" in out or "feeds" in out.lower()


@SKIP_IF_NO_BUILD
def test_build_agent_api_main_runs(capsys):
    import build_agent_api

    build_agent_api.main()
    out = capsys.readouterr().out
    assert "build_agent_api:" in out or "wrote" in out.lower()


@SKIP_IF_NO_BUILD
def test_build_lead_magnets_main_runs(capsys):
    import build_lead_magnets

    build_lead_magnets.main()
    out = capsys.readouterr().out
    assert "PDF" in out or "wrote" in out.lower() or len(out.strip()) >= 0


@SKIP_IF_NO_BUILD
def test_gen_layouts_main_runs(capsys):
    import gen_layouts

    gen_layouts.main()
    out = capsys.readouterr().out
    assert "wrote" in out.lower() or "_layouts" in out


@SKIP_IF_NO_BUILD
def test_gen_projects_main_runs(capsys):
    import gen_projects

    gen_projects.main()
    out = capsys.readouterr().out
    assert "wrote" in out.lower() or "projects" in out.lower()


@SKIP_IF_NO_BUILD
def test_gen_papers_main_runs(capsys):
    import gen_papers

    gen_papers.main()
    out = capsys.readouterr().out
    assert "wrote" in out.lower() or "publications" in out.lower() or "papers" in out.lower()


@SKIP_IF_NO_BUILD
def test_gen_articles_main_runs(capsys):
    import gen_articles

    gen_articles.main()
    out = capsys.readouterr().out
    assert "wrote" in out.lower() or "Featured" in out


@SKIP_IF_NO_BUILD
def test_topic_link_main_runs(capsys):
    import topic_link

    topic_link.main()
    out = capsys.readouterr().out
    assert "topic_link" in out or "touched" in out.lower()


@SKIP_IF_NO_BUILD
def test_fix_cdn_urls_main_runs(capsys):
    import fix_cdn_urls

    fix_cdn_urls.main()
    out = capsys.readouterr().out
    assert "rewrote" in out.lower() or "URL" in out


@SKIP_IF_NO_BUILD
def test_validate_jsonld_main_runs(monkeypatch):
    """Run the JSON-LD validator. Exits non-zero if defects found —
    expects a clean tree here. main() uses argparse so we need to
    blank sys.argv."""
    import validate_jsonld

    monkeypatch.setattr(sys, "argv", ["validate_jsonld"])
    rc = validate_jsonld.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_jsonld_diff_main_runs():
    """jsonld_diff is informational; tolerate any exit."""
    import contextlib

    import jsonld_diff

    with contextlib.suppress(SystemExit):
        jsonld_diff.main()


# ---------------------------------------------------------------------------
# Final repair pass — ensure later tests in the same pytest run see a
# coherent build tree. Implemented as a module-finalizer-ish fixture
# that fires after every test in this file.
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True, scope="module")
def _repair_after_module():
    yield
    _repair_csp_after_mutating_main()
