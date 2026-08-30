// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

// Golden-file + edge-case unit test for the ISO 20022 MCP simulator core
// (mirrors tests/unit/index-scorecard/scoring.test.mjs).
//
// Three jobs:
//   1. GOLDEN - pin the reader-visible segmentation of the real baked
//      capture data (iso20022-simulator-data.js). A diff here means either
//      the captured transcripts or the mapping editorial changed, and must
//      be reviewed.
//   2. DATA SOUNDNESS - run dataProblems() over the whole baked module so a
//      bad re-bake (phrase not in sentence, mark not in the captured XML,
//      wrong scenario count) fails the build, not the reader.
//   3. COVERAGE - exercise every branch of iso20022-simulator-core.js (the
//      build gates this file at 100% line/branch/function coverage on that
//      module and on the data module).
//
// Run: node --test tests/unit/mcp-simulator/simulator-core.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

import {
  scenarioById,
  defaultScenario,
  toolCallJson,
  toolCallSummary,
  resultKind,
  findSpans,
  segmentText,
  sentenceSegments,
  resultSegments,
  mappingById,
  formatCaptureDate,
  captureNote,
  scenarioProblems,
  dataProblems,
} from "../../../assets/js/mcp-simulator/iso20022-simulator-core.js";
import SIMULATOR_DATA_DEFAULT, {
  SIMULATOR_DATA,
} from "../../../assets/js/mcp-simulator/iso20022-simulator-data.js";

const HERE = dirname(fileURLToPath(import.meta.url));
const golden = JSON.parse(
  readFileSync(resolve(HERE, "simulator-core.golden.json"), "utf8"),
);

// --- golden: the baked capture is what we shipped -----------------------------

test("golden: capture date, scenario ids, tools and result kinds", () => {
  assert.equal(SIMULATOR_DATA.capture.date, golden.capture_date);
  assert.deepEqual(
    SIMULATOR_DATA.scenarios.map((s) => ({
      id: s.id,
      tool: s.tool,
      kind: s.result.kind,
      messageType: s.result.messageType ?? null,
    })),
    golden.scenarios,
  );
});

test("golden: pay-supplier sentence segmentation is pinned", () => {
  const s = scenarioById(SIMULATOR_DATA, "pay-supplier");
  assert.deepEqual(sentenceSegments(s), golden.pay_supplier_sentence_segments);
});

test("golden: pay-supplier XML highlights are pinned and real", () => {
  const s = scenarioById(SIMULATOR_DATA, "pay-supplier");
  const marked = resultSegments(s).filter((seg) => seg.mappingId !== null);
  assert.deepEqual(marked, golden.pay_supplier_marked_xml);
  // The highlights point at bytes the live gateway actually returned.
  for (const seg of marked) assert.ok(s.result.text.includes(seg.text));
});

test("golden: the validation-error scenario carries the all-at-once message", () => {
  const s = scenarioById(SIMULATOR_DATA, "missing-details");
  assert.equal(resultKind(s), "error");
  assert.ok(s.result.text.includes(golden.missing_details_error_contains));
  assert.ok(s.result.text.includes("Provide them in one call"));
});

// --- data soundness over the whole baked module -------------------------------

test("baked data module is sound (dataProblems returns nothing)", () => {
  assert.deepEqual(dataProblems(SIMULATOR_DATA), []);
  assert.equal(SIMULATOR_DATA_DEFAULT, SIMULATOR_DATA); // default export alias
});

test("segmentation is total: segments always rebuild the exact input", () => {
  for (const s of SIMULATOR_DATA.scenarios) {
    const sentence = sentenceSegments(s).map((seg) => seg.text).join("");
    assert.equal(sentence, s.sentence, s.id);
    const result = resultSegments(s).map((seg) => seg.text).join("");
    assert.equal(result, s.result.text, s.id);
  }
});

test("every scenario renders a captured tool call verbatim", () => {
  for (const s of SIMULATOR_DATA.scenarios) {
    const json = toolCallJson(s);
    assert.deepEqual(JSON.parse(json), s.args, s.id);
    const summary = toolCallSummary(s);
    assert.ok(summary.startsWith(`tools/call - ${s.tool} - `), s.id);
    assert.ok(summary.endsWith("(stdio)"), s.id);
  }
});

// --- scenario lookup -----------------------------------------------------------

test("scenarioById: found / not found / malformed data", () => {
  assert.equal(scenarioById(SIMULATOR_DATA, "pay-supplier").id, "pay-supplier");
  assert.equal(scenarioById(SIMULATOR_DATA, "nope"), null);
  assert.equal(scenarioById(null, "x"), null);
  assert.equal(scenarioById({ scenarios: "not-a-list" }, "x"), null);
});

test("defaultScenario: first scenario, or null when empty/malformed", () => {
  assert.equal(defaultScenario(SIMULATOR_DATA).id, "pay-supplier");
  assert.equal(defaultScenario({ scenarios: [] }), null);
  assert.equal(defaultScenario(undefined), null);
  assert.equal(defaultScenario({ scenarios: "not-a-list" }), null);
});

test("toolCallSummary tolerates missing server metadata", () => {
  assert.equal(
    toolCallSummary({ tool: "generate" }),
    "tools/call - generate - unknown-server (stdio)",
  );
  assert.equal(
    toolCallSummary({ tool: "generate", server: { name: "iso20022" } }),
    "tools/call - generate - iso20022 (stdio)",
  );
});

test("resultKind defaults to xml for any non-error kind", () => {
  assert.equal(resultKind({ result: { kind: "xml" } }), "xml");
  assert.equal(resultKind({ result: { kind: "weird" } }), "xml");
  assert.equal(resultKind({ result: { kind: "error" } }), "error");
});

// --- findSpans / segmentText edge cases ----------------------------------------

test("findSpans: absent, falsy and overlapping marks", () => {
  const text = "aaa bbb aaa";
  // absent mark -> skipped; falsy mark -> skipped.
  assert.deepEqual(findSpans(text, [{ mappingId: "x", mark: "zzz" }]), []);
  assert.deepEqual(findSpans(text, [{ mappingId: "x", mark: "" }]), []);
  // second mark's first occurrence is claimed; it takes the next one.
  const spans = findSpans(text, [
    { mappingId: "one", mark: "aaa" },
    { mappingId: "two", mark: "aaa" },
  ]);
  assert.deepEqual(spans, [
    { start: 0, end: 3, mappingId: "one" },
    { start: 8, end: 11, mappingId: "two" },
  ]);
  // fully-claimed mark (no free occurrence left) is dropped.
  const claimed = findSpans("abc", [
    { mappingId: "big", mark: "abc" },
    { mappingId: "sub", mark: "b" },
  ]);
  assert.deepEqual(claimed, [{ start: 0, end: 3, mappingId: "big" }]);
  // later-listed mark occurring BEFORE an existing span (ends before it starts).
  assert.deepEqual(
    findSpans("aaa bbb", [
      { mappingId: "b", mark: "bbb" },
      { mappingId: "a", mark: "aaa" },
    ]),
    [
      { start: 0, end: 3, mappingId: "a" },
      { start: 4, end: 7, mappingId: "b" },
    ],
  );
});

test("segmentText: leading/adjacent/trailing segments", () => {
  const text = "xxAByyCDzz";
  const spans = [
    { start: 2, end: 4, mappingId: "ab" },
    { start: 6, end: 8, mappingId: "cd" },
  ];
  assert.deepEqual(segmentText(text, spans), [
    { text: "xx", mappingId: null },
    { text: "AB", mappingId: "ab" },
    { text: "yy", mappingId: null },
    { text: "CD", mappingId: "cd" },
    { text: "zz", mappingId: null },
  ]);
  // Adjacent span at position 0 and span ending at the end: no empty segments.
  assert.deepEqual(
    segmentText("ABCD", [
      { start: 0, end: 2, mappingId: "ab" },
      { start: 2, end: 4, mappingId: "cd" },
    ]),
    [
      { text: "AB", mappingId: "ab" },
      { text: "CD", mappingId: "cd" },
    ],
  );
  assert.deepEqual(segmentText("plain", []), [
    { text: "plain", mappingId: null },
  ]);
});

test("sentenceSegments / resultSegments tolerate missing mappings and marks", () => {
  const bare = {
    sentence: "just words",
    result: { kind: "xml", text: "<a/>" },
  };
  assert.deepEqual(sentenceSegments(bare), [
    { text: "just words", mappingId: null },
  ]);
  assert.deepEqual(resultSegments(bare), [{ text: "<a/>", mappingId: null }]);
  const noMarks = {
    sentence: "just words",
    result: { kind: "xml", text: "<a/>" },
    mappings: [{ id: "m", phrase: "words" }],
  };
  assert.equal(resultSegments(noMarks).length, 1); // marks list absent -> none
});

test("mappingById: found / not found / absent list", () => {
  const s = scenarioById(SIMULATOR_DATA, "cancel-duplicate");
  assert.equal(mappingById(s, "reason").label.includes("DUPL"), true);
  assert.equal(mappingById(s, "nope"), null);
  assert.equal(mappingById({}, "x"), null);
});

// --- provenance strings ---------------------------------------------------------

test("formatCaptureDate: ISO date in, prose date out; garbage unchanged", () => {
  assert.equal(formatCaptureDate("2026-07-16"), "16 July 2026");
  assert.equal(formatCaptureDate("2026-01-05"), "5 January 2026");
  assert.equal(formatCaptureDate("yesterday"), "yesterday");
  assert.equal(formatCaptureDate(""), "");
  assert.equal(formatCaptureDate(undefined), "");
  assert.equal(formatCaptureDate("2026-13-01"), "2026-13-01"); // no 13th month
});

test("captureNote names the capture date and both live servers", () => {
  const note = captureNote(SIMULATOR_DATA);
  assert.ok(note.includes("16 July 2026"));
  assert.ok(note.includes("iso20022 0.0.4"));
  assert.ok(note.includes("camt-exceptions 0.0.14"));
  assert.ok(note.includes("no network calls"));
  // Degrades cleanly with no server metadata at all.
  const bare = captureNote({ capture: { date: "2026-07-16" } });
  assert.ok(bare.includes("16 July 2026"));
  assert.ok(!bare.includes(" from "));
  assert.ok(captureNote(null).includes("no network calls"));
});

// --- validators: every rejection path -------------------------------------------

function validScenario() {
  return {
    id: "s1",
    label: "L",
    sentence: "pay Acme now",
    note: "n",
    tool: "generate",
    server: { name: "x", version: "1", command: "cmd" },
    args: { a: 1 },
    result: { kind: "xml", text: '<?xml version="1.0"?><a>Acme</a>' },
    mappings: [{ id: "m1", phrase: "Acme", marks: ["<a>Acme</a>"] }],
  };
}

test("scenarioProblems: sound scenario has none", () => {
  assert.deepEqual(scenarioProblems(validScenario()), []);
});

test("scenarioProblems: rejects non-objects and missing fields", () => {
  assert.deepEqual(scenarioProblems(null), ["scenario is not an object"]);
  assert.deepEqual(scenarioProblems("x"), ["scenario is not an object"]);
  const s = validScenario();
  delete s.label;
  s.note = "";
  const problems = scenarioProblems(s);
  assert.ok(problems.includes("missing or empty label"));
  assert.ok(problems.includes("missing or empty note"));
});

test("scenarioProblems: server / args / result shape", () => {
  const noServer = validScenario();
  delete noServer.server;
  assert.ok(scenarioProblems(noServer).includes("missing server.command"));
  const noCommand = validScenario();
  noCommand.server = { name: "x", version: "1" };
  assert.ok(scenarioProblems(noCommand).includes("missing server.command"));
  const noText = validScenario();
  noText.result = { kind: "xml" }; // text absent entirely
  const ntp = scenarioProblems(noText);
  assert.ok(ntp.includes("missing result.text"));
  assert.ok(!ntp.some((x) => x.startsWith("mark not in result")));
  const noArgs = validScenario();
  noArgs.args = null;
  assert.ok(scenarioProblems(noArgs).includes("missing args"));
  const noResult = validScenario();
  delete noResult.result;
  const p = scenarioProblems(noResult);
  assert.ok(p.includes("result.kind must be xml or error"));
  assert.ok(p.includes("missing result.text"));
  const badKind = validScenario();
  badKind.result.kind = "maybe";
  assert.ok(
    scenarioProblems(badKind).includes("result.kind must be xml or error"),
  );
  const emptyText = validScenario();
  emptyText.result.text = "";
  assert.ok(scenarioProblems(emptyText).includes("missing result.text"));
  const notXml = validScenario();
  notXml.result.text = "<Document/>";
  assert.ok(
    scenarioProblems(notXml).includes(
      "xml result does not open with an XML declaration",
    ),
  );
  // error results are allowed to be plain prose.
  const err = validScenario();
  err.result = { kind: "error", text: "Missing required fields" };
  err.mappings = [{ id: "m1", phrase: "Acme", marks: ["Missing"] }];
  assert.deepEqual(scenarioProblems(err), []);
});

test("scenarioProblems: mapping cross-references", () => {
  const none = validScenario();
  none.mappings = [];
  assert.ok(scenarioProblems(none).includes("scenario has no mappings"));
  const notList = validScenario();
  delete notList.mappings;
  assert.ok(scenarioProblems(notList).includes("scenario has no mappings"));
  const dupe = validScenario();
  dupe.mappings = [
    { id: "m1", phrase: "Acme", marks: ["<a>Acme</a>"] },
    { id: "m1", phrase: "pay", marks: ["Acme"] },
  ];
  assert.ok(scenarioProblems(dupe).includes("duplicate mapping id m1"));
  const badPhrase = validScenario();
  badPhrase.mappings[0].phrase = "Globex";
  assert.ok(
    scenarioProblems(badPhrase).includes("phrase not in sentence: Globex"),
  );
  const noMarks = validScenario();
  noMarks.mappings[0].marks = [];
  assert.ok(scenarioProblems(noMarks).includes("mapping m1 has no marks"));
  const listless = validScenario();
  delete listless.mappings[0].marks;
  assert.ok(scenarioProblems(listless).includes("mapping m1 has no marks"));
  const badMark = validScenario();
  badMark.mappings[0].marks = ["<b>Ghost</b>"];
  assert.ok(
    scenarioProblems(badMark).includes("mark not in result: <b>Ghost</b>"),
  );
  // Guards: non-string sentence / missing result skip the includes() checks
  // without throwing (the missing-field problems are still reported).
  const wreck = validScenario();
  wreck.sentence = 42;
  delete wreck.result;
  const problems = scenarioProblems(wreck);
  assert.ok(problems.includes("missing or empty sentence"));
  assert.ok(!problems.some((x) => x.startsWith("phrase not in sentence")));
  assert.ok(!problems.some((x) => x.startsWith("mark not in result")));
});

test("dataProblems: every rejection path", () => {
  assert.deepEqual(dataProblems(null), ["data is not an object"]);
  const p1 = dataProblems({});
  assert.ok(p1.includes("capture.date missing or not ISO formatted"));
  assert.ok(p1.includes("capture.servers missing"));
  assert.ok(p1.includes("expected 4 to 6 scenarios"));
  const p2 = dataProblems({
    capture: { date: "July", servers: [] },
    scenarios: "x",
  });
  assert.ok(p2.includes("capture.date missing or not ISO formatted"));
  assert.ok(p2.includes("capture.servers missing"));
  assert.ok(p2.includes("expected 4 to 6 scenarios"));
  const seven = {
    capture: { date: "2026-07-16", servers: [{ name: "s", version: "1" }] },
    scenarios: Array.from({ length: 7 }, (_, i) => ({
      ...validScenario(),
      id: `s${i}`,
    })),
  };
  assert.deepEqual(dataProblems(seven), ["expected 4 to 6 scenarios"]);
  const dupes = {
    capture: { date: "2026-07-16", servers: [{ name: "s", version: "1" }] },
    scenarios: Array.from({ length: 4 }, () => validScenario()),
  };
  const p3 = dataProblems(dupes);
  assert.equal(p3.filter((x) => x === "duplicate scenario id s1").length, 3);
  const nested = {
    capture: { date: "2026-07-16", servers: [{ name: "s", version: "1" }] },
    scenarios: [
      { ...validScenario(), id: "a" },
      { ...validScenario(), id: "b" },
      { ...validScenario(), id: "c" },
      { ...validScenario(), id: "d", note: "" },
    ],
  };
  assert.deepEqual(dataProblems(nested), ["d: missing or empty note"]);
  // capture present but with no date at all / servers not a list.
  const four = () => [
    { ...validScenario(), id: "a" },
    { ...validScenario(), id: "b" },
    { ...validScenario(), id: "c" },
    { ...validScenario(), id: "d" },
  ];
  assert.deepEqual(dataProblems({ capture: { servers: [{ name: "s" }] }, scenarios: four() }), [
    "capture.date missing or not ISO formatted",
  ]);
  assert.deepEqual(
    dataProblems({ capture: { date: "2026-07-16", servers: "nope" }, scenarios: four() }),
    ["capture.servers missing"],
  );
});

// --- guardrails matching the site's editorial rules ------------------------------

test("no em dashes anywhere in reader-visible baked strings", () => {
  for (const s of SIMULATOR_DATA.scenarios) {
    for (const text of [s.label, s.sentence, s.note]) {
      assert.ok(!text.includes("—"), `${s.id}: ${text}`);
    }
    for (const m of s.mappings) {
      assert.ok(!m.label.includes("—"), `${s.id}/${m.id}`);
    }
  }
  assert.ok(!captureNote(SIMULATOR_DATA).includes("—"));
});
