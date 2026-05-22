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

# A full 28-locale publish dispatches 4 parallel translation sub-agents
# plus the main routine; observed cost is $5-10 per article. Set the
# ceiling at $15 to leave headroom; raise via `MAX_BUDGET_USD=20 …` if
# a future article needs more.
MAX_BUDGET_USD="${MAX_BUDGET_USD:-15}"

# Capture stdout so we can sentinel-check it for the budget-exceeded
# marker. tee both to the log file and to a scratch buffer we'll scan
# after the run.
CLAUDE_OUT="$(mktemp -t publish-daily-claude.XXXXXX)"
trap '/bin/rm -f "$CLAUDE_OUT"' EXIT

set +e
claude -p "/publish-today" \
    --dangerously-skip-permissions \
    --max-budget-usd "$MAX_BUDGET_USD" \
    --model opus \
    --output-format text 2>&1 | /usr/bin/tee "$CLAUDE_OUT"
rc=${PIPESTATUS[0]}
set -e

echo "publish-daily: claude exited $rc at $(ts)"

# Detect failure modes claude doesn't surface via exit code:
#   * "Exceeded USD budget" — claude prints this and exits 0, which
#     looked like success but left the routine half-finished.
#   * No "/pull/" URL in the output — the routine should always emit a
#     PR URL on the happy path; absence is a strong signal we never
#     made it that far (translation died, build failed, etc.).
budget_hit=0
if /usr/bin/grep -q "Exceeded USD budget" "$CLAUDE_OUT"; then
  budget_hit=1
fi

pr_opened=0
if /usr/bin/grep -qE "github\\.com/[^[:space:]]+/pull/[0-9]+" "$CLAUDE_OUT"; then
  pr_opened=1
fi

if [[ $rc -eq 0 && $budget_hit -eq 0 && $pr_opened -eq 1 ]]; then
  echo "publish-daily: SUCCESS — PR opened"
  /usr/bin/osascript -e "display notification \"PR opened for ${TODAY}\" with title \"publish-daily\" subtitle \"see ${LOG}\"" || true
  exit 0
fi

# Failure path: figure out which one and report.
reason="exit $rc"
if [[ $budget_hit -eq 1 ]]; then
  reason="budget cap hit (\$$MAX_BUDGET_USD) — raise MAX_BUDGET_USD"
elif [[ $rc -eq 0 && $pr_opened -eq 0 ]]; then
  reason="claude exited 0 but no PR URL in output"
fi

echo "publish-daily: FAILED — $reason"
/usr/bin/osascript -e "display notification \"FAILED — $reason — see ${LOG}\" with title \"publish-daily\" sound name \"Basso\"" || true
exit 1
