#!/usr/bin/env node
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Tests for workers/profile-clock.js.
 *
 * Run from repo root:
 *   node --test --experimental-test-coverage \
 *        --test-coverage-functions=100 --test-coverage-lines=100 \
 *        --test-coverage-branches=100 workers/test_profile_clock.mjs
 */
import { test, before, after } from 'node:test';
import { strict as assert } from 'node:assert';

import worker from './profile-clock.js';

const realFetch = globalThis.fetch;
before(() => {
  globalThis.fetch = async () => new Response('<svg><style>/*clock*/</style></svg>');
});
after(() => {
  globalThis.fetch = realFetch;
});

test('serves the clock route', async () => {
  const res = await worker.fetch(new Request('https://profile-clock.example.workers.dev/api/clock/hero-dark.svg'));
  assert.equal(res.status, 200);
  assert.match(await res.text(), /animation-play-state:running/);
});

test('answers 404 for every other path', async () => {
  const res = await worker.fetch(new Request('https://profile-clock.example.workers.dev/'));
  assert.equal(res.status, 404);
  assert.equal(res.headers.get('Cache-Control'), 'no-store');
});
