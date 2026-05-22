# Local daily-publish automation

> **Status (2026-05-22): currently inactive.** Sebastien now invokes `/publish-today` **manually each evening** so he can review the night's output before merging in the morning. The LaunchAgent below is no longer loaded. This folder is kept as a documented fallback — re-run `bash scripts/cron/install.sh` to switch automation back on. See `.claude/commands/publish-today.md` for the manual flow.

Fires `/publish-today` once a day from your Mac via a launchd `LaunchAgent`. No cloud, no Claude Code web — the job runs as your user, with your git credentials, your GPG signing key, and your `gh` token, so commits get signed and PRs get opened automatically.

## Why local, not cloud

The Anthropic cloud routine has worked sporadically because the cloud container's GitHub proxy token is read-only — `git push` and the GitHub MCP write tools have all returned `403 Resource not accessible by integration` at some point. Running the routine on your Mac sidesteps that: you already have authenticated `git` + `gh` + GPG on this machine.

## What it does

The wrapper at `scripts/cron/publish-daily.sh`:

1. Checks for `_drafts/<today>-*.md`. If neither a draft nor an already-promoted `_posts/<today>-*.md` exists, exits 0 cleanly (no-op for days where you haven't dropped a draft).
2. Fast-forward-pulls `main`.
3. Invokes `claude -p "/publish-today" --dangerously-skip-permissions --max-budget-usd 5 --model opus`. That single command runs the full slash-command pipeline: promote draft → voice gate → scaffold 27 locales → parallel-agent translate → regenerate listings → rotate homepage cards → build → commit (signed) → push → open PR via `gh`.
4. Posts a macOS notification on success or failure.
5. Logs everything to `~/Library/Logs/sebastienrousseau-publish/<YYYY-MM-DD>.log`.

## Install

```bash
bash scripts/cron/install.sh
```

That:

- Copies the plist to `~/Library/LaunchAgents/com.sebastienrousseau.publish-daily.plist`.
- Loads + enables it with `launchctl bootstrap`.
- Creates `~/Library/Logs/sebastienrousseau-publish/` for the daily logs.

## Schedule

launchd fires the LaunchAgent at **03:00 AND 04:00 local time** daily.

That dual-fire is deliberate: launchd uses local time, not UTC, so a single Hour=3 entry drifts an hour twice a year as the UK switches between BST and GMT.

- **GMT (winter)**: 03:00 local = 03:00 UTC → first fire publishes; 04:00 fire is a no-op (script bails out, article already in `_posts/`).
- **BST (summer)**: 03:00 local = 02:00 UTC → first fire is a no-op (no draft yet at 02:00 UTC, but harmless even if there is one); 04:00 local = 03:00 UTC → second fire publishes.

Net effect: **the publish lands at 03:00 UTC reliably year-round**, regardless of BST/GMT.

### Alternative: cron with strict UTC

If you'd rather one fire at exactly 03:00 UTC every day, edit your user crontab:

```bash
crontab -e
```

and add:

```
0 3 * * * TZ=UTC /Users/seb/Code/Public/HTML/sebastienrousseau.github.io/scripts/cron/publish-daily.sh
```

cron honours the `TZ=` env, so this fires exactly at 03:00 UTC. Then disable the LaunchAgent: `bash scripts/cron/uninstall.sh`.

The trade-off: macOS cron now requires Full Disk Access for the `cron` process on Sonoma+, which is annoying. LaunchAgent is the recommended path.

## Test / verify

Status check:

```bash
launchctl print gui/$(id -u)/com.sebastienrousseau.publish-daily | head -30
```

You should see `state = waiting` and a `next run` timestamp.

Test-fire the wrapper now (without waiting until 03:00):

```bash
launchctl kickstart -k gui/$(id -u)/com.sebastienrousseau.publish-daily
tail -f ~/Library/Logs/sebastienrousseau-publish/$(date -u +%F).log
```

If there's no draft for today, the wrapper exits cleanly with `publish-daily: no _drafts/...md and no _posts/...md — nothing to publish, exiting cleanly.` That's a healthy idle.

## Uninstall

```bash
bash scripts/cron/uninstall.sh
```

Logs are retained — delete `~/Library/Logs/sebastienrousseau-publish/` by hand if you want them gone.

## What can break (and how to debug)

| Symptom | Likely cause | Fix |
|---|---|---|
| Logfile shows `claude binary not on PATH` | mise reshimmed; the hardcoded path in `publish-daily.sh` drifted | Update the `export PATH=` line in `publish-daily.sh` to reflect the new mise install path |
| Logfile shows `git pull failed` | Local `main` has uncommitted changes or unpushed commits | Resolve the local state; the daily job won't publish on top of a dirty tree |
| Notification fires but no PR opened | claude inside the routine hit an error mid-pipeline (translation gate, build failure, etc.) | Read `~/Library/Logs/sebastienrousseau-publish/<today>.log` — every step writes a line |
| `launchctl list | grep publish-daily` returns nothing | LaunchAgent loaded under the wrong user session, or `bootstrap` was rejected because the plist was already loaded | Run `bash scripts/cron/install.sh` again; it unloads first |
| `claude` consumed lots of credits | Translation step ran (~$5–10 per full 28-locale article is normal) | Default ceiling is `$15` (set via `MAX_BUDGET_USD` env var in `publish-daily.sh`). Tighten or loosen by exporting `MAX_BUDGET_USD=N` in the LaunchAgent's `EnvironmentVariables` block. |
| Notification says "FAILED — budget cap hit" | claude printed "Exceeded USD budget" mid-run and stopped translating | Bump `MAX_BUDGET_USD` and re-fire with `launchctl kickstart -k gui/$(id -u)/com.sebastienrousseau.publish-daily` |
| Notification says "FAILED — claude exited 0 but no PR URL" | Routine got far enough to exit cleanly but never opened the PR (translation gate, build failure, gh push issue, …) | Read the log file for the specific step that failed |

## Files in this folder

- `publish-daily.sh` — the wrapper that launchd invokes
- `com.sebastienrousseau.publish-daily.plist` — LaunchAgent definition
- `install.sh` — one-shot installer
- `uninstall.sh` — stop + remove
- `README.md` — this file
