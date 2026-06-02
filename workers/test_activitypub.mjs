#!/usr/bin/env node
/**
 * Tests for workers/activitypub.js — pure-logic + integrated route dispatch.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_activitypub.mjs
 *
 * No Cloudflare runtime is required — Node 18+'s native Response, Headers,
 * URL globals are sufficient. The outbox tests inject a fake fetchOrigin
 * so we don't touch the real CDN.
 */
import { test } from 'node:test';
import { strict as assert } from 'node:assert';

import {
  AP_ROUTES,
  webfinger,
  actor,
  outbox,
  inbox,
  tryActivityPub,
} from './activitypub.js';

const BASE = 'https://sebastienrousseau.com';
const ACCT = 'acct:sebastien@sebastienrousseau.com';

function get(path) {
  return new Request(`${BASE}${path}`);
}
function post(path, body = '') {
  return new Request(`${BASE}${path}`, { method: 'POST', body });
}

// ---------------------------------------------------------------------------
// AP_ROUTES exports
// ---------------------------------------------------------------------------

test('AP_ROUTES exposes the four expected paths', () => {
  assert.equal(AP_ROUTES.size, 4);
  for (const p of ['/.well-known/webfinger', '/actor', '/inbox', '/outbox']) {
    assert.ok(AP_ROUTES.has(p), `missing ${p}`);
  }
});

// ---------------------------------------------------------------------------
// /.well-known/webfinger
// ---------------------------------------------------------------------------

test('webfinger: 400 when resource param missing', async () => {
  const r = webfinger(get('/.well-known/webfinger'));
  assert.equal(r.status, 400);
});

test('webfinger: 404 when resource is not the canonical actor', async () => {
  const r = webfinger(get('/.well-known/webfinger?resource=acct:bob@example.com'));
  assert.equal(r.status, 404);
});

test('webfinger: 200 + JRD body for canonical acct: form', async () => {
  const r = webfinger(get(`/.well-known/webfinger?resource=${encodeURIComponent(ACCT)}`));
  assert.equal(r.status, 200);
  assert.match(r.headers.get('content-type'), /jrd\+json/);
  const body = await r.json();
  assert.equal(body.subject, ACCT);
  assert.ok(Array.isArray(body.aliases));
  assert.ok(body.links.find((l) => l.rel === 'self' && l.type === 'application/activity+json'));
  assert.ok(body.links.find((l) => l.rel === 'http://webfinger.net/rel/avatar'));
});

test('webfinger: accepts the bare-username form', async () => {
  const r = webfinger(get('/.well-known/webfinger?resource=acct:sebastien'));
  assert.equal(r.status, 200);
});

test('webfinger: accepts actor URL as the resource', async () => {
  const r = webfinger(
    get(`/.well-known/webfinger?resource=${encodeURIComponent(`${BASE}/actor`)}`),
  );
  assert.equal(r.status, 200);
});

test('webfinger: accepts profile URL as the resource', async () => {
  const r = webfinger(
    get(`/.well-known/webfinger?resource=${encodeURIComponent(`${BASE}/about/`)}`),
  );
  assert.equal(r.status, 200);
});

// ---------------------------------------------------------------------------
// /actor
// ---------------------------------------------------------------------------

test('actor: returns a Person object with the expected fields', async () => {
  const r = actor();
  assert.equal(r.status, 200);
  assert.match(r.headers.get('content-type'), /activity\+json/);
  const body = await r.json();
  assert.equal(body.type, 'Person');
  assert.equal(body.preferredUsername, 'sebastien');
  assert.equal(body.id, `${BASE}/actor`);
  assert.equal(body.inbox, `${BASE}/inbox`);
  assert.equal(body.outbox, `${BASE}/outbox`);
  assert.ok(body.publicKey?.publicKeyPem?.includes('BEGIN PUBLIC KEY'));
  assert.deepEqual(body['@context'], [
    'https://www.w3.org/ns/activitystreams',
    'https://w3id.org/security/v1',
  ]);
});

// ---------------------------------------------------------------------------
// /outbox
// ---------------------------------------------------------------------------

const fakeOrigin = (data, opts = {}) =>
  async (_url) =>
    new Response(typeof data === 'string' ? data : JSON.stringify(data), {
      status: opts.status ?? 200,
      headers: { 'content-type': 'application/json' },
    });

test('outbox: empty OrderedCollection when origin returns empty', async () => {
  const r = await outbox(get('/outbox'), fakeOrigin({ posts: [] }));
  const body = await r.json();
  assert.equal(body.type, 'OrderedCollection');
  assert.equal(body.totalItems, 0);
  assert.deepEqual(body.orderedItems, []);
});

test('outbox: transforms posts into Create + Article activities', async () => {
  const fixture = {
    posts: [
      {
        url: `${BASE}/2026-06-02-banking-infrastructure-index/`,
        title: 'Banking Infrastructure Index',
        description: 'Five metrics that bound 2026.',
        date: '2026-06-02T05:00:00Z',
      },
      {
        slug: '2026-05-29-iso-20022-after-migration',
        name: 'ISO 20022 after migration',
        summary: 'What changes once the cutover lands.',
        published: '2026-05-29T05:00:00Z',
      },
    ],
  };
  const r = await outbox(get('/outbox'), fakeOrigin(fixture));
  const body = await r.json();
  assert.equal(body.totalItems, 2);
  const first = body.orderedItems[0];
  assert.equal(first.type, 'Create');
  assert.equal(first.object.type, 'Article');
  assert.equal(first.object.name, 'Banking Infrastructure Index');
  assert.equal(first.object.url, `${BASE}/2026-06-02-banking-infrastructure-index/`);
  assert.deepEqual(first.to, ['https://www.w3.org/ns/activitystreams#Public']);

  const second = body.orderedItems[1];
  assert.equal(second.object.url, `${BASE}/2026-05-29-iso-20022-after-migration/`);
  assert.equal(second.object.name, 'ISO 20022 after migration');
});

test('outbox: defensive against missing fields in posts', async () => {
  const r = await outbox(get('/outbox'), fakeOrigin({ posts: [{}] }));
  const body = await r.json();
  assert.equal(body.totalItems, 1);
  assert.equal(body.orderedItems[0].object.name, '(untitled)');
  assert.equal(body.orderedItems[0].object.url, `${BASE}/actor`);
});

test('outbox: accepts a bare-array response shape', async () => {
  const r = await outbox(get('/outbox'), fakeOrigin([{ title: 'x', slug: 'x' }]));
  const body = await r.json();
  assert.equal(body.totalItems, 1);
});

test('outbox: empty list when origin fetch returns non-ok', async () => {
  const r = await outbox(get('/outbox'), fakeOrigin('boom', { status: 502 }));
  const body = await r.json();
  assert.equal(body.totalItems, 0);
});

test('outbox: empty list when origin fetch throws', async () => {
  const throwingFetch = async () => {
    throw new Error('network down');
  };
  const r = await outbox(get('/outbox'), throwingFetch);
  const body = await r.json();
  assert.equal(body.totalItems, 0);
});

test('outbox: empty list when origin returns malformed JSON shape', async () => {
  const r = await outbox(get('/outbox'), fakeOrigin({ no_posts_field: true }));
  const body = await r.json();
  assert.equal(body.totalItems, 0);
});

test('outbox: caps at 20 items', async () => {
  const posts = Array.from({ length: 50 }, (_, i) => ({
    title: `post ${i}`,
    slug: `post-${i}`,
    date: `2026-06-${String(i + 1).padStart(2, '0')}T00:00:00Z`,
  }));
  const r = await outbox(get('/outbox'), fakeOrigin({ posts }));
  const body = await r.json();
  assert.equal(body.totalItems, 20);
});

// ---------------------------------------------------------------------------
// /inbox
// ---------------------------------------------------------------------------

test('inbox: 202 on POST', async () => {
  const r = inbox(post('/inbox', '{}'));
  assert.equal(r.status, 202);
});

test('inbox: 405 on GET', async () => {
  const r = inbox(get('/inbox'));
  assert.equal(r.status, 405);
  assert.equal(r.headers.get('allow'), 'POST');
});

// ---------------------------------------------------------------------------
// tryActivityPub dispatcher
// ---------------------------------------------------------------------------

test('tryActivityPub: returns null for non-AP routes', async () => {
  const r = await tryActivityPub(get('/about/'));
  assert.equal(r, null);
});

test('tryActivityPub: webfinger', async () => {
  const r = await tryActivityPub(get(`/.well-known/webfinger?resource=${encodeURIComponent(ACCT)}`));
  assert.equal(r.status, 200);
});

test('tryActivityPub: actor', async () => {
  const r = await tryActivityPub(get('/actor'));
  assert.equal(r.status, 200);
});

test('tryActivityPub: outbox', async () => {
  const r = await tryActivityPub(get('/outbox'), fakeOrigin({ posts: [] }));
  assert.equal(r.status, 200);
});

test('tryActivityPub: inbox POST', async () => {
  const r = await tryActivityPub(post('/inbox'));
  assert.equal(r.status, 202);
});
