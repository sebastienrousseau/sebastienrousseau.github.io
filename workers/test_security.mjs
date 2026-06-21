#!/usr/bin/env node
/**
 * Tests for workers/security.js — UA/ASN pre-filter that guards any
 * future KV-write endpoint.
 */
import { test } from 'node:test';
import { strict as assert } from 'node:assert';

import {
  UA_DENYLIST,
  ASN_DENYLIST,
  classifyRequest,
  rejectionResponse,
  guardMutatingEndpoint,
} from './security.js';

function makeReq({ ua, asn } = {}) {
  const headers = ua ? { 'user-agent': ua } : {};
  // Node Request doesn't carry .cf, but the Worker runtime exposes it as a
  // plain object property — we simulate that.
  const req = new Request('https://sebastienrousseau.com/api/sample', { headers });
  if (asn !== undefined) Object.defineProperty(req, 'cf', { value: { asn } });
  return req;
}

// ---------------------------------------------------------------------------
// UA matching
// ---------------------------------------------------------------------------

test('UA_DENYLIST entries are all lower-case', () => {
  for (const tok of UA_DENYLIST) {
    assert.equal(tok, tok.toLowerCase(), `denylist entry should be lower-case: ${tok}`);
  }
});

test('classifyRequest: GPTBot is blocked', () => {
  const v = classifyRequest(makeReq({ ua: 'Mozilla/5.0 (compatible; GPTBot/1.0)' }));
  assert.equal(v.blocked, true);
  assert.equal(v.reason, 'ua:gptbot');
});

test('classifyRequest: ClaudeBot is blocked (case-insensitive)', () => {
  const v = classifyRequest(makeReq({ ua: 'CLAUDEBOT/1.0' }));
  assert.equal(v.blocked, true);
});

test('classifyRequest: curl/7 is blocked', () => {
  const v = classifyRequest(makeReq({ ua: 'curl/7.85.0' }));
  assert.equal(v.blocked, true);
  assert.equal(v.reason, 'ua:curl/7');
});

test('classifyRequest: real browser UA is allowed', () => {
  const v = classifyRequest(makeReq({
    ua: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
  }));
  assert.equal(v.blocked, false);
  assert.equal(v.reason, null);
});

test('classifyRequest: missing UA is allowed (don\'t deny on absence — false positives)', () => {
  const v = classifyRequest(makeReq({}));
  assert.equal(v.blocked, false);
});

// ---------------------------------------------------------------------------
// ASN matching
// ---------------------------------------------------------------------------

test('classifyRequest: ASN in denylist is blocked', () => {
  const v = classifyRequest(makeReq({ asn: 16509 }));
  assert.equal(v.blocked, true);
  assert.equal(v.reason, 'asn:16509');
});

test('classifyRequest: residential ASN is allowed', () => {
  const v = classifyRequest(makeReq({ asn: 12876 }));
  assert.equal(v.blocked, false);
});

test('classifyRequest: missing cf.asn falls through (no throw)', () => {
  const req = new Request('https://x/');
  assert.doesNotThrow(() => classifyRequest(req));
});

// ---------------------------------------------------------------------------
// rejectionResponse
// ---------------------------------------------------------------------------

test('rejectionResponse: 403 with no-store + private deny-reason header', () => {
  const r = rejectionResponse({ reason: 'ua:gptbot' });
  assert.equal(r.status, 403);
  assert.equal(r.headers.get('cache-control'), 'no-store');
  assert.equal(r.headers.get('x-router-deny-reason'), 'ua:gptbot');
});

test('rejectionResponse: null reason falls back to "unknown"', () => {
  const r = rejectionResponse({ reason: null });
  assert.equal(r.headers.get('x-router-deny-reason'), 'unknown');
});

// ---------------------------------------------------------------------------
// guardMutatingEndpoint
// ---------------------------------------------------------------------------

test('guardMutatingEndpoint: bot request → 403', () => {
  const r = guardMutatingEndpoint(makeReq({ ua: 'GPTBot/1.0' }));
  assert.ok(r);
  assert.equal(r.status, 403);
});

test('guardMutatingEndpoint: human request → null', () => {
  const r = guardMutatingEndpoint(makeReq({ ua: 'Mozilla/5.0 Chrome/120' }));
  assert.equal(r, null);
});

test('ASN_DENYLIST is a Set of numbers', () => {
  assert.ok(ASN_DENYLIST instanceof Set);
  for (const a of ASN_DENYLIST) assert.equal(typeof a, 'number');
});
