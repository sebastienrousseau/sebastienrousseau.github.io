#!/usr/bin/env node
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Tests for workers/edge-routes.js (edge HTML cache + renamed-URL 301s) and
 * the lang-router handler paths that use it.
 *
 * Run from repo root, together with the lang-router suite for the coverage
 * gate (see build.sh):
 *   node --test --experimental-test-coverage \
 *        --test-coverage-include='workers/lang-router.js' \
 *        --test-coverage-include='workers/edge-routes.js' \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 \
 *        workers/test_lang_router.mjs workers/test_edge_routes.mjs
 */
import { test } from 'node:test';
import { strict as assert } from 'node:assert';

import handler, { SECURITY_HEADERS } from './lang-router.js';
import {
  EDGE_HTML_TTL,
  EDGE_HTML_CACHE,
  isEdgeCacheable,
  isHtmlPagePath,
  getRedirectMap,
  _resetRedirectMapCache,
  tryRenamedUrlRedirect,
} from './edge-routes.js';

function makeRequest(url, opts = {}) {
  const headers = new Headers(opts.headers || {});
  return new Request(url, { method: opts.method || 'GET', headers });
}

async function callHandler(request) {
  return handler.fetch(request, {}, {});
}

test('isHtmlPagePath: pages in any locale yes, assets and APIs no', () => {
  assert.equal(isHtmlPagePath('/'), true);
  assert.equal(isHtmlPagePath('/index.html'), true);
  assert.equal(isHtmlPagePath('/fr/a-propos/'), true);
  assert.equal(isHtmlPagePath('/rss.xml'), false);
  assert.equal(isHtmlPagePath('/_csp/x'), false);
});

// ---------------------------------------------------------------------------
// Edge HTML cache: 200s cached at the Cloudflare edge for EDGE_HTML_TTL,
// everything else (redirects, 404, 429, 5xx) never cached.
// ---------------------------------------------------------------------------

// Resolve a status against cacheTtlByStatus the way Cloudflare does:
// exact code or "lo-hi" range keys.
function ttlFor(byStatus, status) {
  for (const [key, ttl] of Object.entries(byStatus)) {
    const [lo, hi = lo] = key.split('-').map(Number);
    if (status >= lo && status <= hi) return ttl;
  }
  return undefined;
}

async function withInitCapture(fn) {
  const calls = [];
  const prev = globalThis.fetch;
  globalThis.fetch = async (input, init) => {
    calls.push({ url: typeof input === 'string' ? input : input.url, init });
    return new Response('<!doctype html><title>ok</title>', {
      status: 200,
      headers: { 'content-type': 'text/html; charset=utf-8' },
    });
  };
  try {
    await fn(calls);
  } finally {
    globalThis.fetch = prev;
  }
}

test('EDGE_HTML_CACHE: 200 cached for 10 minutes, every other status never cached', () => {
  assert.equal(EDGE_HTML_TTL, 600);
  assert.equal(EDGE_HTML_CACHE.cacheEverything, true);
  const by = EDGE_HTML_CACHE.cacheTtlByStatus;
  assert.equal(ttlFor(by, 200), 600);
  for (const status of [100, 201, 204, 206, 301, 302, 304, 404, 410, 429, 500, 502, 503, 504, 599]) {
    const ttl = ttlFor(by, status);
    assert.ok(ttl !== undefined && ttl < 0, `status ${status} must be uncached, got ${ttl}`);
  }
});

test('isEdgeCacheable: GET/HEAD HTML pages in any locale, not assets/APIs/other methods', () => {
  const get = (u, method = 'GET') => isEdgeCacheable(new Request(u, { method }), new URL(u).pathname);
  assert.equal(get('https://x.example/'), true);
  assert.equal(get('https://x.example/about/'), true);
  assert.equal(get('https://x.example/fr/a-propos/'), true);
  assert.equal(get('https://x.example/zh-hant/2026-07-08-slug/', 'HEAD'), true);
  assert.equal(get('https://x.example/about/', 'POST'), false);
  assert.equal(get('https://x.example/sitemap.xml'), false);
  assert.equal(get('https://x.example/main.css'), false);
  assert.equal(get('https://x.example/api/echo'), false);
  assert.equal(get('https://x.example/.well-known/security.txt'), false);
});

test('handler: EN page pass-through asks the edge to cache it', async () => {
  await withInitCapture(async (calls) => {
    const res = await callHandler(makeRequest('https://sebastienrousseau.com/about/'));
    assert.equal(res.status, 200);
    assert.equal(calls.length, 1);
    assert.deepEqual(calls[0].init, { cf: EDGE_HTML_CACHE });
    // Browsers still revalidate every time; the edge holds the copy.
    assert.equal(res.headers.get('cache-control'), 'public, max-age=0, must-revalidate');
    for (const name of Object.keys(SECURITY_HEADERS)) assert.ok(res.headers.get(name), name);
  });
});

test('handler: locale page and HEAD are edge-cached, keyed by their own path', async () => {
  await withInitCapture(async (calls) => {
    await callHandler(makeRequest('https://sebastienrousseau.com/fr/a-propos/'));
    await callHandler(makeRequest('https://sebastienrousseau.com/de/', { method: 'HEAD' }));
    await callHandler(makeRequest('https://sebastienrousseau.com/', { headers: { Cookie: 'pref-lang=en' } }));
    assert.equal(calls.length, 3);
    for (const c of calls) assert.deepEqual(c.init, { cf: EDGE_HTML_CACHE });
    assert.deepEqual(calls.map(c => new URL(c.url).pathname), ['/fr/a-propos/', '/de/', '/']);
  });
});

test('handler: assets and non-GET requests are not forced into the edge cache', async () => {
  await withInitCapture(async (calls) => {
    await callHandler(makeRequest('https://sebastienrousseau.com/sitemap.xml'));
    await callHandler(makeRequest('https://sebastienrousseau.com/contact/', { method: 'POST' }));
    assert.equal(calls.length, 2);
    for (const c of calls) assert.equal(c.init, undefined);
  });
});

test('handler: locale redirects never reach origin, so they cannot be cached', async () => {
  await withInitCapture(async (calls) => {
    const a = await callHandler(makeRequest('https://sebastienrousseau.com/', { headers: { Cookie: 'pref-lang=fr' } }));
    const b = await callHandler(makeRequest('https://sebastienrousseau.com/?lang=de'));
    assert.equal(a.status, 302);
    assert.equal(b.status, 302);
    assert.equal(b.headers.get('cache-control'), 'no-store, private');
    assert.equal(calls.length, 0);
  });
});

test('handler: an origin 429 is passed through unchanged with browser revalidation', async () => {
  const prev = globalThis.fetch;
  globalThis.fetch = async () => new Response('rate limited', { status: 429 });
  try {
    const res = await callHandler(makeRequest('https://sebastienrousseau.com/about/'));
    assert.equal(res.status, 429);
    assert.equal(res.headers.get('cache-control'), 'public, max-age=0, must-revalidate');
  } finally {
    globalThis.fetch = prev;
  }
});

// ---------------------------------------------------------------------------
// Renamed-URL 301s from worker-assets/redirects.json.
// ---------------------------------------------------------------------------

const REDIRECTS_PAYLOAD = {
  version: 1,
  redirects: {
    '/zh-hant/2026-07-08-global-corporate-standard-iso-20022-swift-2026/':
      '/zh-hant/2026-07-08-cong-baowen-dao-ditu-iso-20022-swift-tw/',
    '/2026-banking-architecture-whitepaper/': '/2026-06-21-banking-architecture-whitepaper/',
  },
};

function assetsEnv(payload, status = 200) {
  const env = { calls: 0 };
  env.ASSETS = {
    fetch: async (req) => {
      env.calls += 1;
      const path = new URL(req.url).pathname;
      if (path === '/redirects.json') return new Response(JSON.stringify(payload), { status });
      return new Response('missing', { status: 404 });
    },
  };
  return env;
}

test('getRedirectMap: loads the map once per isolate', async () => {
  _resetRedirectMapCache();
  const env = assetsEnv(REDIRECTS_PAYLOAD);
  const map = await getRedirectMap(env);
  await getRedirectMap(env);
  assert.equal(map.size, 2);
  assert.equal(env.calls, 1);
});

test('getRedirectMap: missing binding, bad status, bad payload or throw → empty, retried later', async () => {
  for (const env of [
    undefined,
    {},
    { ASSETS: { fetch: 'nope' } },
    assetsEnv(REDIRECTS_PAYLOAD, 404),
    assetsEnv({ version: 1 }),
    { ASSETS: { fetch: async () => null } },
    { ASSETS: { fetch: async () => { throw new Error('down'); } } },
  ]) {
    _resetRedirectMapCache();
    assert.equal((await getRedirectMap(env)).size, 0);
  }
  // A failed load is not cached: the next request with a working binding hydrates.
  assert.equal((await getRedirectMap(assetsEnv(REDIRECTS_PAYLOAD))).size, 2);
});

test('tryRenamedUrlRedirect: exact, slashless and index.html forms; query kept', () => {
  const map = new Map(Object.entries(REDIRECTS_PAYLOAD.redirects));
  const loc = (u) => {
    const res = tryRenamedUrlRedirect(new URL(u), map);
    return res && { status: res.status, location: res.headers.get('location') };
  };
  const target = 'https://x.example/zh-hant/2026-07-08-cong-baowen-dao-ditu-iso-20022-swift-tw/';
  assert.deepEqual(loc('https://x.example/zh-hant/2026-07-08-global-corporate-standard-iso-20022-swift-2026/'),
    { status: 301, location: target });
  assert.deepEqual(loc('https://x.example/zh-hant/2026-07-08-global-corporate-standard-iso-20022-swift-2026'),
    { status: 301, location: target });
  assert.deepEqual(loc('https://x.example/zh-hant/2026-07-08-global-corporate-standard-iso-20022-swift-2026/index.html'),
    { status: 301, location: target });
  assert.deepEqual(loc('https://x.example/2026-banking-architecture-whitepaper/?utm_source=x'),
    { status: 301, location: 'https://x.example/2026-06-21-banking-architecture-whitepaper/?utm_source=x' });
  assert.equal(loc('https://x.example/zh-hant/'), null);
  assert.equal(loc('https://x.example/main.css'), null);
});

test('handler: renamed locale URL answers a single-hop 301 without touching origin', async () => {
  _resetRedirectMapCache();
  await withInitCapture(async (calls) => {
    const env = assetsEnv(REDIRECTS_PAYLOAD);
    const res = await handler.fetch(
      makeRequest('https://sebastienrousseau.com/zh-hant/2026-07-08-global-corporate-standard-iso-20022-swift-2026/'),
      env, {},
    );
    assert.equal(res.status, 301);
    assert.equal(res.headers.get('location'),
      'https://sebastienrousseau.com/zh-hant/2026-07-08-cong-baowen-dao-ditu-iso-20022-swift-tw/');
    for (const name of Object.keys(SECURITY_HEADERS)) assert.ok(res.headers.get(name), name);
    assert.equal(calls.length, 0);
  });
});

test('handler: renamed-URL map is skipped for POST and for unmapped paths', async () => {
  _resetRedirectMapCache();
  await withInitCapture(async (calls) => {
    const env = assetsEnv(REDIRECTS_PAYLOAD);
    const post = await handler.fetch(
      makeRequest('https://sebastienrousseau.com/2026-banking-architecture-whitepaper/', { method: 'POST' }),
      env, {},
    );
    const live = await handler.fetch(makeRequest('https://sebastienrousseau.com/zh-hant/'), env, {});
    assert.equal(post.status, 200);
    assert.equal(live.status, 200);
    assert.equal(calls.length, 2);
  });
  _resetRedirectMapCache();
});
