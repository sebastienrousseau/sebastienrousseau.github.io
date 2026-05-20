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
python3 scripts/editorial/translate_post.py "$SLUG"

# 3. Refresh generators so listing pages pick up the new post.
#    gen_articles auto-discovers the latest dated post in _posts/ — no
#    manual ARTICLES[0] edit needed any more.
python3 scripts/generators/gen_layouts.py
python3 scripts/generators/gen_articles.py
python3 scripts/generators/gen_projects.py
python3 scripts/generators/gen_papers.py
python3 scripts/postbuild/topic_link.py
python3 scripts/postbuild/post_enrich.py
python3 scripts/generators/build_topics.py
python3 scripts/generators/build_lang_feeds.py
python3 scripts/generators/build_agent_api.py

# 4. Full build with all i18n + CSP gates.
./build.sh

# 5. Stage source changes — never docs/ or public/, CI rebuilds those.
git add _posts/ _data/i18n/ _drafts/ scripts/generators/gen_articles.py scripts/generators/build_topics.py 2>/dev/null || true

echo
echo "publish_daily: ready ($SLUG)"
echo
echo "Next steps (in Claude Code):"
echo "  1. List stubs still needing translation:"
echo "        python3 scripts/editorial/translate_post.py $SLUG --list-stubs"
echo "  2. For each stub Claude finds, rewrite the body in the target language"
echo "     (rules in .claude/commands/publish-today.md)"
echo "  3. Rotate the homepage card grid in _posts/index.md (drop oldest"
echo "     of 6, prepend today's). build_translations propagates per-locale."
echo "  4. If the article fits an existing TOPICS cluster, prepend its slug"
echo "     to that cluster's slugs[] in scripts/generators/build_topics.py"
echo "  5. Re-run: ./build.sh"
echo "  6. Signed commit + push (or open a PR for mobile review):"
echo "        git commit -S -m 'content($TODAY): <title> + 27 translations'"
echo "        git push"
