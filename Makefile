.PHONY: build serve regenerate audit clean

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

# Wipe build output.
clean:
	@rm -rf public output output.build-tmp
