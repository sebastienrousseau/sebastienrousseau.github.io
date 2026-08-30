#!/usr/bin/env node
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Tests for workers/write-coalescer.js — Durable Object that absorbs
 * KV write bursts into one PUT per logical key per flush window.
 *
 * Run from repo root:
 *   node --test workers/test_write_coalescer.mjs
 *
 * The Cloudflare runtime isn't installed here; we mock DurableObjectState
 * with an in-memory Map + alarm + storage.list() shim, and KV with a
 * captured put() Mock.
 */
import { test } from 'node:test';
import { strict as assert } from 'node:assert';

import {
  WriteCoalescer,
  FLUSH_INTERVAL_MS,
  COOLDOWN_MS,
  DAILY_BUDGET,
} from './write-coalescer.js';

// ---------------------------------------------------------------------------
// In-memory DurableObjectState mock — list/get/put/delete + alarm.
// ---------------------------------------------------------------------------

function makeState() {
  const map = new Map();
  let alarmAt = null;
  return {
    storage: {
      async get(k) { return map.get(k); },
      async put(k, v) { map.set(k, v); },
      async delete(k) { return map.delete(k); },
      async list({ prefix } = {}) {
        const out = new Map();
        for (const [k, v] of map) {
          if (!prefix || k.startsWith(prefix)) out.set(k, v);
        }
        return out;
      },
      async getAlarm() { return alarmAt; },
      async setAlarm(when) { alarmAt = when; },
      _internalMap: map,
      _getAlarm: () => alarmAt,
    },
  };
}

function makeEnv(opts = {}) {
  const puts = [];
  return {
    KV: {
      async put(k, v) {
        if (opts.throwOnPut) throw new Error('kv unavailable');
        puts.push({ k, v });
      },
    },
    _puts: puts,
  };
}

async function postWrite(coalescer, key, value) {
  return coalescer.fetch(new Request('https://internal/queue', {
    method: 'POST',
    body: JSON.stringify({ key, value }),
  }));
}

// ---------------------------------------------------------------------------
// fetch path
// ---------------------------------------------------------------------------

test('fetch: POST queues the row and sets an alarm', async () => {
  const state = makeState();
  const env = makeEnv();
  const co = new WriteCoalescer(state, env);
  const r = await postWrite(co, 'k1', { hello: 'world' });
  assert.equal(r.status, 202);
  assert.ok(state.storage._internalMap.has('pending:k1'));
  assert.ok(state.storage._getAlarm() !== null);
});

test('fetch: non-POST returns 405', async () => {
  const co = new WriteCoalescer(makeState(), makeEnv());
  const r = await co.fetch(new Request('https://internal/queue', { method: 'GET' }));
  assert.equal(r.status, 405);
});

test('fetch: invalid JSON returns 400', async () => {
  const co = new WriteCoalescer(makeState(), makeEnv());
  const r = await co.fetch(new Request('https://internal/queue', {
    method: 'POST',
    body: '<<not json>>',
  }));
  assert.equal(r.status, 400);
});

test('fetch: empty key returns 400', async () => {
  const co = new WriteCoalescer(makeState(), makeEnv());
  const r = await postWrite(co, '', { v: 1 });
  assert.equal(r.status, 400);
});

test('fetch: 513-byte key returns 400 (keys capped at 512)', async () => {
  const co = new WriteCoalescer(makeState(), makeEnv());
  const r = await postWrite(co, 'x'.repeat(513), { v: 1 });
  assert.equal(r.status, 400);
});

test('fetch: existing alarm is not overwritten by a subsequent queue', async () => {
  const state = makeState();
  const env = makeEnv();
  const co = new WriteCoalescer(state, env);
  await postWrite(co, 'k1', { v: 1 });
  const firstAlarm = state.storage._getAlarm();
  await new Promise(r => setTimeout(r, 5));
  await postWrite(co, 'k2', { v: 2 });
  assert.equal(state.storage._getAlarm(), firstAlarm);
});

// ---------------------------------------------------------------------------
// alarm path
// ---------------------------------------------------------------------------

test('alarm: one KV.put per logical key, pending rows cleared', async () => {
  const state = makeState();
  const env = makeEnv();
  const co = new WriteCoalescer(state, env);
  await postWrite(co, 'a', { v: 1 });
  await postWrite(co, 'b', { v: 2 });
  await co.alarm();
  assert.equal(env._puts.length, 2);
  assert.deepEqual(env._puts.map(p => p.k).sort(), ['a', 'b']);
  // Pending cleared
  const remaining = await state.storage.list({ prefix: 'pending:' });
  assert.equal(remaining.size, 0);
});

test('alarm: cooldown skips writes within COOLDOWN_MS', async () => {
  const state = makeState();
  const env = makeEnv();
  const co = new WriteCoalescer(state, env);
  // First flush: writes 'a'.
  await postWrite(co, 'a', { v: 1 });
  await co.alarm();
  assert.equal(env._puts.length, 1);
  // Queue 'a' again and re-run alarm — within cooldown so it's dropped.
  await postWrite(co, 'a', { v: 2 });
  await co.alarm();
  assert.equal(env._puts.length, 1, 'cooldown should skip second write');
});

test('alarm: cooldown elapsed → second write proceeds', async () => {
  const state = makeState();
  const env = makeEnv();
  const co = new WriteCoalescer(state, env);
  await postWrite(co, 'a', { v: 1 });
  await co.alarm();
  // Forge an old cooldown timestamp so the second write is past it.
  const cooldown = (await state.storage.get('cooldown')) || {};
  cooldown.a = Date.now() - COOLDOWN_MS - 1;
  await state.storage.put('cooldown', cooldown);
  await postWrite(co, 'a', { v: 2 });
  await co.alarm();
  assert.equal(env._puts.length, 2);
});

test('alarm: DAILY_BUDGET soft cap stops writes; remaining stay pending', async () => {
  const state = makeState();
  const env = makeEnv();
  const co = new WriteCoalescer(state, env);
  // Seed budget at the cap.
  const today = new Date().toISOString().slice(0, 10);
  await state.storage.put(`budget:${today}`, DAILY_BUDGET);
  await postWrite(co, 'a', { v: 1 });
  await co.alarm();
  assert.equal(env._puts.length, 0, 'no writes at cap');
  const pending = await state.storage.list({ prefix: 'pending:' });
  assert.equal(pending.size, 1, 'row stays queued');
  // Alarm re-armed for the next attempt.
  assert.ok(state.storage._getAlarm() !== null);
});

test('alarm: KV.put throws → loop breaks, row stays for retry', async () => {
  const state = makeState();
  const env = makeEnv({ throwOnPut: true });
  const co = new WriteCoalescer(state, env);
  await postWrite(co, 'a', { v: 1 });
  await postWrite(co, 'b', { v: 2 });
  await co.alarm();
  const pending = await state.storage.list({ prefix: 'pending:' });
  assert.equal(pending.size, 2, 'both rows survive a failing KV');
});

test('alarm: budget counter advances with each successful write', async () => {
  const state = makeState();
  const env = makeEnv();
  const co = new WriteCoalescer(state, env);
  await postWrite(co, 'a', { v: 1 });
  await postWrite(co, 'b', { v: 2 });
  await co.alarm();
  const today = new Date().toISOString().slice(0, 10);
  const spent = await state.storage.get(`budget:${today}`);
  assert.equal(spent, 2);
});

// ---------------------------------------------------------------------------
// constants — make sure they match the policy doc
// ---------------------------------------------------------------------------

test('constants align with the Free-tier policy', () => {
  assert.equal(FLUSH_INTERVAL_MS, 60_000);
  assert.equal(COOLDOWN_MS, 5 * 60 * 1000);
  assert.equal(DAILY_BUDGET, 700);
});
