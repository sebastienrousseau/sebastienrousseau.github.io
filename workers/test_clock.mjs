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

import { isClockRoute, londonSeconds, londonDay, pickKey, loadCalendar, clockCSS, tryClock } from './clock.js';

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

// --- Holiday themes -------------------------------------------------------

const RAW = 'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/main/assets/';
const HOLIDAY_SVG = '<svg><title>Christmas</title><style>/*clock*/</style></svg>';
const calendar = (days, schema = 1) => JSON.stringify({ schema, tz: 'Europe/London', days });

/** An upstream that serves `files` by name under assets/, 404 otherwise, and records every URL. */
function serve(files) {
  const asked = [];
  upstream = (url) => {
    asked.push(url);
    const name = url.slice(RAW.length);
    return name in files ? new Response(files[name]) : new Response('missing', { status: 404 });
  };
  return asked;
}

test('londonDay gives the London date and 24-hour hour across the BST change', () => {
  // Clocks go forward at 01:00 UTC on 29 March 2026.
  assert.deepEqual(londonDay(new Date(Date.UTC(2026, 2, 29, 0, 30))), { iso: '2026-03-29', hour: 0 });
  assert.deepEqual(londonDay(new Date(Date.UTC(2026, 2, 29, 1, 30))), { iso: '2026-03-29', hour: 2 });
  // In winter 23:30 UTC is still the same day; in summer it is already the next.
  assert.deepEqual(londonDay(new Date(Date.UTC(2026, 11, 24, 23, 30))), { iso: '2026-12-24', hour: 23 });
  assert.deepEqual(londonDay(new Date(Date.UTC(2026, 6, 31, 23, 30))), { iso: '2026-08-01', hour: 0 });
});

test('pickKey takes turns by the hour and refuses anything malformed', () => {
  const cal = { days: { a: ['christmas'], b: ['boxing-day', 'kwanzaa', 'hanukkah'], e: [], bad: ['../x'], n: [7] } };
  assert.equal(pickKey(cal, 'none', 3), null);
  assert.equal(pickKey(cal, 'e', 3), null);
  assert.equal(pickKey(cal, 'bad', 3), null);
  assert.equal(pickKey(cal, 'n', 3), null);
  assert.equal(pickKey({ days: { x: 'christmas' } }, 'x', 0), null);
  assert.equal(pickKey(null, 'a', 0), null);
  assert.equal(pickKey(cal, 'a', 17), 'christmas');
  assert.deepEqual([0, 1, 2, 23].map((h) => pickKey(cal, 'b', h)), ['boxing-day', 'kwanzaa', 'hanukkah', 'hanukkah']);
});

test('loadCalendar returns null for an error, a non-JSON page or another schema', async () => {
  upstream = () => new Response('oops', { status: 500 });
  assert.equal(await loadCalendar(), null);
  upstream = () => new Response('<html>not json</html>');
  assert.equal(await loadCalendar(), null);
  upstream = () => new Response(calendar({}, 2));
  assert.equal(await loadCalendar(), null);
  upstream = () => Promise.reject(new Error('down'));
  assert.equal(await loadCalendar(), null);
});

// 2026-12-25 10:00 UTC is 10:00 in London (GMT).
const XMAS = new Date(Date.UTC(2026, 11, 25, 10, 0));

test('tryClock serves the holiday hero with the clock set and says so', async () => {
  const asked = serve({ 'holidays.json': calendar({ '2026-12-25': ['christmas'] }), 'hero-christmas-dark.svg': HOLIDAY_SVG });
  const res = await tryClock(get('/api/clock/hero-dark.svg'), () => XMAS);
  assert.equal(res.status, 200);
  assert.equal(res.headers.get('X-Profile-Theme'), 'christmas');
  const body = await res.text();
  assert.match(body, /<title>Christmas<\/title>/);
  assert.match(body, /\.hh\{animation-delay:-36000\.000s\}/);
  assert.deepEqual(asked, [`${RAW}holidays.json`, `${RAW}hero-christmas-dark.svg`]);
});

test('tryClock alternates overlapping holidays by the London hour', async () => {
  serve({
    'holidays.json': calendar({ '2026-12-26': ['boxing-day', 'kwanzaa'] }),
    'hero-boxing-day-light.svg': HOLIDAY_SVG,
    'hero-kwanzaa-light.svg': HOLIDAY_SVG,
  });
  const at = (h) => () => new Date(Date.UTC(2026, 11, 26, h, 0));
  const themes = [];
  for (const h of [9, 10, 11]) themes.push((await tryClock(get('/api/clock/hero-light.svg'), at(h))).headers.get('X-Profile-Theme'));
  assert.deepEqual(themes, ['kwanzaa', 'boxing-day', 'kwanzaa']);
});

for (const [name, files] of [
  ['the holiday hero is missing', { 'holidays.json': calendar({ '2026-12-25': ['christmas'] }), 'hero-dark.svg': SVG }],
  ['the holiday hero lacks the marker', { 'holidays.json': calendar({ '2026-12-25': ['christmas'] }), 'hero-christmas-dark.svg': '<svg/>', 'hero-dark.svg': SVG }],
  ['the calendar is not JSON', { 'holidays.json': '<html/>', 'hero-dark.svg': SVG }],
  ['the calendar is schema 2', { 'holidays.json': calendar({ '2026-12-25': ['christmas'] }, 2), 'hero-dark.svg': SVG }],
  ['the calendar is missing', { 'hero-dark.svg': SVG }],
  ['today is not a holiday', { 'holidays.json': calendar({ '2026-12-24': ['christmas'] }), 'hero-dark.svg': SVG }],
]) {
  test(`tryClock serves the everyday hero when ${name}`, async () => {
    serve(files);
    const res = await tryClock(get('/api/clock/hero-dark.svg'), () => XMAS);
    assert.equal(res.status, 200);
    assert.equal(res.headers.get('X-Profile-Theme'), 'everyday');
    assert.ok((await res.text()).includes('animation-play-state:running'));
  });
}

test('tryClock still 302s when the everyday hero fails too', async () => {
  serve({ 'holidays.json': calendar({ '2026-12-25': ['christmas'] }) });
  const res = await tryClock(get('/api/clock/hero-light.svg'), () => XMAS);
  assert.equal(res.status, 302);
  assert.equal(res.headers.get('Location'), `${RAW}hero-light.svg`);
});

test('nothing from the request reaches an upstream URL', async () => {
  const asked = serve({ 'holidays.json': calendar({ '2026-12-25': ['christmas'] }), 'hero-christmas-light.svg': HOLIDAY_SVG });
  const res = await tryClock(get('/api/clock/hero-light.svg?key=../../evil&x=1#frag'), () => XMAS);
  assert.equal(res.status, 200);
  assert.deepEqual(asked, [`${RAW}holidays.json`, `${RAW}hero-christmas-light.svg`]);
  assert.ok(asked.every((url) => !url.includes('evil') && !url.includes('?')));
});
