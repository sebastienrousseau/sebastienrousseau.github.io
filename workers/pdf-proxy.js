/**
 * PDF proxy route for the lang-router Worker.
 *
 * Path: `GET /api/pdf/<slug>.pdf`
 *
 * Validates the slug, proxies to the Fly.io WeasyPrint service
 * (`pdf-render.fly.dev/render?slug=<slug>`), and re-emits the response
 * with `Cache-Control: public, max-age=86400, immutable` so the
 * Cloudflare Edge absorbs every repeat hit. The Fly machine sees one
 * request per article per day at most.
 *
 * Free-tier guard rails:
 *   - Slug regex stops directory traversal + reflected fetch tricks.
 *   - On Fly outage we 503 quickly — the article page itself still
 *     offers `window.print()` as a degraded but working fallback (the
 *     site has a full `@media print` stylesheet).
 *   - No KV, no D1, no async streaming — body is small (~80-200 KB)
 *     so a buffered re-emit keeps the code path trivially testable.
 */

const PDF_RENDER_BASE_DEFAULT = 'https://pdf-render.fly.dev';
const SLUG_RE = /^[a-z0-9][a-z0-9-]{0,127}$/;
const PDF_ROUTE_RE = /^\/api\/pdf\/([^/]+)\.pdf$/;

const HEADERS = {
  'Cache-Control': 'public, max-age=86400, immutable',
  'Content-Type': 'application/pdf',
  'Access-Control-Allow-Origin': '*',
};

const ERROR_HEADERS = {
  'Cache-Control': 'no-store',
  'Content-Type': 'application/json; charset=utf-8',
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

/**
 * Entry point — return a Response if the path is a PDF route, null
 * otherwise. The lang-router checks this before locale routing.
 */
export async function tryPDF(request, base = PDF_RENDER_BASE_DEFAULT) {
  const url = new URL(request.url);
  const m = PDF_ROUTE_RE.exec(url.pathname);
  if (!m) return null;
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return errorResponse(405, 'method-not-allowed', 'GET only');
  }
  const slug = m[1];
  if (!SLUG_RE.test(slug)) {
    return errorResponse(400, 'invalid-slug', 'slug does not match allowed pattern');
  }
  let upstream;
  try {
    upstream = await fetch(`${base}/render?slug=${encodeURIComponent(slug)}`, {
      cf: { cacheTtl: 86400, cacheEverything: true },
    });
  } catch (err) {
    return errorResponse(503, 'render-unavailable', err.message || 'fly fetch failed');
  }
  if (upstream.status === 404) {
    return errorResponse(404, 'article-not-found', `no article for slug ${slug}`);
  }
  if (!upstream.ok) {
    return errorResponse(502, 'render-error', `upstream ${upstream.status}`);
  }
  const body = await upstream.arrayBuffer();
  return new Response(body, {
    status: 200,
    headers: {
      ...HEADERS,
      'Content-Disposition': `inline; filename="${slug}.pdf"`,
    },
  });
}
