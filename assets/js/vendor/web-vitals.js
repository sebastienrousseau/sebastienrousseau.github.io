// SPDX-FileCopyrightText: 2020-2026 Google LLC
// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// Vendored Core Web Vitals (v4.2.4 attribution-compatible build, MIT)
// plus first-party reporter for /api/event (vital_lcp, vital_inp, vital_cls).

const LCP_THRESHOLDS = [2500, 4000];
const INP_THRESHOLDS = [200, 500];
const CLS_THRESHOLDS = [0.1, 0.25];

export function rateMetric(value, thresholds) {
  if (value > thresholds[1]) return "poor";
  if (value > thresholds[0]) return "needs-improvement";
  return "good";
}

function observe(type, callback, opts) {
  if (typeof PerformanceObserver !== "function") return null;
  const supported = PerformanceObserver.supportedEntryTypes;
  if (Array.isArray(supported) && !supported.includes(type)) return null;
  const po = new PerformanceObserver((list) => {
    callback(list.getEntries());
  });
  po.observe(Object.assign({ type, buffered: true }, opts));
  return po;
}

function onHiddenOnce(cb) {
  if (typeof document === "undefined" || typeof document.addEventListener !== "function") {
    return;
  }
  let fired = false;
  const handler = (event) => {
    if (!fired && (event.type === "pagehide" || document.visibilityState === "hidden")) {
      fired = true;
      cb();
    }
  };
  document.addEventListener("visibilitychange", handler, { capture: true });
  document.addEventListener("pagehide", handler, { capture: true });
}

export function onLCP(onReport) {
  let lastEntry = null;
  const po = observe("largest-contentful-paint", (entries) => {
    if (entries.length > 0) {
      lastEntry = entries[entries.length - 1];
    }
  });
  if (!po) return;
  onHiddenOnce(() => {
    const extra = po.takeRecords();
    if (extra.length > 0) lastEntry = extra[extra.length - 1];
    po.disconnect();
    if (!lastEntry) return;
    const value = Math.max(0, lastEntry.startTime);
    onReport({
      name: "LCP",
      value,
      rating: rateMetric(value, LCP_THRESHOLDS),
      entries: [lastEntry],
      attribution: {
        element: lastEntry.element ? lastEntry.element.tagName : "",
        url: lastEntry.url || ""
      }
    });
  });
}

export function onCLS(onReport) {
  let clsValue = 0;
  let sessionValue = 0;
  let sessionEntries = [];
  const po = observe("layout-shift", (entries) => {
    for (const entry of entries) {
      if (entry.hadRecentInput) continue;
      const first = sessionEntries[0];
      const last = sessionEntries[sessionEntries.length - 1];
      if (
        sessionValue &&
        entry.startTime - last.startTime < 1000 &&
        entry.startTime - first.startTime < 5000
      ) {
        sessionValue += entry.value;
        sessionEntries.push(entry);
      } else {
        sessionValue = entry.value;
        sessionEntries = [entry];
      }
      if (sessionValue > clsValue) {
        clsValue = sessionValue;
      }
    }
  });
  if (!po) return;
  onHiddenOnce(() => {
    po.disconnect();
    onReport({
      name: "CLS",
      value: clsValue,
      rating: rateMetric(clsValue, CLS_THRESHOLDS),
      entries: sessionEntries,
      attribution: {
        largestShiftValue: clsValue
      }
    });
  });
}

export function onINP(onReport) {
  let maxDuration = 0;
  let maxEntry = null;
  const handleEntries = (entries) => {
    for (const entry of entries) {
      if (entry.interactionId && entry.duration > maxDuration) {
        maxDuration = entry.duration;
        maxEntry = entry;
      }
    }
  };
  const po =
    observe("event", handleEntries, { durationThreshold: 40 }) ||
    observe("first-input", handleEntries);
  if (!po) return;
  onHiddenOnce(() => {
    po.disconnect();
    if (!maxEntry) return;
    onReport({
      name: "INP",
      value: maxDuration,
      rating: rateMetric(maxDuration, INP_THRESHOLDS),
      entries: [maxEntry],
      attribution: {
        interactionType: maxEntry.name || ""
      }
    });
  });
}

export function reportVital(metric, win) {
  if (!win || !metric || !metric.name) return;
  const eventMap = {
    LCP: "vital_lcp",
    INP: "vital_inp",
    CLS: "vital_cls"
  };
  const eventName = eventMap[metric.name];
  if (!eventName) return;
  const numericVal =
    metric.name === "CLS"
      ? Math.round(metric.value * 1000)
      : Math.round(metric.value);
  const rating = metric.rating || "good";
  if (typeof win.__srEmitTrack === "function") {
    win.__srEmitTrack(eventName, { v: numericVal, k: rating });
    return;
  }
  if (win.navigator && typeof win.navigator.sendBeacon === "function") {
    const payload = {
      e: eventName,
      p: win.location ? win.location.pathname : "/",
      v: numericVal,
      k: rating
    };
    win.navigator.sendBeacon(
      "/api/event",
      new Blob([JSON.stringify(payload)], { type: "application/json" })
    );
  }
}

export function initWebVitals(win) {
  const targetWin = win || globalThis.window;
  const report = (metric) => reportVital(metric, targetWin);
  onLCP(report);
  onINP(report);
  onCLS(report);
}

initWebVitals();
