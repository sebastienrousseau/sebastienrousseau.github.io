#!/usr/bin/env bash
# Daily-publish orchestrator (local-only, no cloud API keys).
#
# The flow:
#   1. Find _drafts/<today>-*.md, git mv it to _posts/.
#   2. Scaffold 27 locale stubs + slug-map entries.
#   3. Refresh every gen_*.py listing.
#   4. Full ./build.sh — all i18n + CSP gates pass against stubs.
#   5. STOP. The actual translation work is done IN Claude Code by
#      reading each stub and rewriting its body in-conversation, using
#      your existing Claude subscription. The slash command at
#      .claude/commands/publish-today.md walks you through it.
#
# No ANTHROPIC_API_KEY anywhere. No cloud cron. No CI translation.
# Translation = a human-in-the-loop step in your Claude Code session.
set -euo pipefail

cd "$(dirname "$0")/.."
TODAY="${PUBLISH_DATE:-$(date -u +%F)}"

# 1. Find today's draft.
DRAFT=$(find _drafts -maxdepth 1 -type f -name "${TODAY}-*.md" | head -1 || true)
if [[ -z "$DRAFT" ]]; then
  # If the draft was already promoted earlier today, jump straight
  # to the scaffold + build step against the existing _posts entry.
  EXISTING=$(find _posts -maxdepth 1 -type f -name "${TODAY}-*.md" | head -1 || true)
  if [[ -z "$EXISTING" ]]; then
    echo "publish_daily: no _drafts/${TODAY}-*.md and no _posts/${TODAY}-*.md — nothing to publish"
    exit 0
  fi
  SLUG=$(basename "$EXISTING" .md)
  echo "publish_daily: draft already promoted, re-running pipeline for $SLUG"
else
  SLUG=$(basename "$DRAFT" .md)
  echo "publish_daily: promoting $DRAFT → _posts/$SLUG.md"
  git mv "$DRAFT" "_posts/$SLUG.md"
fi

# 2. Scaffold 27 locale stubs + slug-map. Idempotent — re-running
#    leaves real translations (those without the stub marker) alone.
python3 scripts/translate_post.py "$SLUG"

# 3. Refresh generators so listing pages pick up the new post.
python3 scripts/gen_layouts.py
python3 scripts/gen_articles.py
python3 scripts/gen_projects.py
python3 scripts/gen_papers.py
python3 scripts/topic_link.py
python3 scripts/post_enrich.py

# 4. Full build with all i18n + CSP gates.
./build.sh

# 5. Stage the changes — actual commit + push happens in Claude Code
#    so it can be signed with your local SSH key.
git add _posts/ _data/i18n/ _drafts/ scripts/gen_articles.py docs/ public/ 2>/dev/null || true

echo
echo "publish_daily: ready ($SLUG)"
echo
echo "Next steps (in Claude Code):"
echo "  1. Edit _posts/index.md → add new newsroom-card at the top"
echo "     (mirror the existing card structure; drop the bottom one)"
echo "  2. Edit scripts/gen_articles.py → prepend ARTICLES[0] tuple"
echo "  3. Re-run: python3 scripts/gen_articles.py && ./build.sh"
echo "  4. List stubs still needing translation:"
echo "        python3 scripts/translate_post.py $SLUG --list-stubs"
echo "  5. For each stub Claude finds, rewrite the body in the target language"
echo "     (rules in .claude/commands/publish-today.md)"
echo "  6. Signed commit + push:"
echo "        git commit -S -m 'content($TODAY): <title> + 27 translations'"
echo "        git push"
