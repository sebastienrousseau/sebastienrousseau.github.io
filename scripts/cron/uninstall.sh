#!/usr/bin/env bash
# Stop + remove the publish-daily LaunchAgent.
#
# Usage:
#   bash scripts/cron/uninstall.sh
#
# Doesn't touch logs at ~/Library/Logs/sebastienrousseau-publish/ —
# delete them by hand if you don't want the history.

set -euo pipefail

LABEL="com.sebastienrousseau.publish-daily"
DEST_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

if launchctl list | grep -q "$LABEL"; then
  echo "Unloading $LABEL …"
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || \
    launchctl unload "$DEST_PLIST" 2>/dev/null || true
fi

if [[ -f "$DEST_PLIST" ]]; then
  rm -f "$DEST_PLIST"
  echo "Removed $DEST_PLIST"
fi

echo "Done. Logs at ~/Library/Logs/sebastienrousseau-publish/ retained."
