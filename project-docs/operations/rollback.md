# Runbook — Rollback

**When:** a change merged to `main` shipped a regression (broken page, bad
content, failing gate that slipped through, wrong asset) and you need the
live site back to a known-good state.

**Who deploys:** `main`'s `build-audit` workflow builds `public/` fresh and
deploys it via `actions/deploy-pages`. There is no separate deploy step —
**whatever is on `main` is what deploys.** So rollback = get `main` back to
good, then let CI redeploy.

---

## 1. Decide: revert vs roll-forward

- **Revert** when the bad commit is isolated and recent. Fastest, safest.
- **Roll-forward** (a new fix commit) when the bad change is entangled with
  good changes you want to keep, or a revert would itself break something.

Never `push --force` to `main` (branch protection blocks it, and it rewrites
history other branches depend on).

## 2. Revert the bad merge

Find the merge/squash commit:

```bash
git log --oneline -10 origin/main
```

Open a revert PR (do **not** commit straight to `main`):

```bash
git checkout main && git pull
git checkout -b revert/<short-desc>
git revert --no-edit <bad-sha>        # squash-merges are single commits → clean revert
git push -u origin revert/<short-desc>
gh pr create --title "revert: <what> (<bad-sha>)" --base main --fill
```

Drive CI green (see `ci-flake-triage.md` if a check flakes), then:

```bash
gh pr merge <num> --squash --admin --delete-branch
```

`--admin` is required: branch protection asks for a review the solo
maintainer cannot self-approve. Only use it on a green PR.

## 3. Confirm the redeploy

`main`'s `build-audit` runs on the revert commit (~35–45 min incl. pa11y).
Wait for success:

```bash
gh run list --branch main --workflow build-audit --limit 1 \
  --json status,conclusion,headSha
```

Then verify the live origin (cache-busted, since Cloudflare may still serve
the bad version from edge cache):

```bash
curl -s -o /dev/null -w '%{http_code}\n' "https://sebastienrousseau.com/<path>/?cb=$RANDOM"
```

## 4. Clear the Cloudflare edge cache (if users still see the bad version)

The origin updates as soon as `build-audit` deploys, but Cloudflare can keep
serving a cached copy until its TTL expires. A cache-busted URL (`?cb=…`)
returning the good version while a plain URL returns the old one is the
signature of a stale edge cache, **not** a failed rollback.

This needs Cloudflare credentials and is a maintainer action: Cloudflare
dashboard → Caching → Configuration → **Purge Everything** (or purge the
specific URLs). Claude/CI cannot and should not do this automatically.

## 5. If the bad change was a data/asset, not code

- **Stale `_data/gh-stats.json` / `metrics.json`:** the nightly
  `refresh-gh-stats` cron and per-build `fetch_metrics` self-heal; force a
  refresh by re-running the workflow or pushing a trivial commit.
- **Bad CDN image:** assets live on `cloudcdn.pro`, not in this repo. Fix at
  the CDN; the repo only references URLs.

## Acceptance

`build-audit` green on the revert commit, live origin (cache-busted) serves
the good version, and — if it was user-visible — the Cloudflare cache has
been purged.
