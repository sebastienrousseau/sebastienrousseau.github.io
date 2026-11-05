// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * First-party cookie-free conversion and Core Web Vitals event sink.
 *
 * Route: `POST /api/event`
 *
 * Accepts a small JSON beacon (`<= 2 KB`) from same-origin pages and
 * writes one data point to Cloudflare Workers Analytics Engine (`env.AE`)
 * under `ctx.waitUntil()`. No cookies, no IP address, and no persistent
 * identifier are read or stored.
 */

const ROUTE = '/api/event';
const MAX_BODY_BYTES = 2048;
const MAX_PATH_CHARS = 200;
const ALLOWED_ORIGIN = 'https://sebastienrousseau.com';

export const ALLOWED_EVENTS = new Set([
  'cta_click',
  'cta_get_in_touch',
  'newsletter_submit',
  'paper_download',
  'copy_config',
  'copy_code',
  'advisory_cta',
  'article_cta',
  'read_as_select',
  'tab_select',
  'vital_lcp',
  'vital_inp',
  'vital_cls',
]);

export function isSameOrigin(request) {
  const origin = request.headers.get('Origin');
  if (origin) {
    return origin === ALLOWED_ORIGIN;
  }
  return request.headers.get('Sec-Fetch-Site') === 'same-origin';
}

export function cleanPath(rawPath) {
  const noQuery = rawPath.split(/[?#]/, 1)[0];
  return noQuery.slice(0, MAX_PATH_CHARS);
}

/**
 * Handle `/api/event`. Returns `null` for any other path so `lang-router`
 * falls through to the next route.
 */
export async function tryEvent(request, env, ctx) {
  const url = new URL(request.url);
  if (url.pathname !== ROUTE) return null;
  if (request.method !== 'POST') {
    return new Response(null, {
      status: 405,
      headers: { Allow: 'POST', 'Cache-Control': 'no-store' },
    });
  }
  if (!isSameOrigin(request)) {
    return new Response(null, {
      status: 403,
      headers: { 'Cache-Control': 'no-store' },
    });
  }
  const raw = await request.text();
  if (raw.length === 0 || raw.length > MAX_BODY_BYTES) {
    return new Response(null, {
      status: 400,
      headers: { 'Cache-Control': 'no-store' },
    });
  }
  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    return new Response(null, {
      status: 400,
      headers: { 'Cache-Control': 'no-store' },
    });
  }
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    return new Response(null, {
      status: 400,
      headers: { 'Cache-Control': 'no-store' },
    });
  }
  const { e, p, v, k } = payload;
  if (typeof e !== 'string' || !ALLOWED_EVENTS.has(e)) {
    return new Response(null, {
      status: 400,
      headers: { 'Cache-Control': 'no-store' },
    });
  }
  if (typeof p !== 'string' || !p.startsWith('/')) {
    return new Response(null, {
      status: 400,
      headers: { 'Cache-Control': 'no-store' },
    });
  }
  if (v !== undefined && (typeof v !== 'number' || !Number.isFinite(v))) {
    return new Response(null, {
      status: 400,
      headers: { 'Cache-Control': 'no-store' },
    });
  }
  if (k !== undefined && typeof k !== 'string') {
    return new Response(null, {
      status: 400,
      headers: { 'Cache-Control': 'no-store' },
    });
  }

  if (
    env &&
    env.AE &&
    typeof env.AE.writeDataPoint === 'function' &&
    ctx &&
    typeof ctx.waitUntil === 'function'
  ) {
    const country = (request.cf && request.cf.country) || '??';
    const point = {
      blobs: [e, cleanPath(p), (k || '').slice(0, MAX_PATH_CHARS), String(country)],
      doubles: [v !== undefined ? v : 1],
      indexes: [e],
    };
    ctx.waitUntil(Promise.resolve(env.AE.writeDataPoint(point)));
  }

  return new Response(null, {
    status: 204,
    headers: { 'Cache-Control': 'no-store' },
  });
}
