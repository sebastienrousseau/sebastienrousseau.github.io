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
  tryRetiredPdf,
  EDGE_HTML_STALE,
  EDGE_COPY_PREFIX,
  EDGE_STORED_AT,
  fetchOrigin,
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
      if (path === '/article-locales.json' && env.locales) {
        return new Response(JSON.stringify(env.locales), { status });
      }
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

// ---------------------------------------------------------------------------
// Retired /api/pdf/ route (#515): each old PDF URL 301s to its article so
// inbound links keep their value; anything that was never a PDF URL is 410.
// ---------------------------------------------------------------------------

const PDF = 'https://sebastienrousseau.com/api/pdf/';

test('tryRetiredPdf: not a PDF path → null', async () => {
  assert.equal(await tryRetiredPdf(new URL('https://sebastienrousseau.com/api/event'), {}), null);
});

test('tryRetiredPdf: EN and locale PDFs 301 to the article, query dropped', async () => {
  _resetRedirectMapCache();
  const en = await tryRetiredPdf(new URL(`${PDF}2026-11-17-treasury-automation-half-done.pdf?utm=x`), {});
  assert.equal(en.status, 301);
  assert.equal(en.headers.get('location'), 'https://sebastienrousseau.com/2026-11-17-treasury-automation-half-done/');
  const fr = await tryRetiredPdf(new URL(`${PDF}zh-hans/2026-11-17-caiwu-zidonghua.pdf`), {});
  assert.equal(fr.headers.get('location'), 'https://sebastienrousseau.com/zh-hans/2026-11-17-caiwu-zidonghua/');
});

test('tryRetiredPdf: a renamed article resolves to its final URL in one hop', async () => {
  _resetRedirectMapCache();
  const res = await tryRetiredPdf(
    new URL(`${PDF}zh-hant/2026-07-08-global-corporate-standard-iso-20022-swift-2026.pdf`),
    assetsEnv(REDIRECTS_PAYLOAD),
  );
  assert.equal(res.status, 301);
  assert.equal(res.headers.get('location'),
    'https://sebastienrousseau.com/zh-hant/2026-07-08-cong-baowen-dao-ditu-iso-20022-swift-tw/');
  _resetRedirectMapCache();
});

const LOCALES_PAYLOAD = {
  version: 1,
  articles: {
    '2026-11-17-treasury-automation-half-done': 'en',
    '2025-09-01-pagos-resistentes-al-cuantico-epaa': 'es',
    '2026-07-08-global-corporate-standard-iso-20022-swift-2026': 'zh-hant',
  },
};

test('tryRetiredPdf: a locale-less PDF of a translated article goes to its locale', async () => {
  _resetRedirectMapCache();
  const env = assetsEnv(REDIRECTS_PAYLOAD);
  env.locales = LOCALES_PAYLOAD;
  const es = await tryRetiredPdf(new URL(`${PDF}2025-09-01-pagos-resistentes-al-cuantico-epaa.pdf`), env);
  assert.equal(es.status, 301);
  assert.equal(es.headers.get('location'),
    'https://sebastienrousseau.com/es/2025-09-01-pagos-resistentes-al-cuantico-epaa/');
  const en = await tryRetiredPdf(new URL(`${PDF}2026-11-17-treasury-automation-half-done.pdf`), env);
  assert.equal(en.headers.get('location'), 'https://sebastienrousseau.com/2026-11-17-treasury-automation-half-done/');
  // A renamed translated slug still resolves in one hop.
  const renamed = await tryRetiredPdf(
    new URL(`${PDF}2026-07-08-global-corporate-standard-iso-20022-swift-2026.pdf`), env);
  assert.equal(renamed.headers.get('location'),
    'https://sebastienrousseau.com/zh-hant/2026-07-08-cong-baowen-dao-ditu-iso-20022-swift-tw/');
  _resetRedirectMapCache();
});

test('tryRetiredPdf: a slug that was never an article is 410 once the index loads', async () => {
  _resetRedirectMapCache();
  const env = assetsEnv(REDIRECTS_PAYLOAD);
  env.locales = LOCALES_PAYLOAD;
  const gone = await tryRetiredPdf(new URL(`${PDF}2020-01-01-never-published.pdf`), env);
  assert.equal(gone.status, 410);
  assert.equal(gone.headers.get('X-Robots-Tag'), 'noindex');
  // A locale-prefixed PDF keeps its 301: the index holds one locale per slug.
  const fr = await tryRetiredPdf(new URL(`${PDF}fr/2020-01-01-jamais.pdf`), env);
  assert.equal(fr.status, 301);
  // Without the index the old 301-to-root behaviour stays.
  _resetRedirectMapCache();
  const bare = await tryRetiredPdf(new URL(`${PDF}2020-01-01-never-published.pdf`), {});
  assert.equal(bare.status, 301);
  _resetRedirectMapCache();
});

test('tryRetiredPdf: malformed paths answer 410 Gone, noindex', async () => {
  for (const bad of ['index.html.pdf', 'a/b/c.pdf', 'UPPER.pdf', 'slug', 'x/slug.pdf', '']) {
    const res = await tryRetiredPdf(new URL(PDF + bad), {});
    assert.equal(res.status, 410, bad);
    assert.equal(res.headers.get('X-Robots-Tag'), 'noindex');
    assert.equal(res.headers.get('Cache-Control'), 'public, max-age=86400');
  }
});

// ---------------------------------------------------------------------------
// Stale-while-revalidate: with the Workers Cache API, a page is served from
// the edge copy at once (up to EDGE_HTML_STALE old) and refreshed in the
// background once it is older than EDGE_HTML_TTL.
// ---------------------------------------------------------------------------

function fakeCache() {
  const store = new Map();
  return {
    store,
    async match(req) {
      const hit = store.get(req.url);
      return hit ? hit.clone() : undefined;
    },
    async put(req, res) {
      store.set(req.url, res);
    },
  };
}

function fakeCtx() {
  const pending = [];
  return { pending, waitUntil: (p) => pending.push(p), settle: () => Promise.all(pending) };
}

async function withOrigin(responses, fn) {
  const calls = [];
  const prev = globalThis.fetch;
  globalThis.fetch = async (input, init) => {
    calls.push({ url: typeof input === 'string' ? input : input.url, method: input.method, init });
    const [status, body] = responses.length > 1 ? responses.shift() : responses[0];
    return new Response(body, { status, headers: { 'cache-control': 'max-age=600' } });
  };
  try {
    await fn(calls);
  } finally {
    globalThis.fetch = prev;
  }
}

const PAGE = 'https://sebastienrousseau.com/about/';
const COPY = `https://sebastienrousseau.com${EDGE_COPY_PREFIX}/about/`;

test('SWR: a miss fetches origin and stores the 200 for EDGE_HTML_STALE', async () => {
  const cache = fakeCache();
  const ctx = fakeCtx();
  await withOrigin([[200, 'v1']], async (calls) => {
    const res = await fetchOrigin(new Request(`${PAGE}?utm=x`), new URL(`${PAGE}?utm=x`), ctx, cache);
    assert.equal(await res.text(), 'v1');
    await ctx.settle();
    assert.equal(calls.length, 1);
    assert.deepEqual(calls[0].init, { cf: EDGE_HTML_CACHE });
    const stored = cache.store.get(COPY);
    assert.equal(stored.headers.get('cache-control'), `public, max-age=${EDGE_HTML_STALE}`);
    assert.ok(Number(stored.headers.get(EDGE_STORED_AT)) > 0);
  });
});

test('SWR: a fresh hit is served without touching origin, timestamp stripped', async () => {
  const cache = fakeCache();
  const ctx = fakeCtx();
  await withOrigin([[200, 'v1']], async (calls) => {
    await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    await ctx.settle();
    const res = await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    assert.equal(await res.text(), 'v1');
    assert.equal(res.headers.get(EDGE_STORED_AT), null);
    assert.equal(calls.length, 1);
    const head = await fetchOrigin(new Request(PAGE, { method: 'HEAD' }), new URL(PAGE), ctx, cache);
    assert.equal(head.status, 200);
    assert.equal(await head.text(), '');
  });
});

test('SWR: a stale hit is served at once and refreshed in the background', async () => {
  const cache = fakeCache();
  const ctx = fakeCtx();
  await withOrigin([[200, 'v1'], [200, 'v2']], async (calls) => {
    await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    await ctx.settle();
    const old = cache.store.get(COPY);
    const headers = new Headers(old.headers);
    headers.set(EDGE_STORED_AT, String(Date.now() - (EDGE_HTML_TTL + 1) * 1000));
    cache.store.set(COPY, new Response(await old.text(), { status: 200, headers }));
    const res = await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    assert.equal(await res.text(), 'v1');
    await ctx.settle();
    assert.equal(calls.length, 2);
    assert.equal(await cache.store.get(COPY).clone().text(), 'v2');
  });
});

test('SWR: a refresh reaches origin even though the edge fetch cache shares the copy\'s storage', async () => {
  // On Cloudflare, caches.default and fetch(..., { cf: cacheEverything })
  // read one zone cache. A copy stored under the page URL itself is then
  // what the refresh fetch gets back, so it re-stores the old page for good
  // (the homepage stayed on a 21 Nov build through two deploys).
  const cache = fakeCache();
  const ctx = fakeCtx();
  const origin = ['v1'];
  const prev = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    const shared = cache.store.get(url);
    if (shared) return shared.clone();
    return new Response(origin[0], { status: 200 });
  };
  try {
    await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    await ctx.settle();
    origin[0] = 'v2';
    for (const [k, old] of cache.store) {
      const headers = new Headers(old.headers);
      headers.set(EDGE_STORED_AT, String(Date.now() - (EDGE_HTML_TTL + 1) * 1000));
      cache.store.set(k, new Response(await old.clone().text(), { status: 200, headers }));
    }
    await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    await ctx.settle();
    const res = await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    assert.equal(await res.text(), 'v2');
  } finally {
    globalThis.fetch = prev;
  }
});

test('SWR: non-200 origin answers and HEAD misses are never stored; failed refresh keeps the copy', async () => {
  const cache = fakeCache();
  const ctx = fakeCtx();
  await withOrigin([[503, 'down']], async () => {
    const res = await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    assert.equal(res.status, 503);
    await fetchOrigin(new Request(PAGE, { method: 'HEAD' }), new URL(PAGE), ctx, cache);
    await ctx.settle();
    assert.equal(cache.store.size, 0);
  });
  const headers = new Headers({ [EDGE_STORED_AT]: '0' });
  cache.store.set(COPY, new Response('kept', { status: 200, headers }));
  await withOrigin([[500, 'boom']], async () => {
    const res = await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    assert.equal(await res.text(), 'kept');
    await ctx.settle();
    assert.equal(await cache.store.get(COPY).clone().text(), 'kept');
  });
  const prev = globalThis.fetch;
  globalThis.fetch = async () => { throw new Error('network'); };
  try {
    await fetchOrigin(new Request(PAGE), new URL(PAGE), ctx, cache);
    await ctx.settle();
    assert.equal(await cache.store.get(COPY).clone().text(), 'kept');
  } finally {
    globalThis.fetch = prev;
  }
});

test('SWR: off without a cache or ctx, and never for assets', async () => {
  await withOrigin([[200, 'v']], async (calls) => {
    await fetchOrigin(new Request(PAGE), new URL(PAGE));
    await fetchOrigin(new Request(PAGE), new URL(PAGE), { waitUntil: 'no' }, fakeCache());
    await fetchOrigin(new Request('https://sebastienrousseau.com/main.css'), new URL('https://sebastienrousseau.com/main.css'), fakeCtx(), fakeCache());
    assert.deepEqual(calls.map((c) => c.init), [{ cf: EDGE_HTML_CACHE }, { cf: EDGE_HTML_CACHE }, undefined]);
  });
});

test('handler: uses caches.default when the runtime provides it', async () => {
  const cache = fakeCache();
  const ctx = fakeCtx();
  globalThis.caches = { default: cache };
  try {
    await withOrigin([[200, 'v1']], async () => {
      const res = await handler.fetch(makeRequest(PAGE), {}, ctx);
      assert.equal(res.headers.get('cache-control'), 'public, max-age=0, must-revalidate');
      await ctx.settle();
      assert.ok(cache.store.has(COPY));
    });
  } finally {
    delete globalThis.caches;
  }
});
