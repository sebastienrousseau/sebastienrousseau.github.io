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
 * Holiday themes: the profile repository publishes `assets/holidays.json`,
 * London dates mapped to holiday keys. On a holiday this route serves
 * `hero-<key>-<theme>.svg` instead; when holidays share a day they take
 * turns by the London hour (`keys[hour % keys.length]`). Any problem with
 * the calendar or the holiday hero falls back to the everyday hero. The
 * `X-Profile-Theme` header names what was served.
 *
 * Guard rails:
 *   - Only the two fixed theme paths match; nothing from the request
 *     reaches an upstream URL.
 *   - A holiday key comes only from the calendar file and must match
 *     KEY_RE; the theme comes only from the route regex.
 *   - At most three upstream fetches per request (calendar, holiday hero,
 *     everyday hero), each edge-cached for five minutes; each response is
 *     a string replace, well inside the free-tier CPU and subrequest
 *     budgets.
 *   - If the everyday hero fails or lacks the marker, 302 to the static
 *     SVG so the profile shows a stopped clock rather than a broken image.
 */

const SOURCE = 'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/main/assets/hero-';
const CALENDAR = 'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/main/assets/holidays.json';
const KEY_RE = /^[a-z0-9-]{1,40}$/;
const EDGE = { cf: { cacheTtl: 300, cacheEverything: true } };
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

const LONDON_DAY = new Intl.DateTimeFormat('en-GB', {
  timeZone: 'Europe/London',
  hourCycle: 'h23',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
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

/** The London calendar date (YYYY-MM-DD) and hour (0 to 23) at `date`. */
export function londonDay(date) {
  const part = {};
  for (const { type, value } of LONDON_DAY.formatToParts(date)) part[type] = value;
  return { iso: `${part.year}-${part.month}-${part.day}`, hour: Number(part.hour) };
}

/**
 * The holiday key to serve on `iso` at `hour`, or null for the everyday
 * hero. Several holidays on one day take turns by the hour. A day whose
 * entry is not a non-empty list of well-formed keys counts as no holiday.
 */
export function pickKey(calendar, iso, hour) {
  const keys = calendar?.days?.[iso];
  if (!Array.isArray(keys) || keys.length === 0) return null;
  if (!keys.every((k) => typeof k === 'string' && KEY_RE.test(k))) return null;
  return keys[hour % keys.length];
}

/** The published calendar, or null on any failure. Never throws. */
export async function loadCalendar() {
  try {
    const res = await fetch(CALENDAR, EDGE);
    if (!res.ok) return null;
    const doc = await res.json();
    return doc?.schema === 1 ? doc : null;
  } catch {
    return null;
  }
}

/** A hero SVG that carries the clock marker, or null. Never throws. */
async function heroSVG(name) {
  try {
    const res = await fetch(`${SOURCE}${name}.svg`, EDGE);
    if (!res.ok) return null;
    const svg = await res.text();
    return svg.includes(MARKER) ? svg : null;
  } catch {
    return null;
  }
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
  const at = now();
  const { iso, hour } = londonDay(at);
  const key = pickKey(await loadCalendar(), iso, hour);
  let served = key;
  let svg = key ? await heroSVG(`${key}-${theme}`) : null;
  if (!svg) {
    served = 'everyday';
    svg = await heroSVG(theme);
    if (!svg) return fallback(theme);
  }
  const body = svg.replace(MARKER, clockCSS(londonSeconds(at)));
  const headers = { ...HEADERS, 'X-Profile-Theme': served };
  return new Response(request.method === 'HEAD' ? null : body, { status: 200, headers });
}
