.PHONY: build serve regenerate audit clean test lint coverage

# Default target.
build:
	@./build.sh

# Build and serve on http://127.0.0.1:8000
serve:
	@./build.sh --serve

# Re-emit generator output (layouts, articles, projects) then rebuild.
regenerate:
	@python3 scripts/gen_layouts.py
	@perl -i -pe 's|<h4>Sebastien Rousseau</h4>|<h2 class="ap-foot-title">Sebastien Rousseau</h2>|g; s|<h4>Writing</h4>|<h2 class="ap-foot-title">Writing</h2>|g; s|<h4>Work</h4>|<h2 class="ap-foot-title">Work</h2>|g; s|<h4>Reach</h4>|<h2 class="ap-foot-title">Reach</h2>|g' _layouts/*.html
	@python3 scripts/gen_articles.py
	@python3 scripts/gen_projects.py
	@python3 scripts/topic_link.py
	@python3 scripts/post_enrich.py
	@./build.sh

# Link audit (internal strict; pass --external for an external pass)
audit:
	@python3 scripts/audit_links.py --base-dir public --strict-internal $(EXTRA)

audit-external:
	@python3 scripts/audit_links.py --base-dir public --check-external

# Schema.org JSON-LD validation across the built tree.
validate:
	@python3 scripts/validate_jsonld.py --base-dir public

# Search-index shape guard (EN + FR must have title/url/content/headings).
test-search-index:
	@python3 scripts/test_search_indexes.py

# i18n gates — language + UI-string parity, hreflang reciprocity,
# JSON-LD inLanguage match, sitemap completeness, EN-leakage,
# RTL-safety (baseline mode; --strict required before AR/HE).
test-i18n:
	@python3 scripts/test_i18n_parity.py
	@python3 scripts/test_i18n_strings.py
	@python3 scripts/test_hreflang_reciprocity.py
	@python3 scripts/test_jsonld_localized.py
	@python3 scripts/test_sitemap_completeness.py
	@python3 scripts/test_lang_no_leakage.py
	@python3 scripts/test_rtl_safe.py --strict

# Python test suite (scripts/ utilities).
test:
	@python3 -m pytest tests/ -ra

# Static analysis (ruff, configured in pyproject.toml).
lint:
	@ruff check scripts/ tests/

# Unified coverage report — runs every CLI in scripts/ under
# coverage.py, then runs the pytest suite under the same data file,
# combines, and prints per-file coverage. Requires a prior ./build.sh
# pass so public/ + docs/ are populated.
coverage:
	@./scripts/coverage_build.sh --with-pytest

# Wipe build output.
clean:
	@rm -rf public output output.build-tmp
