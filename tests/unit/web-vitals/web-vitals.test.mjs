// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

import assert from "node:assert/strict";
import { test } from "node:test";

import {
  initWebVitals,
  onCLS,
  onINP,
  onLCP,
  rateMetric,
  reportVital
} from "../../../assets/js/vendor/web-vitals.js";

test("rateMetric classifies good, needs-improvement, and poor", () => {
  assert.equal(rateMetric(1200, [2500, 4000]), "good");
  assert.equal(rateMetric(3000, [2500, 4000]), "needs-improvement");
  assert.equal(rateMetric(4500, [2500, 4000]), "poor");
});

test("reportVital forwards to __srEmitTrack or navigator.sendBeacon", () => {
  const tracked = [];
  const win1 = {
    __srEmitTrack(e, props) {
      tracked.push({ e, props });
    }
  };
  reportVital({ name: "LCP", value: 1420.4, rating: "good" }, win1);
  reportVital({ name: "CLS", value: 0.015, rating: "good" }, win1);
  reportVital({ name: "UNKNOWN", value: 1, rating: "good" }, win1);
  reportVital(null, win1);
  reportVital({ name: "LCP", value: 1 }, null);
  assert.equal(tracked.length, 2);
  assert.deepEqual(tracked[0], { e: "vital_lcp", props: { v: 1420, k: "good" } });
  assert.deepEqual(tracked[1], { e: "vital_cls", props: { v: 15, k: "good" } });

  const beacons = [];
  const win2 = {
    location: { pathname: "/iso20022-mcp/" },
    navigator: {
      sendBeacon(url, blob) {
        beacons.push({ url, blob });
        return true;
      }
    }
  };
  reportVital({ name: "INP", value: 96, rating: "" }, win2);
  assert.equal(beacons.length, 1);
  assert.equal(beacons[0].url, "/api/event");

  reportVital({ name: "LCP", value: 900, rating: "good" }, { navigator: {} });
  reportVital(
    { name: "LCP", value: 900, rating: "good" },
    { navigator: { sendBeacon: () => true } }
  );
});

test("onLCP, onCLS, onINP observe entries and flush on visibilitychange", () => {
  const listeners = [];
  globalThis.document = {
    visibilityState: "visible",
    addEventListener(type, fn) {
      listeners.push({ type, fn });
    }
  };
  const callbacks = new Map();
  let extraLcp = [{ startTime: 1650, element: { tagName: "H1" }, url: "" }];
  class FakePO {
    static supportedEntryTypes = [
      "largest-contentful-paint",
      "layout-shift",
      "event"
    ];
    constructor(cb) {
      this.cb = cb;
    }
    observe(opts) {
      callbacks.set(opts.type, (arr) => this.cb({ getEntries: () => arr }));
    }
    takeRecords() {
      return extraLcp;
    }
    disconnect() {}
  }
  globalThis.PerformanceObserver = FakePO;

  const reports = [];
  initWebVitals({
    __srEmitTrack(e, props) {
      reports.push({ e, props });
    }
  });

  callbacks.get("largest-contentful-paint")([]);
  callbacks.get("largest-contentful-paint")([
    { startTime: 1200, element: null, url: "https://example.com/a.webp" }
  ]);
  callbacks.get("layout-shift")([
    { value: 0.02, startTime: 100, hadRecentInput: false },
    { value: 0.03, startTime: 300, hadRecentInput: false },
    { value: 0.01, startTime: 7000, hadRecentInput: false },
    { value: 0.5, startTime: 400, hadRecentInput: true }
  ]);
  callbacks.get("event")([
    { interactionId: 0, duration: 500 },
    { interactionId: 1, duration: 88, name: "click" },
    { interactionId: 2, duration: 40, name: "" }
  ]);

  // Trigger non-hidden visibilitychange first (no-op)
  for (const l of listeners) {
    if (l.type === "visibilitychange") l.fn({ type: "visibilitychange" });
  }
  assert.equal(reports.length, 0);

  // Now hide page -> flushes all three vitals once
  globalThis.document.visibilityState = "hidden";
  for (const l of listeners) {
    l.fn({ type: l.type });
  }
  assert.equal(reports.length, 3);
  assert.deepEqual(
    reports.map((r) => r.e).sort(),
    ["vital_cls", "vital_inp", "vital_lcp"]
  );

  // Test empty LCP/INP on pagehide (when no entries arrived)
  extraLcp = [];
  listeners.length = 0;
  onLCP(() => {});
  onINP(() => {});
  callbacks.get("largest-contentful-paint")([
    { startTime: 900, element: null, url: "" }
  ]);
  callbacks.get("event")([{ interactionId: 1, duration: 50, name: "" }]);
  for (const l of listeners) {
    if (l.type === "pagehide") l.fn({ type: "pagehide" });
  }

  // Also test when no LCP / INP entry was ever recorded before pagehide
  listeners.length = 0;
  onLCP(() => {});
  onINP(() => {});
  for (const l of listeners) {
    if (l.type === "pagehide") l.fn({ type: "pagehide" });
  }

  delete globalThis.PerformanceObserver;
  delete globalThis.document;
});

test("gracefully no-ops when PerformanceObserver or supportedEntryTypes missing", () => {
  delete globalThis.PerformanceObserver;
  delete globalThis.document;
  onLCP(() => {});
  onCLS(() => {});
  onINP(() => {});

  globalThis.PerformanceObserver = class {
    static supportedEntryTypes = ["first-input"];
    constructor(cb) {
      this.cb = cb;
    }
    observe() {}
    disconnect() {}
  };
  onLCP(() => {});
  onCLS(() => {});
  onINP(() => {});

  globalThis.PerformanceObserver = class {
    static supportedEntryTypes = [];
    constructor(cb) {
      this.cb = cb;
    }
    observe() {}
    disconnect() {}
  };
  onINP(() => {});
  delete globalThis.PerformanceObserver;
});
