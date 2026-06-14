#!/usr/bin/env node
/**
 * Tests for workers/lang-router.js — pure-logic + integrated fetch handler.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_lang_router.mjs
 *
 * The Cloudflare runtime isn't installed here, so we use Node's native
 * Response/Headers/URL globals (Node 18+) and override globalThis.fetch
 * to capture pass-through scenarios without touching the network.
 */
import { test, before, after } from 'node:test';
import { strict as assert } from 'node:assert';

import handler, {
  isPageNavigation,
  getCookie,
  ACTIVE_LANGS,
  buildCspHeader,
  withSecurityHeaders,
  CSP_DIRECTIVES,
  SECURITY_HEADERS,
} from './lang-router.js';

// ---------------------------------------------------------------------------
// fetch stub: capture pass-through requests and return a canned 200 body.
// ---------------------------------------------------------------------------

const realFetch = globalThis.fetch;
let passThroughLog = [];

before(() => {
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    passThroughLog.push(url);
    return new Response('<!doctype html><title>ok</title>', {
      status: 200,
      headers: { 'content-type': 'text/html; charset=utf-8' },
    });
  };
});

after(() => {
  globalThis.fetch = realFetch;
});

function resetLog() {
  passThroughLog = [];
}

function makeRequest(url, opts = {}) {
  // The Worker only reads .method, .url, .headers — Node's Request honours
  // GET-with-Body restrictions, so build manually when we need POST with
  // a header-only payload.
  const headers = new Headers(opts.headers || {});
  return new Request(url, { method: opts.method || 'GET', headers });
}

async function callHandler(request) {
  return handler.fetch(request, {}, {});
}

// ---------------------------------------------------------------------------
// MCP route fall-through: when tryMCP returns a Response, lang-router
// returns it directly (locale routing doesn't apply to API endpoints).
// ---------------------------------------------------------------------------

test('MCP /mcp/v1/list_resources short-circuits locale routing', async () => {
  const realF = globalThis.fetch;
  globalThis.fetch = async (input) => {
    const url = typeof input === 'string' ? input : input.url;
    if (url.endsWith('/api/mcp-resources.json')) {
      return new Response(JSON.stringify({ version: '1.0', total: 0, resources: [] }), { status: 200 });
    }
    return new Response('', { status: 502 });
  };
  try {
    const res = await callHandler(new Request('https://sebastienrousseau.com/mcp/v1/list_resources'));
    assert.equal(res.status, 200);
    assert.match(res.headers.get('Content-Type'), /application\/json/);
    const body = await res.json();
    assert.deepEqual(body.resources, []);
  } finally {
    globalThis.fetch = realF;
  }
});

// ---------------------------------------------------------------------------
// isPageNavigation
// ---------------------------------------------------------------------------

test('isPageNavigation: root paths are navigable', () => {
  assert.equal(isPageNavigation('/'), true);
  assert.equal(isPageNavigation('/index.html'), true);
  assert.equal(isPageNavigation('/about/index.html'), true);
});

test('isPageNavigation: asset extensions are not', () => {
  assert.equal(isPageNavigation('/main.js'), false);
  assert.equal(isPageNavigation('/sitemap.xml'), false);
  assert.equal(isPageNavigation('/x.css'), false);
  assert.equal(isPageNavigation('/x.WEBP'), false, 'extension match is case-insensitive');
  assert.equal(isPageNavigation('/x.woff2'), false);
  assert.equal(isPageNavigation('/x.pdf'), false);
  assert.equal(isPageNavigation('/x.wasm'), false);
});

test('isPageNavigation: API + well-known + CSP-internal paths excluded', () => {
  assert.equal(isPageNavigation('/api/agents/posts.json'), false);
  assert.equal(isPageNavigation('/.well-known/ai-plugin.json'), false);
  assert.equal(isPageNavigation('/_csp/main.abcd.css'), false);
  assert.equal(isPageNavigation('/v1/echo'), false);
});

test('isPageNavigation: already-inside-lang subtree excluded', () => {
  assert.equal(isPageNavigation('/fr/'), false);
  assert.equal(isPageNavigation('/zh-hans/about/index.html'), false);
  assert.equal(isPageNavigation('/FR/something'), false, 'lang segment is case-insensitive');
});

test('isPageNavigation: unknown first segment is navigable', () => {
  assert.equal(isPageNavigation('/papers/index.html'), true);
});

// ---------------------------------------------------------------------------
// getCookie
// ---------------------------------------------------------------------------

test('getCookie: returns first match by name', () => {
  assert.equal(getCookie('pref-lang=fr; other=baz', 'pref-lang'), 'fr');
  assert.equal(getCookie('a=b; pref-lang=zh-hans; c=d', 'pref-lang'), 'zh-hans');
});

test('getCookie: null / absent header → null', () => {
  assert.equal(getCookie(null, 'pref-lang'), null);
  assert.equal(getCookie('', 'pref-lang'), null);
});

test('getCookie: missing name → null', () => {
  assert.equal(getCookie('other=value', 'pref-lang'), null);
});

test('getCookie: tolerates "=" inside cookie value', () => {
  assert.equal(getCookie('pref-lang=a=b', 'pref-lang'), 'a=b');
});

// ---------------------------------------------------------------------------
// ACTIVE_LANGS hygiene
// ---------------------------------------------------------------------------

test('ACTIVE_LANGS entries are lowercase', () => {
  for (const l of ACTIVE_LANGS) {
    assert.equal(l, l.toLowerCase(), `ACTIVE_LANGS entry ${l} should be lowercase`);
  }
});

test('ACTIVE_LANGS includes the 27 site languages', () => {
  // Spot-check a few that have unusual fold rules.
  for (const l of ['fr', 'pt-br', 'zh-hans', 'zh-hant', 'fil', 'uk', 'yo']) {
    assert.ok(ACTIVE_LANGS.has(l), `expected ${l} in ACTIVE_LANGS`);
  }
});

// ---------------------------------------------------------------------------
// buildCspHeader / CSP_DIRECTIVES
// ---------------------------------------------------------------------------

test('buildCspHeader: joins directives with "; "', () => {
  const header = buildCspHeader();
  assert.ok(typeof header === 'string');
  assert.ok(!header.includes('\n'), 'CSP header must be a single line');
});

test('CSP header allows formspree submissions (the bug this PR fixes)', () => {
  const header = buildCspHeader();
  assert.match(header, /form-action 'self' https:\/\/formspree\.io/);
});

test('CSP header includes frame-ancestors none', () => {
  const header = buildCspHeader();
  assert.match(header, /frame-ancestors 'none'/);
});

test('CSP header includes upgrade-insecure-requests', () => {
  assert.match(buildCspHeader(), /upgrade-insecure-requests/);
});

test('CSP header has all required directives', () => {
  const header = buildCspHeader();
  for (const directive of [
    'default-src', 'base-uri', 'form-action', 'object-src',
    'frame-ancestors', 'upgrade-insecure-requests', 'script-src',
    'frame-src', 'connect-src', 'img-src', 'style-src', 'font-src',
    'media-src',
  ]) {
    assert.match(header, new RegExp(`\\b${directive}\\b`), `expected ${directive}`);
  }
});

test('CSP_DIRECTIVES is a non-empty array of strings', () => {
  assert.ok(Array.isArray(CSP_DIRECTIVES));
  assert.ok(CSP_DIRECTIVES.length > 0);
  for (const d of CSP_DIRECTIVES) {
    assert.equal(typeof d, 'string');
    assert.ok(d.length > 0);
    assert.ok(!d.endsWith(';'), 'directives must not be pre-terminated');
  }
});

// ---------------------------------------------------------------------------
// SECURITY_HEADERS
// ---------------------------------------------------------------------------

test('SECURITY_HEADERS contains the canonical set', () => {
  for (const name of [
    'Content-Security-Policy',
    'Strict-Transport-Security',
    'X-Content-Type-Options',
    'Referrer-Policy',
    'Permissions-Policy',
    'Cross-Origin-Opener-Policy',
  ]) {
    assert.ok(name in SECURITY_HEADERS, `missing ${name}`);
    assert.equal(typeof SECURITY_HEADERS[name], 'string');
    assert.ok(SECURITY_HEADERS[name].length > 0);
  }
});

test('HSTS is set for 2 years + includeSubDomains + preload', () => {
  assert.match(SECURITY_HEADERS['Strict-Transport-Security'], /max-age=63072000/);
  assert.match(SECURITY_HEADERS['Strict-Transport-Security'], /includeSubDomains/);
  assert.match(SECURITY_HEADERS['Strict-Transport-Security'], /preload/);
});

test('Permissions-Policy disables high-risk surfaces', () => {
  const pp = SECURITY_HEADERS['Permissions-Policy'];
  for (const feature of ['browsing-topics', 'interest-cohort', 'camera', 'microphone', 'geolocation']) {
    assert.match(pp, new RegExp(`${feature}=\\(\\)`), `expected ${feature}=()`);
  }
});

// ---------------------------------------------------------------------------
// withSecurityHeaders
// ---------------------------------------------------------------------------

test('withSecurityHeaders applies all SECURITY_HEADERS', () => {
  const upstream = new Response('hi', {
    status: 200,
    headers: { 'content-type': 'text/html' },
  });
  const wrapped = withSecurityHeaders(upstream);
  for (const name of Object.keys(SECURITY_HEADERS)) {
    assert.equal(wrapped.headers.get(name), SECURITY_HEADERS[name]);
  }
});

test('withSecurityHeaders preserves existing headers', () => {
  const upstream = new Response('hi', {
    status: 200,
    headers: { 'content-type': 'text/html', 'x-trace-id': 'abc' },
  });
  const wrapped = withSecurityHeaders(upstream);
  assert.equal(wrapped.headers.get('content-type'), 'text/html');
  assert.equal(wrapped.headers.get('x-trace-id'), 'abc');
});

test('withSecurityHeaders preserves status + statusText', () => {
  const upstream = new Response('hi', { status: 418, statusText: "I'm a teapot" });
  const wrapped = withSecurityHeaders(upstream);
  assert.equal(wrapped.status, 418);
  assert.equal(wrapped.statusText, "I'm a teapot");
});

test('withSecurityHeaders overrides any upstream CSP', () => {
  const upstream = new Response('hi', {
    headers: { 'content-security-policy': 'default-src none' },
  });
  const wrapped = withSecurityHeaders(upstream);
  assert.equal(
    wrapped.headers.get('content-security-policy'),
    SECURITY_HEADERS['Content-Security-Policy'],
  );
});

test('withSecurityHeaders extraHeaders appends without replacing', () => {
  const upstream = new Response('hi', {
    headers: { 'set-cookie': 'pre=existing' },
  });
  const wrapped = withSecurityHeaders(upstream, { 'Set-Cookie': 'pref-lang=fr; Path=/' });
  // The Headers API exposes Set-Cookie via getSetCookie() (or as a
  // comma-joined string from .get()). Check both pre-existing and new
  // values are present.
  const cookies = typeof wrapped.headers.getSetCookie === 'function'
    ? wrapped.headers.getSetCookie()
    : (wrapped.headers.get('set-cookie') || '').split(',').map(s => s.trim());
  assert.ok(cookies.some(c => c.includes('pre=existing')), 'pre-existing cookie preserved');
  assert.ok(cookies.some(c => c.includes('pref-lang=fr')), 'new cookie appended');
});

test('withSecurityHeaders sets default validation Cache-Control for non-static assets', () => {
  const upstream = new Response('hi');
  const req = new Request('https://example.com/about/index.html');
  const wrapped = withSecurityHeaders(upstream, req);
  assert.equal(wrapped.headers.get('Cache-Control'), 'public, max-age=0, must-revalidate');
});

test('withSecurityHeaders sets immutable Cache-Control for static assets', () => {
  const assets = [
    'https://example.com/fonts/inter.woff2',
    'https://example.com/_csp/styles.css',
    'https://example.com/main.1234abcd.js',
    'https://example.com/theme.5678ef01.css',
    'https://example.com/image.webp',
    'https://example.com/doc.pdf',
    'https://example.com/demo.wasm',
  ];
  for (const url of assets) {
    const upstream = new Response('asset');
    const req = new Request(url);
    const wrapped = withSecurityHeaders(upstream, req);
    assert.equal(
      wrapped.headers.get('Cache-Control'),
      'public, max-age=31536000, immutable',
      `expected immutable cache for ${url}`
    );
  }
});

test('withSecurityHeaders overrides Cache-Control to private/no-store when Set-Cookie is present', () => {
  const upstream = new Response('cookie-content', {
    headers: { 'Set-Cookie': 'session=xyz' }
  });
  const wrapped = withSecurityHeaders(upstream);
  assert.equal(wrapped.headers.get('Cache-Control'), 'no-store, private');
});

test('withSecurityHeaders works on a 302 redirect response', () => {
  const upstream = Response.redirect('https://example.com/fr/', 302);
  const wrapped = withSecurityHeaders(upstream);
  assert.equal(wrapped.status, 302);
  assert.equal(wrapped.headers.get('location'), 'https://example.com/fr/');
  assert.equal(
    wrapped.headers.get('content-security-policy'),
    SECURITY_HEADERS['Content-Security-Policy'],
  );
});

// ---------------------------------------------------------------------------
// Integrated handler.fetch — covers every branch of the routing decision tree.
// ---------------------------------------------------------------------------

test('handler: POST request passes through with security headers', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/api/echo', {
    method: 'POST',
    headers: { 'x-test': '1' },
  });
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
  assert.equal(res.headers.get('content-security-policy'),
    SECURITY_HEADERS['Content-Security-Policy']);
});

test('handler: HEAD with pref-lang cookie still redirects', async () => {
  // HEAD requests run through the routing decision tree like GETs.
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/', {
    method: 'HEAD',
    headers: { Cookie: 'pref-lang=fr' },
  });
  const res = await callHandler(req);
  assert.equal(res.status, 302);
  assert.equal(res.headers.get('location'), 'https://sebastienrousseau.com/fr/');
});

test('handler: Cookie present but no pref-lang key → pass-through (no auto-redirect)', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/', {
    headers: { Cookie: 'other=value; theme=dark', 'Accept-Language': 'fr' },
  });
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: asset request bypasses redirect, gets security headers', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/sitemap.xml');
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
  assert.ok(res.headers.get('content-security-policy'));
});

test('handler: cookie pref-lang=en passes through (opt-out)', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/', {
    headers: { Cookie: 'pref-lang=en' },
  });
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: cookie pref-lang=fr redirects to /fr/', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/', {
    headers: { Cookie: 'pref-lang=fr' },
  });
  const res = await callHandler(req);
  assert.equal(res.status, 302);
  assert.equal(res.headers.get('location'), 'https://sebastienrousseau.com/fr/');
  assert.equal(passThroughLog.length, 0, 'no upstream fetch on redirect');
});

test('handler: cookie pref-lang=fr on /papers/ redirects to /fr/papers/', async () => {
  const req = makeRequest('https://sebastienrousseau.com/papers/index.html', {
    headers: { Cookie: 'pref-lang=fr' },
  });
  const res = await callHandler(req);
  assert.equal(res.headers.get('location'),
    'https://sebastienrousseau.com/fr/papers/index.html');
});

test('handler: cookie set to inactive lang is ignored → pass-through', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/', {
    headers: { Cookie: 'pref-lang=xx', 'Accept-Language': 'de' },
  });
  const res = await callHandler(req);
  // pref-lang=xx isn't ACTIVE → no cookie redirect. Accept-Language is
  // never sniffed, so the visitor lands on the canonical EN homepage.
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: ?lang=en passes through (explicit opt-out)', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/?lang=en');
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: ?lang=fr redirects, sets cookie, drops ?lang param', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/papers/?lang=fr');
  const res = await callHandler(req);
  assert.equal(res.status, 302);
  assert.equal(res.headers.get('location'),
    'https://sebastienrousseau.com/fr/papers/');
  const cookies = typeof res.headers.getSetCookie === 'function'
    ? res.headers.getSetCookie()
    : [res.headers.get('set-cookie') || ''];
  assert.ok(cookies.some(c => c.startsWith('pref-lang=fr')), 'cookie set');
  assert.ok(cookies.some(c => c.includes('SameSite=Lax')));
});

test('handler: ?lang=ZH-HANS (case mixed) normalises + redirects', async () => {
  const req = makeRequest('https://sebastienrousseau.com/?lang=ZH-HANS');
  const res = await callHandler(req);
  assert.equal(res.headers.get('location'), 'https://sebastienrousseau.com/zh-hans/');
});

test('handler: ?lang=xx (inactive) falls through to canonical site', async () => {
  const req = makeRequest('https://sebastienrousseau.com/?lang=xx', {
    headers: { 'Accept-Language': 'de' },
  });
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: no cookie / no override → pass-through (canonical EN)', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/');
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: Accept-Language fr-FR no longer triggers a redirect', async () => {
  // Regression test for the bilingual-reader complaint: French-browser
  // visitors used to be 302'd to /fr/ before they could even see the
  // canonical site. Now they stay on / unless they explicitly opt in.
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/', {
    headers: { 'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.5' },
  });
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: /fr/ request (already in lang subtree) passes through', async () => {
  resetLog();
  const req = makeRequest('https://sebastienrousseau.com/fr/papers/');
  const res = await callHandler(req);
  assert.equal(res.status, 200);
  assert.equal(passThroughLog.length, 1);
});

test('handler: every response (redirect or origin) carries security headers', async () => {
  for (const scenario of [
    { url: 'https://sebastienrousseau.com/', headers: {} },
    { url: 'https://sebastienrousseau.com/', headers: { Cookie: 'pref-lang=fr' } },
    { url: 'https://sebastienrousseau.com/?lang=de', headers: {} },
    { url: 'https://sebastienrousseau.com/', headers: { 'Accept-Language': 'fr' } },
    { url: 'https://sebastienrousseau.com/main.css', headers: {} },
  ]) {
    const res = await callHandler(makeRequest(scenario.url, { headers: scenario.headers }));
    for (const name of Object.keys(SECURITY_HEADERS)) {
      assert.ok(
        res.headers.get(name),
        `missing ${name} for ${scenario.url} (status ${res.status})`,
      );
    }
  }
});

test('handler: formspree.io is allowlisted by every response CSP', async () => {
  for (const url of [
    'https://sebastienrousseau.com/',
    'https://sebastienrousseau.com/contact/',
    'https://sebastienrousseau.com/?lang=fr',
  ]) {
    const res = await callHandler(makeRequest(url));
    const csp = res.headers.get('content-security-policy');
    assert.match(
      csp,
      /form-action 'self' https:\/\/formspree\.io/,
      `formspree missing from CSP on ${url}`,
    );
  }
});

// ---------------------------------------------------------------------------
// ActivityPub delegation — exercised via /actor (the AP route that needs
// no origin fetch, so the lang-router test stays origin-free). The
// activitypub.js module owns its own coverage; this only verifies the
// router's truthy fast-path branch.
// ---------------------------------------------------------------------------

test('handler: /actor delegates to ActivityPub handler, skips locale + CSP path', async () => {
  resetLog();
  const res = await callHandler(makeRequest('https://sebastienrousseau.com/actor'));
  // While PUBLIC_KEY_PEM is the placeholder, activitypub.js short-circuits to
  // 503 + text/plain (see commit e9caa541cd). The router's responsibility —
  // delegate to AP, never pass to origin — is still what we assert. When a
  // real RSA-2048 key replaces the PEM, flip these back to 200 + /activity\+json/.
  assert.equal(res.status, 503);
  assert.match(res.headers.get('content-type'), /text\/plain/);
  assert.equal(passThroughLog.length, 0, 'AP routes must not pass through to origin');
});
