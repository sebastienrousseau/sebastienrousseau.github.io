/**
 * Cloudflare Worker — Accept-Language redirect + edge security headers.
 *
 * Two responsibilities, both running on every request that hits the
 * apex domain (the Worker is wired to `sebastienrousseau.com/*` and
 * `www.sebastienrousseau.com/*` in the Cloudflare dashboard, sitting
 * in front of the GitHub Pages origin):
 *
 *   1. Locale routing. Bare-root visitors get a 302 to their preferred
 *      locale subtree when they haven't already picked one, their
 *      `Accept-Language` header names an active non-EN language, and a
 *      static page actually exists for that language at the requested
 *      path. Honours the `pref-lang` cookie + `?lang=xx` override.
 *
 *   2. Strict security headers on every response — most importantly
 *      Content-Security-Policy. The header CSP mirrors the per-page
 *      <meta http-equiv="Content-Security-Policy"> that postbuild
 *      injects, minus the per-page sha256 script/style hashes (which
 *      can only live in the meta tag). Browsers enforce the intersection
 *      of header + meta, so the page-specific hashes still narrow
 *      script-src to the exact inline JSON-LD blob on that page, while
 *      `form-action`, `frame-ancestors`, HSTS, X-Content-Type-Options,
 *      Referrer-Policy and Permissions-Policy live in the header where
 *      they're effective.
 *
 * Sub-50ms target — no fetches beyond the origin pass-through, no KV,
 * no compute beyond header parsing and a Headers copy.
 *
 * Deploy: Cloudflare dashboard → Workers & Pages → create application →
 * paste this file → routes:
 *     sebastienrousseau.com/*
 *     www.sebastienrousseau.com/*
 *
 * Once this Worker is live, any `Content-Security-Policy` Transform Rule
 * configured in the Cloudflare dashboard becomes redundant and should
 * be removed so the header CSP has a single source of truth in-repo.
 */

// Active non-EN languages with rendered subtrees in /docs/. Keep this list in
// sync with `scripts/_lang_registry.py`'s `active=True` entries. If a
// language ships static pages they get routed here; otherwise the Worker
// falls through to the EN tree.
export const ACTIVE_LANGS = new Set([
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

// CSP directives, mirroring the per-page meta-CSP that postbuild injects.
// The header version intentionally omits per-page script-src/style-src
// sha256 hashes (they live in the meta tag and narrow further via
// intersection) and adds frame-ancestors, which only has effect when
// served as a response header.
export const CSP_DIRECTIVES = [
  "default-src 'self'",
  "base-uri 'self'",
  "form-action 'self' https://formspree.io",
  "object-src 'none'",
  "frame-ancestors 'none'",
  "upgrade-insecure-requests",
  // Header script-src uses 'unsafe-inline' because per-page sha256 hashes
  // can only live in the meta-CSP. Browser intersection means the meta
  // hash still gates the actual inline JSON-LD blob; this directive
  // only constrains the external-script allowlist at the header layer.
  "script-src 'self' 'unsafe-inline' https://www.google-analytics.com https://www.googletagmanager.com https://www.google.com https://www.gstatic.com https://open.spotify.com https://static.cloudflareinsights.com https://challenges.cloudflare.com https://ajax.cloudflare.com",
  "frame-src 'self' https://www.google.com https://open.spotify.com https://www.youtube.com https://www.youtube-nocookie.com",
  "connect-src 'self' https://www.googletagmanager.com https://www.google-analytics.com https://region1.google-analytics.com https://www.google.com https://stats.g.doubleclick.net https://open.spotify.com",
  "img-src 'self' data: blob: https://cloudcdn.pro https://pacs008.com https://www.googletagmanager.com https://i.scdn.co",
  "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src 'self' https://fonts.gstatic.com",
  "media-src 'self' https://p.scdn.co https://*.scdn.co",
];

export function buildCspHeader() {
  return CSP_DIRECTIVES.join('; ');
}

// Security headers applied to every response. Keys are spelled in the
// canonical Title-Case form for readability; the Headers API is
// case-insensitive on lookup.
export const SECURITY_HEADERS = {
  'Content-Security-Policy': buildCspHeader(),
  // Two years, all subdomains, preload-eligible.
  'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  // Lock down the most-abused legacy feature surfaces. Topics + interest
  // cohort opt-out keeps Chrome's Privacy Sandbox out of the page.
  'Permissions-Policy': 'browsing-topics=(), interest-cohort=(), camera=(), microphone=(), geolocation=()',
  // Defense-in-depth: keep cross-origin window references from poking at
  // the page once it's loaded. Belt-and-braces with frame-ancestors.
  'Cross-Origin-Opener-Policy': 'same-origin',
};

/**
 * Return a clone of `response` with the strict security headers applied
 * on top of whatever the origin (or `Response.redirect`) produced. Any
 * pre-existing header with the same name is overwritten — the Worker
 * owns these.
 *
 * `extraHeaders` is an optional plain-object map merged in last; used by
 * the redirect path to append `Set-Cookie` without forking the wrapping
 * logic.
 */
export function withSecurityHeaders(response, extraHeaders) {
  const headers = new Headers(response.headers);
  for (const name of Object.keys(SECURITY_HEADERS)) {
    headers.set(name, SECURITY_HEADERS[name]);
  }
  if (extraHeaders) {
    for (const name of Object.keys(extraHeaders)) {
      headers.append(name, extraHeaders[name]);
    }
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

/**
 * Parse a single `Accept-Language` header into a list of language codes
 * ordered by descending q-value, normalised to lowercase. Whitespace,
 * malformed q-values and the wildcard `*` are tolerated.
 */
export function parseAcceptLanguage(header) {
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
export function pickSiteLang(tags) {
  for (const tag of tags) {
    if (TAG_TO_LANG[tag]) return TAG_TO_LANG[tag];
    const base = tag.split('-')[0];
    if (TAG_TO_LANG[base]) return TAG_TO_LANG[base];
  }
  return null;
}

export function getCookie(cookieHeader, name) {
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
export function isPageNavigation(pathname) {
  if (pathname === '/' || pathname === '/index.html') return true;
  // Asset / API / feed extensions: pass through unchanged.
  if (/\.(?:css|js|map|json|xml|txt|webp|jpg|jpeg|png|svg|ico|woff2?|pdf|wasm)$/i.test(pathname)) {
    return false;
  }
  // Language-neutral roots that should not be redirected.
  const NEUTRAL_PREFIXES = ['/api/', '/_csp/', '/.well-known/', '/v1/'];
  if (NEUTRAL_PREFIXES.some(p => pathname.startsWith(p))) return false;
  // Already inside a known language subtree — leave it alone.
  // pathname always starts with '/' per URL spec, so split('/')[1] is a
  // string (possibly empty); no fallback needed.
  const firstSegment = pathname.split('/')[1];
  if (firstSegment && ACTIVE_LANGS.has(firstSegment.toLowerCase())) return false;
  return true;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Only act on GET / HEAD page navigation; everything else still gets
    // security headers via the pass-through wrapper.
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return withSecurityHeaders(await fetch(request));
    }
    if (!isPageNavigation(url.pathname)) {
      return withSecurityHeaders(await fetch(request));
    }
    // Visitor has chosen — respect that choice forever (until cookie expires).
    const cookieHeader = request.headers.get('Cookie');
    const prefLang = getCookie(cookieHeader, COOKIE);
    if (prefLang === 'en') {
      return withSecurityHeaders(await fetch(request));
    }
    if (prefLang && ACTIVE_LANGS.has(prefLang)) {
      const redirected = new URL(url);
      redirected.pathname = `/${prefLang}${url.pathname === '/' ? '/' : url.pathname}`;
      return withSecurityHeaders(Response.redirect(redirected.toString(), 302));
    }
    // Honour `?lang=xx` as a one-off override (no cookie set — the user
    // is just deep-linking) — and respect ?lang=en as an opt-out signal.
    const overrideLang = url.searchParams.get('lang');
    if (overrideLang === 'en') {
      return withSecurityHeaders(await fetch(request));
    }
    if (overrideLang && ACTIVE_LANGS.has(overrideLang.toLowerCase())) {
      const redirected = new URL(url);
      redirected.pathname = `/${overrideLang.toLowerCase()}${url.pathname === '/' ? '/' : url.pathname}`;
      redirected.searchParams.delete('lang');
      const cookieValue = `${COOKIE}=${overrideLang.toLowerCase()}; Path=/; Max-Age=${COOKIE_MAX_AGE}; SameSite=Lax; Secure`;
      return withSecurityHeaders(
        Response.redirect(redirected.toString(), 302),
        { 'Set-Cookie': cookieValue },
      );
    }
    // No cookie, no override — fall back to Accept-Language sniffing.
    const tags = parseAcceptLanguage(request.headers.get('Accept-Language'));
    if (tags.length === 0) {
      return withSecurityHeaders(await fetch(request));
    }
    // If EN ranks first in the visitor's preference list, leave them be —
    // they want the canonical site. parseAcceptLanguage drops empty tags,
    // so tags[0] is a non-empty string and split('-')[0] is at minimum ''.
    const topBase = tags[0].split('-')[0].toLowerCase();
    if (topBase === 'en') {
      return withSecurityHeaders(await fetch(request));
    }
    const siteLang = pickSiteLang(tags);
    if (!siteLang) {
      return withSecurityHeaders(await fetch(request));
    }
    const redirected = new URL(url);
    redirected.pathname = `/${siteLang}${url.pathname === '/' ? '/' : url.pathname}`;
    return withSecurityHeaders(Response.redirect(redirected.toString(), 302));
  },
};
