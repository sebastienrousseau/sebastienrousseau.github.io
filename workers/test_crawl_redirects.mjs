#!/usr/bin/env node
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Tests for workers/crawl-redirects.js: one 301 for each kind of URL Search
 * Console reported that no page should have produced. Run with the
 * lang-router suites (build.sh holds the 100% coverage gate).
 */
import { test } from 'node:test';
import { strict as assert } from 'node:assert';

import handler from './lang-router.js';
import { tryCrawlRedirect, safeDecodePath } from './crawl-redirects.js';
import {
  tryRenamedUrlRedirect,
  fetchOrigin,
  BUILD_ID_PATH,
  _resetBuildIdCache,
} from './edge-routes.js';

const SITE = 'https://sebastienrousseau.com';

function location(path) {
  const res = tryCrawlRedirect(new URL(SITE + path));
  return res && { status: res.status, location: res.headers.get('location') };
}

test('index.html: a page and its index.html share one URL, the directory', () => {
  assert.deepEqual(location('/glossary/index.html'), { status: 301, location: `${SITE}/glossary/` });
  assert.deepEqual(location('/libmake/libmake/index.html?x=1'),
    { status: 301, location: `${SITE}/libmake/libmake/?x=1` });
  assert.deepEqual(location('/index.html'), { status: 301, location: `${SITE}/` });
  assert.equal(location('/glossary/'), null);
  assert.equal(location('/glossary/index.htm'), null);
});

test('markdown residue: a link pasted whole into a URL goes to its target', () => {
  const path = '/2023-11-19-[crystals-kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)-the-safeguarding-algorithm-in-a-quantum-age/index.html';
  assert.deepEqual(location(path), {
    status: 301,
    location: `${SITE}/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/`,
  });
  assert.deepEqual(location('/[about](/about/)'), { status: 301, location: `${SITE}/about/` });
});

test('quote residue: a segment opened by a quote is dropped with what follows', () => {
  const page = '/tr/2026-05-22-uk-acid-jazz-renewal-artists-concerts-albums-2026/';
  for (const tail of ['”/about/index.html”', '”https://github.com/sebastienrousseau”', '"x"', "'x'", '“x', '‘x', '’x']) {
    assert.deepEqual(location(page + encodeURI(tail)), { status: 301, location: SITE + page }, tail);
  }
});

test('patterns read as links: any path with "*" goes home', () => {
  for (const path of ['/*', '/*.pdf', '/*.xml', '/contact/*', '/fr/contact/*', '/_csp/*']) {
    assert.deepEqual(location(path), { status: 301, location: `${SITE}/` }, path);
  }
});

test('/mcp/ has no page of its own: its product page', () => {
  assert.deepEqual(location('/mcp/'), { status: 301, location: `${SITE}/iso20022-mcp/` });
  assert.deepEqual(location('/mcp'), { status: 301, location: `${SITE}/iso20022-mcp/` });
  assert.equal(location('/mcp/v1/list_resources'), null);
});

test('a leaked ?__build= is dropped, other parameters kept', () => {
  assert.deepEqual(location('/static-site-generator/?__build=abc'),
    { status: 301, location: `${SITE}/static-site-generator/` });
  assert.deepEqual(location('/glossary/index.html?__build=abc&x=1'),
    { status: 301, location: `${SITE}/glossary/?x=1` });
  assert.equal(location('/about/?x=1'), null);
});

test('ordinary pages, assets and locale URLs are left alone', () => {
  for (const path of ['/', '/fr/', '/about/', '/assets/app.js', '/2026-11-25-shor-rsa-2048-cat-qubits/']) {
    assert.equal(location(path), null, path);
  }
});

test('safeDecodePath: decodes UTF-8, keeps a malformed escape as sent', () => {
  assert.equal(safeDecodePath('/2018-01-24-the-erc-20-%E0%A4%9F%E0%A5%8B%E0%A4%95%E0%A4%A8-standard/'),
    '/2018-01-24-the-erc-20-टोकन-standard/');
  assert.equal(safeDecodePath('/bad-%E0%A4/'), '/bad-%E0%A4/');
});

test('tryRenamedUrlRedirect: a non-ASCII old slug matches its decoded key', () => {
  const map = new Map([['/2018-01-24-the-erc-20-टोकन-standard/', '/2018-01-24-the-erc-20-token-standard/']]);
  const res = tryRenamedUrlRedirect(new URL(`${SITE}/2018-01-24-the-erc-20-टोकन-standard/index.html`), map);
  assert.equal(res.status, 301);
  assert.equal(res.headers.get('location'), `${SITE}/2018-01-24-the-erc-20-token-standard/`);
});

test('handler: a crawl redirect answers before origin, with security headers', async () => {
  const realFetch = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => { calls += 1; return new Response('origin'); };
  try {
    const res = await handler.fetch(new Request(`${SITE}/glossary/index.html`), {}, {});
    assert.equal(res.status, 301);
    assert.equal(res.headers.get('location'), `${SITE}/glossary/`);
    assert.ok(res.headers.get('strict-transport-security'));
    const star = await handler.fetch(new Request(`${SITE}/*.pdf`), {}, {});
    assert.equal(star.headers.get('location'), `${SITE}/`);
    assert.equal(calls, 0);
  } finally {
    globalThis.fetch = realFetch;
  }
});

// GitHub Pages echoes the query string on its own redirects, so the
// ?__build=<id> the Worker adds to a page fetch came back in Location
// (/static-site-generator/ -> ...?__build=<sha>): every redirect handed
// crawlers a new URL. The Worker now drops the parameter from Location.
test('fetchOrigin: an origin redirect never carries the internal build parameter', async () => {
  const build = 'c'.repeat(40);
  const prev = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith(BUILD_ID_PATH)) return new Response(`${build}\n`);
    const target = new URL(url);
    if (target.pathname === '/plain/') return new Response('page');
    if (target.pathname === '/away/') {
      return new Response(null, { status: 301, headers: { location: 'https://docs.example/' } });
    }
    target.pathname += '/';
    target.searchParams.set('keep', '1');
    return new Response(null, { status: 301, headers: { location: target.toString() } });
  };
  _resetBuildIdCache();
  const cache = { match: async () => undefined, put: async () => {} };
  const ctx = { waitUntil: () => {} };
  try {
    const page = `${SITE}/2026-06-12-kyberlib-post-quantum-banking-migration-standards-code-2026`;
    const res = await fetchOrigin(new Request(page), new URL(page), ctx, cache);
    assert.equal(res.status, 301);
    assert.equal(res.headers.get('location'), `${page}/?keep=1`);
    const away = await fetchOrigin(new Request(`${SITE}/away/`), new URL(`${SITE}/away/`), ctx, cache);
    assert.equal(away.headers.get('location'), 'https://docs.example/');
    const plain = await fetchOrigin(new Request(`${SITE}/plain/`), new URL(`${SITE}/plain/`), ctx, cache);
    assert.equal(await plain.text(), 'page');
  } finally {
    globalThis.fetch = prev;
    _resetBuildIdCache();
  }
});
