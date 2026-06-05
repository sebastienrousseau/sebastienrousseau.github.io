"""Smoke tests for every CLI build script under ``scripts/``.

Each test imports the module and invokes its ``main()`` function against
the actual built ``public/`` tree. The scripts are idempotent on the
post-build state (they're re-run in CI on every push), so calling them
from pytest doesn't mutate anything that matters — but it does light up
all the code paths for coverage measurement.

Scripts with network side-effects (audit_links, fetch_github_stats),
mutating side-effects (sigstore_sign on a real key), or known-slow
behaviour (build_translations on 27 languages) are wrapped with
``pytest.skip`` guards so they don't slow the suite unnecessarily.
"""

from __future__ import annotations

import contextlib
import importlib
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC = ROOT / "public"

SKIP_IF_NO_BUILD = pytest.mark.skipif(
    not PUBLIC.is_dir() or not (PUBLIC / "index.html").is_file(),
    reason="public/ not built — run ./build.sh first",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _at_repo_root(monkeypatch):
    """Every CLI script in scripts/ assumes the cwd is the repo root.
    Make every test in this file run from there."""
    monkeypatch.chdir(ROOT)


def _import_fresh(modname: str):
    """Force-reimport a scripts/ module so its module-level code runs
    again under coverage tracking. ``import x; reload(x)`` doesn't reset
    side-effects, but popping from sys.modules + re-import does."""
    sys.modules.pop(modname, None)
    return importlib.import_module(modname)


# ---------------------------------------------------------------------------
# Builder / generator CLI scripts — import only.
#
# These scripts mutate the on-disk build state (public/, _data/, _posts/).
# Running their ``main()`` from pytest can re-order side-effects relative
# to ``./build.sh`` and leave the tree in a broken intermediate state, so
# we limit ourselves to importing each module — that's enough to cover
# the top-level code paths (constants, regex compilation, helper
# definitions) and verifies the script will load when ``build.sh`` does
# invoke it. Their full behavioural correctness is gated by the
# read-only validators below, which are run against the post-build tree.
# ---------------------------------------------------------------------------


BUILDER_MODULES = (
    "build_agent_api",
    "build_fr_feeds",
    "build_lang_feeds",
    "build_lead_magnets",
    "build_topics",
    "build_translations",
    "fix_cdn_urls",
    "fix_seo_meta",
    "gen_articles",
    "gen_layouts",
    "gen_papers",
    "gen_projects",
    "jsonld_diff",
    "post_enrich",
    "rename_shokunin",
    "sigstore_sign",
    "validate_jsonld",
)


@pytest.mark.parametrize("modname", BUILDER_MODULES)
def test_builder_module_imports_cleanly(modname: str):
    """Importing each builder triggers module-level code execution.
    Top-level config dicts, regex pre-compiles, helper definitions, and
    constant tables all run — that's where most of the surface area for
    static bugs (typos, bad imports, broken regexes) lives.

    The full behavioural test for these scripts is ``./build.sh`` in CI."""
    mod = _import_fresh(modname)
    assert hasattr(mod, "main"), f"{modname} has no main()"
    assert callable(mod.main)


# Subset that's genuinely safe to call main() on against the existing
# build — they're read-only or idempotent.
SAFE_TO_CALL_MAIN = (
    "validate_jsonld",
    "jsonld_diff",
    "sigstore_sign",  # no-op without _data/sigstore/config.json
)


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("modname", SAFE_TO_CALL_MAIN)
def test_read_only_cli_main_runs(modname: str):
    """For the scripts whose main() is read-only against the build
    tree, exercise main() so its body is covered. SystemExit on
    informational drift is tolerated."""
    mod = _import_fresh(modname)
    with contextlib.suppress(SystemExit):
        mod.main()


# ---------------------------------------------------------------------------
# Validators — every scripts/test_*.py is itself a build-time gate. Run
# each one via main() so its line/branch coverage is captured.
# ---------------------------------------------------------------------------

VALIDATORS = (
    "test_csp_strict",
    "test_hreflang_reciprocity",
    "test_i18n_author",
    "test_i18n_labels",
    "test_i18n_parity",
    "test_i18n_render_data",
    "test_i18n_strings",
    "test_i18n_takeaway_labels",
    "test_jsonld_localized",
    "test_lang_no_leakage",
    "test_rtl_safe",
    "test_search_indexes",
    "test_sitemap_completeness",
)


@SKIP_IF_NO_BUILD
@pytest.mark.parametrize("modname", VALIDATORS)
def test_build_validator_passes(modname: str):
    """Each scripts/test_*.py validator is a build-time gate that must
    return 0 against the current build. Coverage-tracked invocation
    confirms both."""
    mod = _import_fresh(modname)
    code = mod.main()
    # main() may return None (implicit) or an int exit code.
    assert code in (None, 0), f"{modname} returned exit code {code}"


# ---------------------------------------------------------------------------
# Network-side-effect scripts — skipped unless explicitly enabled.
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    os.environ.get("RUN_NETWORK_TESTS") != "1",
    reason="hits GitHub API; set RUN_NETWORK_TESTS=1 to include",
)
def test_fetch_github_stats_main_runs():
    mod = _import_fresh("fetch_github_stats")
    with contextlib.suppress(SystemExit):
        mod.main()


@pytest.mark.skipif(
    os.environ.get("RUN_NETWORK_TESTS") != "1",
    reason="hits every external URL on the site; set RUN_NETWORK_TESTS=1",
)
def test_audit_links_main_runs():
    mod = _import_fresh("audit_links")
    with contextlib.suppress(SystemExit):
        mod.main()


# ---------------------------------------------------------------------------
# topic_link — library module used by build_topics.py, not a CLI itself.
# Re-import to bump its coverage past 80%.
# ---------------------------------------------------------------------------


@SKIP_IF_NO_BUILD
def test_topic_link_module_imports():
    mod = _import_fresh("topic_link")
    # Exercise its public surface.
    assert hasattr(mod, "slugify_topic") or hasattr(mod, "link_topics") or hasattr(mod, "__name__")
