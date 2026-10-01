#!/usr/bin/env node
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Tests for workers/clock.js.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_clock.mjs
 *
 * No Cloudflare runtime needed; globalThis.fetch is stubbed for every
 * upstream call so the tests are hermetic and zero-network.
 */
import { test, before, after } from 'node:test';
import { strict as assert } from 'node:assert';

import { isClockRoute, londonSeconds, clockCSS, tryClock } from './clock.js';

const BASE = 'https://sebastienrousseau.com';
const SVG = '<svg><style>.hand{animation-play-state:paused}/*clock*/</style></svg>';

let upstream;
const realFetch = globalThis.fetch;
before(() => {
  globalThis.fetch = async (url) => upstream(url);
});
after(() => {
  globalThis.fetch = realFetch;
});

const get = (path, method = 'GET') => new Request(`${BASE}${path}`, { method });
// 2026-07-01 13:45:10.250 UTC is 14:45:10.250 in London (BST).
const SUMMER = new Date(Date.UTC(2026, 6, 1, 13, 45, 10, 250));
// 2026-01-15 09:05:00 UTC is 09:05:00 in London (GMT).
const WINTER = new Date(Date.UTC(2026, 0, 15, 9, 5, 0));

test('isClockRoute matches only the two theme paths', () => {
  assert.ok(isClockRoute('/api/clock/hero-light.svg'));
  assert.ok(isClockRoute('/api/clock/hero-dark.svg'));
  assert.ok(!isClockRoute('/api/clock/hero-blue.svg'));
  assert.ok(!isClockRoute('/api/clock/../hero-light.svg'));
});

test('londonSeconds follows British Summer Time and GMT on a 12-hour dial', () => {
  assert.equal(londonSeconds(SUMMER), 2 * 3600 + 45 * 60 + 10.25);
  assert.equal(londonSeconds(WINTER), 9 * 3600 + 5 * 60);
});

test('clockCSS starts the hands with per-hand negative delays', () => {
  const css = clockCSS(9930.25);
  assert.match(css, /\.hand\{animation-play-state:running\}/);
  assert.match(css, /\.hh\{animation-delay:-9930\.250s\}/);
  assert.match(css, /\.mm\{animation-delay:-2730\.250s\}/);
  assert.match(css, /\.ss\{animation-delay:-30\.250s\}/);
});

test('tryClock ignores other paths', async () => {
  assert.equal(await tryClock(get('/articles/')), null);
});

test('tryClock rejects methods other than GET and HEAD', async () => {
  const res = await tryClock(get('/api/clock/hero-light.svg', 'POST'));
  assert.equal(res.status, 405);
  assert.equal(res.headers.get('Allow'), 'GET, HEAD');
});

test('tryClock injects London time into the themed SVG, uncached', async () => {
  let asked;
  upstream = (url) => {
    asked = url;
    return new Response(SVG);
  };
  const res = await tryClock(get('/api/clock/hero-dark.svg'), () => SUMMER);
  assert.equal(asked, 'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/main/assets/hero-dark.svg');
  assert.equal(res.status, 200);
  assert.equal(res.headers.get('Content-Type'), 'image/svg+xml; charset=utf-8');
  assert.match(res.headers.get('Cache-Control'), /no-cache/);
  const body = await res.text();
  assert.ok(!body.includes('/*clock*/'));
  assert.match(body, /\.hh\{animation-delay:-9910\.250s\}/);
});

test('tryClock answers HEAD without a body', async () => {
  upstream = () => new Response(SVG);
  const res = await tryClock(get('/api/clock/hero-light.svg', 'HEAD'), () => WINTER);
  assert.equal(res.status, 200);
  assert.equal(res.body, null);
});

test('tryClock uses the real clock by default', async () => {
  upstream = () => new Response(SVG);
  const res = await tryClock(get('/api/clock/hero-light.svg'));
  assert.equal(res.status, 200);
});

for (const [name, stub] of [
  ['an upstream error status', () => new Response('nope', { status: 503 })],
  ['a network failure', () => Promise.reject(new Error('down'))],
  ['an SVG without the marker', () => new Response('<svg/>')],
]) {
  test(`tryClock falls back to the static SVG on ${name}`, async () => {
    upstream = stub;
    const res = await tryClock(get('/api/clock/hero-light.svg'));
    assert.equal(res.status, 302);
    assert.equal(
      res.headers.get('Location'),
      'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/main/assets/hero-light.svg',
    );
  });
}
