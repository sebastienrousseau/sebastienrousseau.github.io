.PHONY: bootstrap build serve regenerate audit audit-external validate test-search-index test-i18n clean test lint typecheck sbom coverage publish-today verify

# Default target.
build:
	@./build.sh

# Build and serve on http://127.0.0.1:8000
serve:
	@./build.sh --serve

# Re-emit generator output (layouts, articles, projects) then rebuild.
regenerate:
	@python3 scripts/generators/gen_layouts.py
	@perl -i -pe 's|<h4>Sebastien Rousseau</h4>|<h2 class="ap-foot-title">Sebastien Rousseau</h2>|g; s|<h4>Writing</h4>|<h2 class="ap-foot-title">Writing</h2>|g; s|<h4>Work</h4>|<h2 class="ap-foot-title">Work</h2>|g; s|<h4>Reach</h4>|<h2 class="ap-foot-title">Reach</h2>|g' _layouts/*.html
	@python3 scripts/generators/gen_articles.py
	@# gen_projects + topic_link rewrite committed files in place; an
	@# intentional source regeneration passes --dir explicitly (ADR-0003).
	@python3 scripts/generators/gen_projects.py --dir _posts
	@python3 scripts/postbuild/topic_link.py --dir _posts
	@python3 scripts/generators/build_news_sitemap.py
	@./build.sh

# Link audit (internal strict; pass --external for an external pass)
audit:
	@python3 scripts/seo_and_audit/audit_links.py --base-dir public --strict-internal $(EXTRA)

audit-external:
	@python3 scripts/seo_and_audit/audit_links.py --base-dir public --check-external

# Schema.org JSON-LD validation across the built tree.
validate:
	@python3 scripts/seo_and_audit/validate_jsonld.py --base-dir public

# Search-index shape guard (EN + FR must have title/url/content/headings).
test-search-index:
	@python3 tests/validation/test_search_indexes.py

# i18n gates — language + UI-string parity, hreflang reciprocity,
# JSON-LD inLanguage match, sitemap completeness, EN-leakage,
# RTL-safety (baseline mode; --strict required before AR/HE).
test-i18n:
	@python3 tests/validation/test_i18n_parity.py
	@python3 tests/validation/test_i18n_strings.py
	@python3 tests/validation/test_hreflang_reciprocity.py
	@python3 tests/validation/test_jsonld_localized.py
	@python3 tests/validation/test_sitemap_completeness.py
	@python3 tests/validation/test_lang_no_leakage.py
	@python3 tests/validation/test_rtl_safe.py --strict

# Python test suite (scripts/ utilities).
test:
	@python3 -m pytest tests/unit/ -ra

# Static analysis (ruff, configured in pyproject.toml).
lint:
	@ruff check scripts/ tests/
	@python3 scripts/dev/check_naming_conventions.py

# Strict mypy over the strict-clean module tier (ratchets outward).
typecheck:
	@bash scripts/typecheck.sh

# Generate + validate the CycloneDX SBOM (public/sbom.cdx.json).
sbom:
	@bash scripts/security/gen-sbom.sh public/sbom.cdx.json

# Unified coverage report — runs every CLI in scripts/ under
# coverage.py, then runs the pytest suite under the same data file,
# combines, and prints per-file coverage. Requires a prior ./build.sh
# pass so public/ + docs/ are populated.
coverage:
	@./tests/validation/coverage-build.sh --with-pytest

# Pick up today's _drafts/YYYY-MM-DD-*.md, promote it, translate to
# all 27 non-EN locales (Anthropic API), regenerate listings, build,
# and stage. The cron + commit/push wrapper is in
# .github/workflows/publish-daily.yml.
publish-today:
	@chmod +x scripts/editorial/publish-daily.sh
	@./scripts/editorial/publish-daily.sh

# One-command onboarding: provision the pinned toolchain + dependencies,
# then you're ready for `make build`. Idempotent — re-running skips what is
# already installed. Versions are pinned per ADR-0002 (mise.toml is the
# canonical toolchain matrix; the dev-tool pins mirror .github/workflows/ci.yml).
bootstrap:
	@command -v mise >/dev/null 2>&1 || { echo "mise not found — install it from https://mise.jdx.dev, then re-run 'make bootstrap'"; exit 1; }
	@echo "==> mise install (python 3.12, node 22, rust, pa11y-ci, http-server)"
	@mise install
	@echo "==> ssg static-site compiler (0.0.46, pinned — ADR-0002)"
	@command -v ssg >/dev/null 2>&1 || cargo install ssg --locked --version 0.0.46
	@echo "==> python build + dev deps (hash-pinned lock — same as CI)"
	@pip install --quiet --require-hashes -r requirements-dev.lock
	@echo "==> bootstrap complete. Next: make build  (first build target: under 10 min)."

# Full repo-integrity regression suite. Runs every gate the way CI does,
# fail-fast. Cheap source checks (lint, types) run first; then `build`,
# which itself runs the 37 in-build gates (CSP, SRI, i18n parity/hreflang,
# search-index, …). The pytest suite runs AFTER build because part of it
# (test_build_output) walks the freshly-built public/ tree. Finally the
# post-build gates that need public/ (JSON-LD, internal links, SBOM).
# Green here == the same green CI enforces before deploy.
#
# Requires a bootstrapped toolchain (make bootstrap) — notably ssg 0.0.46
# (ADR-0002); ssg 0.0.45 emits a known lang-leakage false positive.
verify:
	@echo "==> [1/7] lint (ruff + naming)";         $(MAKE) --no-print-directory lint
	@echo "==> [2/7] typecheck (mypy strict tier)"; $(MAKE) --no-print-directory typecheck
	@echo "==> [3/7] build + in-build gates";        $(MAKE) --no-print-directory build
	@echo "==> [4/7] unit tests (pytest, post-build)"; $(MAKE) --no-print-directory test
	@echo "==> [5/7] JSON-LD schema validation";    $(MAKE) --no-print-directory validate
	@echo "==> [6/7] internal link audit (strict)"; $(MAKE) --no-print-directory audit
	@echo "==> [7/7] SBOM generate + validate";     $(MAKE) --no-print-directory sbom
	@echo "✓ verify: full repo integrity green"

# Wipe build output.
clean:
	@rm -rf public output output.build-tmp
