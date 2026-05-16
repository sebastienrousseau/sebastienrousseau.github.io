/**
 * Cloudflare Worker — Accept-Language redirect at the edge.
 *
 * Visitors hitting the bare root path receive a 302 to their preferred
 * locale subtree when:
 *   1. They haven't already declared a preference (no `pref-lang` cookie).
 *   2. Their `Accept-Language` header names one of the site's active
 *      non-EN languages — and a static page actually exists for that
 *      language at the requested path.
 *
 * Everything else passes through untouched. Sub-50ms target — no
 * fetches, no KV, no compute beyond header parsing.
 *
 * Deploy: Cloudflare dashboard → Workers & Pages → create application →
 * paste this file → routes:
 *     sebastienrousseau.com/*
 *
 * The site is GitHub Pages-backed; Cloudflare proxies all traffic so
 * the Worker is the first thing visitors hit.
 */

// Active non-EN languages with rendered subtrees in /docs/. Keep this list in
// sync with `scripts/_lang_registry.py`'s `active=True` entries. If a
// language ships static pages they get routed here; otherwise the Worker
// falls through to the EN tree.
const ACTIVE_LANGS = new Set([
  'ar', 'bn', 'cs', 'de', 'es', 'fil', 'fr', 'ha', 'he', 'hi', 'id',
  'it', 'ja', 'ko', 'nl', 'pl', 'pt-br', 'ro', 'ru', 'sv', 'th', 'tr',
  'uk', 'vi', 'yo', 'zh-hans', 'zh-hant',
]);

// BCP-47 base tag → site lang code. Multiple base tags can map to the
// same site code (e.g. 'pt-PT' and 'pt-BR' both map to 'pt-br').
const TAG_TO_LANG = {
  'ar': 'ar',
  'bn': 'bn',
  'cs': 'cs',
  'de': 'de',
  'es': 'es',
  'fil': 'fil',  'tl': 'fil',
  'fr': 'fr',
  'ha': 'ha',
  'he': 'he',
  'hi': 'hi',
  'id': 'id',
  'it': 'it',
  'ja': 'ja',
  'ko': 'ko',
  'nl': 'nl',
  'pl': 'pl',
  'pt': 'pt-br',  // pt-BR ships first; pt-PT readers get pt-br
  'ro': 'ro',
  'ru': 'ru',
  'sv': 'sv',
  'th': 'th',
  'tr': 'tr',
  'uk': 'uk',
  'vi': 'vi',
  'yo': 'yo',
  'zh-cn': 'zh-hans', 'zh-sg': 'zh-hans', 'zh-hans': 'zh-hans',
  'zh-tw': 'zh-hant', 'zh-hk': 'zh-hant', 'zh-mo': 'zh-hant', 'zh-hant': 'zh-hant',
};

const COOKIE = 'pref-lang';
// 30 days — long enough to be sticky, short enough to honour later changes.
const COOKIE_MAX_AGE = 60 * 60 * 24 * 30;

/**
 * Parse a single `Accept-Language` header into a list of language codes
 * ordered by descending q-value, normalised to lowercase. Whitespace,
 * malformed q-values and the wildcard `*` are tolerated.
 */
function parseAcceptLanguage(header) {
  if (!header) return [];
  return header
    .split(',')
    .map(part => {
      const [tag, ...params] = part.trim().split(';');
      let q = 1.0;
      for (const p of params) {
        const m = p.trim().match(/^q=([\d.]+)$/);
        if (m) q = parseFloat(m[1]) || 0;
      }
      return { tag: tag.trim().toLowerCase(), q };
    })
    .filter(t => t.tag && t.tag !== '*')
    .sort((a, b) => b.q - a.q)
    .map(t => t.tag);
}

/**
 * Map a list of BCP-47 tags (already ordered by preference) to the first
 * site lang code we serve. Tries the exact tag first, then the language
 * primary subtag.
 */
function pickSiteLang(tags) {
  for (const tag of tags) {
    if (TAG_TO_LANG[tag]) return TAG_TO_LANG[tag];
    const base = tag.split('-')[0];
    if (TAG_TO_LANG[base]) return TAG_TO_LANG[base];
  }
  return null;
}

function getCookie(cookieHeader, name) {
  if (!cookieHeader) return null;
  for (const part of cookieHeader.split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return decodeURIComponent(v.join('='));
  }
  return null;
}

/**
 * Reject paths that obviously aren't human page navigation — assets,
 * feeds, API endpoints, well-known metadata. These are language-neutral
 * by design.
 */
function isPageNavigation(pathname) {
  if (pathname === '/' || pathname === '/index.html') return true;
  // Asset / API / feed extensions: pass through unchanged.
  if (/\.(?:css|js|map|json|xml|txt|webp|jpg|jpeg|png|svg|ico|woff2?|pdf|wasm)$/i.test(pathname)) {
    return false;
  }
  // Language-neutral roots that should not be redirected.
  const NEUTRAL_PREFIXES = ['/api/', '/_csp/', '/.well-known/', '/v1/'];
  if (NEUTRAL_PREFIXES.some(p => pathname.startsWith(p))) return false;
  // Already inside a known language subtree — leave it alone.
  const firstSegment = pathname.split('/')[1] || '';
  if (ACTIVE_LANGS.has(firstSegment.toLowerCase())) return false;
  return true;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Only act on GET / HEAD page navigation.
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return fetch(request);
    }
    if (!isPageNavigation(url.pathname)) {
      return fetch(request);
    }
    // Visitor has chosen — respect that choice forever (until cookie expires).
    const cookieHeader = request.headers.get('Cookie');
    const prefLang = getCookie(cookieHeader, COOKIE);
    if (prefLang === 'en') {
      return fetch(request);
    }
    if (prefLang && ACTIVE_LANGS.has(prefLang)) {
      const redirected = new URL(url);
      redirected.pathname = `/${prefLang}${url.pathname === '/' ? '/' : url.pathname}`;
      return Response.redirect(redirected.toString(), 302);
    }
    // Honour `?lang=xx` as a one-off override (no cookie set — the user
    // is just deep-linking) — and respect ?lang=en as an opt-out signal.
    const overrideLang = url.searchParams.get('lang');
    if (overrideLang === 'en') {
      return fetch(request);
    }
    if (overrideLang && ACTIVE_LANGS.has(overrideLang.toLowerCase())) {
      const redirected = new URL(url);
      redirected.pathname = `/${overrideLang.toLowerCase()}${url.pathname === '/' ? '/' : url.pathname}`;
      redirected.searchParams.delete('lang');
      const response = Response.redirect(redirected.toString(), 302);
      const headers = new Headers(response.headers);
      headers.append(
        'Set-Cookie',
        `${COOKIE}=${overrideLang.toLowerCase()}; Path=/; Max-Age=${COOKIE_MAX_AGE}; SameSite=Lax; Secure`,
      );
      return new Response(response.body, { status: 302, headers });
    }
    // No cookie, no override — fall back to Accept-Language sniffing.
    const tags = parseAcceptLanguage(request.headers.get('Accept-Language'));
    if (tags.length === 0) {
      return fetch(request);
    }
    // If EN ranks first in the visitor's preference list, leave them be —
    // they want the canonical site.
    const topBase = (tags[0].split('-')[0] || '').toLowerCase();
    if (topBase === 'en') {
      return fetch(request);
    }
    const siteLang = pickSiteLang(tags);
    if (!siteLang) {
      return fetch(request);
    }
    const redirected = new URL(url);
    redirected.pathname = `/${siteLang}${url.pathname === '/' ? '/' : url.pathname}`;
    return Response.redirect(redirected.toString(), 302);
  },
};
