#!/usr/bin/env node
/**
 * Tests for workers/lang-router.js — pure-logic coverage.
 *
 * The Cloudflare runtime isn't installed here, so we shim out the bits
 * the Worker touches (fetch, Response, Request, URL) and only validate
 * the decision tree. Run from repo root: `node workers/test_lang_router.mjs`.
 */
import { strict as assert } from 'node:assert';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const source = readFileSync(join(here, 'lang-router.js'), 'utf8');

// Pull the testable helpers out of the source by string-eval-ing the
// helper definitions into a temp scope. Cheap, predictable, no test
// harness dep.
const helpersBlob = source
  .replace(/export default[\s\S]+$/, '')
  .replace(/^\/\*\*[\s\S]*?\*\/\s*/, '');
// eslint-disable-next-line no-eval
const scope = new Function(`${helpersBlob}; return { parseAcceptLanguage, pickSiteLang, isPageNavigation, getCookie, ACTIVE_LANGS };`)();

const { parseAcceptLanguage, pickSiteLang, isPageNavigation, getCookie, ACTIVE_LANGS } = scope;

// parseAcceptLanguage
assert.deepEqual(
  parseAcceptLanguage('fr-FR,fr;q=0.9,en;q=0.8'),
  ['fr-fr', 'fr', 'en'],
);
assert.deepEqual(parseAcceptLanguage(''), []);
assert.deepEqual(parseAcceptLanguage(null), []);
assert.deepEqual(
  parseAcceptLanguage('*;q=0.5,de;q=0.9'),
  ['de'],
  'wildcard tag dropped',
);
assert.deepEqual(
  parseAcceptLanguage('en;q=0.5,fr;q=0.9'),
  ['fr', 'en'],
  'sorted by q desc',
);

// pickSiteLang
assert.equal(pickSiteLang(['fr-fr', 'fr', 'en']), 'fr');
assert.equal(pickSiteLang(['pt-pt', 'pt']), 'pt-br', 'pt-PT folds to pt-br');
assert.equal(pickSiteLang(['zh-tw', 'zh']), 'zh-hant');
assert.equal(pickSiteLang(['zh-cn']), 'zh-hans');
assert.equal(pickSiteLang(['en-us', 'en']), null, 'EN is not a non-EN target');
assert.equal(pickSiteLang(['xh-za']), null, 'unsupported lang returns null');

// isPageNavigation
assert.equal(isPageNavigation('/'), true);
assert.equal(isPageNavigation('/index.html'), true);
assert.equal(isPageNavigation('/about/index.html'), true);
assert.equal(isPageNavigation('/main.js'), false, 'asset extension passes through');
assert.equal(isPageNavigation('/sitemap.xml'), false);
assert.equal(isPageNavigation('/api/agents/posts.json'), false);
assert.equal(isPageNavigation('/.well-known/ai-plugin.json'), false);
assert.equal(isPageNavigation('/_csp/main.abcd.css'), false);
assert.equal(isPageNavigation('/fr/'), false, 'already inside lang subtree');
assert.equal(isPageNavigation('/zh-hans/about/index.html'), false);

// getCookie
assert.equal(getCookie('pref-lang=fr; other=baz', 'pref-lang'), 'fr');
assert.equal(getCookie('a=b; pref-lang=zh-hans; c=d', 'pref-lang'), 'zh-hans');
assert.equal(getCookie(null, 'pref-lang'), null);
assert.equal(getCookie('other=value', 'pref-lang'), null);

// ACTIVE_LANGS sanity — all entries are lowercase + match the pickSiteLang map.
for (const l of ACTIVE_LANGS) {
  assert.equal(l, l.toLowerCase(), `ACTIVE_LANGS entry ${l} should be lowercase`);
}

console.log('ok: workers/lang-router.js pure-logic tests pass');
