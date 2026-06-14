#!/usr/bin/env node
/**
 * Tests for workers/pdf-proxy.js.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_pdf_proxy.mjs
 *
 * No Cloudflare runtime needed; globalThis.fetch is stubbed for every
 * upstream call so the tests are hermetic and zero-network.
 */
import { test, before, after } from 'node:test';
import { strict as assert } from 'node:assert';

import { isPDFRoute, tryPDF } from './pdf-proxy.js';

const BASE = 'https://sebastienrousseau.com';
const FAKE_PDF = new Uint8Array([0x25, 0x50, 0x44, 0x46]); // "%PDF"

const realFetch = globalThis.fetch;
before(() => {
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.includes('/render?slug=ok-slug')) {
      return new Response(FAKE_PDF, { status: 200, headers: { 'Content-Type': 'application/pdf' } });
    }
    if (url.includes('/render?slug=missing-slug')) {
      return new Response('', { status: 404 });
    }
    if (url.includes('/render?slug=broken-slug')) {
      return new Response('', { status: 500 });
    }
    if (url.includes('/render?slug=throw-slug')) {
      throw new Error('fly down');
    }
    return new Response('', { status: 502 });
  };
});
after(() => {
  globalThis.fetch = realFetch;
});

function req(path, method = 'GET') {
  return new Request(`${BASE}${path}`, { method });
}

// ---------------------------------------------------------------------------
// isPDFRoute
// ---------------------------------------------------------------------------

test('isPDFRoute matches /api/pdf/<slug>.pdf and rejects others', () => {
  assert.equal(isPDFRoute('/api/pdf/2026-06-08-banking-resilience-index.pdf'), true);
  assert.equal(isPDFRoute('/api/pdf/abc.pdf'), true);
  assert.equal(isPDFRoute('/api/pdf/'), false);
  assert.equal(isPDFRoute('/api/pdf/foo'), false);
  assert.equal(isPDFRoute('/api/pdf/sub/foo.pdf'), false);
  assert.equal(isPDFRoute('/articles/'), false);
  assert.equal(isPDFRoute('/api/pdf/foo.pdf.bak'), false);
});

// ---------------------------------------------------------------------------
// tryPDF — pass-through cases
// ---------------------------------------------------------------------------

test('tryPDF returns null for non-PDF paths', async () => {
  assert.equal(await tryPDF(req('/articles/')), null);
  assert.equal(await tryPDF(req('/api/pdf/')), null);
  assert.equal(await tryPDF(req('/')), null);
});

// ---------------------------------------------------------------------------
// Happy path
// ---------------------------------------------------------------------------

test('valid slug → 200 PDF with immutable cache + inline disposition', async () => {
  const r = await tryPDF(req('/api/pdf/ok-slug.pdf'));
  assert.equal(r.status, 200);
  assert.equal(r.headers.get('Content-Type'), 'application/pdf');
  assert.equal(r.headers.get('Cache-Control'), 'public, max-age=86400, immutable');
  assert.match(r.headers.get('Content-Disposition'), /inline; filename="ok-slug\.pdf"/);
  const bytes = new Uint8Array(await r.arrayBuffer());
  assert.deepEqual(Array.from(bytes), [0x25, 0x50, 0x44, 0x46]);
});

test('HEAD also accepted', async () => {
  const r = await tryPDF(req('/api/pdf/ok-slug.pdf', 'HEAD'));
  assert.equal(r.status, 200);
});

// ---------------------------------------------------------------------------
// Slug validation
// ---------------------------------------------------------------------------

test('invalid slug (uppercase, dot, traversal) → 400', async () => {
  const r = await tryPDF(req('/api/pdf/UPPER.pdf'));
  assert.equal(r.status, 400);
  const body = await r.json();
  assert.equal(body.error.code, 'invalid-slug');
});

test('invalid slug starting with hyphen → 400', async () => {
  const r = await tryPDF(req('/api/pdf/-leading-hyphen.pdf'));
  assert.equal(r.status, 400);
});

test('invalid slug too long → 400', async () => {
  const r = await tryPDF(req(`/api/pdf/${'a'.repeat(200)}.pdf`));
  assert.equal(r.status, 400);
});

// ---------------------------------------------------------------------------
// Upstream errors
// ---------------------------------------------------------------------------

test('upstream 404 → 404 article-not-found', async () => {
  const r = await tryPDF(req('/api/pdf/missing-slug.pdf'));
  assert.equal(r.status, 404);
  const body = await r.json();
  assert.equal(body.error.code, 'article-not-found');
});

test('upstream 500 → 502 render-error', async () => {
  const r = await tryPDF(req('/api/pdf/broken-slug.pdf'));
  assert.equal(r.status, 502);
  const body = await r.json();
  assert.equal(body.error.code, 'render-error');
});

test('fetch throw → 503 render-unavailable', async () => {
  const r = await tryPDF(req('/api/pdf/throw-slug.pdf'));
  assert.equal(r.status, 503);
  const body = await r.json();
  assert.equal(body.error.code, 'render-unavailable');
});

test('fetch throw without message → 503 with fallback message', async () => {
  const realF = globalThis.fetch;
  globalThis.fetch = async () => {
    const err = new Error();
    err.message = '';
    throw err;
  };
  try {
    const r = await tryPDF(req('/api/pdf/ok-slug.pdf'));
    assert.equal(r.status, 503);
    const body = await r.json();
    assert.equal(body.error.message, 'fly fetch failed');
  } finally {
    globalThis.fetch = realF;
  }
});

// ---------------------------------------------------------------------------
// Method gate
// ---------------------------------------------------------------------------

test('POST → 405 method-not-allowed', async () => {
  const r = await tryPDF(req('/api/pdf/ok-slug.pdf', 'POST'));
  assert.equal(r.status, 405);
  const body = await r.json();
  assert.equal(body.error.code, 'method-not-allowed');
});

// ---------------------------------------------------------------------------
// Custom base
// ---------------------------------------------------------------------------

test('tryPDF accepts a custom base origin', async () => {
  const realF = globalThis.fetch;
  let lastUrl = null;
  globalThis.fetch = async (input) => {
    lastUrl = typeof input === 'string' ? input : input.url;
    return new Response(FAKE_PDF, { status: 200 });
  };
  try {
    const r = await tryPDF(req('/api/pdf/ok-slug.pdf'), 'https://staging-pdf.fly.dev');
    assert.equal(r.status, 200);
    assert.equal(lastUrl, 'https://staging-pdf.fly.dev/render?slug=ok-slug');
  } finally {
    globalThis.fetch = realF;
  }
});
