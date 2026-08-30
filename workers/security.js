// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/**
 * Pre-filter for any future mutating endpoint that would otherwise be a
 * KV-write target for scrapers and bots. Free-tier defence in depth:
 * Bot Fight Mode + the 5 WAF rules + the 1 rate-limit rule live in the
 * Cloudflare dashboard; this module is the in-Worker layer that runs
 * *before* the mutating codepath so an undeclared scraper never touches
 * `env.KV.put()` or the `WriteCoalescer` DO.
 *
 * Policy: project-docs/adr/0001-kv-free-tier-policy.md (Part 4)
 *
 * Strategy:
 *   - Match on User-Agent against a curated denylist (AI scrapers,
 *     LLM crawlers, marketing bots, known mass-scrape clients).
 *   - Match on ASN against a curated denylist (datacentre ASNs used
 *     primarily for scraping; covers Tor exit ASNs and well-known
 *     headless-Chrome farms).
 *   - Accept Cloudflare's verified-bot signal (`cf.botManagement` is
 *     paid-only — Free gets only `cf.verifiedBotCategory` populated for
 *     genuinely verified bots; treat absence as "not verified").
 *
 * All matching is lower-case substring or numeric equality — cheap and
 * deterministic. No regex backtracking. Updated by hand; rolling cycle
 * via PR rather than per-request fetch.
 */

// Lower-case substring tokens. A User-Agent header containing ANY of these
// is rejected. Kept short on purpose — every entry adds CPU to every request.
export const UA_DENYLIST = Object.freeze([
  // AI scrapers
  'gptbot',
  'chatgpt-user',
  'oai-searchbot',
  'claudebot',
  'claude-web',
  'anthropic-ai',
  'perplexitybot',
  'ccbot',           // Common Crawl — high-volume scraper
  'meta-externalagent',
  'bytespider',      // ByteDance
  'diffbot',
  'amazonbot',
  'applebot-extended',
  'cohere-ai',
  'mistralai-user',
  'google-extended',
  // Mass-scraping clients
  'wget',
  'curl/7',
  'curl/8',
  'python-requests',
  'go-http-client',
  'scrapy',
  'httrack',
  'libwww-perl',
  'headlesschrome',
  'phantomjs',
]);

// Numeric ASN denylist. These are ASNs known primarily for scrapers,
// commercial proxy farms, or Tor. Real human users sit behind broadband
// ISPs and mobile carriers, not these.
export const ASN_DENYLIST = Object.freeze(new Set([
  13335,  // Cloudflare itself (loopback / our own probes)
  16509,  // Amazon AWS
  14618,  // Amazon AWS (different range)
  15169,  // Google Cloud
  8075,   // Microsoft Azure
  16276,  // OVH
  20473,  // Choopa / Vultr
  396982, // Google Cloud (additional)
  // Tor — common exit ASNs
  16276,  // OVH (also a Tor exit)
]));

/**
 * Return true if the request should be rejected before reaching a
 * KV-write path. Cheap O(N) where N = UA_DENYLIST length.
 *
 * @param {Request} request — Cloudflare Request with optional cf object.
 * @returns {{ blocked: boolean, reason: string | null }}
 */
export function classifyRequest(request) {
  const ua = (request.headers.get('user-agent') || '').toLowerCase();
  for (const tok of UA_DENYLIST) {
    if (ua.includes(tok)) {
      return { blocked: true, reason: `ua:${tok}` };
    }
  }
  const asn = request.cf && typeof request.cf.asn === 'number' ? request.cf.asn : null;
  if (asn !== null && ASN_DENYLIST.has(asn)) {
    return { blocked: true, reason: `asn:${asn}` };
  }
  return { blocked: false, reason: null };
}

/**
 * Convenience: 403 Response carrying the rejection reason in a header
 * (handy for diagnostics; never echoed back to the client body so the
 * denylist contents stay opaque to scrapers).
 */
export function rejectionResponse({ reason }) {
  return new Response('forbidden', {
    status: 403,
    headers: {
      'content-type': 'text/plain; charset=utf-8',
      'cache-control': 'no-store',
      // Reason goes to a private header so dashboard logs can diff it
      // without leaking the denylist surface to the client UA.
      'x-router-deny-reason': reason || 'unknown',
    },
  });
}

/**
 * One-call guard for mutating endpoints. Returns null when the request
 * passes; returns a 403 Response when it should be blocked.
 *
 * Usage in lang-router.js (when wiring a mutating endpoint):
 *   const deny = guardMutatingEndpoint(request);
 *   if (deny) return deny;
 *   // ...proceed to env.KV.put() / WriteCoalescer fetch
 */
export function guardMutatingEndpoint(request) {
  const verdict = classifyRequest(request);
  return verdict.blocked ? rejectionResponse(verdict) : null;
}
