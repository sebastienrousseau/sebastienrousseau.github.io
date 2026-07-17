// ISO 20022 MCP simulator core - pure, DOM-free ES module.
//
// This module is the single source of truth for how the simulator turns a
// baked scenario (a real captured MCP transcript, see
// iso20022-simulator-data.js) into what the reader sees. It is imported
// unchanged by both:
//   1. the browser Web Component (iso20022-simulator.js), and
//   2. the Node unit test (tests/unit/mcp-simulator/simulator-core.test.mjs),
// which the build gates at 100% line/branch/function coverage - the same
// contract as the index-scorecard scoring core (see build.sh and
// project-docs/adr/0011-index-scorecard-architecture.md for the precedent).
//
// Design invariants:
//   - Everything is derived from the baked data; nothing here fabricates a
//     tool call, an XML element or an error message.
//   - Segmentation is total: for any text and any mark list (including marks
//     that do not occur, overlap, or repeat) the output segments concatenate
//     back to the exact input text. The component renders segments verbatim,
//     so a rendering bug can never alter the captured bytes.
//   - No DOM, no network, no globals: pure functions over plain data.

/**
 * The scenario carrying `id`, or null when absent.
 * @param {{scenarios: Array<object>}} data
 * @param {string} id
 * @returns {object|null}
 */
export function scenarioById(data, id) {
  const list = Array.isArray(data && data.scenarios) ? data.scenarios : [];
  for (const s of list) {
    if (s.id === id) return s;
  }
  return null;
}

/**
 * The scenario shown before the reader picks one: the first in baked order.
 * @param {{scenarios: Array<object>}} data
 * @returns {object|null}
 */
export function defaultScenario(data) {
  const list = Array.isArray(data && data.scenarios) ? data.scenarios : [];
  return list.length > 0 ? list[0] : null;
}

/**
 * The exact MCP tool-call arguments as display JSON (2-space indent). This is
 * a re-serialisation of the captured `arguments` object, key order preserved
 * from capture.
 * @param {{args: object}} scenario
 * @returns {string}
 */
export function toolCallJson(scenario) {
  return JSON.stringify(scenario.args, null, 2);
}

/**
 * One line summarising the JSON-RPC frame around the tool call, e.g.
 * "tools/call - generate - iso20022 0.0.4 (stdio)".
 * @param {{tool: string, server: {name: string, version: string}}} scenario
 * @returns {string}
 */
export function toolCallSummary(scenario) {
  const srv = scenario.server || {};
  const name = srv.name || "unknown-server";
  const version = srv.version ? ` ${srv.version}` : "";
  return `tools/call - ${scenario.tool} - ${name}${version} (stdio)`;
}

/**
 * Whether the scenario's captured result is a validated XML document
 * ("xml") or the server's all-at-once validation error ("error").
 * @param {{result: {kind: string}}} scenario
 * @returns {"xml"|"error"}
 */
export function resultKind(scenario) {
  return scenario.result.kind === "error" ? "error" : "xml";
}

/**
 * Non-overlapping highlight spans for `marks` inside `text`.
 *
 * Each mark string claims its first occurrence not already claimed by an
 * earlier span; marks that do not occur (or only occur inside an existing
 * span) are skipped. Spans come back sorted by start offset, each carrying
 * the id of the mapping that owns it.
 *
 * @param {string} text
 * @param {Array<{mappingId: string, mark: string}>} marks
 * @returns {Array<{start: number, end: number, mappingId: string}>}
 */
export function findSpans(text, marks) {
  const spans = [];
  const overlaps = (start, end) =>
    spans.some((s) => start < s.end && end > s.start);
  for (const { mappingId, mark } of marks) {
    if (!mark) continue;
    let from = 0;
    for (;;) {
      const at = text.indexOf(mark, from);
      if (at === -1) break;
      const end = at + mark.length;
      if (!overlaps(at, end)) {
        spans.push({ start: at, end, mappingId });
        break;
      }
      from = at + 1;
    }
  }
  spans.sort((a, b) => a.start - b.start);
  return spans;
}

/**
 * Split `text` into ordered segments around highlight spans. Plain segments
 * carry `mappingId: null`; highlighted segments carry the owning mapping id.
 * Concatenating every segment's `text` reproduces the input exactly.
 * @param {string} text
 * @param {Array<{start: number, end: number, mappingId: string}>} spans
 * @returns {Array<{text: string, mappingId: string|null}>}
 */
export function segmentText(text, spans) {
  const segments = [];
  let cursor = 0;
  for (const span of spans) {
    if (span.start > cursor) {
      segments.push({ text: text.slice(cursor, span.start), mappingId: null });
    }
    segments.push({
      text: text.slice(span.start, span.end),
      mappingId: span.mappingId,
    });
    cursor = span.end;
  }
  if (cursor < text.length) {
    segments.push({ text: text.slice(cursor), mappingId: null });
  }
  return segments;
}

/**
 * The scenario sentence segmented by its mapping phrases (one span per
 * mapping, first occurrence).
 * @param {{sentence: string, mappings: Array<object>}} scenario
 * @returns {Array<{text: string, mappingId: string|null}>}
 */
export function sentenceSegments(scenario) {
  const marks = (scenario.mappings || []).map((m) => ({
    mappingId: m.id,
    mark: m.phrase,
  }));
  return segmentText(scenario.sentence, findSpans(scenario.sentence, marks));
}

/**
 * The captured result text segmented by every mapping's XML/error marks.
 * @param {{result: {text: string}, mappings: Array<object>}} scenario
 * @returns {Array<{text: string, mappingId: string|null}>}
 */
export function resultSegments(scenario) {
  const marks = [];
  for (const m of scenario.mappings || []) {
    for (const mark of m.marks || []) {
      marks.push({ mappingId: m.id, mark });
    }
  }
  const text = scenario.result.text;
  return segmentText(text, findSpans(text, marks));
}

/**
 * The mapping carrying `id`, or null - used to resolve a highlight's
 * explanatory label on hover/focus.
 * @param {{mappings: Array<object>}} scenario
 * @param {string} id
 * @returns {object|null}
 */
export function mappingById(scenario, id) {
  for (const m of scenario.mappings || []) {
    if (m.id === id) return m;
  }
  return null;
}

const MONTHS = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

/**
 * "2026-07-16" -> "16 July 2026". Anything that is not an ISO date comes
 * back unchanged rather than mis-parsed.
 * @param {string} iso
 * @returns {string}
 */
export function formatCaptureDate(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
  if (!m) return iso || "";
  const month = MONTHS[Number(m[2]) - 1];
  if (!month) return iso;
  return `${Number(m[3])} ${month} ${m[1]}`;
}

/**
 * The provenance line rendered under the simulator: capture date, servers
 * and the no-network guarantee.
 * @param {{capture: {date: string, servers: Array<{name:string,version:string}>}}} data
 * @returns {string}
 */
export function captureNote(data) {
  const capture = (data && data.capture) || {};
  const servers = Array.isArray(capture.servers) ? capture.servers : [];
  const from = servers.map((s) => `${s.name} ${s.version}`).join(" and ");
  const date = formatCaptureDate(capture.date);
  return (
    `Real transcripts, captured ${date} over MCP stdio` +
    (from ? ` from ${from}` : "") +
    ". This demo makes no network calls; every byte shown was returned by " +
    "a live server then and baked into this page at build time."
  );
}

/**
 * Validate one baked scenario's shape and cross-references. Returns a list
 * of human-readable problems (empty = sound). The unit test runs this over
 * the entire data module, so a bad bake fails the build, not the reader.
 * @param {object} scenario
 * @returns {Array<string>}
 */
export function scenarioProblems(scenario) {
  const problems = [];
  if (!scenario || typeof scenario !== "object") {
    return ["scenario is not an object"];
  }
  for (const key of ["id", "label", "sentence", "note", "tool"]) {
    if (typeof scenario[key] !== "string" || scenario[key] === "") {
      problems.push(`missing or empty ${key}`);
    }
  }
  if (!scenario.server || typeof scenario.server.command !== "string") {
    problems.push("missing server.command");
  }
  if (!scenario.args || typeof scenario.args !== "object") {
    problems.push("missing args");
  }
  const result = scenario.result;
  if (!result || (result.kind !== "xml" && result.kind !== "error")) {
    problems.push("result.kind must be xml or error");
  }
  if (!result || typeof result.text !== "string" || result.text === "") {
    problems.push("missing result.text");
  }
  if (result && result.kind === "xml" && !/^<\?xml /.test(result.text)) {
    problems.push("xml result does not open with an XML declaration");
  }
  const mappings = Array.isArray(scenario.mappings) ? scenario.mappings : [];
  if (mappings.length === 0) {
    problems.push("scenario has no mappings");
  }
  const seen = new Set();
  for (const m of mappings) {
    if (seen.has(m.id)) problems.push(`duplicate mapping id ${m.id}`);
    seen.add(m.id);
    if (typeof scenario.sentence === "string" && !scenario.sentence.includes(m.phrase)) {
      problems.push(`phrase not in sentence: ${m.phrase}`);
    }
    const marks = Array.isArray(m.marks) ? m.marks : [];
    if (marks.length === 0) problems.push(`mapping ${m.id} has no marks`);
    for (const mark of marks) {
      if (result && typeof result.text === "string" && !result.text.includes(mark)) {
        problems.push(`mark not in result: ${mark}`);
      }
    }
  }
  return problems;
}

/**
 * Validate the whole baked data module (capture metadata + every scenario).
 * @param {object} data
 * @returns {Array<string>}
 */
export function dataProblems(data) {
  const problems = [];
  if (!data || typeof data !== "object") return ["data is not an object"];
  const capture = data.capture;
  if (!capture || !/^\d{4}-\d{2}-\d{2}$/.test(capture.date || "")) {
    problems.push("capture.date missing or not ISO formatted");
  }
  if (!capture || !Array.isArray(capture.servers) || capture.servers.length === 0) {
    problems.push("capture.servers missing");
  }
  const scenarios = Array.isArray(data.scenarios) ? data.scenarios : [];
  if (scenarios.length < 4 || scenarios.length > 6) {
    problems.push("expected 4 to 6 scenarios");
  }
  const ids = new Set();
  for (const s of scenarios) {
    if (ids.has(s.id)) problems.push(`duplicate scenario id ${s.id}`);
    ids.add(s.id);
    for (const p of scenarioProblems(s)) problems.push(`${s.id}: ${p}`);
  }
  return problems;
}
