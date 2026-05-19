/**
 * Cloudflare Worker — locale cookie / query-param routing + edge security headers.
 *
 * Two responsibilities, both running on every request that hits the
 * apex domain (the Worker is wired to `sebastienrousseau.com/*` and
 * `www.sebastienrousseau.com/*` in the Cloudflare dashboard, sitting
 * in front of the GitHub Pages origin):
 *
 *   1. Locale routing — explicit only. Visitors land on the canonical
 *      EN site by default. The Worker redirects to `/<lang>/<path>` only
 *      when the visitor has actively opted in: either a `pref-lang=<lang>`
 *      cookie (set by clicking the in-page locale switcher) or a
 *      `?lang=<lang>` deep-link parameter. Accept-Language is no longer
 *      sniffed — too many bilingual readers were getting bounced off the
 *      canonical site they actually wanted.
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
  // Header script-src deliberately omits 'unsafe-inline'. CSP intersection
  // means the meta-CSP hash list still gates the actual inline JSON-LD
  // blob on every postbuild-processed page, so this layer doesn't need
  // to repeat the relaxation. Stripping it closes the response-header
  // gap that security scanners flag and provides defence in depth on
  // any page that might bypass postbuild (none today — verified all
  // pages, including 404, ship with hashed meta-CSP).
  "script-src 'self' https://www.google.com https://www.gstatic.com https://open.spotify.com https://static.cloudflareinsights.com https://challenges.cloudflare.com https://ajax.cloudflare.com",
  "frame-src 'self' https://www.google.com https://open.spotify.com https://www.youtube.com https://www.youtube-nocookie.com",
  "connect-src 'self' https://www.google.com https://open.spotify.com",
  "img-src 'self' data: blob: https://cloudcdn.pro https://pacs008.com https://i.scdn.co",
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
    // No cookie, no override — serve the canonical EN site. Visitors
    // can still pick a locale via the in-page switcher (which sets
    // `pref-lang`) or by deep-linking with `?lang=xx`. Auto-redirect on
    // Accept-Language alone surprises too many bilingual readers who
    // expect the English version by default; keeping discovery opt-in.
    return withSecurityHeaders(await fetch(request));
  },
};
