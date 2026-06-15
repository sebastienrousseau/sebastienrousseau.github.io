#!/usr/bin/env node
/**
 * Tests for workers/mcp.js — pure-logic + integrated route dispatch.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_mcp.mjs
 *
 * No Cloudflare runtime is required. Node 18+'s native Response /
 * Headers / URL globals are sufficient. We stub globalThis.fetch to
 * serve a canned manifest + JSONL feed so the tests are hermetic.
 */
import { test, before, after } from 'node:test';
import { strict as assert } from 'node:assert';

import { isMCPRoute, tryMCP } from './mcp.js';

const BASE = 'https://sebastienrousseau.com';

const MANIFEST = {
  version: '1.0',
  generated_at: '2026-06-13',
  total: 3,
  resources: [
    {
      slug: '2026-06-12-kyberlib',
      url: `${BASE}/2026-06-12-kyberlib/`,
      title: 'KyberLib and post-quantum banking',
      summary: 'Kyber + FIPS 203 in Rust.',
      tags: ['post-quantum cryptography', 'KyberLib', 'Rust'],
      pillars: ['infra', 'open-source'],
      lang: 'en',
      license: 'CC-BY-4.0',
      published_at: '2026-06-12',
      updated_at: '2026-06-12',
    },
    {
      slug: '2026-05-31-pq-payments',
      url: `${BASE}/2026-05-31-pq-payments/`,
      title: 'Post-quantum payments',
      summary: 'Replace vs retrofit.',
      tags: ['post-quantum cryptography', 'payments'],
      pillars: ['infra', 'payments'],
      lang: 'en',
      license: 'CC-BY-4.0',
      published_at: '2026-05-31',
      updated_at: '2026-05-31',
    },
    {
      slug: '2026-06-11-cloudcdn',
      url: `${BASE}/2026-06-11-cloudcdn/`,
      title: 'CloudCDN blueprint',
      summary: 'AI-native edge.',
      tags: ['CloudCDN', 'cdn', 'AI'],
      pillars: ['ai', 'infra'],
      lang: 'en',
      license: 'CC-BY-4.0',
      published_at: '2026-06-11',
      updated_at: '2026-06-11',
    },
  ],
};

const FEED_JSONL = MANIFEST.resources
  .map(r => JSON.stringify({
    ...r,
    body_markdown: `# ${r.title}\n\nBody of ${r.slug}.`,
    body_text: `Body of ${r.slug}.`,
  }))
  .join('\n') + '\n';

const realFetch = globalThis.fetch;
before(() => {
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) {
      return new Response(JSON.stringify(MANIFEST), { status: 200 });
    }
    if (url.endsWith('/feed.jsonl')) {
      return new Response(FEED_JSONL, { status: 200 });
    }
    if (url.endsWith('/missing/api/mcp-resources.json')) {
      return new Response('', { status: 503 });
    }
    return new Response('not stubbed', { status: 502 });
  };
});
after(() => {
  globalThis.fetch = realFetch;
});

function req(path, method = 'GET') {
  return new Request(`${BASE}${path}`, { method });
}

// ---------------------------------------------------------------------------
// isMCPRoute
// ---------------------------------------------------------------------------

test('isMCPRoute matches /mcp/v1/* and rejects others', () => {
  assert.equal(isMCPRoute('/mcp/v1/list_resources'), true);
  assert.equal(isMCPRoute('/mcp/v1/read_resource'), true);
  assert.equal(isMCPRoute('/mcp/v1/search'), true);
  assert.equal(isMCPRoute('/mcp/v2/list_resources'), false);
  assert.equal(isMCPRoute('/mcp/'), false);
  assert.equal(isMCPRoute('/.well-known/mcp/server.json'), false);
  assert.equal(isMCPRoute('/articles/'), false);
  assert.equal(isMCPRoute('/'), false);
});

// ---------------------------------------------------------------------------
// tryMCP — null pass-through
// ---------------------------------------------------------------------------

test('tryMCP returns null for non-MCP paths', async () => {
  assert.equal(await tryMCP(req('/articles/')), null);
  assert.equal(await tryMCP(req('/')), null);
  assert.equal(await tryMCP(req('/.well-known/mcp/server.json')), null);
});

// ---------------------------------------------------------------------------
// list_resources
// ---------------------------------------------------------------------------

test('list_resources returns all three records with default limit', async () => {
  const r = await tryMCP(req('/mcp/v1/list_resources'));
  assert.equal(r.status, 200);
  const body = await r.json();
  assert.equal(body.total, 3);
  assert.equal(body.resources.length, 3);
  assert.equal(body.resources[0].uri, 'mcp+article://sebastienrousseau.com/2026-06-12-kyberlib');
  assert.equal(body.resources[0].mimeType, 'text/markdown');
  assert.equal(body.resources[0].license, 'CC-BY-4.0');
  assert.equal(body.nextCursor, null);
});

test('list_resources respects cursor + limit pagination', async () => {
  const r = await tryMCP(req('/mcp/v1/list_resources?cursor=1&limit=1'));
  const body = await r.json();
  assert.equal(body.resources.length, 1);
  assert.equal(body.resources[0].name, 'Post-quantum payments');
  assert.equal(body.nextCursor, '2');
  // Last page nextCursor=null
  const r2 = await tryMCP(req('/mcp/v1/list_resources?cursor=2&limit=1'));
  const b2 = await r2.json();
  assert.equal(b2.nextCursor, null);
});

test('list_resources clamps limit to 100 max + 1 min', async () => {
  const r = await tryMCP(req('/mcp/v1/list_resources?limit=99999'));
  const body = await r.json();
  assert.equal(body.resources.length, 3); // all 3 since corpus is small
  const r2 = await tryMCP(req('/mcp/v1/list_resources?limit=0'));
  const b2 = await r2.json();
  assert.ok(b2.resources.length >= 1);
  // Negative limit hits the parseIntParam `n >= 0` false branch
  const r3 = await tryMCP(req('/mcp/v1/list_resources?limit=-5'));
  assert.equal(r3.status, 200);
});

test('list/search/read tolerate manifest without resources key', async () => {
  // Hits the `manifest.resources || []` fallback in handleListResources,
  // findBySlugOrUri, and handleSearch — three uncovered branches.
  const realF = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) {
      return new Response(JSON.stringify({ version: '1.0' }), { status: 200 });
    }
    return new Response('', { status: 502 });
  };
  try {
    const l = await tryMCP(req('/mcp/v1/list_resources'));
    assert.equal(l.status, 200);
    assert.equal((await l.json()).total, 0);
    const s = await tryMCP(req('/mcp/v1/search?q=any'));
    assert.equal((await s.json()).total, 0);
    const rd = await tryMCP(req('/mcp/v1/read_resource?uri=anything'));
    assert.equal(rd.status, 404);
  } finally {
    globalThis.fetch = realF;
  }
});

test('tryMCP honours custom originBase', async () => {
  // Default ORIGIN_BASE is sebastienrousseau.com; pass an explicit
  // base to exercise the non-default branch of the default param.
  const realF = globalThis.fetch;
  let lastUrl = null;
  globalThis.fetch = async (input) => {
    lastUrl = typeof input === 'string' ? input : input.url;
    if (lastUrl.endsWith('/api/mcp-resources.json')) {
      return new Response(JSON.stringify(MANIFEST), { status: 200 });
    }
    return new Response('', { status: 502 });
  };
  try {
    const r = await tryMCP(req('/mcp/v1/list_resources'), 'https://staging.sebastienrousseau.com');
    assert.equal(r.status, 200);
    assert.equal(lastUrl, 'https://staging.sebastienrousseau.com/api/mcp-resources.json');
  } finally {
    globalThis.fetch = realF;
  }
});

test('list_resources falls back to default limit on non-numeric input', async () => {
  const r = await tryMCP(req('/mcp/v1/list_resources?limit=banana&cursor=oranges'));
  assert.equal(r.status, 200);
  const body = await r.json();
  assert.equal(body.resources.length, 3);
});

// ---------------------------------------------------------------------------
// read_resource
// ---------------------------------------------------------------------------

test('read_resource by mcp+article:// URI returns body markdown', async () => {
  const r = await tryMCP(req(
    '/mcp/v1/read_resource?uri=' + encodeURIComponent('mcp+article://sebastienrousseau.com/2026-06-11-cloudcdn'),
  ));
  assert.equal(r.status, 200);
  const body = await r.json();
  assert.equal(body.contents.length, 1);
  assert.match(body.contents[0].text, /CloudCDN blueprint/);
  assert.equal(body.contents[0].metadata.canonical, `${BASE}/2026-06-11-cloudcdn/`);
  assert.equal(body.contents[0].metadata.license, 'CC-BY-4.0');
});

test('read_resource by canonical URL works equivalently', async () => {
  const r = await tryMCP(req(
    '/mcp/v1/read_resource?uri=' + encodeURIComponent(`${BASE}/2026-06-11-cloudcdn/`),
  ));
  assert.equal(r.status, 200);
});

test('read_resource by bare slug works', async () => {
  const r = await tryMCP(req('/mcp/v1/read_resource?uri=2026-06-11-cloudcdn'));
  assert.equal(r.status, 200);
});

test('read_resource missing uri parameter → 400', async () => {
  const r = await tryMCP(req('/mcp/v1/read_resource'));
  assert.equal(r.status, 400);
  const body = await r.json();
  assert.equal(body.error.code, 'missing-uri');
});

test('read_resource unknown uri → 404', async () => {
  const r = await tryMCP(req('/mcp/v1/read_resource?uri=does-not-exist'));
  assert.equal(r.status, 404);
});

test('read_resource handles malformed JSONL lines without crashing', async () => {
  const realF = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) return new Response(JSON.stringify(MANIFEST), { status: 200 });
    if (url.endsWith('/feed.jsonl')) {
      return new Response(
        'not json\n' + JSON.stringify({ url: `${BASE}/2026-06-11-cloudcdn/`, body_markdown: 'OK' }) + '\nalso not json\n',
        { status: 200 },
      );
    }
    return new Response('', { status: 502 });
  };
  try {
    const r = await tryMCP(req('/mcp/v1/read_resource?uri=2026-06-11-cloudcdn'));
    assert.equal(r.status, 200);
    const body = await r.json();
    assert.equal(body.contents[0].text, 'OK');
  } finally {
    globalThis.fetch = realF;
  }
});

test('read_resource feed.jsonl 502 → 502 corpus-unavailable', async () => {
  const realF = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) return new Response(JSON.stringify(MANIFEST), { status: 200 });
    if (url.endsWith('/feed.jsonl')) return new Response('', { status: 502 });
    return new Response('', { status: 502 });
  };
  try {
    const r = await tryMCP(req('/mcp/v1/read_resource?uri=2026-06-11-cloudcdn'));
    assert.equal(r.status, 502);
    const body = await r.json();
    assert.equal(body.error.code, 'corpus-unavailable');
  } finally {
    globalThis.fetch = realF;
  }
});

test('read_resource feed missing the record → 404', async () => {
  const realF = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) return new Response(JSON.stringify(MANIFEST), { status: 200 });
    // Feed has only one unrelated record
    if (url.endsWith('/feed.jsonl')) return new Response(JSON.stringify({ url: `${BASE}/other/` }) + '\n', { status: 200 });
    return new Response('', { status: 502 });
  };
  try {
    const r = await tryMCP(req('/mcp/v1/read_resource?uri=2026-06-11-cloudcdn'));
    assert.equal(r.status, 404);
    const body = await r.json();
    assert.equal(body.error.code, 'not-found');
  } finally {
    globalThis.fetch = realF;
  }
});

// ---------------------------------------------------------------------------
// search
// ---------------------------------------------------------------------------

test('search by q matches title + summary case-insensitive', async () => {
  const r = await tryMCP(req('/mcp/v1/search?q=KYBERLIB'));
  assert.equal(r.status, 200);
  const body = await r.json();
  assert.equal(body.total, 1);
  assert.equal(body.resources[0].name, 'KyberLib and post-quantum banking');
});

test('search by tag matches canonical slug', async () => {
  const r = await tryMCP(req('/mcp/v1/search?tag=post-quantum%20cryptography'));
  assert.equal(r.status, 200);
  const body = await r.json();
  assert.equal(body.total, 2);
});

test('search by pillar matches via pillars list', async () => {
  const r = await tryMCP(req('/mcp/v1/search?tag=ai'));
  assert.equal(r.status, 200);
  const body = await r.json();
  assert.equal(body.total, 1);
  assert.equal(body.resources[0].name, 'CloudCDN blueprint');
});

test('search with neither q nor tag returns empty', async () => {
  const r = await tryMCP(req('/mcp/v1/search'));
  const body = await r.json();
  assert.equal(body.total, 0);
});

test('search applies limit', async () => {
  const r = await tryMCP(req('/mcp/v1/search?tag=infra&limit=1'));
  const body = await r.json();
  assert.equal(body.resources.length, 1);
  assert.ok(body.total >= 1);
});

test('search returns query echo for both q and tag', async () => {
  const r = await tryMCP(req('/mcp/v1/search?q=cloud&tag=infra'));
  const body = await r.json();
  assert.equal(body.query.q, 'cloud');
  assert.equal(body.query.tag, 'infra');
});

test('search + list tolerate records missing optional fields', async () => {
  // Stub a manifest where one record is bare-minimum — no tags, no
  // pillars, no lang, no license, no summary, no title — exercises the
  // `|| 'en'` / `|| []` / `|| ''` fallbacks in resourceToMcp +
  // handleSearch's `(rec.tags || []).map(...)` and the empty-haystack
  // string concat.
  const skinny = {
    version: '1.0',
    total: 1,
    resources: [{ slug: 'bare', url: `${BASE}/bare/` }],
  };
  const realF = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) return new Response(JSON.stringify(skinny), { status: 200 });
    return new Response('', { status: 502 });
  };
  try {
    const r = await tryMCP(req('/mcp/v1/list_resources'));
    const body = await r.json();
    assert.equal(body.resources[0].lang, 'en');
    assert.equal(body.resources[0].license, 'CC-BY-4.0');
    assert.deepEqual(body.resources[0].tags, []);
    assert.deepEqual(body.resources[0].pillars, []);
    // Search by tag misses (no tags) — should return empty
    const s = await tryMCP(req('/mcp/v1/search?tag=anything'));
    assert.equal((await s.json()).total, 0);
    // Search by q misses too (no title/summary to match)
    const s2 = await tryMCP(req('/mcp/v1/search?q=anything'));
    assert.equal((await s2.json()).total, 0);
  } finally {
    globalThis.fetch = realF;
  }
});

test('read_resource metadata defaults when feed record is bare', async () => {
  // The manifest is fine, but the feed.jsonl record for the same slug
  // is missing license + tags + pillars — exercise the `|| 'CC-BY-4.0'`
  // and `|| []` fallbacks in handleReadResource.
  const realF = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) return new Response(JSON.stringify(MANIFEST), { status: 200 });
    if (url.endsWith('/feed.jsonl')) {
      return new Response(
        JSON.stringify({ url: `${BASE}/2026-06-11-cloudcdn/` }) + '\n',
        { status: 200 },
      );
    }
    return new Response('', { status: 502 });
  };
  try {
    const r = await tryMCP(req('/mcp/v1/read_resource?uri=2026-06-11-cloudcdn'));
    assert.equal(r.status, 200);
    const body = await r.json();
    assert.equal(body.contents[0].metadata.license, 'CC-BY-4.0');
    assert.deepEqual(body.contents[0].metadata.tags, []);
    assert.deepEqual(body.contents[0].metadata.pillars, []);
    assert.equal(body.contents[0].text, '');
  } finally {
    globalThis.fetch = realF;
  }
});

// ---------------------------------------------------------------------------
// Method + error paths
// ---------------------------------------------------------------------------

test('OPTIONS returns 204 with CORS headers', async () => {
  const r = await tryMCP(req('/mcp/v1/list_resources', 'OPTIONS'));
  assert.equal(r.status, 204);
  assert.equal(r.headers.get('Access-Control-Allow-Origin'), '*');
});

test('POST returns 405 method-not-allowed', async () => {
  const r = await tryMCP(req('/mcp/v1/list_resources', 'POST'));
  assert.equal(r.status, 405);
  const body = await r.json();
  assert.equal(body.error.code, 'method-not-allowed');
});

test('unknown /mcp/v1/* sub-route returns 404', async () => {
  const r = await tryMCP(req('/mcp/v1/unknown'));
  assert.equal(r.status, 404);
  const body = await r.json();
  assert.equal(body.error.code, 'unknown-route');
});

test('manifest fetch failure → 503 manifest-unavailable', async () => {
  const realF = globalThis.fetch;
  globalThis.fetch = async () => new Response('', { status: 503 });
  try {
    const r = await tryMCP(req('/mcp/v1/list_resources'));
    assert.equal(r.status, 503);
    const body = await r.json();
    assert.equal(body.error.code, 'manifest-unavailable');
  } finally {
    globalThis.fetch = realF;
  }
});

// ---------------------------------------------------------------------------
// Cache headers — every successful response is Edge-cacheable for 24h
// ---------------------------------------------------------------------------

test('every 2xx response carries immutable cache headers', async () => {
  const r = await tryMCP(req('/mcp/v1/list_resources'));
  assert.equal(r.headers.get('Cache-Control'), 'public, max-age=86400, immutable');
  assert.match(r.headers.get('Content-Type'), /application\/json/);
});

test('error responses do NOT carry immutable cache (they should retry quickly)', async () => {
  const r = await tryMCP(req('/mcp/v1/read_resource'));
  assert.equal(r.headers.get('Cache-Control'), 'no-store');
});
