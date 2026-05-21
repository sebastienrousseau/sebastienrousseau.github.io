#!/usr/bin/env bash
# Install the publish-daily LaunchAgent on this Mac.
#
# Usage:
#   bash scripts/cron/install.sh
#
# Idempotent: re-running is safe (it unloads + reloads). Writes the
# plist to ~/Library/LaunchAgents/, then loads it with `launchctl`.
#
# To verify the schedule fires:
#   launchctl print gui/$(id -u)/com.sebastienrousseau.publish-daily
#
# To test the wrapper without waiting for 03:00:
#   launchctl kickstart -k gui/$(id -u)/com.sebastienrousseau.publish-daily
#
# To uninstall:
#   bash scripts/cron/uninstall.sh

set -euo pipefail

LABEL="com.sebastienrousseau.publish-daily"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SRC_PLIST="$REPO/scripts/cron/$LABEL.plist"
DEST_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
WRAPPER="$REPO/scripts/cron/publish-daily.sh"

if [[ ! -f "$SRC_PLIST" ]]; then
  echo "ERROR: $SRC_PLIST not found"
  exit 1
fi

if [[ ! -f "$WRAPPER" ]]; then
  echo "ERROR: $WRAPPER not found"
  exit 1
fi

chmod +x "$WRAPPER"

mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "$HOME/Library/Logs/sebastienrousseau-publish"

# Unload any prior installation so the load below doesn't error out.
if launchctl list | grep -q "$LABEL"; then
  echo "Unloading existing $LABEL …"
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || \
    launchctl unload "$DEST_PLIST" 2>/dev/null || true
fi

cp "$SRC_PLIST" "$DEST_PLIST"
echo "Wrote $DEST_PLIST"

# Load + enable so launchd will fire at the scheduled times.
launchctl bootstrap "gui/$(id -u)" "$DEST_PLIST"
launchctl enable "gui/$(id -u)/$LABEL"

echo
echo "Installed. Status:"
launchctl print "gui/$(id -u)/$LABEL" 2>/dev/null | /usr/bin/grep -E "state|next run|last exit|program " | /usr/bin/head -10 || \
  echo "  (not yet visible — try \`launchctl list | grep $LABEL\` in a minute)"

echo
echo "Schedule: 03:00 + 04:00 local time daily (covers BST/GMT — see plist comment)"
echo "Logs:     ~/Library/Logs/sebastienrousseau-publish/<YYYY-MM-DD>.log"
echo
echo "Test fire (runs the wrapper now):"
echo "  launchctl kickstart -k gui/$(id -u)/$LABEL"
echo "  tail -f ~/Library/Logs/sebastienrousseau-publish/$(date -u +%F).log"
