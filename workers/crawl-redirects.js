// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * One 301 for each kind of URL Search Console reported that no page should
 * have produced, so a crawler that still holds one lands on a real page:
 *
 *  - `/<page>/index.html` is the same page as `/<page>/`; Google kept
 *    picking a canonical between the two. Sent to the directory URL, the
 *    one every canonical tag names (rustdoc project pages included).
 *  - A link that lost its markup. A Markdown link pasted whole into a URL
 *    (`/<text>](/<target>)<rest>`) goes to its target; a segment opened by
 *    a quote (`/<page>/”/about/index.html”`, typographic quotes left in a
 *    translated href) is dropped with everything after it.
 *  - A URL pattern read as a link (`/*`, `/*.pdf`, `/contact/*`, from the
 *    inline speculation rules before they used CSS selectors) goes home.
 *  - `/mcp/`, the root of the site's MCP API, has no page: its product page.
 *  - `?__build=<id>`, the Worker's own origin cache key, which GitHub Pages
 *    once echoed into its redirects: the same URL without it.
 */

const MARKDOWN_LINK_RE = /\]\((\/[^)\s]*)\)/;
const QUOTES = new Set(['"', "'", '“', '”', '‘', '’']);
const FIXED = new Map([
  ['/mcp', '/iso20022-mcp/'],
  ['/mcp/', '/iso20022-mcp/'],
]);

/** The decoded path, or the path as sent when its escapes are malformed. */
export function safeDecodePath(pathname) {
  try {
    return decodeURIComponent(pathname);
  } catch {
    return pathname;
  }
}

function withoutIndex(path) {
  return path.endsWith('/index.html') ? path.slice(0, -'index.html'.length) : path;
}

function mangledTarget(path) {
  const markdown = MARKDOWN_LINK_RE.exec(path);
  if (markdown) return withoutIndex(markdown[1]);
  if (path.includes('*')) return '/';
  const segments = path.split('/');
  const cut = segments.findIndex((segment) => QUOTES.has(segment[0]));
  if (cut !== -1) return `${segments.slice(0, cut).join('/')}/`;
  return FIXED.get(path) || null;
}

/** 301 Response for a URL no page should have produced, else null. */
export function tryCrawlRedirect(url) {
  const path = safeDecodePath(url.pathname);
  const target = mangledTarget(path) || withoutIndex(path);
  const leaked = url.searchParams.has('__build');
  if (target === path && !leaked) return null;
  const redirected = new URL(url);
  redirected.pathname = target;
  redirected.searchParams.delete('__build');
  return Response.redirect(redirected.toString(), 301);
}
