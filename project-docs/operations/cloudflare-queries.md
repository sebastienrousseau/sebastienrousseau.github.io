# Cloudflare operations — observability cheat sheet

Reference queries for Cloudflare KV write-budget monitoring, Workers
Analytics Engine (AE) telemetry, and DO storage health. Pair with the
weekly `.github/workflows/kv-burndown.yml` automation.

Policy: `project-docs/adr/0001-kv-free-tier-policy.md`

---

## 1. KV write budget — daily counts (GraphQL)

Cloudflare GraphQL API root: `https://api.cloudflare.com/client/v4/graphql`.
Token needs **Account › Account Analytics › Read**. Account ID is the
32-character account tag.

### Trailing 24 h total writes (single number)

```graphql
query KvWrites24h($account: String!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
      kvOperationsAdaptiveGroups(
        filter: { datetime_geq: "<24h-ago>", actionType: "write" }
        limit: 1
      ) {
        sum { requests }
      }
    }
  }
}
```

Free-tier cap: 1,000/day. Alert threshold: 700 (70 %).

### Trailing 7 d, grouped per day per namespace

```graphql
query KvWrites7d($account: String!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
      kvOperationsAdaptiveGroups(
        filter: { datetime_geq: "<7d-ago>", actionType: "write" }
        limit: 1000
        orderBy: [datetime_DESC]
      ) {
        sum { requests }
        dimensions { datetimeDay namespaceId }
      }
    }
  }
}
```

### Latency P99 per namespace (24 h)

```graphql
query KvLatency($account: String!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
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
query KvStorage($account: String!) {
  viewer {
    accounts(filter: { accountTag: $account }) {
      kvStorageAdaptiveGroups(limit: 100) {
        max { byteCount keyCount }
        dimensions { namespaceId }
      }
    }
  }
}
```

Free-tier storage cap: 1 GB total across all namespaces.

---

## 2. Workers Analytics Engine SQL

Dataset name (`sebastien_pageviews`) and binding (`AE`) are declared in
`workers/wrangler.toml`. Query via the dashboard SQL console or the
Analytics Engine SQL API (`/accounts/<id>/analytics_engine/sql`).

Per Free tier: **100,000 data points/day write, 10,000 SQL queries/day,
3-month retention**, 20 blobs/20 doubles/1 index per data point, 16 KB
total blobs, 96 B index, max 250 points per Worker invocation.

### Daily redirect volume by target locale

```sql
SELECT blob4 AS to_lang, COUNT() AS redirects
FROM sebastien_pageviews
WHERE blob1 = 'redirect'
  AND timestamp > NOW() - INTERVAL '1' DAY
GROUP BY to_lang
ORDER BY redirects DESC;
```

`lang-router.recordRedirect()` populates `blobs` as
`['redirect', country, fromLang, toLang]` with `indexes: [toLang]`.

### Redirect volume by source country (7 d)

```sql
SELECT blob2 AS country, COUNT() AS redirects
FROM sebastien_pageviews
WHERE blob1 = 'redirect'
  AND timestamp > NOW() - INTERVAL '7' DAY
GROUP BY country
ORDER BY redirects DESC
LIMIT 25;
```

### Hourly histogram of redirect traffic

```sql
SELECT toStartOfHour(timestamp) AS bucket, COUNT() AS redirects
FROM sebastien_pageviews
WHERE blob1 = 'redirect'
  AND timestamp > NOW() - INTERVAL '24' HOUR
GROUP BY bucket
ORDER BY bucket ASC;
```

### Self-instrumented KV writes (if any get added)

When a feature eventually wires `WriteCoalescer` → KV, the policy in
`project-docs/adr/0001-kv-free-tier-policy.md` (§3.3) requires also
emitting a data point on every successful flush:

```sql
SELECT blob3 AS logical_key, COUNT() AS writes
FROM sebastien_pageviews
WHERE blob1 = 'kv-write'
  AND timestamp > NOW() - INTERVAL '1' DAY
GROUP BY logical_key
ORDER BY writes DESC;
```

---

## 3. Durable Object storage health (Free tier)

Dashboard → Workers & Pages → `lang-router` → Durable Objects →
`WriteCoalescer` → Storage tab. Watch for:

- **SQLite row count** trending upward without flushing → the alarm
  isn't firing, or it's firing but `env.KV` is rejecting writes.
- **Storage size in MB** approaching 5 GB → Free-tier hard cap. The
  WriteCoalescer should never accumulate this much; if it does the
  flush logic has stalled.
- **Alarm-execution failure rate** > 0 → check Workers logs for
  exceptions in the `alarm()` handler.

---

## 4. WAF / Bot Fight Mode visibility

Dashboard → Security → Events → Filter by:

- Action ≠ Allow (denied / challenged traffic)
- Source ASN ∈ ASN_DENYLIST (cross-check against
  `workers/security.js`)

Add a **Allow rule** with the narrowest possible scope if a real user
is misclassified.

---

## 5. Manual cross-checks

### Confirm the Worker is actually emitting AE points

```sh
# Hit a redirect path; Worker should emit a data point. Query within ~1 min.
curl -sI 'https://sebastienrousseau.com/?lang=fr' >/dev/null
sleep 60
# Then run the redirect-volume SQL above and check the count.
```

### Confirm the KV burndown workflow can read the API

```sh
gh workflow run kv-burndown.yml
gh run watch
```

Failure modes:

- `CLOUDFLARE_API_TOKEN` not set → workflow warns and skips silently.
- `CLOUDFLARE_ACCOUNT_ID` not set → same.
- API returns errors → workflow surfaces them in the run log; investigate
  via the token-permissions UI.

---

## 6. Capacity-planning shortcuts

Quick mental-model formulae (full version in
`project-docs/adr/0001-kv-free-tier-policy.md` Appendix A):

```
KV writes/day ≈ unique_keys_per_window × windows_per_day × write_probability

DO row writes/day ≈ unique_writers × actions × budget-skip-rate

AE data points/day ≈ pageviews × instrumentation-rate
```

Targets:

| Metric | Free cap | Soft cap | Today |
|---|---|---|---|
| KV writes/day | 1,000 | 700 | 0 |
| KV reads/day | 100,000 | 70,000 | 0 |
| AE points/day | 100,000 | 70,000 | depends on traffic |
| DO row writes/day | 100,000 | 70,000 | 0 (no caller) |
| DO SQLite storage | 5 GB | 3.5 GB | 0 |

"Today" rows update via the kv-burndown workflow.
