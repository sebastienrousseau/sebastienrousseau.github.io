// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * PDF proxy route for the lang-router Worker.
 *
 * Path: `GET /api/pdf/<slug>.pdf` (EN) or `GET /api/pdf/<lang>/<slug>.pdf`
 *
 * Validates the slug, proxies to the Fly.io WeasyPrint service
 * (`<PDF_RENDER_BASE>/render?slug=<slug>[&lang=<lang>]`), and re-emits the response
 * with `Cache-Control: public, max-age=86400, immutable` so the
 * Cloudflare Edge absorbs every repeat hit. The Fly machine sees one
 * request per article per day at most.
 *
 * Free-tier guard rails:
 *   - Slug regex stops directory traversal + reflected fetch tricks.
 *   - No renderer configured (`PDF_RENDER_BASE` unset) -> 503 at once.
 *     There is deliberately no default host: the old default,
 *     `https://pdf-render.fly.dev`, does not run this repo's service (it
 *     answers with a different stack and hangs every GET), so every PDF request
 *     sat for ~60 s and ended in a 502. Search Console logged 678 of them.
 *   - A renderer that does not answer within RENDER_TIMEOUT_MS -> 504.
 *     On any failure the article page still offers `window.print()` as
 *     a degraded but working fallback (full `@media print` stylesheet).
 *   - Every response carries `X-Robots-Tag: noindex, nofollow`: the PDF
 *     duplicates the HTML article, which is the page that should rank.
 *   - No KV, no D1, no async streaming — body is small (~80-200 KB)
 *     so a buffered re-emit keeps the code path trivially testable.
 */

export const RENDER_TIMEOUT_MS = 10000;
const SLUG_RE = /^[a-z0-9][a-z0-9-]{0,127}$/;
const LANG_RE = /^[a-z]{2,3}(?:-[a-z]{2,4})?$/;
const PDF_ROUTE_RE = /^\/api\/pdf\/(?:([^/]+)\/)?([^/]+)\.pdf$/;
const ROBOTS = 'noindex, nofollow';

const HEADERS = {
  'Cache-Control': 'public, max-age=86400, immutable',
  'Content-Type': 'application/pdf',
  'Access-Control-Allow-Origin': '*',
  'X-Robots-Tag': ROBOTS,
};

const ERROR_HEADERS = {
  'Cache-Control': 'no-store',
  'Content-Type': 'application/json; charset=utf-8',
  'X-Robots-Tag': ROBOTS,
};

function errorResponse(status, code, message) {
  return new Response(
    JSON.stringify({ error: { code, message } }),
    { status, headers: ERROR_HEADERS },
  );
}

export function isPDFRoute(pathname) {
  return PDF_ROUTE_RE.test(pathname);
}

function renderUrl(base, slug, lang) {
  const q = `slug=${encodeURIComponent(slug)}`;
  return `${base}/render?${q}${lang ? `&lang=${encodeURIComponent(lang)}` : ''}`;
}

function upstreamError(upstream, slug) {
  if (upstream.status === 404) {
    return errorResponse(404, 'article-not-found', `no article for slug ${slug}`);
  }
  return errorResponse(502, 'render-error', `upstream ${upstream.status}`);
}

function fetchFailure(err) {
  if (err && (err.name === 'TimeoutError' || err.name === 'AbortError')) {
    return errorResponse(504, 'render-timeout', 'renderer did not answer in time');
  }
  return errorResponse(503, 'render-unavailable', (err && err.message) || 'fly fetch failed');
}

/**
 * Entry point — return a Response if the path is a PDF route, null
 * otherwise. The lang-router checks this before locale routing.
 * `base` is the renderer origin (env.PDF_RENDER_BASE); empty means no
 * renderer is deployed and the route answers 503 without a fetch.
 */
export async function tryPDF(request, base = '', originToken = '', timeoutMs = RENDER_TIMEOUT_MS) {
  const url = new URL(request.url);
  const m = PDF_ROUTE_RE.exec(url.pathname);
  if (!m) return null;
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return errorResponse(405, 'method-not-allowed', 'GET only');
  }
  const [, lang, slug] = m;
  if (!SLUG_RE.test(slug) || (lang !== undefined && !LANG_RE.test(lang))) {
    return errorResponse(400, 'invalid-slug', 'slug does not match allowed pattern');
  }
  if (!base) {
    return errorResponse(503, 'render-unconfigured', 'no PDF renderer configured');
  }
  const fetchInit = {
    cf: { cacheTtl: 86400, cacheEverything: true },
    signal: AbortSignal.timeout(timeoutMs),
  };
  if (originToken) {
    fetchInit.headers = { 'X-Origin-Verify': originToken };
  }
  let upstream;
  try {
    upstream = await fetch(renderUrl(base, slug, lang), fetchInit);
  } catch (err) {
    return fetchFailure(err);
  }
  if (!upstream.ok) return upstreamError(upstream, slug);
  const body = await upstream.arrayBuffer();
  return new Response(body, {
    status: 200,
    headers: {
      ...HEADERS,
      'Content-Disposition': `inline; filename="${slug}.pdf"`,
    },
  });
}
