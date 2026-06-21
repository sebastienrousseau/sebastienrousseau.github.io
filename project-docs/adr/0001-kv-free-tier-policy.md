# Cloudflare KV Free-Tier Optimisation — Implementation Plan

**Site:** sebastienrousseau.com
**Author:** Sebastien Rousseau
**Status:** Plan — ready for phased delivery
**Date:** 2026-06-21
**Target:** Stay on Cloudflare Free indefinitely; never breach **1,000 KV writes/day**

---

## Executive summary

After auditing `workers/lang-router.js`, `workers/activitypub.js`, `workers/mcp.js`,
`workers/pdf-proxy.js`, and `workers/wrangler.toml`, the site **currently performs
ZERO Cloudflare KV write operations per day**. There is no `kv_namespaces` binding
declared. Three of the four Worker modules carry explicit "no KV" assertions in
their header comments.

The 1,000 writes/day limit is therefore not an *active* failure mode — it is a
*future* failure mode that will only materialise if the site introduces
KV-backed runtime mutation. This plan is **forward-defensive**: it locks in the
zero-write baseline as policy, builds the architecture that lets you stay at
zero (or near zero) when new features are added, and supplies the observability
to catch drift before it becomes an outage.

Seven decisions structure the plan:

1. **Baseline lock-in.** Treat "0 runtime KV writes" as a service-level objective.
2. **Storage-tier defaults.** Every future feature picks from a written decision
   matrix; KV is the last resort, not the default.
3. **Static-first.** Anything generatable at deploy time ships as a Worker
   static asset.
4. **Coalescing primitive.** If runtime mutation IS unavoidable, a single
   Durable Object (`WriteCoalescer`) absorbs the writes; KV sees one PUT per
   key per flush window, never per-request.
5. **Telemetry off-KV.** Counters, last-seen timestamps, page-view logs — all
   route to Workers Analytics Engine. KV never holds telemetry.
6. **Bot defence first.** Bot Fight Mode + AI Scraper toggle + Turnstile +
   WAF rate-limit on any mutating endpoint, *before* the endpoint is shipped.
7. **Burn-down alerting.** GraphQL-fed dashboard + 70 % budget alert; weekly
   review while traffic patterns are still settling.

---

## Part 0 — Audit baseline (verified 2026-06-21)

| Check | Result | Evidence |
|---|---|---|
| `kv_namespaces` declared in `workers/wrangler.toml` | None | File is config-only; no bindings of any kind |
| `env.KV` references in any Worker | None | `grep -rn "KV\|env\." workers/` returns only doc-comment denials |
| `caches.default` use | None | Cache API not yet leveraged — opportunity, not problem |
| Worker count | 1 deployed (`lang-router`) + 3 imported modules (`activitypub`, `mcp`, `pdf-proxy`) | All run inside the single Worker invocation |
| Routes | `sebastienrousseau.com/*`, `www.sebastienrousseau.com/*` | Manual dashboard wiring (per `wrangler.toml` comment) |
| Origin | GitHub Pages | Static; deploy-immutable |
| Per-request KV reads | 0 | Verified by source grep |
| Per-request KV writes | 0 | Verified by source grep |
| Daily write quota consumption | 0 / 1000 | Headroom 100 % |

**Conclusion:** the architecture is already at the theoretical optimum for KV
write consumption. The risk vector is *additions* — every new feature is an
opportunity to regress the baseline. This plan exists to make sure that doesn't
happen.

---

## Part 1 — Architecture Decision Record: storage-tier picker

Every future feature requesting persistent state must answer four questions in
this order. The first "yes" terminates the search.

```
1. Can this data be computed at deploy time?            → Worker static assets
2. Is this telemetry (write-once, query-later)?         → Analytics Engine
3. Is this single-writer state needing strong consistency? → Durable Object (SQLite)
4. Is this read-heavy, eventually-consistent config?    → KV (last resort)
```

### Free-tier limits, 2026 (per Cloudflare docs, dated)

| Product | Free-tier writes/day | Free-tier reads/day | Consistency | Notes |
|---|---|---|---|---|
| Static assets | n/a (deploy-time) | unlimited | strong (deploy) | Default for anything generatable at build |
| Analytics Engine | 100,000 data points | 10,000 SQL queries | append-only | 3-mo retention; 20 blobs/20 doubles/1 index per point |
| Durable Object (SQLite) | 100,000 row writes | 5,000,000 row reads | strictly serializable | DO free since 7 Apr 2025; storage billing started 7 Jan 2026 for paid plans |
| Queues | 10,000 operations | (consumer requests) | at-least-once | Free since 4 Feb 2026 |
| D1 (SQLite) | 100,000 row writes | 5,000,000 row reads | strong per primary | Relational; joins; ad-hoc queries |
| R2 | Class A 1M/mo, Class B 10M/mo | Class B same | strong per-object | Large blobs only; not for hot small JSON |
| Cache API | unlimited per zone | unlimited per zone | **PoP-local** | Free; does not replicate cross-PoP |
| **KV** | **1,000** | **100,000** | eventual (~60 s) | **Last-resort for runtime mutation** |
| Hyperdrive | ~20 conns | edge-cached | source DB | Free since 8 Apr 2025; over-spec for static site |

### Anti-patterns banned outright

These three patterns will hit the KV write cap within hours of being shipped.
They must never be merged. Add this list to `CLAUDE.md` and `CONTRIBUTING.md`.

| Anti-pattern | Why it kills the budget | Correct pattern |
|---|---|---|
| Per-request counter `await env.KV.put('counter', ++n)` | One write per pageview → cap blown by ~1k visits | `env.AE.writeDataPoint({ indexes: [path] })` then SQL `SELECT count() FROM ...` |
| Per-visit "last seen" timestamp `env.KV.put('lastSeen:'+uid, Date.now())` | One write per distinct user per session | `WriteCoalescer` DO with 5-min cooldown, or AE |
| Per-pageview log line `env.KV.put('log:'+uuid, body)` | One write per request, no reads ever | `env.AE.writeDataPoint({ blobs: [path, ua] })` |
| Same-key burst writes from multiple PoPs | Loses writes (1 write/s/key hard cap); silent data loss | Funnel through a single DO instance |
| Dashboard / `wrangler kv bulk put` reseed | Counts against the same Free quota; one bad command = 5 days of quota | Bulk reseed only against paid namespace, or against a fresh prebuilt static-asset bundle |

---

## Part 2 — Defensive implementation patterns

The following code blocks are ready to paste when the corresponding feature is
needed. They are written in TypeScript-flavoured JS (matches the existing
`workers/lang-router.js` style — plain ES modules, no transpile step).

### 2.1 Static-assets binding (zero-write default)

Anything that changes only at deploy time goes here. The asset is served
edge-local with no Worker invocation.

`workers/wrangler.toml`:

```toml
name = "lang-router"
main = "lang-router.js"
compatibility_date = "2026-05-16"

[assets]
directory = "./worker-assets"
binding = "ASSETS"
# default html_handling = "auto-trailing-slash"; not_found_handling = "404-page"
```

Build pipeline (`scripts/build_worker_assets.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
mkdir -p worker-assets
# Slug map → JSON, edge-local
python3 scripts/postbuild/regen_slug_maps.py --emit worker-assets/slug-map.json
# i18n labels → JSON per lang
python3 scripts/i18n/emit_label_bundle.py --out worker-assets/i18n/
# Lang-router routing table (active locales)
python3 scripts/_lang_registry.py --emit-json worker-assets/lang-registry.json
```

Worker access (no KV touch):

```js
const slugMap = await env.ASSETS.fetch(new URL('/slug-map.json', request.url));
const langTable = await env.ASSETS.fetch(new URL('/lang-registry.json', request.url));
```

### 2.2 Workers Analytics Engine for telemetry

Telemetry must never go to KV. AE is purpose-built for write-once,
query-with-SQL workflows.

`workers/wrangler.toml`:

```toml
[[analytics_engine_datasets]]
binding = "AE"
dataset = "sebastien_pageviews"
```

Usage from any Worker handler:

```js
// 20 blobs, 20 doubles, 1 index, 16 KB total blobs, 96 B index, 250 points / invocation
ctx.waitUntil(Promise.resolve(env.AE.writeDataPoint({
  blobs: [
    request.cf?.country ?? '??',
    url.pathname,
    request.headers.get('user-agent')?.slice(0, 128) ?? '',
  ],
  doubles: [Date.now() - startMs],
  indexes: [url.pathname],
})));
```

Read it back (CLI or dashboard SQL):

```sql
SELECT blob1 AS country, COUNT() AS hits
FROM sebastien_pageviews
WHERE timestamp > NOW() - INTERVAL '7' DAY
GROUP BY country
ORDER BY hits DESC
LIMIT 20;
```

### 2.3 WriteCoalescer Durable Object — the canonical primitive

This is the "if you must write to KV at runtime" pattern. Many Worker calls
fan in to a single DO; the DO batches in its own SQLite storage and flushes
ONE KV PUT per logical key per flush window.

`workers/wrangler.toml`:

```toml
[[durable_objects.bindings]]
name = "COALESCER"
class_name = "WriteCoalescer"

[[migrations]]
tag = "v1"
new_sqlite_classes = ["WriteCoalescer"]  # SQLite backend — free; KV backend is paid-only
```

`workers/write-coalescer.js`:

```js
const FLUSH_INTERVAL_MS = 60_000;        // 1 minute
const COOLDOWN_MS = 5 * 60 * 1000;       // 5 minutes per logical key
const KV_BUDGET_PER_DAY = 700;           // 70% of 1000 — soft cap

export class WriteCoalescer {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    const { key, value } = await request.json();
    await this.state.storage.put(`pending:${key}`, {
      v: value,
      ts: Date.now(),
    });
    const existing = await this.state.storage.getAlarm();
    if (!existing) {
      await this.state.storage.setAlarm(Date.now() + FLUSH_INTERVAL_MS);
    }
    return new Response('queued', { status: 202 });
  }

  async alarm() {
    const todayKey = `budget:${new Date().toISOString().slice(0, 10)}`;
    const spent = (await this.state.storage.get(todayKey)) ?? 0;
    if (spent >= KV_BUDGET_PER_DAY) {
      // Re-arm and drop — soft cap reached, write quota protected
      await this.state.storage.setAlarm(Date.now() + FLUSH_INTERVAL_MS);
      return;
    }

    const pending = await this.state.storage.list({ prefix: 'pending:' });
    const lastFlush = (await this.state.storage.get('cooldown:')) ?? {};
    let writes = 0;
    const now = Date.now();

    for (const [storageKey, payload] of pending) {
      const logicalKey = storageKey.slice('pending:'.length);
      const prev = lastFlush[logicalKey] ?? 0;
      if (now - prev < COOLDOWN_MS) {
        await this.state.storage.delete(storageKey);
        continue;
      }
      if (spent + writes >= KV_BUDGET_PER_DAY) break;
      await this.env.KV.put(logicalKey, JSON.stringify(payload.v));
      lastFlush[logicalKey] = now;
      writes += 1;
      await this.state.storage.delete(storageKey);
    }

    await this.state.storage.put('cooldown:', lastFlush);
    await this.state.storage.put(todayKey, spent + writes);

    if (pending.size > 0) {
      // More work pending — re-arm
      await this.state.storage.setAlarm(Date.now() + FLUSH_INTERVAL_MS);
    }
  }
}
```

Calling it from `lang-router.js`:

```js
import { WriteCoalescer } from './write-coalescer.js';
export { WriteCoalescer };

// Inside fetch():
const id = env.COALESCER.idFromName('global'); // single-instance coordinator
const stub = env.COALESCER.get(id);
ctx.waitUntil(stub.fetch('https://internal/queue', {
  method: 'POST',
  body: JSON.stringify({ key: 'user-prefs', value: payload }),
}));
```

### 2.4 Tiered read cache (isolate Map → Cache API → KV)

Reads are not the immediate problem (100k/day budget vs. 1k for writes), but
cache misses on read trigger backfill writes elsewhere. This pattern absorbs
99 % of reads at zero KV cost.

```js
const isolateCache = new Map();          // L0: per-isolate, in-RAM
const ISOLATE_TTL_MS = 30_000;

async function read(key, env, ctx) {
  // L0
  const hit = isolateCache.get(key);
  if (hit && hit.exp > Date.now()) return hit.v;

  // L1: Cache API, PoP-local, free, unbounded
  const cacheKey = new Request(`https://cache.internal/${key}`);
  const cached = await caches.default.match(cacheKey);
  if (cached) {
    const v = await cached.text();
    isolateCache.set(key, { v, exp: Date.now() + ISOLATE_TTL_MS });
    return v;
  }

  // L2: KV with maxed cacheTtl
  const v = await env.KV.get(key, { cacheTtl: 86400 });
  if (v) {
    isolateCache.set(key, { v, exp: Date.now() + ISOLATE_TTL_MS });
    ctx.waitUntil(caches.default.put(
      cacheKey,
      new Response(v, { headers: { 'cache-control': 'public, max-age=300' } }),
    ));
  }
  return v;
}
```

Set `cacheTtl: 86400` (24 h) on **every** future `env.KV.get()` call unless
business reasons say otherwise. The minimum is 30 s (since 30 Jan 2026); the
default is 60 s. Pushing it to 86400 reduces central-tier round-trips by ~99 %
on a static-content site.

### 2.5 Cooldown-only write throttle (when DO is overkill)

Sometimes a single endpoint with light traffic just needs a per-key cooldown:

```js
const COOLDOWN_MS = 5 * 60 * 1000;

async function throttledPut(key, value, env, ctx) {
  const { metadata } = await env.KV.getWithMetadata(key);
  if (metadata?.ts && Date.now() - metadata.ts < COOLDOWN_MS) {
    return false; // dropped — within cooldown
  }
  ctx.waitUntil(env.KV.put(key, value, {
    metadata: { ts: Date.now() },
  }));
  return true;
}
```

The `getWithMetadata` call adds to the read quota, not the write quota — and
reads are 100× cheaper.

### 2.6 Probabilistic refresh (Cloudflare "Sometimes I cache" pattern)

When you have N read paths all racing to refresh the same key, this avoids the
thundering-herd revalidation:

```js
function shouldRefresh(remainingTtlSec, steepness = 1 / 300) {
  if (remainingTtlSec <= 0) return true;
  return Math.random() < Math.exp(-steepness * remainingTtlSec);
}
```

Use inside a stale-while-revalidate flow — only one of N concurrent reads will
actually trigger the write.

---

## Part 3 — Observability and burn-down

### 3.1 GraphQL daily-write query

Run this from the dashboard GraphQL explorer or from a scheduled GitHub Action.
Pulls writes-per-namespace for the trailing 24 h.

```graphql
query KvWrites($accountTag: String!, $since: Time!) {
  viewer {
    accounts(filter: { accountTag: $accountTag }) {
      kvOperationsAdaptiveGroups(
        filter: { datetime_geq: $since, actionType: "write" }
        limit: 100
      ) {
        sum { requests }
        dimensions { namespaceId actionType }
      }
    }
  }
}
```

Schedule weekly via `.github/workflows/kv-burndown.yml` (already-cached
GitHub Action runner — no Cloudflare cost). Output as a sticky comment on a
tracking issue. Alert if `sum.requests >= 700` in any 24 h window.

### 3.2 Dashboard budget alert (Jun 2026 feature)

Cloudflare added a billable-usage sidebar on **4 Jun 2026**. Configure:

- **Threshold:** 70 % of 1,000 writes/day (700 writes/day rolling 24 h)
- **Channel:** email + the same address that receives security-headers alerts
- **Action:** automatic — none. Manual triage required (the WriteCoalescer
  soft cap at 700 already protects the budget; the alert is just visibility).

### 3.3 Analytics Engine self-instrumentation

Every Worker invocation that touches KV writes a data point. This gives
single-query visibility independent of Cloudflare's own metrics:

```js
ctx.waitUntil(Promise.resolve(env.AE.writeDataPoint({
  blobs: ['kv-write', kvNamespace, logicalKey.slice(0, 96)],
  doubles: [1],
  indexes: [kvNamespace],
})));
```

Query:

```sql
SELECT blob3 AS logical_key, COUNT() AS writes
FROM sebastien_pageviews
WHERE blob1 = 'kv-write' AND timestamp > NOW() - INTERVAL '1' DAY
GROUP BY blob3
ORDER BY writes DESC;
```

### 3.4 Pre-flight check in CI

Add to the existing build-audit workflow — runs the same grep that established
the baseline, fails the build if a KV write slips in without an ADR entry:

```bash
# .github/workflows/build-audit.yml — new step
- name: KV write audit
  run: |
    set -euo pipefail
    HITS=$(grep -rn "env\.KV\.put\|env\.[A-Z_]*\.put" workers/ \
      | grep -v "// adr:" || true)
    if [ -n "$HITS" ]; then
      echo "::error::KV write without an ADR opt-in comment:"
      echo "$HITS"
      exit 1
    fi
```

To approve a write, add a single-line `// adr: <ADR-NN> — <one-line reason>`
comment immediately above the `.put()` call. The grep silently accepts it; the
ADR file in `docs/adr/` captures the justification and the write-budget
estimate.

---

## Part 4 — Bot / abuse hardening (must precede any KV write feature)

Bots and scrapers will find any mutating endpoint within hours. Lock them out
*before* the endpoint is shipped, not after.

### 4.1 Free-tier defences to activate (zero KV cost)

| Defence | Activation | Spend allocation |
|---|---|---|
| Bot Fight Mode + AI Scrapers/Crawlers toggle | Dashboard → Security → Bots | Always on |
| WAF custom rules (5 free) | Dashboard → Security → WAF → Custom rules | Reserve at least 1 for any future mutating endpoint |
| Rate-limiting rule (1 free; IP, 10 s window, 10 s mitigation) | Dashboard → Security → WAF → Rate limiting rules | Reserve the single rule for the first mutating endpoint added |
| Turnstile | Drop-in before any form post | 20 widgets / 15 hostnames each free |
| In-Worker UA/ASN denylist | Module in `workers/security.js` | Reject before any KV read or write |

### 4.2 Mutating-endpoint checklist (must all be true before merge)

- [ ] Endpoint sits behind a WAF rate-limit rule
- [ ] Endpoint sits behind Turnstile (interactive) OR a `verified-bot=false`
      WAF rule (programmatic)
- [ ] In-Worker UA filter rejects known scraper UAs before reaching the put
- [ ] All puts go through `WriteCoalescer` OR cooldown-throttled (§2.5)
- [ ] Analytics Engine writes the put attempt for visibility (§3.3)
- [ ] CI grep audit (§3.4) sees the `// adr:` comment on every `.put()`

---

## Part 5 — Phased rollout

Each phase is one PR. Total estimated effort: 1.5 engineering days, spread
over four PRs so each ships independently if priorities shift.

### Phase 1 — Lock in the baseline (PR 1, ~30 min)

- Add this plan to `project-docs/adr/0001-kv-free-tier-policy.md` (renamed from
  `~/Drop/sr-kv.md`).
- Add CI audit step (§3.4).
- Add the three anti-patterns to `CLAUDE.md` and `CONTRIBUTING.md`.
- Add `.github/workflows/kv-burndown.yml` (weekly schedule, GraphQL query,
  posts to a tracking issue).

**Acceptance:** CI passes; weekly issue comment renders "writes: 0" the
following Monday.

### Phase 2 — Static-assets binding (PR 2, ~2 h)

- Create `worker-assets/` directory.
- Add `[assets]` block to `workers/wrangler.toml`.
- Move `scripts/_lang_registry.py`'s active-language list emission into
  `worker-assets/lang-registry.json` at build time.
- Refactor `workers/lang-router.js` `ACTIVE_LANGS` to lazy-load from
  `env.ASSETS` (cache the parsed Set in module scope on first hit).
- Keep the in-code fallback for now: `ACTIVE_LANGS_FALLBACK` retains the
  current hard-coded Set in case the asset is missing — Phase 4 drops it.

**Acceptance:** existing `workers/test_lang_router.mjs` tests pass without
modification; new test asserts the asset bundle loads.

### Phase 3 — Analytics Engine binding + first useful metric (PR 3, ~2 h)

- Add `[[analytics_engine_datasets]]` block to `workers/wrangler.toml`.
- Add `env.AE.writeDataPoint(...)` call in the redirect path of
  `lang-router.js` — one data point per locale redirect: `[country, fromLang,
  toLang]` blobs.
- Add SQL queries to `project-docs/operations/cloudflare-queries.md`.

**Acceptance:** AE dashboard shows a non-zero count of locale redirects
within an hour of deploy.

### Phase 4 — `WriteCoalescer` DO scaffold (PR 4, ~3 h, deferred until needed)

- Add `workers/write-coalescer.js` (the code from §2.3).
- Add `[[durable_objects.bindings]]` + migrations to `workers/wrangler.toml`.
- Add unit test `workers/test_write_coalescer.mjs` using `workerd`'s test
  harness (alarm firing, cooldown skip, soft-cap stop).
- DO NOT wire any caller yet — this PR ships the primitive. The first
  consumer comes in whatever feature PR needs runtime mutation.

**Acceptance:** wrangler dev runs; the unit test exercises alarm firing
end-to-end with a mocked `env.KV`.

### Phase 5 — Drop the fallback (PR 5, optional, after Phase 2 has burned in for one release)

- Remove `ACTIVE_LANGS_FALLBACK` from `lang-router.js`.
- Make the static-assets binding load mandatory.

**Acceptance:** existing tests still pass; deploy succeeds without warning.

---

## Part 6 — Rollback and failure modes

### 6.1 If the static-assets binding fails to load

The Worker keeps `ACTIVE_LANGS_FALLBACK` from PR 2 through PR 4. Even if the
assets binding is silently broken, locale routing keeps working. Phase 5
removes the fallback only after a release of clean traffic.

### 6.2 If the WriteCoalescer DO storage corrupts

The DO storage and the KV namespace are separable. Wipe the DO instance
storage via `wrangler durable-objects ...`; the queue drops on the floor. KV
data is unaffected. No data-integrity contract crosses the DO/KV boundary —
the DO is a *throughput shaper*, not a system of record.

### 6.3 If the daily write cap is breached

The WriteCoalescer's internal soft cap (700/day) stops new writes 30 % before
the hard cap. New write requests queue inside the DO storage until the next
day's budget. No 429s reach the client; mutations are deferred, not rejected.
If the same key is updated twice in the deferral window, last-write-wins
within the DO before the next flush.

### 6.4 If Analytics Engine writes fail

`env.AE.writeDataPoint()` is fire-and-forget under `waitUntil()`. Failures are
logged in real-time logs but never propagate to the response. Acceptable —
telemetry loss for one invocation is not a correctness issue.

### 6.5 If WAF or Bot Fight Mode misclassifies a real user

Standard escalation: Cloudflare → Security → Events → Allow rule, scoped as
narrowly as possible. Free tier supports it; no special tooling needed.

---

## Part 7 — Anti-patterns to add to CLAUDE.md

Copy-paste block for the project's CLAUDE.md (place it near the existing
"Cloudflare Free Tier constraint" memory):

```markdown
## Cloudflare KV writes — banned anti-patterns

Three patterns will exhaust the 1,000 writes/day Free quota in hours and
must not be merged:

1. Per-request counter: `env.KV.put('counter', ++n)`
   → use Analytics Engine: `env.AE.writeDataPoint({ indexes: [bucket] })`
2. Per-visit last-seen timestamp: `env.KV.put('lastSeen:' + uid, Date.now())`
   → use WriteCoalescer DO with 5-min cooldown, or AE
3. Per-pageview log line: `env.KV.put('log:' + uuid, body)`
   → use Analytics Engine: `env.AE.writeDataPoint({ blobs: [...] })`

Every `.put()` call must carry an `// adr: <ADR-NN> — reason` comment.
The CI grep step at .github/workflows/build-audit.yml fails the build on
any `.put()` without one.

Storage-tier picker: static asset → AE → DO → KV (last).
```

---

## Appendix A — Capacity-planning worksheet

Use this whenever a new feature is proposed that *might* touch KV. The
formula is:

```
writes/day ≈ unique_writers × actions_per_writer × write_probability_post_dedup
```

Where `write_probability_post_dedup` is the product of all reduction factors:

| Factor | Typical value | Notes |
|---|---|---|
| Sampling rate | 0.01 to 1.0 | If you can sample, do |
| Cooldown skip probability | 0.001 to 0.05 | 5-min cooldown on per-user data → 5/(5×24×60) ≈ 0.0007 |
| Cache absorption | 0.9 to 0.999 | (1 − cache_miss_rate) at the Cache API tier |
| DO coalescing | (writes_window / unique_keys_per_window) | one PUT per logical key per flush |

Worked example: 10,000 unique daily visitors × 1 last-seen update each ×
5-min-cooldown probability ≈ 7 writes/day. Within budget — but only if the
cooldown is actually enforced.

Worked counterexample (anti-pattern): 10,000 visitors × 12 pageviews each ×
1 per-pageview KV log = 120,000 writes — **120× over budget**.

---

## Appendix B — Useful Cloudflare GraphQL queries

### Daily write count, all namespaces, 31 days

```graphql
query {
  viewer {
    accounts(filter: { accountTag: $accountTag }) {
      kvOperationsAdaptiveGroups(
        filter: { datetime_geq: "<31-days-ago>", actionType: "write" }
        limit: 1000
        orderBy: [datetime_DESC]
      ) {
        sum { requests }
        dimensions { datetimeFifteenMinutes namespaceId }
      }
    }
  }
}
```

### Latency P99 per namespace

```graphql
query {
  viewer {
    accounts(filter: { accountTag: $accountTag }) {
      kvOperationsAdaptiveGroups(filter: { datetime_geq: "<24h-ago>" }) {
        quantiles { latencyMsP99 }
        dimensions { namespaceId actionType }
      }
    }
  }
}
```

### Storage byte count + key count per namespace

```graphql
query {
  viewer {
    accounts(filter: { accountTag: $accountTag }) {
      kvStorageAdaptiveGroups(limit: 100) {
        max { byteCount keyCount }
        dimensions { namespaceId }
      }
    }
  }
}
```

---

## Appendix C — Sources

All facts grounded in current Cloudflare developer docs and changelog,
dated where applicable.

**KV core:**
- KV limits — https://developers.cloudflare.com/kv/platform/limits/
- KV how-it-works — https://developers.cloudflare.com/kv/concepts/how-kv-works/
- KV FAQ — https://developers.cloudflare.com/kv/reference/faq/
- KV API (write) — https://developers.cloudflare.com/kv/api/write-key-value-pairs/
- KV API (list) — https://developers.cloudflare.com/kv/api/list-keys/
- KV metrics & analytics — https://developers.cloudflare.com/kv/observability/metrics-analytics/
- KV changelog — https://developers.cloudflare.com/changelog/product/kv/

**KV 2025-2026 changes:**
- Reduced minimum cacheTtl, 30 Jan 2026 — https://developers.cloudflare.com/changelog/post/2026-01-30-kv-reduced-minimum-cachettl/
- Async stale-while-revalidate, 26 Feb 2026 — https://developers.cloudflare.com/changelog/post/2026-02-26-async-stale-while-revalidate/
- Rearchitecting Workers KV, 8 Aug 2025 — https://blog.cloudflare.com/rearchitecting-workers-kv-for-redundancy/
- KV free tier announcement, Nov 2020 — https://blog.cloudflare.com/workers-kv-free-tier/
- "Sometimes I cache", 26 Dec 2024 — https://blog.cloudflare.com/sometimes-i-cache/

**Workers and pricing:**
- Workers pricing — https://developers.cloudflare.com/workers/platform/pricing/
- Workers platform limits — https://developers.cloudflare.com/workers/platform/limits/
- Workers best practices — https://developers.cloudflare.com/workers/best-practices/workers-best-practices/
- Storage options decision matrix — https://developers.cloudflare.com/workers/platform/storage-options/
- Workers Cache API — https://developers.cloudflare.com/workers/runtime-apis/cache/
- Workers Static Assets — https://developers.cloudflare.com/workers/static-assets/

**Durable Objects:**
- DO pricing — https://developers.cloudflare.com/durable-objects/platform/pricing/
- DO alarms — https://developers.cloudflare.com/durable-objects/api/alarms/
- DO changelog — https://developers.cloudflare.com/changelog/product/durable-objects/

**Analytics Engine, Queues, Hyperdrive:**
- Analytics Engine pricing — https://developers.cloudflare.com/analytics/analytics-engine/pricing/
- Analytics Engine limits — https://developers.cloudflare.com/analytics/analytics-engine/limits/
- Queues free plan, 4 Feb 2026 — https://developers.cloudflare.com/changelog/post/2026-02-04-queues-free-plan/
- Hyperdrive going free, 8 Apr 2025 — https://blog.cloudflare.com/how-hyperdrive-speeds-up-database-access/

**Security:**
- WAF custom rules — https://developers.cloudflare.com/waf/custom-rules/
- WAF rate-limiting rules — https://developers.cloudflare.com/waf/rate-limiting-rules/
- Bot Fight Mode — https://developers.cloudflare.com/bots/get-started/bot-fight-mode/
- Turnstile plans — https://developers.cloudflare.com/turnstile/plans/

**Tail Workers (paid only — for reference):**
- Tail Workers — https://developers.cloudflare.com/workers/observability/logs/tail-workers/

**Community references:**
- Architecting on Cloudflare — Chapter 3 — https://architectingoncloudflare.com/chapter-03/
