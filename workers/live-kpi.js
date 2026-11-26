// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
/**
 * Live headline figures for every page that shows them.
 *
 * The GitHub profile (github.com/sebastienrousseau) and this site show the
 * same four figures: all-time downloads, downloads in the last 30 days,
 * GitHub stars and packages published. The profile refreshes them every
 * three hours into `profile.json` on its `profile-data` branch; the build
 * only reads them when the site deploys, so between deploys the two drifted
 * apart.
 *
 * This module rewrites the text of each `[data-kpi]` element for those four
 * keys with the exact strings the profile's numbers panel prints
 * (`numbers.display` in profile.json), so both always show the same
 * figures. The build-time value stays in the HTML as the fallback: any
 * problem with profile.json leaves the page as it was built.
 *
 * Guard rails:
 *   - One fixed upstream URL, edge-cached for five minutes; nothing from
 *     the request reaches it.
 *   - profile.json is fetched only once a page actually has one of the
 *     four elements, and at most once per response.
 *   - A display string must look like a figure (FIGURE_RE) or it is not
 *     used; only text content is replaced, never markup.
 */
const PROFILE = 'https://raw.githubusercontent.com/sebastienrousseau/sebastienrousseau/profile-data/profile.json';
const EDGE = { cf: { cacheTtl: 300, cacheEverything: true } };
// Site data-kpi key -> profile.json numbers key.
const KEYS = {
  downloads_total: 'all_time_downloads',
  downloads_30d: 'recent_downloads',
  github_stars: 'github_stars',
  packages_published: 'packages',
};
const FIGURE_RE = /^\d{1,9}(\.\d)?[KM]?$/;

/** The four display strings keyed by data-kpi name, or null. Never throws. */
export async function loadFigures() {
  try {
    const res = await fetch(PROFILE, EDGE);
    if (!res.ok) return null;
    const display = (await res.json())?.numbers?.display;
    const figures = {};
    for (const [ours, theirs] of Object.entries(KEYS)) {
      const value = display?.[theirs];
      if (typeof value !== 'string' || !FIGURE_RE.test(value)) return null;
      figures[ours] = value;
    }
    return figures;
  } catch {
    return null;
  }
}

/** True for a 200 HTML response with a body, on a runtime with HTMLRewriter. */
function rewritable(response) {
  if (typeof HTMLRewriter === 'undefined') return false; // Node tests, local tools
  const type = response.headers.get('Content-Type') || '';
  return response.status === 200 && response.body !== null && type.startsWith('text/html');
}

/**
 * The response with its four headline figures replaced by the profile's,
 * or the response unchanged when it is not a page with a body.
 */
export function withLiveFigures(response, load = loadFigures) {
  if (!rewritable(response)) return response;
  let figures;
  const handler = {
    async element(el) {
      const key = el.getAttribute('data-kpi');
      if (!Object.hasOwn(KEYS, key)) return;
      figures ??= load();
      const value = (await figures)?.[key];
      if (value) el.setInnerContent(value);
    },
  };
  return new HTMLRewriter().on('[data-kpi]', handler).transform(response);
}
