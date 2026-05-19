#!/usr/bin/env bash
# Re-run the full Python half of build.sh under coverage.py instrumentation
# and emit a combined coverage report covering every CLI in scripts/.
#
# `./build.sh` invokes 20 distinct Python scripts; each runs as its own
# process, so coverage data files have to accumulate via --append and
# then be combined. The data file is written next to the source tree.
#
# This script assumes ./build.sh has already produced public/ at least
# once — the per-script CLIs that mutate public/ need a starting tree.
# Run order matches build.sh so the data lands consistently.
#
# Usage:
#   ./scripts/coverage_build.sh            # run all steps under coverage
#   ./scripts/coverage_build.sh --report   # combine + print report only
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Coverage config — collect from scripts/ only, parallel mode so each
# child process writes its own data file (combined at the end).
cat > .coveragerc <<'COVERC'
[run]
source = scripts
omit =
    scripts/__pycache__/*
    scripts/postbuild_lib/__pycache__/*
parallel = True

[report]
show_missing = True
skip_empty = True

[paths]
source =
    scripts
    */scripts
COVERC

if [[ "${1:-}" == "--report" ]]; then
  python3 -m coverage combine 2>&1 | tail -1 || true
  python3 -m coverage report
  exit
fi

# --with-pytest: also run the pytest suite under coverage and combine
# its data with the build-script data. Produces the unified per-line
# coverage picture across everything in scripts/.
WITH_PYTEST=0
if [[ "${1:-}" == "--with-pytest" ]]; then
  WITH_PYTEST=1
fi

# Wipe stale data from previous runs.
rm -f .coverage .coverage.*

# Each CLI gets one --append'd coverage data file. Failures don't stop
# the run — we want the report to include partial data for diagnosis.
run() {
  echo "coverage[$1]:"
  python3 -m coverage run --rcfile=.coveragerc "$@" 2>&1 | tail -3 || true
}

run scripts/build_topics.py
run scripts/build_translations.py
run scripts/build_lang_feeds.py
run scripts/build_agent_api.py
run scripts/build_lead_magnets.py
run scripts/postbuild.py
run scripts/sigstore_sign.py
run scripts/test_search_indexes.py
run scripts/test_i18n_parity.py
run scripts/test_i18n_strings.py
run scripts/test_i18n_labels.py
run scripts/test_i18n_takeaway_labels.py
run scripts/test_i18n_render_data.py
run scripts/test_i18n_author.py
run scripts/test_hreflang_reciprocity.py
run scripts/test_jsonld_localized.py
run scripts/test_sitemap_completeness.py
run scripts/test_lang_no_leakage.py
run scripts/test_rtl_safe.py --strict
run scripts/test_csp_strict.py

# Also exercise the import-side of the validators that ./build.sh doesn't
# call directly — these are referenced by tests/ or by ad-hoc tooling.
run scripts/validate_jsonld.py || true
run scripts/jsonld_diff.py || true
run scripts/audit_links.py --no-network || true
run scripts/fix_cdn_urls.py || true
run scripts/fix_seo_meta.py || true
run scripts/gen_articles.py || true
run scripts/gen_layouts.py || true
run scripts/gen_papers.py || true
run scripts/gen_projects.py || true
run scripts/post_enrich.py || true
run scripts/rename_shokunin.py || true
run scripts/topic_link.py || true

echo "---"
if [[ "$WITH_PYTEST" == "1" ]]; then
  echo "pytest (under coverage):"
  python3 -m coverage run --rcfile=.coveragerc -m pytest tests/ -q 2>&1 | tail -3 || true
fi
python3 -m coverage combine 2>&1 | tail -3
python3 -m coverage report
