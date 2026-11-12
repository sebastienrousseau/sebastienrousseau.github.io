// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/* Rendered design-system gate (Task 3.8).
 *
 * Verifies across 14 representative routes and 5 viewport widths
 * [390, 768, 1280, 1440, 1920]:
 *   1. Alignment: every visible h1/h2 (not centred, not inside cards/panels,
 *      article, footer, or .report-article) aligns within ±2 px of the nav
 *      content edge (.ap-nav .wrap left + padding-left) OR a centred
 *      --measure column.
 *   2. Type conformance: every visible h1,h2,h3,p,li,summary,label outside
 *      nav, footer, pre, code, svg, .mcp-term (plus known exceptions: inline
 *      code, hub terminal, homepage clock caption) has a computed font-size
 *      within ±0.6 px of one of the 14 --fs-* design-system tokens.
 *   3. Reflow (WCAG 1.4.10): document.documentElement.scrollWidth <= clientWidth.
 */

import { existsSync } from 'node:fs';
import puppeteer from 'puppeteer-core';

const PATHS = [
  '/',
  '/iso20022-mcp/',
  '/speaking/',
  '/trust/',
  '/case-studies/',
  '/research/',
  '/topics/',
  '/projects/',
  '/articles/',
  '/2026-10-28-why-the-fca-is-regulating-ai-without-an-ai-rulebook/',
  '/about/',
  '/contact/',
  '/privacy/',
  '/iso20022-mcp-docs/',
];

const WIDTHS = [375, 390, 768, 1280, 1440, 1920];

const TOKENS = [
  '--fs-micro',
  '--fs-meta',
  '--fs-small',
  '--fs-ui',
  '--fs-body',
  '--fs-prose',
  '--fs-lead',
  '--fs-h4',
  '--fs-h3',
  '--fs-h2-prose',
  '--fs-h2',
  '--fs-h1',
  '--fs-display',
  '--fs-stat',
];

const CHROME_ARGS = [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--blink-settings=preferredColorScheme=1',
  '--force-prefers-reduced-motion',
  '--hide-scrollbars',
  '--disable-lcd-text',
  '--font-render-hinting=none',
];

function findChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const candidates = [
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
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

async function auditPageAtWidths(browser, base, baseHost, path) {
  const failures = [];
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  await page.setBypassCSP(true);
  await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    let host = '';
    try {
      host = new URL(req.url()).host;
    } catch {
      /* data:/about: URLs - allow */
    }
    if (host === '' || host === baseHost) req.continue();
    else req.abort('blockedbyclient');
  });

  try {
    for (const width of WIDTHS) {
      await page.setViewport({ width, height: 900, deviceScaleFactor: 1 });
      await page.goto(`${base}${path}`, { waitUntil: 'networkidle0', timeout: 60000 });
      await page.evaluate(() => document.fonts.ready);
      const res = await page.evaluate((tokenNames) => {
        const errs = [];
        const docEl = document.documentElement;
        const cw = docEl.clientWidth;
        const sw = docEl.scrollWidth;
        if (sw > cw) {
          errs.push({
            kind: 'reflow',
            selector: 'documentElement',
            detail: `scrollWidth ${sw} > clientWidth ${cw}`,
          });
        }

        const remPx = parseFloat(getComputedStyle(docEl).fontSize) || 16;
        const rootCs = getComputedStyle(docEl);

        function evalTerm(term) {
          const s = term.trim();
          if (s.endsWith('rem')) return parseFloat(s) * remPx;
          if (s.endsWith('vw')) return (parseFloat(s) * cw) / 100;
          if (s.endsWith('px')) return parseFloat(s);
          return NaN;
        }

        function evalExpr(expr) {
          const s = expr.trim();
          // CSS math requires spaces around + and -; reject malformed e.g. "1.125rem+ 0.5vw"
          if (/[0-9a-z%][+-]|[+-][0-9a-z.]/i.test(s)) return NaN;
          const parts = s.split(/\s+\+\s+/);
          let sum = 0;
          for (const p of parts) {
            const v = evalTerm(p);
            if (!Number.isFinite(v)) return NaN;
            sum += v;
          }
          return sum;
        }

        function evalCssProp(name) {
          const raw = rootCs.getPropertyValue(name).trim();
          if (!raw) return NaN;
          if (raw.startsWith('clamp(') && raw.endsWith(')')) {
            const inner = raw.slice(6, -1);
            const segs = inner.split(',');
            if (segs.length !== 3) return NaN;
            const lo = evalExpr(segs[0]);
            const mid = evalExpr(segs[1]);
            const hi = evalExpr(segs[2]);
            if (!Number.isFinite(lo) || !Number.isFinite(mid) || !Number.isFinite(hi)) return NaN;
            return Math.min(hi, Math.max(lo, mid));
          }
          return evalExpr(raw);
        }

        const tokenPx = {};
        for (const t of tokenNames) {
          tokenPx[t] = evalCssProp(t);
        }
        const measureWidth = evalCssProp('--measure');
        const padX = evalCssProp('--pad-x');

        const tokenValues = Object.values(tokenPx).filter((v) => Number.isFinite(v) && v > 0);

        function isVisible(el) {
          if (el.closest('[hidden], template, .sr-only, .visually-hidden')) return false;
          const closedDetails = el.closest('details:not([open])');
          if (closedDetails) {
            const sum = closedDetails.querySelector(':scope > summary');
            if (!sum || !sum.contains(el)) return false;
          }
          let cur = el;
          while (cur && cur.nodeType === 1) {
            const cs = getComputedStyle(cur);
            if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) {
              return false;
            }
            if (cs.clip === 'rect(0px, 0px, 0px, 0px)' || cs.clipPath === 'inset(50%)') {
              return false;
            }
            cur = cur.parentElement;
          }
          const r = el.getBoundingClientRect();
          return r.width > 1 && r.height > 1;
        }

        function describeEl(el) {
          const tag = el.tagName.toLowerCase();
          const id = el.id ? `#${el.id}` : '';
          const cls =
            typeof el.className === 'string' && el.className.trim()
              ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.')
              : '';
          const parent = el.parentElement;
          const pCls =
            parent && typeof parent.className === 'string' && parent.className.trim()
              ? parent.tagName.toLowerCase() + '.' + parent.className.trim().split(/\s+/)[0] + ' > '
              : '';
          return `${pCls}${tag}${id}${cls}`;
        }

        // 2. Alignment check
        const navWrap = document.querySelector('.ap-nav .wrap');
        if (navWrap) {
          const navRect = navWrap.getBoundingClientRect();
          const navCs = getComputedStyle(navWrap);
          const navEdge = navRect.left + parseFloat(navCs.paddingLeft || '0');
          // A centred --measure column inside a padded or unpadded container:
          const measureEdgeUnpadded = Math.max(padX, (cw - measureWidth) / 2);
          const measureEdgePadded = Math.max(padX, (cw - Math.min(cw - 2 * padX, measureWidth)) / 2);

          for (const h of document.querySelectorAll('h1, h2')) {
            if (!isVisible(h)) continue;
            const cs = getComputedStyle(h);
            if (cs.textAlign === 'center' || cs.textAlign === '-webkit-center') continue;
            if (
              h.closest(
                'article, [class*=card], footer, .report-article, .offer-panel, .docs-flow, .spk-media, .spk-book-aside, .contact-aside, .author-card, .article-toc, .reuse, .cite-panel, .mcp-advisory, .tr-col, .story-grid, .narrative-section',
              )
            ) {
              continue;
            }
            const left = h.getBoundingClientRect().left;
            const dNav = Math.abs(left - navEdge);
            const dMeas1 = Math.abs(left - measureEdgeUnpadded);
            const dMeas2 = Math.abs(left - measureEdgePadded);
            if (Math.min(dNav, dMeas1, dMeas2) > 2.2) {
              errs.push({
                kind: 'alignment',
                selector: describeEl(h),
                detail: `left=${left.toFixed(1)}px vs nav=${navEdge.toFixed(1)}px / measure=${measureEdgeUnpadded.toFixed(1)}px`,
              });
            }
          }
        }

        // 3. Type conformance check
        // Known exceptions:
        //   - inline code, pre, code, svg
        //   - hub terminal (.mcp-term) and interactive web-component shadow/light controls
        //   - homepage clock caption (.feat-clock-caption, .hero-clock-caption, figcaption inside .feat-hero-stage)
        const TYPE_EXCLUDE =
          '.ap-nav, nav, footer, pre, code, svg, .mcp-term, iso20022-simulator, index-scorecard, .feat-hero-stage figcaption, .feat-clock-caption';
        for (const el of document.querySelectorAll('h1, h2, h3, p, li, summary, label')) {
          if (!isVisible(el)) continue;
          if (el.closest(TYPE_EXCLUDE)) continue;
          // Skip elements that contain only inline code when the code sets its own em size,
          // or check the element's own computed font-size (which is unaffected by child <code>).
          const fs = parseFloat(getComputedStyle(el).fontSize);
          let matched = false;
          for (const tv of tokenValues) {
            if (Math.abs(fs - tv) <= 0.6) {
              matched = true;
              break;
            }
          }
          if (!matched) {
            errs.push({
              kind: 'type-scale',
              selector: describeEl(el),
              detail: `font-size=${fs.toFixed(2)}px not in tokens [${tokenValues.map((v) => v.toFixed(1)).join(', ')}]`,
            });
          }
        }

        return errs;
      }, TOKENS);

      for (const e of res) {
        failures.push({ path, width, ...e });
      }
    }
  } finally {
    await context.close().catch(() => {});
  }
  return failures;
}

// Home page structure (plan C-3): at most 7 top-level sections (hero,
// <main>'s sections, closing), at most 2 buttons in the first viewport
// besides the header's, at most 6 distinct call-to-action labels, and an
// H1 of at most 10 words.
async function auditHome(browser, base) {
  const failures = [];
  const page = await browser.newPage();
  try {
    for (const [width, height] of [[1440, 900], [375, 812]]) {
      await page.setViewport({ width, height, deviceScaleFactor: 1 });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle0', timeout: 60000 });
      const r = await page.evaluate(() => {
        const sections = document.querySelectorAll(
          'body > section, body > aside.feat, main > .home-content > section, main > section',
        ).length;
        const buttons = [...document.querySelectorAll('.pill, .btn-primary, .btn-ghost')].filter((b) => {
          if (b.closest('.ap-nav')) return false;
          const box = b.getBoundingClientRect();
          return box.width > 0 && box.top < innerHeight && box.bottom > 0;
        }).length;
        const labels = new Set(
          [...document.querySelectorAll('main .pill, .feat-hero .pill, .closing-v3 .pill')].map((b) =>
            b.textContent.replace(/\s+/g, ' ').replace(/[›>]/g, '').trim(),
          ),
        );
        const h1 = (document.querySelector('h1')?.textContent || '').trim().split(/\s+/).length;
        return { sections, buttons, labels: [...labels], h1 };
      });
      if (r.sections > 7) failures.push(`@${width}: ${r.sections} sections (max 7)`);
      if (r.buttons > 2) failures.push(`@${width}: ${r.buttons} buttons in the first viewport (max 2)`);
      if (r.labels.length > 6) failures.push(`@${width}: ${r.labels.length} CTA labels (max 6): ${r.labels.join(' | ')}`);
      if (r.h1 > 10) failures.push(`@${width}: H1 has ${r.h1} words (max 10)`);
    }
  } finally {
    await page.close().catch(() => {});
  }
  return failures;
}

async function main() {
  const base = arg('base', 'http://127.0.0.1:8080').replace(/\/$/, '');
  const baseHost = new URL(base).host;
  const browser = await puppeteer.launch({
    executablePath: findChrome(),
    args: CHROME_ARGS,
  });

  const allFailures = [];
  try {
    for (const path of PATHS) {
      const f = await auditPageAtWidths(browser, base, baseHost, path);
      allFailures.push(...f);
      console.log(
        `${f.length === 0 ? 'ok  ' : 'FAIL'} ${path} (${f.length} issue${f.length === 1 ? '' : 's'})`,
      );
    }
    const home = await auditHome(browser, base);
    console.log(`${home.length === 0 ? 'ok  ' : 'FAIL'} home structure (${home.length} issue(s))`);
    for (const h of home) allFailures.push({ kind: 'home', path: '/', width: '-', selector: 'home', detail: h });
  } finally {
    await browser.close();
  }

  if (allFailures.length > 0) {
    console.error('\nDesign-system browser gate failures:');
    for (const f of allFailures) {
      console.error(`  [${f.kind}] ${f.path} @${f.width}px :: ${f.selector} -> ${f.detail}`);
    }
    process.exit(1);
  }
  console.log(`\nDesign-system gate passed: ${PATHS.length} pages x ${WIDTHS.length} widths.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
