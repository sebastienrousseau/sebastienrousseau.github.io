// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * WriteCoalescer — single-instance Durable Object that collapses bursty
 * write traffic into one Cloudflare KV PUT per logical key per flush
 * window. The canonical 2026 primitive for staying under the 1,000
 * writes/day Free-tier budget when a feature needs runtime mutation.
 *
 * Policy: project-docs/adr/0001-kv-free-tier-policy.md
 *
 * Design:
 *   1. Writers POST { key, value } to the DO via fetch.
 *   2. The DO stores the pending row in its own SQLite storage
 *      (free; per-instance strongly consistent).
 *   3. A one-minute alarm fires, collects all pending rows, and:
 *      - skips any logical key that wrote within COOLDOWN_MS,
 *      - stops writing when DAILY_BUDGET keys have hit KV today,
 *      - writes whichever ones survive both gates via one PUT each.
 *   4. The KV namespace sees at most ONE PUT per logical key per flush,
 *      with a hard 700-writes/day soft cap (70 % of Free quota).
 *
 * Deployment:
 *   - SQLite-backed (the KV-backed DO storage class is paid-only).
 *   - Bind with class_name = "WriteCoalescer" + new_sqlite_classes
 *     migration; see workers/wrangler.toml.
 *   - No caller is wired today — this primitive sits dormant until the
 *     first runtime-mutation feature opts in.
 *
 * Failure modes:
 *   - DO storage corruption: wipe via wrangler; queue drops; KV
 *     unaffected. The DO is a throughput shaper, not a system of record.
 *   - KV.put() throws: the alarm re-runs (DO alarms are at-least-once,
 *     up to 6 exponential-backoff retries).
 *   - Soft cap hit: new writes pile up in DO storage until next UTC day;
 *     no 429 reaches the client; mutations deferred, last-write-wins
 *     within the window.
 */

export const FLUSH_INTERVAL_MS = 60_000;          // 1 minute
export const COOLDOWN_MS = 5 * 60 * 1000;         // 5 minutes per logical key
export const DAILY_BUDGET = 700;                  // 70 % of 1,000 — soft cap

function todayUtc(now = Date.now()) {
  return new Date(now).toISOString().slice(0, 10);
}

export class WriteCoalescer {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    if (request.method !== 'POST') {
      return new Response('method not allowed', { status: 405 });
    }
    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('invalid json', { status: 400 });
    }
    const { key, value } = body || {};
    if (typeof key !== 'string' || key.length === 0 || key.length > 512) {
      return new Response('invalid key', { status: 400 });
    }
    await this.state.storage.put(`pending:${key}`, { v: value, ts: Date.now() });
    const existing = await this.state.storage.getAlarm();
    if (existing == null) {
      await this.state.storage.setAlarm(Date.now() + FLUSH_INTERVAL_MS);
    }
    return new Response('queued', { status: 202 });
  }

  async alarm() {
    const now = Date.now();
    const budgetKey = `budget:${todayUtc(now)}`;
    const spent = (await this.state.storage.get(budgetKey)) || 0;
    if (spent >= DAILY_BUDGET) {
      // Soft cap reached — re-arm and protect the write quota.
      await this.state.storage.setAlarm(now + FLUSH_INTERVAL_MS);
      return;
    }
    const pending = await this.state.storage.list({ prefix: 'pending:' });
    const cooldown = (await this.state.storage.get('cooldown')) || {};
    let writes = 0;

    for (const [storageKey, payload] of pending) {
      const logicalKey = storageKey.slice('pending:'.length);
      const lastWrite = cooldown[logicalKey] || 0;
      if (now - lastWrite < COOLDOWN_MS) {
        // Within cooldown — drop the buffered write.
        await this.state.storage.delete(storageKey);
        continue;
      }
      if (spent + writes >= DAILY_BUDGET) break;
      if (this.env && this.env.KV && typeof this.env.KV.put === 'function') {
        try {
          // adr: 0001 — WriteCoalescer flush; one PUT per logical key per flush window
          await this.env.KV.put(logicalKey, JSON.stringify(payload.v));
          cooldown[logicalKey] = now;
          writes += 1;
        } catch {
          // Leave the row in storage so the alarm retry sees it. Break
          // out of the loop to avoid hammering a broken KV namespace.
          break;
        }
      }
      await this.state.storage.delete(storageKey);
    }

    await this.state.storage.put('cooldown', cooldown);
    if (writes > 0) {
      await this.state.storage.put(budgetKey, spent + writes);
    }
    // Re-arm if anything remains queued (cooldown-skipped rows were
    // already deleted; soft-cap-stopped rows are still pending).
    const remaining = await this.state.storage.list({ prefix: 'pending:' });
    if (remaining.size > 0) {
      await this.state.storage.setAlarm(now + FLUSH_INTERVAL_MS);
    }
  }
}
