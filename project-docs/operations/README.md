# Operations runbooks

Short, do-this-now guides for running sebastienrousseau.com. Each is written
to be followed under pressure: triage first, restore the site, investigate
after.

| Runbook | Use when |
|---|---|
| [publishing.md](../publishing.md) · [daily-publishing.md](../daily-publishing.md) | Publishing an article + its 27 translations |
| [rollback.md](rollback.md) | A bad change reached `main`/production and must be reverted |
| [ci-flake-triage.md](ci-flake-triage.md) | A CI check is red and you suspect infrastructure, not your change |
| [incident-response.md](incident-response.md) | The live site is broken or wrong, or a security issue is reported |
| [cloudflare-bindings-setup.md](cloudflare-bindings-setup.md) · [cloudflare-queries.md](cloudflare-queries.md) | Cloudflare edge configuration and queries |

**Two facts that underpin all of these:**

1. **`main` is the deploy.** `build-audit` builds `public/` fresh from `main`
   and deploys it; there is no separate deploy step. Restoring the site means
   getting `main` good and letting CI redeploy.
2. **Cloudflare caches the edge.** The origin updates the moment `build-audit`
   deploys, but users may see a stale copy until the cache TTL expires or it
   is purged. A cache-busted URL (`?cb=$RANDOM`) returning the right thing
   while a plain URL does not is a *cache* issue, not a deploy failure.
