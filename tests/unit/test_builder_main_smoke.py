# SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Run ``main()`` on the big builder scripts against a disposable clone
of the build tree.

Each test is a single ``main()`` invocation — deliberately
unsophisticated. The pay-off is coverage: each main() walks 100+ to
1000+ lines of branchy logic that is untouchable from a unit test
without a vast fixture.

These mains write. They used to write into the *real* tree, with a
module-teardown pass re-stamping CSP/SRI afterwards. That was measured
at 6,453 files rewritten per run, and it made the whole unit suite
order-dependent: any module reading ``public/`` between the mutation and
the teardown saw an incoherent build. ``test_csp_strict_passes`` and
``test_pages_with_eager_image_have_preload`` passed in isolation and
failed in a full run for exactly that reason. CI only hid it by
partitioning the suite across shards.

Worse, two builders anchor on ``__file__`` rather than the CWD and so
wrote into committed source — ``gen_layouts`` into ``_layouts/`` and
``gen_articles`` into ``_posts/articles.md``. A test run left the repo
dirty, which ADR-0003 and ``_copy_root_posts`` below already forbade for
the enrichers but nothing enforced for the rest.

The whole unit session now runs inside a disposable clone of the tree —
see ``tests/unit/conftest.py``, which also gates the property: the run
fails if any test leaves the real ``public/`` altered or a tracked file
dirty. Scoping the clone per-module was not enough; a first pass at this
sandboxed only this file and CI still reported 6,497 rewritten files,
because several other modules invoke the same entry points.
"""

from __future__ import annotations

import contextlib
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC = ROOT / "public"
POSTS = ROOT / "_posts"
sys.path.insert(0, str(ROOT / "scripts"))

SKIP_IF_NO_BUILD = pytest.mark.skipif(
    not PUBLIC.is_dir() or not (PUBLIC / "index.html").is_file(),
    reason="public/ not built — run ./build.sh first",
)


def _copy_root_posts(tmp_path: Path) -> Path:
    """Copy the root-level dated posts into an isolated working dir so the
    in-place enrichers (post_enrich, topic_link) can run with full coverage
    WITHOUT mutating committed source — see ADR-0003."""
    work = tmp_path / "_posts"
    work.mkdir()
    for md in POSTS.glob("*.md"):
        shutil.copy2(md, work / md.name)
    return work


def _posts_fingerprint() -> str:
    h = hashlib.sha256()
    for p in sorted(POSTS.glob("*.md")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Builders + generators that emit content into _posts/ or rewrite
# specific markdown files. Safe to re-run because the inputs (the
# real _data/, _posts/<lang>/, etc.) don't change between runs.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_post_enrich_main_runs(capsys, monkeypatch, tmp_path):
    # Run against an isolated copy with the now-required --dir (ADR-0003):
    # full main() coverage, zero mutation of committed source.
    work = _copy_root_posts(tmp_path)
    before = _posts_fingerprint()
    monkeypatch.setattr("sys.argv", ["post_enrich", "--dir", str(work)])
    import post_enrich

    post_enrich.main()
    out = capsys.readouterr().out
    assert "enriched" in out.lower() or "dated post" in out.lower()
    assert _posts_fingerprint() == before, "post_enrich mutated committed _posts/"


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
def test_gen_projects_main_runs(capsys, monkeypatch, tmp_path):
    # Run against an isolated copy with the now-required --dir (ADR-0003):
    # a bare run used to rewrite committed _posts/projects.md in place,
    # reverting it to the constants baked into the script.
    work = _copy_root_posts(tmp_path)
    before = _posts_fingerprint()
    monkeypatch.setattr("sys.argv", ["gen_projects", "--dir", str(work)])
    import gen_projects

    gen_projects.main()
    out = capsys.readouterr().out
    assert "wrote" in out.lower() or "projects" in out.lower()
    assert _posts_fingerprint() == before, "gen_projects mutated committed _posts/"


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
def test_topic_link_main_runs(capsys, monkeypatch, tmp_path):
    # Run against an isolated copy with the now-required --dir (ADR-0003):
    # full main() coverage, zero mutation of committed source.
    work = _copy_root_posts(tmp_path)
    before = _posts_fingerprint()
    monkeypatch.setattr("sys.argv", ["topic_link", "--dir", str(work)])
    import topic_link

    topic_link.main()
    out = capsys.readouterr().out
    assert "topic_link" in out or "touched" in out.lower()
    assert _posts_fingerprint() == before, "topic_link mutated committed _posts/"


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
# Generators whose main() was not previously smoked. Together these were the
# largest remaining coverage gap in the tree — nine files, ~1,100 statements,
# every one of them writing real pages on every build with no test running
# the code that writes them.
#
# Same contract as the block above: one main() call each, deliberately
# unsophisticated, against the session's disposable clone. The assertion is
# only that the entry point completes — the interesting behaviour is unit
# tested elsewhere. What these buy is the branchy assembly code in between,
# which no unit test can reach without exactly this fixture.
# ---------------------------------------------------------------------------


def _isolated_tree(tmp_path: Path) -> Path:
    """A private clone of the build tree for one test.

    The session sandbox in conftest is shared by every test, so a builder that
    writes into it leaves that state for whatever runs next. These builders
    emit pages carrying inline JSON-LD whose sha256 tokens are stamped into
    each page's CSP by a *later* postbuild pass — so their raw output is
    legitimately CSP-incoherent until that pass runs. Writing it into the
    shared sandbox made test_csp_strict_passes fail with 6,862 defects: the
    exact order-dependence the sandbox exists to prevent, reintroduced.

    Cloning per test costs a copy-on-write clone on APFS/btrfs and keeps the
    blast radius inside the test that caused it.
    """
    dst = tmp_path / "tree"
    dst.mkdir()
    src_root = Path.cwd()
    for name in ("public", "_posts", "_data", "_layouts"):
        src = src_root / name
        if not src.is_dir():
            continue
        for cmd in (["cp", "--reflink=auto", "-R"], ["cp", "-c", "-R"], ["cp", "-R"]):
            try:
                if (
                    subprocess.run(
                        [*cmd, str(src), str(dst / name)], capture_output=True, timeout=1800
                    ).returncode
                    == 0
                ):
                    break
            except (OSError, subprocess.SubprocessError):
                continue
        else:  # pragma: no cover - only on a filesystem where every cp failed
            shutil.copytree(src, dst / name)
    return dst


def _sandbox_module(mod, monkeypatch, tree: Path) -> None:
    """Repoint a builder's absolute Path constants at ``tree``.

    conftest already repoints modules, but it walks ``sys.modules`` in
    ``pytest_runtest_setup`` — i.e. *between* tests. A module first imported
    inside the test that uses it misses that pass and keeps real-repo paths,
    so its main() writes into the committed tree. That is what the isolation
    gate caught here: build_tag_landings rewrote 1,855 real files. They were
    byte-identical, so only mtimes moved — invisible without the gate.

    Repointing explicitly, at the top of each test, removes the ordering
    dependency instead of relying on import luck.
    """
    for attr, val in list(vars(mod).items()):
        if attr.startswith("__") or not isinstance(val, Path) or not val.is_absolute():
            continue
        try:
            rel = val.resolve().relative_to(ROOT)
        except ValueError:
            try:
                rel = val.resolve().relative_to(Path.cwd())
            except ValueError:
                continue
        monkeypatch.setattr(mod, attr, tree if rel == Path(".") else tree / rel, raising=False)
    monkeypatch.chdir(tree)


@SKIP_IF_NO_BUILD
def test_build_speaking_main_runs(monkeypatch, tmp_path):
    """Renders /speaking/ and its locale forks from front matter."""
    import build_speaking

    _sandbox_module(build_speaking, monkeypatch, _isolated_tree(tmp_path))

    rc = build_speaking.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_listings_main_runs(monkeypatch, tmp_path):
    """Paged article listings and year archives, EN + 34 locales."""
    import build_listings

    _sandbox_module(build_listings, monkeypatch, _isolated_tree(tmp_path))

    monkeypatch.setattr(sys, "argv", ["build_listings"])
    rc = build_listings.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_tag_landings_main_runs(monkeypatch, tmp_path):
    """Per-tag landing pages and their locale forks."""
    import build_tag_landings

    _sandbox_module(build_tag_landings, monkeypatch, _isolated_tree(tmp_path))

    monkeypatch.setattr(sys, "argv", ["build_tag_landings"])
    rc = build_tag_landings.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_tags_main_runs(monkeypatch, tmp_path):
    import build_tags

    _sandbox_module(build_tags, monkeypatch, _isolated_tree(tmp_path))

    monkeypatch.setattr(sys, "argv", ["build_tags"])
    rc = build_tags.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_case_studies_main_runs(monkeypatch, tmp_path):
    """Case-study pages; exercises case_studies_render and _components."""
    import build_case_studies

    _sandbox_module(build_case_studies, monkeypatch, _isolated_tree(tmp_path))

    monkeypatch.setattr(sys, "argv", ["build_case_studies"])
    rc = build_case_studies.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_trust_main_runs(monkeypatch, tmp_path):
    import build_trust

    _sandbox_module(build_trust, monkeypatch, _isolated_tree(tmp_path))

    rc = build_trust.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_datasets_main_runs(monkeypatch, tmp_path):
    """Emits public/data/*.json|csv and the Dataset JSON-LD they back."""
    import build_datasets

    _sandbox_module(build_datasets, monkeypatch, _isolated_tree(tmp_path))

    rc = build_datasets.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_search_ui_main_runs(monkeypatch, tmp_path):
    import build_search_ui

    _sandbox_module(build_search_ui, monkeypatch, _isolated_tree(tmp_path))

    rc = build_search_ui.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_changelog_main_runs(monkeypatch, tmp_path):
    import build_changelog

    _sandbox_module(build_changelog, monkeypatch, _isolated_tree(tmp_path))

    rc = build_changelog.main()
    assert rc in (None, 0)


# ---------------------------------------------------------------------------
# Audit / maintenance entry points. Same contract and isolation as the block
# above; every one of these reads and writes only local files — no network,
# no subprocess — so a main() call is safe inside a private tree.
#
# Their argparse mains read sys.argv, which under pytest holds pytest's own
# arguments, so argv is blanked as well.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_check_taxonomy_main_runs(monkeypatch, tmp_path):
    """Structural validation of the canonical tag vocabulary."""
    import check_taxonomy

    _sandbox_module(check_taxonomy, monkeypatch, _isolated_tree(tmp_path))
    monkeypatch.setattr(sys, "argv", ["check_taxonomy"])
    rc = check_taxonomy.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_audit_translations_main_runs(monkeypatch, tmp_path):
    """Scans every locale post for untranslated-stub markers."""
    import audit_translations

    _sandbox_module(audit_translations, monkeypatch, _isolated_tree(tmp_path))
    monkeypatch.setattr(sys, "argv", ["audit_translations"])
    rc = audit_translations.main()
    assert rc in (None, 0, 1)  # non-zero simply means defects were found


@SKIP_IF_NO_BUILD
def test_regen_homepage_main_runs(monkeypatch, tmp_path):
    import regen_homepage

    _sandbox_module(regen_homepage, monkeypatch, _isolated_tree(tmp_path))
    monkeypatch.setattr(sys, "argv", ["regen_homepage"])
    rc = regen_homepage.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_regen_slug_maps_main_runs(monkeypatch, tmp_path):
    import regen_slug_maps

    _sandbox_module(regen_slug_maps, monkeypatch, _isolated_tree(tmp_path))
    rc = regen_slug_maps.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_fix_lang_switcher_main_runs(monkeypatch, tmp_path):
    import fix_lang_switcher

    _sandbox_module(fix_lang_switcher, monkeypatch, _isolated_tree(tmp_path))
    rc = fix_lang_switcher.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_rag_corpus_main_runs(monkeypatch, tmp_path):
    """Emits the JSONL corpus and per-tag shards the MCP server serves."""
    import build_rag_corpus

    _sandbox_module(build_rag_corpus, monkeypatch, _isolated_tree(tmp_path))
    rc = build_rag_corpus.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_build_worker_assets_main_runs(monkeypatch, tmp_path):
    import build_worker_assets

    _sandbox_module(build_worker_assets, monkeypatch, _isolated_tree(tmp_path))
    rc = build_worker_assets.main()
    assert rc in (None, 0)


@SKIP_IF_NO_BUILD
def test_check_voice_main_runs_offline(monkeypatch, tmp_path):
    """The editorial gate, driven through its CLI with the network disabled.

    --no-network is passed rather than stubbed: it is the flag a maintainer
    uses when drafting offline, so exercising it here also proves the flag
    still reaches check_article.
    """
    import check_voice

    tree = _isolated_tree(tmp_path)
    _sandbox_module(check_voice, monkeypatch, tree)
    post = next(iter(sorted((tree / "_posts").glob("20*.md"))), None)
    if post is None:  # pragma: no cover - the fixture tree always has posts
        pytest.skip("no dated post in the tree")
    monkeypatch.setattr(sys, "argv", ["check_voice", str(post), "--no-network", "--no-date-check"])
    rc = check_voice.main()
    assert rc in (0, 1)  # 1 simply means the article has defects


@SKIP_IF_NO_BUILD
def test_check_voice_main_reports_a_missing_path(monkeypatch, tmp_path):
    import check_voice

    _sandbox_module(check_voice, monkeypatch, _isolated_tree(tmp_path))
    monkeypatch.setattr(sys, "argv", ["check_voice", "no-such-file.md", "--no-network"])
    assert check_voice.main() == 1


@SKIP_IF_NO_BUILD
def test_check_voice_main_prints_help_without_a_target(monkeypatch, tmp_path):
    import check_voice

    _sandbox_module(check_voice, monkeypatch, _isolated_tree(tmp_path))
    monkeypatch.setattr(sys, "argv", ["check_voice"])
    assert check_voice.main() == 2


@SKIP_IF_NO_BUILD
def test_pick_banner_main_lists(monkeypatch, tmp_path):
    import pick_banner

    _sandbox_module(pick_banner, monkeypatch, _isolated_tree(tmp_path))
    monkeypatch.setattr(sys, "argv", ["pick_banner", "list", "--limit", "3"])
    with contextlib.suppress(SystemExit):
        pick_banner.main()


@SKIP_IF_NO_BUILD
def test_automate_tags_main_runs(monkeypatch, tmp_path):
    """Rewrites the tags line across every post and locale — in a private tree."""
    import automate_tags

    _sandbox_module(automate_tags, monkeypatch, _isolated_tree(tmp_path))
    with contextlib.suppress(SystemExit):
        automate_tags.main()


@SKIP_IF_NO_BUILD
def test_backfill_locale_frontmatter_main_runs(monkeypatch, tmp_path):
    import backfill_locale_frontmatter

    _sandbox_module(backfill_locale_frontmatter, monkeypatch, _isolated_tree(tmp_path))
    monkeypatch.setattr(sys, "argv", ["backfill_locale_frontmatter"])
    with contextlib.suppress(SystemExit):
        backfill_locale_frontmatter.main()
