.DEFAULT_GOAL := help
.PHONY: help bootstrap build demo serve theme-sync regenerate audit audit-external validate test-search-index test-i18n clean test lint typecheck sbom coverage publish-today verify verify-versions

# Single source of truth for the ssg pin, parsed straight out of the CI
# workflow so `make bootstrap` can never install a version CI would reject.
# It drifted before: this Makefile installed 0.0.46 while CI built with
# 0.0.39 and the README documented a third value. ADR-0002.
# tests/unit/test_ssg_pin_single_source.py fails the build on any conflict.
SSG_VERSION := $(shell sed -n 's/^[[:space:]]*SSG_VERSION:[[:space:]]*"\([^"]*\)".*/\1/p' .github/workflows/ci.yml | head -1)

# Display available commands.
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Default build target.
build: ## Build the static site to public/ across all locales
	@./build.sh

# Render README animated demo (.github/demo.gif) from visual baselines.
demo: ## Generate .github/demo.gif from visual baselines
	@mkdir -p .build/demo .github
	@ffmpeg -loglevel error -y -i .github/ci-tools/visual/baseline/home.png -vf "crop=1440:900:0:0" .build/demo/1.png
	@ffmpeg -loglevel error -y -i .github/ci-tools/visual/baseline/papers.png -vf "crop=1440:900:0:0" .build/demo/2.png
	@ffmpeg -loglevel error -y -i .github/ci-tools/visual/baseline/docs.png -vf "crop=1440:900:0:0" .build/demo/3.png
	@ffmpeg -loglevel error -y -i .github/ci-tools/visual/baseline/trust.png -vf "crop=1440:900:0:0" .build/demo/4.png
	@ffmpeg -loglevel error -y -framerate 1/3 -i .build/demo/%d.png \
	  -vf "scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a" \
	  -loop 0 .github/demo.gif
	@rm -rf .build/demo
	@echo "demo: wrote .github/demo.gif"

# Build and serve on http://127.0.0.1:8000
serve: ## Build and serve public/ on http://127.0.0.1:8000
	@./build.sh --serve

# Refresh _layouts/ from the theme (ADR-0014). THEME_DIR points at a checkout
# of ssg-themes.github.io; the flattened files are committed here so a build
# never needs that checkout.
THEME_DIR ?= ../ssg-themes.github.io/themes/sebastienrousseau
theme-sync: ## Synchronize _layouts/ from theme repository
	@test -d "$(THEME_DIR)/_layouts" || { echo "theme not found at $(THEME_DIR) (set THEME_DIR)"; exit 1; }
	@python3 "$(THEME_DIR)/tools/flatten.py" --site "$(THEME_DIR)/_layouts" _layouts
	@git --no-pager diff --stat -- _layouts

# Re-emit generator output (layouts, articles, projects) then rebuild.
# gen_layouts.py is superseded by `make theme-sync` (ADR-0014).
regenerate: ## Re-generate layouts, articles, and sitemaps
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
audit: ## Run strict internal link audit
	@python3 scripts/seo_and_audit/audit_links.py --base-dir public --strict-internal $(EXTRA)

audit-external: ## Run external link audit
	@python3 scripts/seo_and_audit/audit_links.py --base-dir public --check-external

# Schema.org JSON-LD validation across the built tree.
validate: ## Validate Schema.org JSON-LD structured data
	@python3 scripts/seo_and_audit/validate_jsonld.py --base-dir public

# Search-index shape guard (EN + FR must have title/url/content/headings).
test-search-index: ## Verify search index consistency across locales
	@python3 tests/validation/test_search_indexes.py

# i18n gates: language + UI-string parity, hreflang reciprocity,
# JSON-LD inLanguage match, sitemap completeness, EN-leakage,
# RTL-safety (baseline mode; --strict required before AR/HE).
test-i18n: ## Run internationalization and locale parity suite
	@python3 tests/validation/test_i18n_parity.py
	@python3 tests/validation/test_i18n_strings.py
	@python3 tests/validation/test_hreflang_reciprocity.py
	@python3 tests/validation/test_jsonld_localized.py
	@python3 tests/validation/test_sitemap_completeness.py
	@python3 tests/validation/test_i18n_playlists.py
	@python3 tests/validation/test_i18n_listings.py
	@python3 tests/validation/test_i18n_projects.py
	@python3 tests/validation/test_i18n_speaking.py
	@python3 tests/validation/test_i18n_cross_locale_script.py --strict
	@python3 tests/validation/test_lang_no_leakage.py
	@python3 tests/validation/test_body_translation.py --strict
	@python3 tests/validation/test_rtl_safe.py --strict
	@python3 tests/validation/test_slug_policy.py

# Python test suite (scripts/ utilities).
test: ## Run Python unit test suite
	@python3 -m pytest tests/unit/ -ra

# Static analysis (ruff, configured in pyproject.toml).
lint: ## Run ruff, naming conventions, and complexity gates
	@ruff check scripts/ tests/
# CI's Static analysis job gates formatting separately from linting, so a
# ruff-check-clean branch could still fail there - which is what happened to
# PR #455 after local verification passed. Same check, same scope as CI.
	@ruff format --check scripts/ tests/
	@python3 scripts/dev/check_naming_conventions.py
	@bash scripts/dev/check-complexity.sh

# Strict mypy over the strict-clean module tier (ratchets outward).
typecheck: ## Run strict mypy type check
	@bash scripts/typecheck.sh

# Generate + validate the CycloneDX SBOM (public/sbom.cdx.json).
sbom: ## Generate and validate CycloneDX SBOM
	@bash scripts/security/gen-sbom.sh public/sbom.cdx.json

# Unified coverage report: runs every CLI in scripts/ under
# coverage.py, then runs the pytest suite under the same data file,
# combines, and prints per-file coverage. Requires a prior ./build.sh
# pass so public/ + docs/ are populated.
coverage: ## Run unified test and CLI coverage report
	@./tests/validation/coverage-build.sh --with-pytest

# Pick up today's _drafts/YYYY-MM-DD-*.md, promote it, translate to
# all 27 non-EN locales (Anthropic API), regenerate listings, build,
# and stage. The cron + commit/push wrapper is in
# .github/workflows/publish-daily.yml.
publish-today: ## Promote and publish today's draft post
	@chmod +x scripts/editorial/publish-daily.sh
	@./scripts/editorial/publish-daily.sh

# One-command onboarding: provision the pinned toolchain + dependencies,
# then you're ready for `make build`. Idempotent - re-running skips what is
# already installed. Versions are pinned per ADR-0002 (mise.toml is the
# canonical toolchain matrix; the dev-tool pins mirror .github/workflows/ci.yml).
bootstrap: ## Provision pinned toolchain and dependencies via mise
	@command -v mise >/dev/null 2>&1 || { echo "mise not found - install it from https://mise.jdx.dev, then re-run 'make bootstrap'"; exit 1; }
	@echo "==> mise install (python 3.12, node 22, rust, pa11y-ci, http-server)"
	@mise install
	@echo "==> ssg static-site compiler ($(SSG_VERSION) - ADR-0002)"
	@# `command -v ssg` is not a version check: a stale binary already on PATH
	@# satisfies it and the pin never applies. Compare the running version,
	@# reinstall on mismatch, then assert - same contract as ci.yml.
	@have=$$(ssg --version 2>/dev/null | awk '{print $$2}' || true); \
	 if [ "$(SSG_VERSION)" = "latest" ]; then \
	   want=$$(cargo search ssg --limit 1 | sed -n 's/^ssg = "\([^"]*\)".*/\1/p'); \
	 else want="$(SSG_VERSION)"; fi; \
	 if [ "$$have" != "$$want" ]; then \
	   echo "    ssg: have '$${have:-none}', want $$want - installing"; \
	   cargo install ssg --locked --version $$want --force; \
	 fi; \
	 got=$$(ssg --version | awk '{print $$2}'); \
	 [ "$$got" = "$$want" ] || { echo "ssg $$got running but $$want requested"; exit 1; }
	@echo "==> python build + dev deps (hash-pinned lock - same as CI)"
	@pip install --quiet --require-hashes -r requirements-dev.lock
	@echo "==> bootstrap complete. Next: make build  (first build target: under 10 min)."

verify-versions: ## Verify consistency across release version references
	@scripts/security/verify-release-versions.sh

# Full repo-integrity regression suite. Runs every gate the way CI does,
# fail-fast. Cheap source checks (lint, types, versions) run first; then `build`,
# which itself runs the 37 in-build gates (CSP, SRI, i18n parity/hreflang,
# search-index, ...). The pytest suite runs AFTER build because part of it
# (test_build_output) walks the freshly-built public/ tree. Finally the
# post-build gates that need public/ (JSON-LD, internal links, SBOM).
# Green here == the same green CI enforces before deploy.
#
# Requires a bootstrapped toolchain (make bootstrap) - notably the pinned
# ssg (ADR-0002); ssg 0.0.45 emits a known lang-leakage false positive.
verify: ## Full repo-integrity regression gate (mirrors CI)
	@echo "==> [1/8] version consistency";        $(MAKE) --no-print-directory verify-versions
	@echo "==> [2/8] lint (ruff + naming)";         $(MAKE) --no-print-directory lint
	@echo "==> [3/8] typecheck (mypy strict tier)"; $(MAKE) --no-print-directory typecheck
	@echo "==> [4/8] build + in-build gates";        $(MAKE) --no-print-directory build
	@echo "==> [5/8] unit tests (pytest, post-build)"; $(MAKE) --no-print-directory test
	@echo "==> [6/8] JSON-LD schema validation";    $(MAKE) --no-print-directory validate
	@echo "==> [7/8] internal link audit (strict)"; $(MAKE) --no-print-directory audit
	@echo "==> [8/8] SBOM generate + validate";     $(MAKE) --no-print-directory sbom
	@echo "✓ verify: full repo integrity green"

# Wipe build output and temporary caches.
clean: ## Clean build artifacts and temporary files
	@rm -rf public output output.build-tmp public.build-tmp _posts_build/ .pytest_cache/ .ruff_cache/
