# Wiring the Cloudflare bindings — ASSETS, AE, COALESCER

The `workers/wrangler.toml` declares three bindings the
`lang-router` Worker will consume at runtime:

| Binding | Type | Required for | Set up via |
|---|---|---|---|
| `ASSETS` | Static-asset binding | Static-first storage tier (lang-registry.json, future slug maps) | wrangler deploy |
| `AE` | Analytics Engine dataset | `recordRedirect()` telemetry in the Worker | dashboard OR wrangler deploy |
| `COALESCER` | Durable Object | `WriteCoalescer` write-batching primitive (no caller yet) | dashboard OR wrangler deploy |

`lang-router.js` falls back gracefully when any of these are missing,
so partial activation is safe. But you'll want all three live before
the AE telemetry shows up in the dashboard.

Policy: `project-docs/adr/0001-kv-free-tier-policy.md`

---

## Decision: keep paste-the-code deploys, or move to `wrangler deploy`?

**The `ASSETS` binding cannot be configured via the dashboard's "paste
your code" editor.** It requires either:

- `wrangler deploy` from a checkout, OR
- a multi-file upload through the dashboard's "Upload Worker" flow.

So if you want ASSETS, you'll need to switch to `wrangler deploy` for
this Worker. The good news: routes set in the dashboard
(`sebastienrousseau.com/*`, `www.sebastienrousseau.com/*`) are NOT in
`wrangler.toml` and survive the move.

`AE` and `COALESCER` work either way — dashboard clicks or `wrangler
deploy`. Pick one and stick with it for consistency.

---

## Path A — `wrangler deploy` (recommended)

Sets up all three bindings in one command using the existing
`workers/wrangler.toml`.

### A.0 One-time: install + auth

```sh
# Wrangler ships with Node; verify
wrangler --version

# Authenticate (opens browser). Token is stored at ~/.wrangler/config/
wrangler login
```

### A.1 Build worker-assets/, then deploy

```sh
cd /Users/seb/Code/Public/HTML/sebastienrousseau.github.io
python3 scripts/build_worker_assets.py   # writes worker-assets/lang-registry.json
cd workers
wrangler deploy
```

Wrangler reads `wrangler.toml`, picks up:

- `[assets]` → uploads `../worker-assets/` as static assets, binds them to `env.ASSETS`
- `[[analytics_engine_datasets]]` → creates / wires the `sebastien_pageviews` dataset, binds it to `env.AE`
- `[[durable_objects.bindings]]` + `[[migrations]] new_sqlite_classes` → registers the `WriteCoalescer` class for the `COALESCER` binding

The first deploy may need ~30 s for the DO migration to apply. Watch
for `Successfully created durable object class WriteCoalescer`.

### A.2 Verify

```sh
# Tail the live Worker
wrangler tail --format pretty

# In another terminal, fire a redirect
curl -sI 'https://sebastienrousseau.com/?lang=fr' | head -3

# tail should show the request; AE data point appears in dashboard ~60s later
```

---

## Path B — Dashboard clicks (no wrangler)

Skip the `ASSETS` binding (incompatible with paste-the-code flow); set
up `AE` and `COALESCER` only.

### B.1 Analytics Engine — `AE`

1. Dashboard → **Workers & Pages** → click **lang-router**
2. Left sidebar → **Settings** → scroll to **Bindings**
3. **Add** → **Analytics Engine Dataset**
   - Variable name: `AE`
   - Dataset: `sebastien_pageviews`
4. **Save and deploy**

The dataset is created on first write — no separate "create dataset"
step. Data points appear in the dashboard SQL console (Analytics →
Workers Analytics → SQL) within ~60 s.

### B.2 Durable Object — `COALESCER`

A DO needs (i) the class exported by the Worker (already done in
`lang-router.js`), (ii) a migration to register the class, (iii) the
binding to expose it as `env.COALESCER`.

Through the dashboard:

1. Dashboard → **Workers & Pages** → click **lang-router**
2. **Settings** → **Bindings** → **Add** → **Durable Object**
   - Binding name: `COALESCER`
   - Class name: `WriteCoalescer`
   - Script: `lang-router` (the same Worker)
3. Dashboard → **lang-router** → **Settings** → **Migrations** →
   **Add migration**
   - Tag: `v1`
   - New SQLite class: `WriteCoalescer`
4. **Save and deploy**

After step 4 the binding is wired but unused — no caller exists in
`lang-router.js` yet. The WriteCoalescer comes online when the first
feature opts in via `env.COALESCER.idFromName('global')`.

### B.3 You skipped ASSETS — what does that cost?

Nothing today. `lang-router.js` calls `getActiveLangs(env)`, which
tries `env.ASSETS.fetch('https://assets/lang-registry.json')` first
and falls back to the hard-coded `ACTIVE_LANGS_FALLBACK` set when
the binding is missing. Both produce the same result for the 27
current locales. The static-assets pattern starts paying off when
you move slug maps, banner manifests, or any other deploy-time data
off the in-Worker constants — at which point you'll want ASSETS,
and Path A becomes the path.

---

## Path C — Hybrid (one-off upload through dashboard)

If you want `ASSETS` without committing to `wrangler deploy`:

1. Locally: `python3 scripts/build_worker_assets.py` then
   `zip -r lang-router.zip workers/lang-router.js workers/activitypub.js
   workers/mcp.js workers/pdf-proxy.js workers/security.js
   workers/write-coalescer.js worker-assets/`
2. Dashboard → **Workers & Pages** → **lang-router** → **Settings**
   → **Triggers** → there isn't a zip-upload flow for an existing
   paste-edited Worker. You'd need to delete it and recreate via
   **Create application** → **Upload an existing Worker**.

This is messier than Path A. Recommendation: do Path A.

---

## Post-setup checks (any path)

```sh
# AE redirect counter — emits a data point on a redirect path
curl -sI 'https://sebastienrousseau.com/?lang=fr' >/dev/null
sleep 60

# Verify in dashboard SQL console:
#   SELECT blob4 AS to_lang, COUNT() AS hits
#   FROM sebastien_pageviews
#   WHERE blob1 = 'redirect' AND timestamp > NOW() - INTERVAL '5' MINUTE
#   GROUP BY to_lang;

# KV burndown workflow can read the API
gh secret set CLOUDFLARE_API_TOKEN < /dev/tty   # paste the token (Account › Account Analytics › Read)
gh secret set CLOUDFLARE_ACCOUNT_ID < /dev/tty  # paste the 32-char account tag
gh workflow run kv-burndown.yml
gh run watch
```

The burndown should report **`Peak day in trailing 7 d: <date> 0`** —
zero writes, full headroom.

---

## Rollback

If anything goes sideways:

- **ASSETS**: drop the binding in Settings → Bindings. The Worker
  immediately falls back to `ACTIVE_LANGS_FALLBACK`. No data loss.
- **AE**: drop the binding. `recordRedirect()` becomes a no-op.
  Existing data points stay in the dataset (3-month retention).
- **COALESCER**: drop the binding + add a new migration with
  `deleted_classes = ["WriteCoalescer"]`. DO storage is wiped; no
  caller exists today so nothing breaks.

The Worker source code itself never needs to roll back — every
new binding is defensive-checked at runtime.
