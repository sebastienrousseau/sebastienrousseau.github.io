// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/* Visual-regression harness for the CI `visual` job.
 *
 * Two subcommands:
 *
 *   node visual.mjs shoot   --base <url> --out <dir>
 *   node visual.mjs compare --baseline <dir> --current <dir> --diff <dir>
 *                           [--max-diff-ratio 0.01]
 *
 * `shoot` screenshots the six key pages at 1440px wide in the LIGHT
 * theme, forced deterministically at Chrome launch with
 * --blink-settings=preferredColorScheme=1 (Blink enum kLight=1), so
 * the host/system theme can never leak into the pixels. Animations,
 * transitions and carets are disabled by injected CSS before capture.
 *
 * `compare` runs pixelmatch between baseline/ and current/ PNGs and
 * fails (exit 1) when any page's changed-pixel ratio exceeds
 * --max-diff-ratio (default 1%). Diff heatmap PNGs are written to
 * --diff for upload as workflow artifacts.
 *
 * Baseline regeneration: run the build-audit workflow via
 * workflow_dispatch with refresh-baselines=true and download the
 * `visual-baselines-refresh` artifact; commit its PNGs to
 * .github/ci-tools/visual/baseline/. Baselines are renderer-specific
 * (font rasterisation differs across OSes), so runner-rendered
 * baselines are the source of truth for CI; locally-rendered ones are
 * only valid for local runs.
 */

import { mkdirSync, readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import puppeteer from 'puppeteer-core';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';

// One entry per layout/surface family. Keys are the stable screenshot
// file names; values the public/-relative page paths.
const PAGES = {
  home: 'index.html',
  hub: 'iso20022-mcp/index.html',
  docs: 'iso20022-mcp-docs/index.html',
  trust: 'trust/index.html',
  // /papers/ is a meta-refresh stub since the /research/ move; shoot
  // the real content page (the stub would redirect Puppeteer to the
  // PRODUCTION site and screenshot that instead of the local build).
  papers: 'research/index.html',
  speaking: 'speaking/index.html',
};

const VIEWPORT = { width: 1440, height: 900, deviceScaleFactor: 1 };

// Deterministic rendering: force light theme + reduced motion at the
// engine level, regardless of the host OS theme.
const CHROME_ARGS = [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--blink-settings=preferredColorScheme=1',
  '--force-prefers-reduced-motion',
  '--hide-scrollbars',
  '--disable-lcd-text',
  '--font-render-hinting=none',
];

const FREEZE_CSS = `
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
    caret-color: transparent !important;
  }
`;

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

// Puppeteer protocol errors that mean "the page moved under us" rather
// than "the page is wrong": a client-side navigation, reload or history
// hop tears down the execution context mid-evaluate. These are transient
// and safe to retry from a clean navigation; they must NOT be confused
// with a real regression (a pixel diff or a wrong-theme assertion).
const TRANSIENT_ERROR =
  /Execution context was destroyed|Cannot find context|Target closed|Session closed|frame (?:was )?detached|Navigating frame/i;

async function newConfiguredPage(browser, baseHost) {
  const page = await browser.newPage();
  // The site ships a strict CSP (hash-pinned style-src) that would
  // reject the FREEZE_CSS injection. Bypassing CSP here only affects
  // this screenshot harness, never the shipped pages.
  await page.setBypassCSP(true);
  await page.setViewport(VIEWPORT);
  // Hermetic rendering: block every request that does not target the
  // local fixture server. Remote CDN images (cloudcdn.pro banners,
  // card art) load non-deterministically — measured 8.6% pixel churn
  // between two back-to-back local runs — and a CI runner's network
  // must never decide whether the gate passes. The trade-off is that
  // remote image CONTENT is not regression-tested; layout, chrome,
  // typography and every locally-served asset are.
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    let host = '';
    try {
      host = new URL(req.url()).host;
    } catch {
      /* data:/about: URLs — allow */
    }
    if (host === '' || host === baseHost) req.continue();
    else req.abort('blockedbyclient');
  });
  return page;
}

async function capturePage(page, name, url, out) {
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.addStyleTag({ content: FREEZE_CSS });
  // Self-hosted woff2 fonts must be rasterised before capture, or
  // a FOUT frame becomes a phantom whole-page diff.
  await page.evaluate(() => document.fonts.ready);
  // Walk the page so lazy-loaded images decode before capture.
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let y = 0;
      const step = () => {
        y += 900;
        window.scrollTo(0, y);
        if (y >= document.body.scrollHeight) {
          window.scrollTo(0, 0);
          resolve();
        } else {
          setTimeout(step, 60);
        }
      };
      step();
    });
  });
  await new Promise((r) => setTimeout(r, 400));
  const theme = await page.evaluate(() =>
    document.documentElement.getAttribute('data-theme'));
  if (theme !== 'light') {
    throw new Error(`${url}: expected light theme, got ${theme}`);
  }
  await page.screenshot({ path: join(out, `${name}.png`), fullPage: true });
  console.log(`shot ${name} <- ${url} (theme=${theme})`);
}

async function shoot() {
  const base = arg('base', 'http://127.0.0.1:8000').replace(/\/$/, '');
  const out = arg('out', 'shots');
  mkdirSync(out, { recursive: true });
  const baseHost = new URL(base).host;
  const browser = await puppeteer.launch({
    executablePath: findChrome(),
    args: CHROME_ARGS,
  });
  try {
    for (const [name, rel] of Object.entries(PAGES)) {
      const url = `${base}/${rel}`;
      // A transient teardown of the execution context is not a
      // regression — retry the page from a fresh tab. A real failure
      // (wrong theme, a genuinely broken page) is not TRANSIENT_ERROR
      // and rethrows on the first attempt, so the gate still fails fast.
      const MAX_ATTEMPTS = 3;
      for (let attempt = 1; ; attempt++) {
        const page = await newConfiguredPage(browser, baseHost);
        try {
          await capturePage(page, name, url, out);
          break;
        } catch (err) {
          const msg = String(err && err.message);
          if (!TRANSIENT_ERROR.test(msg) || attempt >= MAX_ATTEMPTS) throw err;
          console.log(
            `retry ${name} (attempt ${attempt}/${MAX_ATTEMPTS - 1} after: ${msg.split('\n')[0]})`,
          );
        } finally {
          await page.close().catch(() => {});
        }
      }
    }
  } finally {
    await browser.close();
  }
}

function compare() {
  const baselineDir = arg('baseline', 'baseline');
  const currentDir = arg('current', 'shots');
  const diffDir = arg('diff', 'diffs');
  const maxRatio = parseFloat(arg('max-diff-ratio', '0.01'));
  mkdirSync(diffDir, { recursive: true });

  const names = readdirSync(baselineDir).filter((f) => f.endsWith('.png'));
  if (names.length === 0) throw new Error(`no baseline PNGs in ${baselineDir}`);
  let failures = 0;
  for (const file of names) {
    const currentPath = join(currentDir, file);
    if (!existsSync(currentPath)) {
      console.log(`FAIL ${file}: missing current screenshot`);
      failures += 1;
      continue;
    }
    const a = PNG.sync.read(readFileSync(join(baselineDir, file)));
    const b = PNG.sync.read(readFileSync(currentPath));
    if (a.width !== b.width || a.height !== b.height) {
      console.log(
        `FAIL ${file}: size ${a.width}x${a.height} -> ${b.width}x${b.height} (layout shift)`);
      failures += 1;
      continue;
    }
    const diff = new PNG({ width: a.width, height: a.height });
    const changed = pixelmatch(a.data, b.data, diff.data, a.width, a.height, {
      threshold: 0.1,
    });
    const ratio = changed / (a.width * a.height);
    const pct = (ratio * 100).toFixed(3);
    if (ratio > maxRatio) {
      writeFileSync(join(diffDir, file), PNG.sync.write(diff));
      console.log(`FAIL ${file}: ${pct}% pixels differ (limit ${maxRatio * 100}%)`);
      failures += 1;
    } else {
      console.log(`ok   ${file}: ${pct}% pixels differ`);
    }
  }
  if (failures > 0) {
    console.log(`${failures} page(s) exceeded the visual-diff threshold; diffs in ${diffDir}/`);
    process.exit(1);
  }
}

const cmd = process.argv[2];
if (cmd === 'shoot') {
  await shoot();
} else if (cmd === 'compare') {
  compare();
} else {
  console.error('usage: node visual.mjs shoot|compare [--flags]');
  process.exit(2);
}
