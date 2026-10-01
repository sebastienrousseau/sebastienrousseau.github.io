// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Live wall clock route for the lang-router Worker.
 *
 * Path: `GET /api/clock/hero-<light|dark>.svg`
 *
 * The GitHub profile README (github.com/sebastienrousseau) shows a hero
 * panel with a wall clock. The committed SVG is static: its hands are
 * CSS animations, paused at 10:09:30. This route fetches that SVG from the
 * profile repository, replaces its `/*clock*\/` marker with CSS that sets
 * the hands to the current London time and starts them, and returns it
 * uncached, so GitHub's camo image proxy refetches it on every profile
 * view. The browser then keeps the hands moving.
 *
 * London time, not the viewer's: camo fetches the image, so the request
 * carries no viewer time zone.
 *
 * Guard rails:
 *   - Only the two fixed theme paths match; nothing from the request
 *     reaches the upstream URL.
 *   - Upstream is edge-cached for five minutes; each response is a string
 *     replace, well inside the free-tier CPU budget.
 *   - If upstream fails or lacks the marker, 302 to the static SVG so the
 *     profile shows a stopped clock rather than a broken image.
 */

const SOURCE = 'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/main/assets/hero-';
const ROUTE_RE = /^\/api\/clock\/hero-(light|dark)\.svg$/;
const MARKER = '/*clock*/';
const HALF_DAY = 43200;

const HEADERS = {
  'Content-Type': 'image/svg+xml; charset=utf-8',
  'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0',
  'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; font-src data:",
  'X-Content-Type-Options': 'nosniff',
  'Access-Control-Allow-Origin': '*',
};

const LONDON = new Intl.DateTimeFormat('en-GB', {
  timeZone: 'Europe/London',
  hourCycle: 'h23',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
});

export function isClockRoute(pathname) {
  return ROUTE_RE.test(pathname);
}

/** Seconds past 12 o'clock (0 to 43199.999) in London at `date`. */
export function londonSeconds(date) {
  const part = {};
  for (const { type, value } of LONDON.formatToParts(date)) part[type] = Number(value);
  const whole = part.hour * 3600 + part.minute * 60 + part.second;
  return (whole % HALF_DAY) + date.getUTCMilliseconds() / 1000;
}

/** CSS that overrides the static delays and starts the hands. */
export function clockCSS(seconds) {
  const d = (n) => `-${n.toFixed(3)}s`;
  return (
    '.hand{animation-play-state:running}' +
    `.hh{animation-delay:${d(seconds)}}` +
    `.mm{animation-delay:${d(seconds % 3600)}}` +
    `.ss{animation-delay:${d(seconds % 60)}}`
  );
}

function fallback(theme) {
  return new Response(null, {
    status: 302,
    headers: { Location: `${SOURCE}${theme}.svg`, 'Cache-Control': 'no-store' },
  });
}

/**
 * Entry point: a Response for a clock route, null otherwise. The
 * lang-router checks this before locale routing.
 */
export async function tryClock(request, now = () => new Date()) {
  const m = ROUTE_RE.exec(new URL(request.url).pathname);
  if (!m) return null;
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return new Response(null, { status: 405, headers: { Allow: 'GET, HEAD' } });
  }
  const theme = m[1];
  let svg;
  try {
    const upstream = await fetch(`${SOURCE}${theme}.svg`, { cf: { cacheTtl: 300, cacheEverything: true } });
    if (!upstream.ok) return fallback(theme);
    svg = await upstream.text();
  } catch {
    return fallback(theme);
  }
  if (!svg.includes(MARKER)) return fallback(theme);
  const body = svg.replace(MARKER, clockCSS(londonSeconds(now())));
  return new Response(request.method === 'HEAD' ? null : body, { status: 200, headers: HEADERS });
}
