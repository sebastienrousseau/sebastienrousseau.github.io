#!/usr/bin/env bash
# Daily-publish wrapper — fires once a day via launchd LaunchAgent
# (or cron if you prefer; see scripts/cron/README.md).
#
# Pre-flight:
#   * Verify _drafts/<today>-*.md exists; bail out cleanly if not.
#   * Switch to main + fast-forward pull.
#   * Sanity-check the claude binary is on PATH.
#
# Body:
#   * Invoke `claude -p "/publish-today"` with --dangerously-skip-permissions
#     so the publish-today slash command can promote the draft, scaffold
#     27 locale stubs, translate them via parallel sub-agents, build,
#     commit + sign, push to a fresh `content/<today>-*` branch, and
#     open the PR via `gh` — all in one non-interactive run.
#
# Post:
#   * macOS notification on success or failure.
#   * Full log at ~/Library/Logs/sebastienrousseau-publish/<YYYY-MM-DD>.log
#   * Exit code mirrors claude's; non-zero is a real failure.
#
# Idempotent: if the article is already in _posts/ (re-run after a
# partial earlier fire), the publish-today routine resumes from the
# next pending step rather than re-publishing.

set -euo pipefail
shopt -s nullglob

REPO="/Users/seb/Code/Public/HTML/sebastienrousseau.github.io"
LOG_DIR="$HOME/Library/Logs/sebastienrousseau-publish"
TODAY=$(date -u +%F)
LOG="$LOG_DIR/${TODAY}.log"

mkdir -p "$LOG_DIR"

# All output (stdout + stderr) lands in the day's log file.
exec >>"$LOG" 2>&1

ts() { /bin/date -u +'%Y-%m-%d %H:%M:%S UTC'; }
echo
echo "==================== publish-daily $(ts) ===================="

# launchd does not inherit the user's shell environment, so we rebuild
# PATH from the known mise installs + system bins. Add new entries here
# if mise installs move on this machine.
export PATH="/Users/seb/.local/share/mise/installs/npm-anthropic-ai-claude-code/latest/bin:/Users/seb/.local/share/mise/installs/python/3.12/bin:/Users/seb/.local/share/mise/installs/node/24/bin:/Users/seb/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

if [[ ! -d "$REPO" ]]; then
  echo "ERROR: repo $REPO not found"
  exit 1
fi
cd "$REPO"

DRAFT=( _drafts/${TODAY}-*.md )
EXISTING=( _posts/${TODAY}-*.md )

if [[ ${#DRAFT[@]} -eq 0 && ${#EXISTING[@]} -eq 0 ]]; then
  echo "publish-daily: no _drafts/${TODAY}-*.md and no _posts/${TODAY}-*.md — nothing to publish, exiting cleanly."
  exit 0
fi

if [[ ${#DRAFT[@]} -gt 0 ]]; then
  echo "publish-daily: draft ready — ${DRAFT[0]}"
else
  echo "publish-daily: draft already promoted earlier — ${EXISTING[0]}; resuming pipeline."
fi

echo "publish-daily: refreshing main"
git checkout main >/dev/null 2>&1
git pull --ff-only origin main >/dev/null 2>&1 || {
  echo "ERROR: git pull failed — main not fast-forwardable from origin/main"
  /usr/bin/osascript -e "display notification \"git pull failed — see ${LOG}\" with title \"publish-daily\" sound name \"Basso\"" || true
  exit 1
}

if ! command -v claude >/dev/null 2>&1; then
  echo "ERROR: claude binary not on PATH"
  /usr/bin/osascript -e "display notification \"claude binary not found — see ${LOG}\" with title \"publish-daily\" sound name \"Basso\"" || true
  exit 1
fi

echo "publish-daily: launching \`claude -p /publish-today\`"
echo "  PATH=$PATH"
echo "  claude=$(command -v claude)"
echo "  starting at $(ts)"

if claude -p "/publish-today" \
    --dangerously-skip-permissions \
    --max-budget-usd 5 \
    --model opus \
    --output-format text; then
  echo "publish-daily: claude exited 0 at $(ts)"
  /usr/bin/osascript -e "display notification \"PR opened for ${TODAY}\" with title \"publish-daily\" subtitle \"see ${LOG}\"" || true
  exit 0
fi

rc=$?
echo "publish-daily: claude exited $rc at $(ts)"
/usr/bin/osascript -e "display notification \"FAILED (exit $rc) — see ${LOG}\" with title \"publish-daily\" sound name \"Basso\"" || true
exit "$rc"
