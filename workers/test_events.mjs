#!/usr/bin/env node
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Tests for workers/events.js.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-include='workers/events.js' \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_events.mjs
 */
import { test } from 'node:test';
import { strict as assert } from 'node:assert';

import { ALLOWED_EVENTS, cleanPath, isSameOrigin, tryEvent } from './events.js';

const BASE = 'https://sebastienrousseau.com';

function makeReq(body, {
  path = '/api/event',
  method = 'POST',
  origin = BASE,
  secFetchSite = undefined,
  cf = undefined,
} = {}) {
  const headers = {};
  if (origin !== null) headers.Origin = origin;
  if (secFetchSite !== undefined) headers['Sec-Fetch-Site'] = secFetchSite;
  const req = new Request(`${BASE}${path}`, {
    method,
    headers,
    body: method === 'POST' ? body : undefined,
  });
  if (cf !== undefined) {
    Object.defineProperty(req, 'cf', { value: cf });
  }
  return req;
}

function makeEnvCtx() {
  const points = [];
  const waited = [];
  const env = {
    AE: {
      writeDataPoint(pt) {
        points.push(pt);
      },
    },
  };
  const ctx = {
    waitUntil(p) {
      waited.push(p);
    },
  };
  return { env, ctx, points, waited };
}

test('ALLOWED_EVENTS contains conversion and Core Web Vitals event names', () => {
  for (const name of [
    'cta_click',
    'cta_get_in_touch',
    'newsletter_submit',
    'paper_download',
    'copy_config',
    'copy_code',
    'advisory_cta',
    'article_cta',
    'read_as_select',
    'tab_select',
    'vital_lcp',
    'vital_inp',
    'vital_cls',
  ]) {
    assert.ok(ALLOWED_EVENTS.has(name), `missing ${name}`);
  }
});

test('cleanPath strips query and hash and caps length at 200 chars', () => {
  assert.equal(cleanPath('/iso20022-mcp/?client=claude#top'), '/iso20022-mcp/');
  const longPath = '/' + 'a'.repeat(250);
  assert.equal(cleanPath(longPath).length, 200);
});

test('isSameOrigin accepts exact Origin or absent Origin with Sec-Fetch-Site: same-origin', () => {
  assert.equal(isSameOrigin(makeReq('{}', { origin: BASE })), true);
  assert.equal(isSameOrigin(makeReq('{}', { origin: 'https://evil.example' })), false);
  assert.equal(
    isSameOrigin(makeReq('{}', { origin: null, secFetchSite: 'same-origin' })),
    true,
  );
  assert.equal(
    isSameOrigin(makeReq('{}', { origin: null, secFetchSite: 'cross-site' })),
    false,
  );
});

test('tryEvent returns null for other paths', async () => {
  const res = await tryEvent(makeReq('{}', { path: '/articles/' }), {}, {});
  assert.equal(res, null);
});

test('tryEvent rejects non-POST methods with 405', async () => {
  const res = await tryEvent(makeReq(undefined, { method: 'GET' }), {}, {});
  assert.equal(res.status, 405);
  assert.equal(res.headers.get('Allow'), 'POST');
});

test('tryEvent rejects cross-origin requests with 403', async () => {
  const res = await tryEvent(
    makeReq('{"e":"copy_code","p":"/"}', { origin: 'https://evil.example' }),
    {},
    {},
  );
  assert.equal(res.status, 403);
});

test('tryEvent rejects empty, oversized, or malformed JSON bodies with 400', async () => {
  for (const bad of [
    '',
    'x'.repeat(2049),
    '{not-json',
    'null',
    '[]',
    JSON.stringify({ e: 'unknown_event', p: '/' }),
    JSON.stringify({ e: 123, p: '/' }),
    JSON.stringify({ e: 'copy_code', p: 'relative-path' }),
    JSON.stringify({ e: 'copy_code', p: 42 }),
    JSON.stringify({ e: 'copy_code', p: '/', v: 'not-a-number' }),
    JSON.stringify({ e: 'copy_code', p: '/', v: null }),
    JSON.stringify({ e: 'copy_code', p: '/', k: 99 }),
  ]) {
    const res = await tryEvent(makeReq(bad), {}, {});
    assert.equal(res.status, 400, `expected 400 for ${bad.slice(0, 40)}`);
  }
});

test('tryEvent writes Analytics Engine data point and returns 204', async () => {
  const { env, ctx, points, waited } = makeEnvCtx();
  const req = makeReq(
    JSON.stringify({
      e: 'copy_config',
      p: '/iso20022-mcp/?client=claude',
      v: 2,
      k: 'claude-desktop',
    }),
    { cf: { country: 'GB' } },
  );
  const res = await tryEvent(req, env, ctx);
  assert.equal(res.status, 204);
  assert.equal(waited.length, 1);
  await Promise.all(waited);
  assert.deepEqual(points, [
    {
      blobs: ['copy_config', '/iso20022-mcp/', 'claude-desktop', 'GB'],
      doubles: [2],
      indexes: ['copy_config'],
    },
  ]);
});

test('tryEvent defaults v to 1, k to empty string, country to ??, and tolerates missing AE binding', async () => {
  const { env, ctx, points } = makeEnvCtx();
  const req = makeReq(JSON.stringify({ e: 'cta_click', p: '/' }));
  const res = await tryEvent(req, env, ctx);
  assert.equal(res.status, 204);
  assert.deepEqual(points, [
    {
      blobs: ['cta_click', '/', '', '??'],
      doubles: [1],
      indexes: ['cta_click'],
    },
  ]);

  const resNoAe = await tryEvent(
    makeReq(JSON.stringify({ e: 'cta_click', p: '/' }), {
      origin: null,
      secFetchSite: 'same-origin',
    }),
    null,
    null,
  );
  assert.equal(resNoAe.status, 204);
});
