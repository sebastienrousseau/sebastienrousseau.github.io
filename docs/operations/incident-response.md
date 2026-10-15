# Runbook — Incident response

**When:** the live site is broken or wrong in a user-visible way — pages 404
or 500, a deploy shipped a defect, content is incorrect, or a security
concern is reported.

**Priority order:** stop user harm → restore good state → find root cause →
prevent recurrence. Do the fast safe thing first; investigate after the site
is healthy.

---

## 1. Triage — what is actually broken?

```bash
# Is the origin healthy? (cache-bust to bypass Cloudflare)
curl -s -o /dev/null -w '%{http_code}\n' "https://sebastienrousseau.com/?cb=$RANDOM"
curl -s -o /dev/null -w '%{http_code}\n' "https://sebastienrousseau.com/<reported-path>/?cb=$RANDOM"

# What deployed last, and did it pass?
gh run list --branch main --workflow build-audit --limit 3 \
  --json status,conclusion,headSha,createdAt
git log --oneline -5 origin/main
```

Classify:

| Signal | Likely cause | Go to |
|---|---|---|
| Cache-busted URL good, plain URL bad | stale Cloudflare edge cache | §2 |
| Cache-busted URL also bad, last `build-audit` **failed** | deploy never updated | §3 |
| Cache-busted URL bad, last `build-audit` **success** | the deployed commit is itself bad | §4 (rollback) |
| Page exists but content is wrong | bad source merged | §4 (rollback) |

## 2. Stale edge cache (most common "it's broken" that isn't)

The origin is fine; Cloudflare is serving an old copy. Confirm with the
cache-bust test above, then purge: Cloudflare dashboard → Caching →
**Purge Everything** (maintainer action; needs Cloudflare creds). Wait for
TTL otherwise — it self-heals.

## 3. Deploy didn't run / failed

If the latest `main` `build-audit` failed, the site still serves the
*previous* good deploy (no partial deploys). So the live site is usually
*stale*, not broken. Fix the failing build:

```bash
gh run view <run-id> --log-failed | tail -40   # find the failing gate/job
```

- Flake (pa11y hang, network) → `gh run rerun <run-id> --failed`
  (see `ci-flake-triage.md`).
- Real failure → push a fix commit to `main` via a PR; it redeploys on
  merge.

## 4. The deployed commit is bad → roll back

Follow `rollback.md`: open a `git revert` PR for the bad commit, drive it
green, `gh pr merge --squash --admin`, wait for `build-audit`, verify
cache-busted, purge cache if user-visible. This is the default response to a
content or code regression that actually reached production.

## 5. Broken internal links reported live

The build gates `tests/unit/test_build_output.py::test_page_internal_links_resolve`,
so a broken internal link usually means a slug-map mismatch slipped through.
The classic case: a locale slug-map auto-translated a token (e.g. fr
`quantum`→`quantique`) so the page built at one path while the archive links
to another. Fix: force the locale slug-map entry to **identity** in
`_data/i18n/<lang>/slugs.json`, rebuild, verify, ship via PR + rollback-style
redeploy.

## 6. Security report

- **Secret exposure:** rotate the secret at its source immediately; secret
  scanning + push protection are on repo-wide (ADR-0005). Do not commit the
  rotated value.
- **Dependency/supply-chain:** the deployed SBOM (`public/sbom.cdx.json`)
  with SLSA provenance (`gh attestation verify`) identifies what shipped.
- **Never** paste credentials, tokens, or customer data into commits,
  issues, or logs while investigating.

## After the incident

- Write what happened + the fix in the PR body (and link the run).
- If it was a class of bug a gate could catch, add the gate (this is how the
  `test_schemas` label gate, the `.story-hero` pa11y `hideElements`, and the
  golden-file generator snapshots were added).

## Acceptance

Live origin healthy (cache-busted), Cloudflare cache purged if needed, root
cause recorded, and — where applicable — a regression test/gate added.
