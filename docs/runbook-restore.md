<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Restore runbook

How to bring sebastienrousseau.com back from a backup, or roll back a bad
deploy (plan F-9). Last restore drill: _not yet done_ (record the date here).

## What is backed up

| What | Where | Kept |
| --- | --- | --- |
| The whole repository (every branch and tag) | `git bundle` release assets on the private repo `sebastienrousseau.github.io-backup` (`.github/workflows/backup.yml`, weekly and on every `v*` tag) | Last 12 bundles |
| Each build's `public/` | `build-output` artefact of the CI run (`ci.yml`) | 30 days |
| Each deploy | `github-pages` artefact of the CI run | 30 days |
| Each release | Signed tag, release notes, `tar.gz`/`zip` of the built site with Sigstore bundles, SBOM and `SHA256SUMS` | Permanent |
| Cloudflare rules, DNS and Worker routes | `ops/cloudflare/` (from `cf-terraforming`, no secrets) | In git |

## Roll back a bad deploy (minutes)

1. Find the last good deploy: `gh run list --workflow ci.yml --branch main --event push`.
2. Redeploy its site, unchanged and without a rebuild (about two minutes):
   `gh workflow run rollback.yml --ref main -f run-id=<run-id>`.
   It works while that run's `github-pages` artefact exists (30 days).
   Purge the Cloudflare cache for HTML.
3. main is still ahead of production: fix or revert it before merging
   anything, since the next push to main deploys main again. deploy-drift
   fails every hour until then.
4. Older than 30 days: re-run the whole run (`gh run rerun <run-id>`),
   which rebuilds that commit (about 1h40m). Or deploy a release: download
   its `sebastienrousseau.github.io-X.Y.Z.tar.gz`, check it
   (`sha256sum -c SHA256SUMS`, `cosign verify-blob --bundle ...`), and
   publish it with the `release.yml` artefacts as the Pages source.

## Rebuild from a bundle (the repository is gone)

```
gh release download <backup-tag> -R sebastienrousseau/sebastienrousseau.github.io-backup
sha256sum -c site-*.bundle.sha256
git clone site-*.bundle sebastienrousseau.github.io
cd sebastienrousseau.github.io && git remote set-url origin <new remote>
mise install        # pins ssg and Python
./build.sh          # the full build and every gate
```

Push to a new repository, enable Pages (GitHub Actions source), add the
secrets back (`INDEXNOW_KEY`, `BACKUP_TOKEN`, the Search Console key), and
point the Cloudflare DNS record at it.

## Restore Cloudflare

`ops/cloudflare/` holds the exported rulesets, DNS records and Worker
routes. `terraform init && terraform plan` against the zone shows any
drift; `terraform apply` restores them. The Worker itself deploys with
`npx wrangler deploy` from `workers/`.

## Restore drill

Once a year, and after any change to the backup workflow: clone the
newest bundle into a temporary directory, run `./build.sh`, and compare
`public/sitemap.xml` with production. Record the date at the top of this
file.
