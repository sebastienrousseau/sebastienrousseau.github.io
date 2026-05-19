#!/usr/bin/env bash
# Daily-publish orchestrator. Looks for `_drafts/<today>-*.md`, promotes
# it to `_posts/`, regenerates listing pages, translates to every active
# non-EN locale via scripts/translate_post.py, runs the full build, and
# stages everything for commit. The cron + commit/push wrapper is in
# `.github/workflows/publish-daily.yml`.
#
# Designed to be idempotent: if today's article was already promoted in
# an earlier run, the second invocation is a no-op.
set -euo pipefail

cd "$(dirname "$0")/.."
TODAY="${PUBLISH_DATE:-$(date -u +%F)}"

# 1. Find today's draft.
DRAFT=$(find _drafts -maxdepth 1 -type f -name "${TODAY}-*.md" | head -1 || true)
if [[ -z "$DRAFT" ]]; then
  echo "publish_daily: no _drafts/${TODAY}-*.md — nothing to publish"
  exit 0
fi
SLUG=$(basename "$DRAFT" .md)
echo "publish_daily: promoting $DRAFT → _posts/$SLUG.md"

# 2. Promote draft → post.
TARGET="_posts/$SLUG.md"
if [[ -f "$TARGET" ]]; then
  echo "publish_daily: $TARGET already exists — skipping promote (re-running pipeline only)"
else
  git mv "$DRAFT" "$TARGET"
fi

# 3. Translate to every non-EN locale + update slug maps.
# scripts/translate_post.py reads ANTHROPIC_API_KEY from env. Without
# it, the script still writes stub posts + slug mappings so the build
# gates pass; the user can re-run with the key to fill in real
# translations.
python3 scripts/translate_post.py "$SLUG"

# 4. Refresh generators (article listing, projects, topics, …) so the
#    auto-emitted pages pick up the new post.
python3 scripts/gen_layouts.py
python3 scripts/gen_articles.py
python3 scripts/gen_projects.py
python3 scripts/gen_papers.py
python3 scripts/topic_link.py
python3 scripts/post_enrich.py

# 5. Full build with all i18n + CSP gates.
./build.sh

# 6. Stage everything for the commit step. The actual commit + push
# lives in the GitHub Action so it can sign with the runner key.
git add _posts/ _data/i18n/ _drafts/ scripts/gen_articles.py docs/ public/ 2>/dev/null || true
git status --short | head -20

echo "publish_daily: ready to commit ($SLUG)"
