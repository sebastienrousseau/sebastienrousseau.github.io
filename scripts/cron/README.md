<h1 align="center">Local daily-publish automation</h1>

<p align="center">
  Promotes the day's draft, translates 27 locales, and opens a PR — run
  locally each evening so the output is reviewed before it ships.
</p>

---

## Contents

- [Why local, not cloud](#why-local-not-cloud) — secrets + signing stay on-device
- [What it does](#what-it-does) — the publish steps
- [Install](#install) — register the scheduler
- [Schedule](#schedule) — when it runs
- [Cron alternative](#cron-alternative) — fixed-time UTC
- [Test / verify](#test--verify)
- [Uninstall](#uninstall)
- [Troubleshooting](#troubleshooting)
- [Layout](#layout)
- [License](#license)

## Why local, not cloud

Publishing runs locally to keep API secrets off shared infrastructure. The runner uses your GPG key to sign commits and push.

## What it does

Pulls the latest `main`, promotes today's draft, runs the translation pipeline, runs the test gates, and opens a pull request.

## Install

```bash
./scripts/cron/install.sh   # registers the launchd plist + log path
```

## Schedule

Runs each morning so posts land at peak publishing time.

## Cron alternative

Prefer a fixed UTC time? Edit your user crontab. Note macOS needs Full Disk Access for `cron`, so the launchd plist is the recommended path.

## Test / verify

```bash
./scripts/cron/publish-daily.sh   # exits cleanly with no changes if there is no draft
```

Logs are written to the registered log folder.

## Uninstall

```bash
./scripts/cron/uninstall.sh   # unloads the service + removes the plist
```

Delete the log files manually if desired.

## Troubleshooting

Common failures: wrong paths, a blocked Git push, budget caps, or signing errors. Check the run log to see which step failed.

## Layout

The launchd plist, the install/uninstall scripts, the runner, and this guide.

## License

Licensed under [Apache-2.0](../../LICENSE).

<p align="right"><a href="#local-daily-publish-automation">Back to Top</a></p>
