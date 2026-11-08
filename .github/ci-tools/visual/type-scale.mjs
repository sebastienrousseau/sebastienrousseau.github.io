// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/* Type-scale gate for the CI `visual` job.
 *
 *   node type-scale.mjs [--base http://127.0.0.1:8080] [--report]
 *
 * The shared stylesheet defines one fluid type scale (--fs-micro to
 * --fs-display). At 390, 1024, 1440 and 1920 px wide this renders a probe
 * element per token on each of the key pages, reads the size the token
 * resolves to there, and then checks every visible text element (h1, h2,
 * h3, p, li, summary, label and anything whose class names an eyebrow,
 * outside the nav, the footer, code and SVG) against those sizes. An
 * element whose computed font-size is not within 0.6 px of a token fails,
 * and so does a page that scrolls sideways (scrollWidth > clientWidth).
 *
 * --report also prints the H1, H2 and eyebrow sizes found on each page.
 * Exit status: 0 when every page passes, 1 otherwise.
 */

import puppeteer from 'puppeteer-core';
import { existsSync } from 'node:fs';

const PAGES = {
  home: '/index.html',
  'iso20022-mcp': '/iso20022-mcp/index.html',
  speaking: '/speaking/index.html',
  trust: '/trust/index.html',
  'case-studies': '/case-studies/index.html',
  research: '/research/index.html',
  topics: '/topics/index.html',
  articles: '/articles/index.html',
  article: '/2026-10-28-why-the-fca-is-regulating-ai-without-an-ai-rulebook/index.html',
  about: '/about/index.html',
  contact: '/contact/index.html',
};

const WIDTHS = [390, 1024, 1440, 1920];

const TOKENS = [
  'micro', 'meta', 'small', 'ui', 'body', 'prose', 'lead',
  'h4', 'h3', 'h2-prose', 'h2', 'h1', 'display', 'stat',
];

const TOLERANCE = 0.6;

const CHROME_ARGS = [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--blink-settings=preferredColorScheme=1',
  '--force-prefers-reduced-motion',
  '--hide-scrollbars',
];

function findChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const candidates = [
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ];
  for (const p of candidates) if (existsSync(p)) return p;
  throw new Error('No Chrome/Chromium found; set CHROME_PATH');
}

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 ? process.argv[i + 1] : fallback;
}

// Runs in the page: resolve each token, then list every visible text
// element whose size is not one of them.
function measure(tokens, tolerance) {
  // One fresh probe per token: restyling a single probe in a loop read
  // back the first token's size for every token in headless Chrome.
  const sizes = {};
  for (const t of tokens) {
    const probe = document.createElement('span');
    probe.textContent = 'x';
    probe.style.fontSize = `var(--fs-${t})`;
    document.body.appendChild(probe);
    sizes[t] = parseFloat(getComputedStyle(probe).fontSize);
    probe.remove();
  }
  const fallback = parseFloat(getComputedStyle(document.body).fontSize);
  const error = Object.values(sizes).every((v) => v === fallback)
    ? 'no --fs-* tokens resolve on this page'
    : '';
  const skip = 'nav, footer, pre, code, svg, .mcp-term';
  const sel = 'h1, h2, h3, p, li, summary, label, [class*="eyebrow"]';
  const visible = (el) => {
    if (!el.textContent.trim()) return false;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return false;
    const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none' && cs.opacity !== '0';
  };
  const describe = (el) => {
    const cls = typeof el.className === 'string' ? el.className.trim().split(/\s+/).slice(0, 2) : [];
    const parent = el.parentElement && el.parentElement.className;
    const where = typeof parent === 'string' && parent ? ` in .${parent.trim().split(/\s+/)[0]}` : '';
    return `${el.tagName.toLowerCase()}${cls.map((c) => `.${c}`).join('')}${where}`;
  };
  const bad = [];
  const seen = { h1: [], h2: [], eyebrow: [] };
  for (const el of document.querySelectorAll(sel)) {
    if (el.closest(skip) || !visible(el)) continue;
    const px = parseFloat(getComputedStyle(el).fontSize);
    const tag = el.tagName.toLowerCase();
    if (tag === 'h1' || tag === 'h2') seen[tag].push(px);
    if (/eyebrow|kicker/.test(String(el.className))) seen.eyebrow.push(px);
    const ok = Object.values(sizes).some((v) => Math.abs(v - px) <= tolerance);
    if (!ok && !error) bad.push(`${describe(el)} ${px}px "${el.textContent.trim().slice(0, 40)}"`);
  }
  const de = document.documentElement;
  const overflow = de.scrollWidth > de.clientWidth ? `${de.scrollWidth} > ${de.clientWidth}` : '';
  return { error, sizes, bad, seen, overflow };
}

const uniq = (xs) => [...new Set(xs.map((x) => Math.round(x)))].sort((a, b) => a - b).join(' / ') || '-';

async function checkPage(browser, base, name, path, width, report) {
  const context = await browser.createBrowserContext();
  try {
    const page = await context.newPage();
    await page.setViewport({ width, height: 900, deviceScaleFactor: 1 });
    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
    const baseHost = new URL(base).host;
    await page.setRequestInterception(true);
    page.on('request', (req) => {
      let host = '';
      try {
        host = new URL(req.url()).host;
      } catch {
        /* data:/about: URLs: allow */
      }
      if (host === '' || host === baseHost) req.continue();
      else req.abort('blockedbyclient');
    });
    await page.goto(`${base}${path}`, { waitUntil: 'networkidle0', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    const r = await page.evaluate(measure, TOKENS, TOLERANCE);
    const label = `${name}@${width}`;
    if (report) {
      console.log(`size ${label}: h1 ${uniq(r.seen?.h1 || [])} | h2 ${uniq(r.seen?.h2 || [])} | eyebrow ${uniq(r.seen?.eyebrow || [])}`);
    }
    const problems = [];
    if (r.error) problems.push(r.error);
    for (const b of r.bad || []) problems.push(`off-scale ${b}`);
    if (r.overflow) problems.push(`horizontal overflow ${r.overflow}`);
    for (const p of problems) console.log(`FAIL ${label}: ${p}`);
    if (problems.length === 0) console.log(`ok   ${label}`);
    return problems.length;
  } finally {
    await context.close().catch(() => {});
  }
}

const base = arg('base', 'http://127.0.0.1:8080').replace(/\/$/, '');
const report = process.argv.includes('--report');
const browser = await puppeteer.launch({ executablePath: findChrome(), args: CHROME_ARGS });
let failures = 0;
try {
  for (const [name, path] of Object.entries(PAGES)) {
    for (const width of WIDTHS) {
      failures += await checkPage(browser, base, name, path, width, report);
    }
  }
} finally {
  await browser.close();
}
if (failures > 0) {
  console.log(`${failures} type-scale problem(s)`);
  process.exit(1);
}
console.log('type scale: every page on the scale');
