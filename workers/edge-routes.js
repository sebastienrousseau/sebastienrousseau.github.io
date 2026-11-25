// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Edge routing helpers for the lang-router Worker: which paths are HTML
 * pages, how those pages are fetched from origin (edge-cached), and the
 * renamed-URL 301s, including the Shokunin rebrand slugs. lang-router.js
 * imports these and re-exports the public ones; the split only keeps that
 * file under the 500-line ceiling.
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
const _redirectCache = { map: null, articles: null };

export function _resetRedirectMapCache() {
  _redirectCache.map = null;
  _redirectCache.articles = null;
}

/**
 * `payload[field]` of an ASSETS JSON file as a Map, cached per isolate under
 * `_redirectCache[slot]`. A failed load returns an empty Map and is not
 * cached, so the next request retries.
 */
async function loadAssetMap(env, file, field, slot) {
  if (_redirectCache[slot]) return _redirectCache[slot];
  if (!env || !env.ASSETS || typeof env.ASSETS.fetch !== 'function') return new Map();
  try {
    const res = await env.ASSETS.fetch(new Request(`https://assets/${file}`));
    if (!res || !res.ok) return new Map();
    const payload = await res.json();
    if (!payload || typeof payload[field] !== 'object' || payload[field] === null) {
      return new Map();
    }
    _redirectCache[slot] = new Map(Object.entries(payload[field]));
    return _redirectCache[slot];
  } catch {
    return new Map();
  }
}

/** Old path -> new path Map from the ASSETS binding (redirects.json). */
export function getRedirectMap(env) {
  return loadAssetMap(env, 'redirects.json', 'redirects', 'map');
}

/**
 * Article slug -> locale code ('en' for the root) for every built article
 * page (article-locales.json). A slug built in several locales maps to
 * 'en' when English has it.
 */
export function getArticleLocales(env) {
  return loadAssetMap(env, 'article-locales.json', 'articles', 'articles');
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

// Permanent slug redirects shipped with the Shokunin → Static Site
// Generator rebrand. Returns a 301 Response when the URL matches the
// rename patterns, or null when it doesn't. Preserves SEO continuity
// for incoming links that still point at the old slugs.
//
// Two pattern families are handled:
//   * 2023-10-09 article: ``/(<lang>/)?2023-10-09-shokunin-<rest>``
//     redirects to the same path with the ``shokunin-`` segment
//     dropped (matches the rename in PR #N).
//   * ``made-with-ssg`` credit page + its 27 localized slug
//     variants (each suffixed with ``-shokunin``) redirect to the
//     ``-static-site-generator`` equivalent.
export function trySlugRedirects(url) {
  const path = url.pathname;
  // 2023-10-09 article rename: strip the literal ``shokunin-`` token
  // that follows the date in every locale's filename.
  const ARTICLE_RE = /^(\/(?:[a-z]{2}(?:-[a-z]+)?\/)?)2023-10-09-shokunin-/;
  if (ARTICLE_RE.test(path)) {
    const redirected = new URL(url);
    redirected.pathname = path.replace("2023-10-09-shokunin-", "2023-10-09-");
    return Response.redirect(redirected.toString(), 301);
  }
  // ``made-with-ssg`` (EN) and any localized variant ending in
  // ``-shokunin`` or ``-shokunin/`` (e.g. ``concu-avec-shokunin``,
  // ``gemaakt-met-shokunin``, ``hecho-con-shokunin``) redirect to
  // the ``-static-site-generator`` form.
  if (path === "/made-with-ssg" || path === "/made-with-ssg/") {
    const redirected = new URL(url);
    redirected.pathname = "/made-with-static-site-generator/";
    return Response.redirect(redirected.toString(), 301);
  }
  const LOCALE_CREDIT_RE = /^(\/[a-z]{2}(?:-[a-z]+)?\/)([^/]+)-shokunin\/?$/;
  const m = path.match(LOCALE_CREDIT_RE);
  if (m) {
    const redirected = new URL(url);
    redirected.pathname = `${m[1]}${m[2]}-static-site-generator/`;
    return Response.redirect(redirected.toString(), 301);
  }
  return null;
}

// A rebranded slug whose stripped form was renamed again (the Arabic
// 2023-10-09 article) is a key in redirects.json. Follow that entry so the
// client gets one 301 to the final URL, not shokunin -> stripped -> renamed.
export async function resolveRenamed(redirect, env) {
  const target = new URL(redirect.headers.get('location'));
  return tryRenamedUrlRedirect(target, await getRedirectMap(env)) || redirect;
}

// Retired /api/pdf/ route (#515). It served `/api/pdf/<slug>.pdf` and
// `/api/pdf/<lang>/<slug>.pdf`, with the same slug and locale as the
// article page. Each such URL now 301s to that article (through the
// renamed-URL map, so one hop to the final URL), which keeps the value of
// any inbound link and lands a reader on the page. The older form carried
// no locale, so a translated article's slug is looked up in
// article-locales.json to find its locale; a slug that is in neither map
// was never an article and answers 410 Gone, like anything else under the
// prefix, so crawlers drop it instead of following a 301 to a 404.
const PDF_PREFIX = '/api/pdf/';
const PDF_RE = /^\/api\/pdf\/(?:([a-z]{2,3}(?:-[a-z]{2,4})?)\/)?([a-z0-9][a-z0-9-]{0,127})\.pdf$/;

function pdfGone() {
  return new Response('Gone\n', {
    status: 410,
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
      'X-Robots-Tag': 'noindex',
    },
  });
}

/** Article path for a PDF slug: its own locale, or the root when unknown. */
function pdfArticlePath(lang, slug, locales) {
  const code = lang || locales.get(slug);
  return code && code !== 'en' ? `/${code}/${slug}/` : `/${slug}/`;
}

/** 301 to the article for an old PDF URL, 410 for other /api/pdf/ paths, else null. */
export async function tryRetiredPdf(url, env) {
  if (!url.pathname.startsWith(PDF_PREFIX)) return null;
  const m = PDF_RE.exec(url.pathname);
  if (!m) return pdfGone();
  const locales = await getArticleLocales(env);
  const target = new URL(url);
  target.pathname = pdfArticlePath(m[1], m[2], locales);
  target.search = '';
  const renamed = tryRenamedUrlRedirect(target, await getRedirectMap(env));
  if (renamed) return renamed;
  // Without the index (binding missing), keep the 301; with it, an unknown
  // slug is not an article.
  if (!m[1] && locales.size && !locales.has(m[2])) return pdfGone();
  return Response.redirect(target.toString(), 301);
}

// Stale-while-revalidate for pages, when the Workers Cache API is present.
// The fetch cache above expires a page after EDGE_HTML_TTL, so a crawler
// that walks thousands of URLs, each rarely, almost always misses it and
// waits on GitHub Pages (Search Console measured ~1.1 s per request). Here
// each 200 is also kept in caches.default for EDGE_HTML_STALE, keyed by path
// alone (a query string never changes a static page). A copy younger than
// EDGE_HTML_TTL is served as is; an older one is served at once and
// refreshed in the background. Only GET 200s are stored; a failed refresh
// keeps the copy.
export const EDGE_HTML_STALE = 7 * 24 * 60 * 60;
export const EDGE_STORED_AT = 'x-edge-stored-at';
// The copy lives under its own path, never the page URL: caches.default and
// fetch(..., { cf: cacheEverything }) read the same zone cache, so a copy
// keyed by the page URL is what the refresh fetch got back, and it stored
// that old page again every ten minutes. A busy page (the homepage) then
// never saw a deploy.
export const EDGE_COPY_PREFIX = '/__edge-copy';

// Deploy-aware copies. SWR alone let the first visitor per cache node after
// a deploy see the previous build, and caches.default is per node, so after
// every deploy some visitors somewhere got the old page. Each deploy now
// writes its commit to /build-id.txt (ci.yml, "Prepare CNAME"), every copy
// records the build it was fetched for, and a copy from another build is
// treated as a miss: the page is fetched again before it is served. The
// refetch adds ?__build=<id> so the zone cache, which keys on the query
// string, cannot hand back the old build's page (GitHub Pages ignores the
// query). The id costs one extra lookup, cached for BUILD_ID_TTL per node
// and per isolate. Without a readable id (a local build, origin down) the
// Worker behaves as before.
export const EDGE_BUILD = 'x-edge-build';
export const BUILD_ID_PATH = '/build-id.txt';
export const BUILD_ID_TTL = 30;
const BUILD_ID_RE = /^[0-9a-f]{7,64}$/;
const _buildCache = { id: '', at: -Infinity };

export function _resetBuildIdCache() {
  _buildCache.id = '';
  _buildCache.at = -Infinity;
}

async function readBuildId(origin) {
  try {
    const res = await fetch(`${origin}${BUILD_ID_PATH}`, {
      cf: { cacheEverything: true, cacheTtl: BUILD_ID_TTL },
    });
    if (res.status !== 200) return '';
    const id = (await res.text()).trim();
    return BUILD_ID_RE.test(id) ? id : '';
  } catch {
    return '';
  }
}

/** The deployed build's id, '' when unknown; re-read every BUILD_ID_TTL. */
export async function currentBuildId(origin) {
  if (Date.now() - _buildCache.at < BUILD_ID_TTL * 1000) return _buildCache.id;
  _buildCache.id = await readBuildId(origin);
  _buildCache.at = Date.now();
  return _buildCache.id;
}

function pageKey(url) {
  return new Request(`${url.origin}${EDGE_COPY_PREFIX}${url.pathname}`, { method: 'GET' });
}

/** The origin URL for a page, carrying the build id when one is known. */
function originUrl(url, build) {
  return build ? `${url.origin}${url.pathname}?__build=${build}` : `${url.origin}${url.pathname}`;
}

async function storePage(cache, key, res, build) {
  const headers = new Headers(res.headers);
  headers.set('Cache-Control', `public, max-age=${EDGE_HTML_STALE}`);
  headers.set(EDGE_STORED_AT, String(Date.now()));
  if (build) headers.set(EDGE_BUILD, build);
  // adr: ADR-0015: Cache API (caches.default) page copy, not a KV write
  await cache.put(key, new Response(res.body, { status: 200, headers }));
}

async function revalidate(cache, key, url, build) {
  const res = await fetch(new Request(originUrl(url, build), { method: 'GET' }), { cf: EDGE_HTML_CACHE });
  if (res.status === 200) await storePage(cache, key, res, build);
}

function servedCopy(hit, method) {
  const headers = new Headers(hit.headers);
  headers.delete(EDGE_STORED_AT);
  headers.delete(EDGE_BUILD);
  return new Response(method === 'HEAD' ? null : hit.body, { status: hit.status, headers });
}

/** A copy is current unless the deployed build is known and differs. */
function isCurrentBuild(hit, build) {
  return !build || hit.headers.get(EDGE_BUILD) === build;
}

function serveHit(hit, request, url, ctx, cache, key, build) {
  const age = (Date.now() - Number(hit.headers.get(EDGE_STORED_AT))) / 1000;
  if (!(age < EDGE_HTML_TTL)) ctx.waitUntil(revalidate(cache, key, url, build).catch(() => {}));
  return servedCopy(hit, request.method);
}

/** Origin fetch for a miss; a copy from an older build is the fallback. */
async function fetchFresh(request, url, build, fallback) {
  const target = build ? new Request(originUrl(url, build), request) : request;
  try {
    const res = await fetch(target, { cf: EDGE_HTML_CACHE });
    return res.status === 200 || !fallback ? res : null;
  } catch (err) {
    if (!fallback) throw err;
    return null;
  }
}

async function fetchPageSwr(request, url, ctx, cache) {
  const key = pageKey(url);
  const [hit, build] = await Promise.all([cache.match(key), currentBuildId(url.origin)]);
  if (hit && isCurrentBuild(hit, build)) return serveHit(hit, request, url, ctx, cache, key, build);
  const res = await fetchFresh(request, url, build, hit);
  if (!res) return servedCopy(hit, request.method);
  if (res.status === 200 && request.method === 'GET') {
    ctx.waitUntil(storePage(cache, key, res.clone(), build));
  }
  return res;
}

// Not-found pages. GitHub Pages answers a missing page with its own
// generic "Page not found · GitHub Pages" document, and serves the site's
// not-found pages at /404/ and /<lang>/404/ with status 200, which Search
// Console files as Soft 404. A missing page now gets the site's not-found
// page in its locale (English when the locale has none) with status 404,
// and /404/ itself answers 404.
const NOT_FOUND_RE = /^\/(?:[a-z]{2,3}(?:-[a-z]{2,4})?\/)?404\/(?:index\.html)?$/;
const LOCALE_SEGMENT_RE = /^\/([a-z]{2,3}(?:-[a-z]{2,4})?)\//;

/** True for the site's own not-found page paths, in any locale. */
export function isNotFoundPage(pathname) {
  return NOT_FOUND_RE.test(pathname);
}

function asNotFound(res, method) {
  return new Response(method === 'HEAD' ? null : res.body, { status: 404, headers: res.headers });
}

function fetchPage(request, url, ctx, cache) {
  if (cache && typeof ctx?.waitUntil === 'function') return fetchPageSwr(request, url, ctx, cache);
  return fetch(request, { cf: EDGE_HTML_CACHE });
}

/** The not-found page for `url`'s locale, else English, as a 404; null when neither loads. */
async function notFoundPage(request, url, ctx, cache) {
  const m = LOCALE_SEGMENT_RE.exec(url.pathname);
  const paths = m ? [`/${m[1]}/404/`, '/404/'] : ['/404/'];
  for (const path of paths) {
    const target = new URL(path, url.origin);
    const res = await fetchPage(new Request(target, { method: 'GET' }), target, ctx, cache);
    if (res.status === 200) return asNotFound(res, request.method);
  }
  return null;
}

/** Fetch from origin, serving pages from the edge copy where one exists. */
export async function fetchOrigin(request, url, ctx, cache = globalThis.caches?.default) {
  if (!isEdgeCacheable(request, url.pathname)) return fetch(request);
  const res = await fetchPage(request, url, ctx, cache);
  if (isNotFoundPage(url.pathname)) return res.status === 200 ? asNotFound(res, request.method) : res;
  if (res.status !== 404) return res;
  return (await notFoundPage(request, url, ctx, cache)) || res;
}
