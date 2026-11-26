#!/usr/bin/env node
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Tests for workers/live-kpi.js.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-include='workers/live-kpi.js' \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_live_kpi.mjs
 *
 * Node has no HTMLRewriter, so a small stand-in applies the handler to
 * every `<span ... data-kpi="key">text</span>` in the body, the way the
 * Cloudflare runtime calls `element()` on each match. globalThis.fetch is
 * stubbed, so the tests make no network calls.
 */
import { test, before, after } from 'node:test';
import { strict as assert } from 'node:assert';

import { loadFigures, withLiveFigures } from './live-kpi.js';

const PROFILE = 'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/profile-data/profile.json';
const DISPLAY = { all_time_downloads: '54.9M', recent_downloads: '2.6M', github_stars: '760', packages: '201' };

class FakeRewriter {
  on(selector, handler) {
    assert.equal(selector, '[data-kpi]');
    this.handler = handler;
    return this;
  }

  transform(response) {
    const handler = this.handler;
    const body = (async () => {
      const html = await response.text();
      const re = /(<span[^>]*data-kpi="([^"]*)"[^>]*>)([^<]*)(<\/span>)/g;
      let out = '';
      let last = 0;
      for (const m of html.matchAll(re)) {
        let text = m[3];
        await handler.element({
          getAttribute: (name) => (name === 'data-kpi' ? m[2] : null),
          setInnerContent: (value) => {
            text = value;
          },
        });
        out += html.slice(last, m.index) + m[1] + text + m[4];
        last = m.index + m[0].length;
      }
      return out + html.slice(last);
    })();
    return new Response(new ReadableStream({
      async start(controller) {
        controller.enqueue(new TextEncoder().encode(await body));
        controller.close();
      },
    }), { status: response.status, headers: response.headers });
  }
}

let upstream;
let calls;
const realFetch = globalThis.fetch;
before(() => {
  globalThis.HTMLRewriter = FakeRewriter;
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return upstream(url);
  };
});
after(() => {
  globalThis.fetch = realFetch;
  delete globalThis.HTMLRewriter;
});

const json = (doc) => async () => new Response(JSON.stringify(doc), { status: 200 });
const page = (html, type = 'text/html; charset=utf-8', status = 200) =>
  new Response(html, { status, headers: { 'Content-Type': type } });
const KPIS =
  '<span class="kpi-cell-value" data-kpi="downloads_total">54.8M</span>' +
  '<span class="kpi-cell-value" data-kpi="downloads_30d">2.5M</span>' +
  '<span class="kpi-cell-value" data-kpi="github_stars">758</span>' +
  '<span class="kpi-inline" data-kpi="packages_published">200</span>' +
  '<span class="kpi-cell-value" data-kpi="articles_signed">131</span>';

test('loadFigures maps the profile display strings to the site keys', async () => {
  calls = [];
  upstream = json({ schema: 1, numbers: { display: DISPLAY } });
  assert.deepEqual(await loadFigures(), {
    downloads_total: '54.9M',
    downloads_30d: '2.6M',
    github_stars: '760',
    packages_published: '201',
  });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, PROFILE);
  assert.equal(calls[0].init.cf.cacheTtl, 300);
});

for (const [name, respond] of [
  ['profile.json answers 404', async () => new Response('missing', { status: 404 })],
  ['profile.json is not JSON', async () => new Response('<html/>', { status: 200 })],
  ['profile.json has no display strings', json({ schema: 1, numbers: { packages: 200 } })],
  ['a display string is not a figure', json({ numbers: { display: { ...DISPLAY, packages: '<b>201</b>' } } })],
  ['a display string is a number, not a string', json({ numbers: { display: { ...DISPLAY, github_stars: 760 } } })],
  ['the fetch throws', async () => { throw new Error('network'); }],
]) {
  test(`loadFigures returns null when ${name}`, async () => {
    calls = [];
    upstream = respond;
    assert.equal(await loadFigures(), null);
  });
}

test('withLiveFigures rewrites the four headline figures and nothing else', async () => {
  calls = [];
  upstream = json({ numbers: { display: DISPLAY } });
  const res = withLiveFigures(page(`<p>${KPIS}</p>`));
  const html = await res.text();
  assert.ok(html.includes('data-kpi="downloads_total">54.9M<'));
  assert.ok(html.includes('data-kpi="downloads_30d">2.6M<'));
  assert.ok(html.includes('data-kpi="github_stars">760<'));
  assert.ok(html.includes('data-kpi="packages_published">201<'));
  assert.ok(html.includes('data-kpi="articles_signed">131<'), 'a site-only figure is left alone');
  assert.equal(calls.length, 1, 'profile.json is fetched once per page');
});

test('withLiveFigures keeps the built figures when profile.json fails', async () => {
  upstream = async () => new Response('down', { status: 503 });
  const html = await withLiveFigures(page(KPIS)).text();
  assert.equal(html, KPIS);
});

test('withLiveFigures does not fetch profile.json for a page without the figures', async () => {
  calls = [];
  upstream = json({ numbers: { display: DISPLAY } });
  const html = await withLiveFigures(page('<span data-kpi="articles_signed">131</span>')).text();
  assert.equal(html, '<span data-kpi="articles_signed">131</span>');
  assert.equal(calls.length, 0);
});

test('withLiveFigures passes through responses that are not 200 HTML pages', () => {
  const load = () => assert.fail('must not load figures');
  for (const res of [
    page('{}', 'application/json'),
    page(KPIS, 'text/html', 404),
    new Response(null, { status: 200, headers: { 'Content-Type': 'text/html' } }),
    new Response(new ReadableStream(), { status: 200 }), // no Content-Type at all
  ]) {
    assert.equal(withLiveFigures(res, load), res);
  }
});

test('withLiveFigures leaves the page alone where HTMLRewriter does not exist', () => {
  const saved = globalThis.HTMLRewriter;
  delete globalThis.HTMLRewriter;
  try {
    const res = page(KPIS);
    assert.equal(withLiveFigures(res, () => assert.fail('must not load figures')), res);
  } finally {
    globalThis.HTMLRewriter = saved;
  }
});
