// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * MCP (Model Context Protocol) server routes for sebastienrousseau.com.
 *
 * Exposes the corpus as a JSON-RPC-style HTTP API that AI clients
 * (Claude, ChatGPT, Perplexity, Brave Leo, custom MCP clients) can
 * call to enumerate, read, and search articles by canonical URL or
 * tag. All routes are read-only.
 *
 * Read path: a single static manifest at /api/mcp-resources.json built
 * at postbuild time. Per-resource bodies come from the existing static
 * JSONL feeds (/feed.jsonl + /tags/<slug>/feed.jsonl) — already
 * Edge-cacheable, immutable, served by GitHub Pages with zero KV hits.
 *
 * Cloudflare Free Tier-safe: every response is `Cache-Control: public,
 * max-age=86400, immutable` so the Edge Cache absorbs repeat traffic
 * before the Worker fires. Rate-limiting on /mcp/v1/* is enforced by
 * Cloudflare's Free WAF (UA allow-list + 30 req/min/IP), not the
 * Worker — see docs/CLOUDFLARE-WAF.md.
 *
 * Routes:
 *   GET /mcp/v1/list_resources?cursor=<n>&limit=<n>
 *     → { resources: [{ uri, name, description, mimeType }, ...], nextCursor }
 *   GET /mcp/v1/read_resource?uri=<canonical>
 *     → { contents: [{ uri, mimeType, text }] }
 *   GET /mcp/v1/search?q=<query>&tag=<slug>&limit=<n>
 *     → { resources: [...], total }
 */

const MAX_LIMIT = 100;
const DEFAULT_LIMIT = 20;
const CACHE_HEADERS = {
  'Cache-Control': 'public, max-age=86400, immutable',
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const ORIGIN_BASE = 'https://sebastienrousseau.com';

export function isMCPRoute(pathname) {
  return pathname.startsWith('/mcp/v1/');
}

function jsonResponse(body, init = {}) {
  return new Response(JSON.stringify(body), {
    status: init.status || 200,
    headers: { ...CACHE_HEADERS, ...(init.headers || {}) },
  });
}

function errorResponse(status, code, message) {
  return jsonResponse(
    { error: { code, message } },
    { status, headers: { 'Cache-Control': 'no-store' } },
  );
}

function parseIntParam(v, def) {
  if (v == null) return def;
  const n = parseInt(v, 10);
  return Number.isFinite(n) && n >= 0 ? n : def;
}

function clampLimit(v) {
  return Math.min(MAX_LIMIT, Math.max(1, parseIntParam(v, DEFAULT_LIMIT)));
}

// Origin-relative fetch helper. Cloudflare Workers can call `fetch()` on
// an absolute URL to hit the same zone's origin — that's the documented
// pattern for reading static assets from the bound site. The `cf:`
// directive marks the response as cacheable for an hour so the Edge
// absorbs repeats.
async function fetchManifest(originBase) {
  const res = await fetch(`${originBase}/api/mcp-resources.json`, {
    cf: { cacheTtl: 3600, cacheEverything: true },
  });
  if (!res.ok) {
    throw new Error(`manifest ${res.status}`);
  }
  return await res.json();
}

function resourceToMcp(rec) {
  return {
    uri: `mcp+article://sebastienrousseau.com/${rec.slug}`,
    name: rec.title,
    description: rec.summary,
    mimeType: 'text/markdown',
    canonical: rec.url,
    lang: rec.lang || 'en',
    license: rec.license || 'CC-BY-4.0',
    tags: rec.tags || [],
    pillars: rec.pillars || [],
    published_at: rec.published_at,
    updated_at: rec.updated_at,
  };
}

async function handleListResources(url, manifest) {
  const cursor = parseIntParam(url.searchParams.get('cursor'), 0);
  const limit = clampLimit(url.searchParams.get('limit'));
  const all = manifest.resources || [];
  const slice = all.slice(cursor, cursor + limit);
  const next = cursor + limit < all.length ? String(cursor + limit) : null;
  return jsonResponse({
    resources: slice.map(resourceToMcp),
    nextCursor: next,
    total: all.length,
  });
}

function findBySlugOrUri(manifest, key) {
  const all = manifest.resources || [];
  const slug = key.startsWith('mcp+article://sebastienrousseau.com/')
    ? key.replace('mcp+article://sebastienrousseau.com/', '')
    : key.startsWith('https://sebastienrousseau.com/')
      ? key.replace('https://sebastienrousseau.com/', '').replace(/\/$/, '')
      : key.replace(/^\/+|\/+$/g, '');
  return all.find(r => r.slug === slug);
}

async function handleReadResource(url, manifest, originBase) {
  const uri = url.searchParams.get('uri');
  if (!uri) return errorResponse(400, 'missing-uri', 'uri query parameter required');
  const rec = findBySlugOrUri(manifest, uri);
  if (!rec) return errorResponse(404, 'not-found', `no resource for ${uri}`);
  // Body is the markdown record from /feed.jsonl (one JSON line per
  // article). Read the full feed once and pick the matching record.
  const feedRes = await fetch(`${originBase}/feed.jsonl`, {
    cf: { cacheTtl: 3600, cacheEverything: true },
  });
  if (!feedRes.ok) {
    return errorResponse(502, 'corpus-unavailable', `feed ${feedRes.status}`);
  }
  const text = await feedRes.text();
  let body = null;
  for (const line of text.split('\n')) {
    if (!line) continue;
    try {
      const obj = JSON.parse(line);
      if (obj && obj.url && obj.url.includes(`/${rec.slug}/`)) {
        body = obj;
        break;
      }
    } catch {
      // skip malformed line
    }
  }
  if (!body) return errorResponse(404, 'not-found', `feed missing ${rec.slug}`);
  return jsonResponse({
    contents: [
      {
        uri: `mcp+article://sebastienrousseau.com/${rec.slug}`,
        mimeType: 'text/markdown',
        text: body.body_markdown || '',
        metadata: {
          title: body.title,
          summary: body.summary,
          canonical: body.url,
          license: body.license || 'CC-BY-4.0',
          tags: body.tags || [],
          pillars: body.pillars || [],
          published_at: body.published_at,
          updated_at: body.updated_at,
        },
      },
    ],
  });
}

async function handleSearch(url, manifest) {
  const q = (url.searchParams.get('q') || '').toLowerCase().trim();
  const tag = (url.searchParams.get('tag') || '').toLowerCase().trim();
  const limit = clampLimit(url.searchParams.get('limit'));
  const all = manifest.resources || [];
  const matches = all.filter(rec => {
    if (tag) {
      const tags = (rec.tags || []).map(t => t.toLowerCase());
      const pillars = (rec.pillars || []).map(t => t.toLowerCase());
      if (!tags.includes(tag) && !pillars.includes(tag)) return false;
    }
    if (q) {
      const hay = `${rec.title || ''} ${rec.summary || ''}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return q || tag ? true : false;
  });
  return jsonResponse({
    resources: matches.slice(0, limit).map(resourceToMcp),
    total: matches.length,
    query: { q: q || null, tag: tag || null },
  });
}

/**
 * Entry point — return a Response if the path is an MCP route, null
 * otherwise. The lang-router checks this before locale routing.
 */
export async function tryMCP(request, originBase = ORIGIN_BASE) {
  const url = new URL(request.url);
  if (!isMCPRoute(url.pathname)) return null;
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CACHE_HEADERS });
  }
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return errorResponse(405, 'method-not-allowed', 'GET only');
  }
  let manifest;
  try {
    manifest = await fetchManifest(originBase);
  } catch (err) {
    return errorResponse(503, 'manifest-unavailable', err.message);
  }
  if (url.pathname === '/mcp/v1/list_resources') {
    return handleListResources(url, manifest);
  }
  if (url.pathname === '/mcp/v1/read_resource') {
    return handleReadResource(url, manifest, originBase);
  }
  if (url.pathname === '/mcp/v1/search') {
    return handleSearch(url, manifest);
  }
  return errorResponse(404, 'unknown-route', `no handler for ${url.pathname}`);
}
