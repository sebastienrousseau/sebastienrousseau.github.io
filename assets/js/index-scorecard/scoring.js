// Index-scorecard scoring core — pure, DOM-free ES module.
//
// This module is the single source of truth for how a reader's per-dimension
// self-assessment collapses into a composite maturity score. It is imported
// unchanged by both:
//   1. the browser Web Component (index-scorecard.js), and
//   2. the Node golden-file test (tests/unit/index-scorecard/scoring.test.mjs).
//
// Because the golden test pins the exact outputs of these functions, the
// number a reader sees in the article and the number the test asserts are
// computed by the same code — there is no second re-implementation to drift.
//
// Design invariants (see docs/adr/0001-index-scorecard-architecture.md):
//   - Composite is a weight-normalised average, NOT a raw weighted sum, so a
//     spec whose weights do not total exactly 1.0 still yields a score on the
//     declared scale.
//   - Every score is clamped to [scale.min, scale.max] before it contributes.
//   - Rounding is deterministic: half-up to `scale.round` decimal places.
//
// The module is data-driven: it makes no assumption about the number of
// dimensions, the scale (0–100 for the Agentic index, 0–5 CMM for a future
// index), or the band thresholds. Everything comes from the per-index JSON
// spec in _data/indices/<slug>.json.

/**
 * Clamp a raw numeric input to the spec's declared scale.
 * Non-finite input collapses to the scale minimum (an empty control reads 0).
 * @param {{scale:{min:number,max:number}}} spec
 * @param {number} value
 * @returns {number}
 */
export function clampScore(spec, value) {
  const { min, max } = spec.scale;
  const n = Number(value);
  if (!Number.isFinite(n)) return min;
  if (n < min) return min;
  if (n > max) return max;
  return n;
}

/**
 * Round half-up to `places` decimals, deterministically (independent of the
 * platform's floating-point Math.round tie behaviour on .5 for negatives).
 * @param {number} value
 * @param {number} places
 * @returns {number}
 */
export function roundTo(value, places) {
  const factor = 10 ** places;
  return Math.round((value + Number.EPSILON) * factor) / factor;
}

/**
 * Compute the composite index score from an array of per-dimension scores
 * aligned positionally to spec.dimensions.
 * @param {object} spec  the parsed index JSON spec
 * @param {Array<number>} scores  one raw score per dimension, spec order
 * @returns {number} composite on the spec's scale, rounded to spec.scale.round
 */
export function compositeScore(spec, scores) {
  const places = Number.isInteger(spec.scale.round) ? spec.scale.round : 0;
  let weighted = 0;
  let weightSum = 0;
  spec.dimensions.forEach((dim, i) => {
    const weight = Number(dim.weight) || 0;
    weighted += clampScore(spec, scores[i]) * weight;
    weightSum += weight;
  });
  const composite = weightSum > 0 ? weighted / weightSum : 0;
  return roundTo(composite, places);
}

/**
 * Resolve the maturity band a composite score falls into. Bands are inclusive
 * of their `min` and `max`. Returns the first matching band, or null.
 * @param {object} spec
 * @param {number} composite
 * @returns {object|null}
 */
export function bandFor(spec, composite) {
  const bands = Array.isArray(spec.bands) ? spec.bands : [];
  for (const band of bands) {
    const lo = Number.isFinite(band.min) ? band.min : -Infinity;
    const hi = Number.isFinite(band.max) ? band.max : Infinity;
    if (composite >= lo && composite <= hi) return band;
  }
  return null;
}

/**
 * Resolve which of a dimension's declared levels a raw score sits in, using
 * each level's [min,max] band (inclusive). Used to show the live maturity
 * label ("Level 3 — Operational") as the reader moves a control.
 * @param {object} dimension  a single spec.dimensions[] entry
 * @param {number} value
 * @returns {object|null}
 */
export function levelFor(dimension, value) {
  const levels = Array.isArray(dimension.levels) ? dimension.levels : [];
  for (const level of levels) {
    const lo = Number.isFinite(level.min) ? level.min : -Infinity;
    const hi = Number.isFinite(level.max) ? level.max : Infinity;
    if (value >= lo && value <= hi) return level;
  }
  return null;
}

/**
 * Default starting score for a dimension: the spec-declared default if finite,
 * else the scale minimum.
 * @param {object} spec
 * @param {object} dimension
 * @returns {number}
 */
export function defaultScore(spec, dimension) {
  return Number.isFinite(dimension.default)
    ? clampScore(spec, dimension.default)
    : spec.scale.min;
}

/**
 * The array of default scores for a whole spec, one per dimension in order.
 * @param {object} spec
 * @returns {Array<number>}
 */
export function defaultScores(spec) {
  return spec.dimensions.map((dim) => defaultScore(spec, dim));
}

// --- URL-state codec ---------------------------------------------------------
//
// State is round-tripped through the URL query string (?s=<token>) with NO
// backend, so a scored result is shareable and bookmarkable. The token is a
// base64url encoding of a tiny, versioned, delimited string:
//
//     "1:0,25,50,75,100,40"   ->  base64url  ->  "MTowLDI1LDUwLDc1LDEwMCw0MA"
//
// Rationale for the format (see ADR 0001): a delimited integer list is an
// order of magnitude shorter than base64(JSON) for six small integers, has no
// structural ambiguity to parse, and the leading version field lets the
// decoder reject tokens written by an incompatible future schema instead of
// silently mis-reading them. base64url (RFC 4648 §5, `+/=` -> `-_` stripped)
// keeps the token URL-safe with no percent-encoding.

const STATE_VERSION = "1";

/** base64url-encode an ASCII string (no padding). */
export function b64urlEncode(ascii) {
  return btoa(ascii).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

/** base64url-decode to an ASCII string. Returns null on malformed input. */
export function b64urlDecode(token) {
  try {
    const b64 = token.replace(/-/g, "+").replace(/_/g, "/");
    return atob(b64);
  } catch {
    return null;
  }
}

/**
 * Encode a full scores array to a shareable URL token.
 * @param {object} spec
 * @param {Array<number>} scores
 * @returns {string}
 */
export function encodeState(spec, scores) {
  const ints = spec.dimensions.map((dim, i) =>
    Math.round(clampScore(spec, scores[i])),
  );
  return b64urlEncode(`${STATE_VERSION}:${ints.join(",")}`);
}

/**
 * Decode a URL token back to a validated scores array. Returns null if the
 * token is malformed, carries an unknown version, or does not carry exactly
 * one score per dimension — the caller then falls back to spec defaults.
 * @param {object} spec
 * @param {string} token
 * @returns {Array<number>|null}
 */
export function decodeState(spec, token) {
  if (!token) return null;
  const raw = b64urlDecode(token);
  if (raw === null) return null;
  const sep = raw.indexOf(":");
  if (sep === -1) return null;
  if (raw.slice(0, sep) !== STATE_VERSION) return null;
  const parts = raw.slice(sep + 1).split(",");
  if (parts.length !== spec.dimensions.length) return null;
  const scores = [];
  for (const part of parts) {
    const n = Number(part);
    if (!Number.isFinite(n)) return null;
    scores.push(clampScore(spec, n));
  }
  return scores;
}
