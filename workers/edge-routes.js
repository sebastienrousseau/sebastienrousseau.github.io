// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Edge routing helpers for the lang-router Worker: which paths are HTML
 * pages, how those pages are fetched from origin (edge-cached), and the
 * renamed-URL 301 map. lang-router.js imports and re-exports everything
 * here; the split only keeps that file under the 500-line ceiling.
 */

/**
 * True for paths that serve an HTML page (any locale): not an asset, feed,
 * API endpoint or well-known file.
 */
export function isHtmlPagePath(pathname) {
  if (pathname === '/' || pathname === '/index.html') return true;
  // Asset / API / feed extensions: pass through unchanged.
  if (/\.(?:css|js|map|json|xml|txt|webp|jpg|jpeg|png|svg|ico|woff2?|pdf|wasm)$/i.test(pathname)) {
    return false;
  }
  // Language-neutral roots that should not be redirected.
  const NEUTRAL_PREFIXES = ['/api/', '/_csp/', '/.well-known/', '/v1/'];
  return !NEUTRAL_PREFIXES.some(p => pathname.startsWith(p));
}

// ---------------------------------------------------------------------------
// Edge HTML cache
// ---------------------------------------------------------------------------
// Without this every HTML request went Worker -> GitHub Pages with
// cf-cache-status DYNAMIC, and Pages answers bursts with HTTP 429 (30 of 40
// parallel requests in a reproduction). Page navigations are now fetched with
// `cacheEverything`, so the Cloudflare edge keeps a copy of each 200.
//
// TTL: 600 s. GitHub Pages itself serves `cache-control: max-age=600`, so a
// deploy already takes up to ten minutes to show through GitHub's own CDN.
// Matching it means no purge-on-deploy step is needed and worst-case
// staleness after a deploy is about 20 minutes, while a crawler burst on one
// URL costs one origin hit per PoP per ten minutes instead of one per request.
//
// Only 200 is cached. Redirects, 404, 429 and 5xx get a negative TTL, which
// tells Cloudflare not to store them at all, so a transient origin error is
// never replayed to later visitors. The locale decision (cookie / ?lang=)
// is taken before any origin fetch and its 302s are generated here, never
// fetched, so a cached response can only ever be the origin page for its own
// path: /fr/... and /de/... are different cache keys. The browser-facing
// Cache-Control stays `max-age=0, must-revalidate` (set in
// withSecurityHeaders), so browsers revalidate and only the edge holds a copy.
export const EDGE_HTML_TTL = 600;
export const EDGE_HTML_CACHE = Object.freeze({
  cacheEverything: true,
  cacheTtlByStatus: Object.freeze({
    '100-199': -1,
    '200': EDGE_HTML_TTL,
    '201-599': -1,
  }),
});

/** True for GET/HEAD requests for an HTML page path, in any locale. */
export function isEdgeCacheable(request, pathname) {
  return (request.method === 'GET' || request.method === 'HEAD') && isHtmlPagePath(pathname);
}

// ---------------------------------------------------------------------------
// Renamed-URL 301s
// ---------------------------------------------------------------------------
// ADR-0012 localised locale article slugs; the old URLs are still built as
// meta-refresh stub pages (postbuild_lib/redirects.py). Search Console files
// each stub as "Page with redirect". worker-assets/redirects.json maps every
// stub path to its final target (scripts/build_worker_assets.py derives it
// from the built stubs and collapses chains), and the Worker answers those
// paths with one 301 before origin is touched. The stubs stay in the build
// as a fallback for when the binding is missing.
const _redirectCache = { map: null };

export function _resetRedirectMapCache() {
  _redirectCache.map = null;
}

/**
 * Old path -> new path Map from the ASSETS binding, loaded once per
 * isolate. A failed load returns an empty Map and is not cached, so the
 * next request retries.
 */
export async function getRedirectMap(env) {
  if (_redirectCache.map) return _redirectCache.map;
  if (!env || !env.ASSETS || typeof env.ASSETS.fetch !== 'function') return new Map();
  try {
    const res = await env.ASSETS.fetch(new Request('https://assets/redirects.json'));
    if (!res || !res.ok) return new Map();
    const payload = await res.json();
    if (!payload || typeof payload.redirects !== 'object' || payload.redirects === null) {
      return new Map();
    }
    _redirectCache.map = new Map(Object.entries(payload.redirects));
    return _redirectCache.map;
  } catch {
    return new Map();
  }
}

/** 301 Response when `url` is a renamed path in `map`, else null. */
export function tryRenamedUrlRedirect(url, map) {
  let path = url.pathname;
  if (path.endsWith('/index.html')) path = path.slice(0, -'index.html'.length);
  if (!path.endsWith('/')) path += '/';
  const target = map.get(path);
  if (!target) return null;
  const redirected = new URL(url);
  redirected.pathname = target;
  return Response.redirect(redirected.toString(), 301);
}

/** Fetch from origin, asking the edge to cache the response if it is a page. */
export function fetchOrigin(request, url) {
  return isEdgeCacheable(request, url.pathname)
    ? fetch(request, { cf: EDGE_HTML_CACHE })
    : fetch(request);
}
