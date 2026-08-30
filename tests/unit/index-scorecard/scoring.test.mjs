// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

// Golden-file + edge-case unit test for the index-scorecard scoring core.
//
// Two jobs:
//   1. GOLDEN — assert that the pinned input->output cases in
//      scoring.golden.json still hold against the real Agentic AI Index spec.
//      A diff here is a reader-visible behaviour change and must be reviewed.
//   2. COVERAGE — exercise every branch of scoring.js (the build gates this
//      file at 100% branch coverage on that module) with the URL-state codec
//      round-trip and the malformed-input rejection paths.
//
// Run: node --test tests/unit/index-scorecard/scoring.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

import {
  clampScore,
  roundTo,
  compositeScore,
  bandFor,
  levelFor,
  defaultScore,
  defaultScores,
  b64urlEncode,
  b64urlDecode,
  encodeState,
  decodeState,
} from "../../../assets/js/index-scorecard/scoring.js";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "../../..");
const spec = JSON.parse(
  readFileSync(resolve(ROOT, "_data/indices/agentic-ai-index-banks-2026.json"), "utf8"),
);
const golden = JSON.parse(readFileSync(resolve(HERE, "scoring.golden.json"), "utf8"));

test("golden: composite + band match the pinned fixture", () => {
  assert.equal(golden.spec, spec.slug, "golden spec slug drifted from the data file");
  for (const [name, expected] of Object.entries(golden.cases)) {
    const composite = compositeScore(spec, expected.scores);
    assert.equal(composite, expected.composite, `composite mismatch for "${name}"`);
    const band = bandFor(spec, composite);
    assert.equal(band ? band.id : null, expected.band, `band mismatch for "${name}"`);
  }
});

test("golden: anchor cases are arithmetically hand-verifiable", () => {
  // Independent of the fixture: the weighted average of the descending vector.
  // 80*.25 + 70*.20 + 60*.15 + 50*.15 + 40*.10 + 30*.15 = 59
  assert.equal(compositeScore(spec, [80, 70, 60, 50, 40, 30]), 59);
  assert.equal(compositeScore(spec, [0, 0, 0, 0, 0, 0]), 0);
  assert.equal(compositeScore(spec, [100, 100, 100, 100, 100, 100]), 100);
});

test("clampScore covers non-finite / below / above / in-range", () => {
  assert.equal(clampScore(spec, Number.NaN), 0);
  assert.equal(clampScore(spec, undefined), 0);
  assert.equal(clampScore(spec, -5), 0);
  assert.equal(clampScore(spec, 250), 100);
  assert.equal(clampScore(spec, 42), 42);
});

test("roundTo is deterministic half-up", () => {
  assert.equal(roundTo(49.45, 0), 49);
  assert.equal(roundTo(2.675, 2), 2.68);
});

test("compositeScore handles non-integer round + zero total weight", () => {
  // round absent -> defaults to 0 decimal places.
  const noRound = { scale: { min: 0, max: 10 }, dimensions: [{ weight: 1 }] };
  assert.equal(compositeScore(noRound, [7.6]), 8);
  // all weights zero / non-numeric -> weightSum 0 -> composite 0.
  const zeroW = {
    scale: { min: 0, max: 100, round: 0 },
    dimensions: [{ weight: 0 }, { weight: "x" }],
  };
  assert.equal(compositeScore(zeroW, [80, 90]), 0);
});

test("bandFor: open-ended bounds, match, and no-match", () => {
  const s = {
    bands: [
      { id: "low", max: 49 }, // no min -> -Infinity
      { id: "high", min: 50 }, // no max -> +Infinity
    ],
  };
  assert.equal(bandFor(s, 10).id, "low");
  assert.equal(bandFor(s, 90).id, "high");
  assert.equal(bandFor({ bands: [{ id: "x", min: 10, max: 20 }] }, 5), null);
  assert.equal(bandFor({}, 42), null); // bands not an array
});

test("levelFor: open-ended bounds, match, and empty levels", () => {
  const dim = {
    levels: [
      { label: "lo", max: 24 },
      { label: "hi", min: 75 },
    ],
  };
  assert.equal(levelFor(dim, 10).label, "lo");
  assert.equal(levelFor(dim, 90).label, "hi");
  assert.equal(levelFor(dim, 50), null); // gap
  assert.equal(levelFor({}, 3), null); // levels not an array
});

test("defaultScore / defaultScores respect declared defaults", () => {
  assert.equal(defaultScore(spec, { default: 40 }), 40);
  assert.equal(defaultScore(spec, {}), 0); // no default -> scale.min
  assert.equal(defaultScore(spec, { default: 500 }), 100); // clamped
  assert.deepEqual(defaultScores(spec), [0, 0, 0, 0, 0, 0]);
});

test("base64url codec round-trips and rejects garbage", () => {
  const token = b64urlEncode("1:0,25,50,75,100,40");
  assert.match(token, /^[A-Za-z0-9\-_]+$/); // url-safe, no padding
  assert.equal(b64urlDecode(token), "1:0,25,50,75,100,40");
  assert.equal(b64urlDecode("@@@not-base64@@@"), null);
});

test("encodeState/decodeState round-trip through the URL token", () => {
  const scores = [80, 70, 60, 50, 40, 30];
  const token = encodeState(spec, scores);
  assert.deepEqual(decodeState(spec, token), scores);
  // encode clamps + rounds before writing the token.
  const clampedToken = encodeState(spec, [150, -1, 62.4, 62.6, 62, 62]);
  assert.deepEqual(decodeState(spec, clampedToken), [100, 0, 62, 63, 62, 62]);
});

test("decodeState rejects every malformed form", () => {
  assert.equal(decodeState(spec, ""), null); // empty token
  assert.equal(decodeState(spec, null), null); // nullish token
  assert.equal(decodeState(spec, "@@@"), null); // undecodable base64
  assert.equal(decodeState(spec, b64urlEncode("no-colon-here")), null); // no separator
  assert.equal(decodeState(spec, b64urlEncode("9:0,0,0,0,0,0")), null); // wrong version
  assert.equal(decodeState(spec, b64urlEncode("1:0,0,0")), null); // wrong length
  assert.equal(decodeState(spec, b64urlEncode("1:a,b,c,d,e,f")), null); // non-numeric
});
