// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Standalone Worker for the GitHub profile clock.
 *
 * Serves only `GET /api/clock/hero-<light|dark>.svg` (see clock.js) on its
 * own workers.dev hostname, so the profile clock can keep time without a
 * lang-router release. Every other path is a 404. Deploy with
 * `wrangler deploy -c workers/profile-clock.toml`.
 */

import { tryClock } from './clock.js';

export default {
  async fetch(request) {
    const response = await tryClock(request);
    return response ?? new Response('Not found', { status: 404, headers: { 'Cache-Control': 'no-store' } });
  },
};
