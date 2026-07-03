// <index-scorecard> — a reusable, data-driven self-assessment Web Component.
//
// Progressive enhancement contract (see ADR 0001):
//   - The article ships the full static maturity tables. Those are the JS-off
//     baseline and are never removed at build time.
//   - This element arrives in the page inert, carrying a light-DOM fallback
//     paragraph and a <script type="application/json"> data island (the index
//     spec + localized UI strings, inlined by the postbuild pass so there is
//     no runtime fetch). With JS off, the fallback paragraph shows and the
//     tables above stand on their own.
//   - When JS runs, we attach a Shadow DOM (which hides the light-DOM
//     fallback) and build the interactive scorecard there. Styling is applied
//     via a constructable stylesheet — no inline <style>, no style="" — so the
//     page's hash-strict `style-src` is untouched. No inline event handlers;
//     every listener is attached with addEventListener. CSP stays clean.
//
// One component, N indices: nothing here knows about "agentic AI". Dimensions,
// levels, weights, scale and copy all come from the spec.

import {
  compositeScore,
  bandFor,
  levelFor,
  defaultScores,
  encodeState,
  decodeState,
} from "./scoring.js";

const SVG_NS = "http://www.w3.org/2000/svg";
const SVG_TAGS = new Set([
  "svg",
  "g",
  "polygon",
  "polyline",
  "circle",
  "line",
  "text",
  "title",
  "desc",
]);

/** Tiny hyperscript. Attributes via setAttribute only (never inline style). */
function h(tag, attrs, ...kids) {
  const node = SVG_TAGS.has(tag)
    ? document.createElementNS(SVG_NS, tag)
    : document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "text") {
      node.textContent = v;
    } else {
      node.setAttribute(k, String(v));
    }
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined) continue;
    node.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
  }
  return node;
}

// Component styles. Uses the page's design tokens (CSS custom properties
// inherit across the shadow boundary) so light/dark theming is automatic, with
// safe fallbacks if a token is absent. Logical properties throughout (RTL-safe).
const SHEET_CSS = `
:host { display: block; margin-block: 2rem; container-type: inline-size; }
* { box-sizing: border-box; }
.card {
  border: 1px solid var(--cl-grey-200, rgba(128,128,128,.35));
  border-radius: 12px;
  padding: clamp(1rem, 3vw, 1.75rem);
  background: var(--cl-surface, Canvas);
  color: var(--foreground-color, CanvasText);
}
.head { margin-block-end: 1rem; }
.head h3 { margin: 0 0 .35rem; font-size: 1.35rem; line-height: 1.2; }
.head p { margin: 0; max-width: 60ch; font-size: .95rem; }
.grid { display: grid; gap: clamp(1rem, 4vw, 2rem); grid-template-columns: 1fr; }
@container (min-width: 40rem) { .grid { grid-template-columns: 1fr 1fr; } }
.controls { margin: 0; padding: 0; border: 0; min-inline-size: 0; }
.controls legend { font-weight: 700; padding: 0; margin-block-end: .5rem; }
.dim { margin-block-end: 1.1rem; }
.dim .row { display: flex; justify-content: space-between; align-items: baseline; gap: .5rem; }
.dim label { font-weight: 600; }
.dim .val { font-variant-numeric: tabular-nums; font-weight: 700; white-space: nowrap; }
.dim input[type="range"] {
  inline-size: 100%; margin-block: .35rem; accent-color: var(--link-color, #005cbf);
  block-size: 1.5rem;
}
.dim .lvl { font-size: .85rem; margin: 0; }
.viz { min-inline-size: 0; }
.score { text-align: center; margin-block-end: 1rem; }
.score .n { font-size: clamp(2.5rem, 12cqw, 3.75rem); font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.score .of { font-size: 1.1rem; }
/* Band is conveyed by its descriptive text, not colour alone — text colour
   stays the high-contrast page foreground so it clears WCAG2AAA (7:1); the
   semantic hue is carried only by the (non-text) inline-start marker. */
.band {
  display: inline-block; margin-block-start: .5rem; padding: .3rem .7rem;
  border-radius: 999px; font-weight: 700; font-size: .9rem;
  border: 1px solid var(--cl-grey-200, rgba(128,128,128,.5));
  border-inline-start-width: 4px;
  color: var(--foreground-color, CanvasText);
}
.band[data-band="at-risk"] { border-inline-start-color: var(--cl-danger, #b3261e); }
.band[data-band="developing"] { border-inline-start-color: var(--cl-warning, #8a6d00); }
.band[data-band="evidence-ready"] { border-inline-start-color: var(--cl-success, #1a7f37); }
.band-desc { font-size: .85rem; margin-block: .5rem 0; }
svg.radar { display: block; inline-size: 100%; block-size: auto; margin-inline: auto; max-inline-size: 22rem; }
.radar .ring { fill: none; stroke: var(--cl-grey-200, rgba(128,128,128,.4)); stroke-width: 1; }
.radar .axis { stroke: var(--cl-grey-200, rgba(128,128,128,.4)); stroke-width: 1; }
.radar .area { fill: var(--link-color, #005cbf); fill-opacity: .18; stroke: var(--link-color, #005cbf); stroke-width: 2; stroke-linejoin: round; }
.radar .node { fill: var(--link-color, #005cbf); }
.radar .axis-label { fill: var(--foreground-color, CanvasText); font-size: 9px; }
table.equiv { inline-size: 100%; border-collapse: collapse; margin-block-start: 1rem; font-size: .9rem; }
table.equiv caption { text-align: start; font-weight: 700; margin-block-end: .4rem; }
table.equiv th, table.equiv td { text-align: start; padding: .35rem .5rem; border-block-end: 1px solid var(--cl-grey-200, rgba(128,128,128,.3)); }
table.equiv td.num { text-align: end; font-variant-numeric: tabular-nums; }
.actions { display: flex; flex-wrap: wrap; gap: .5rem; margin-block-start: 1.25rem; }
.actions button {
  font: inherit; cursor: pointer; padding: .5rem .9rem; border-radius: 8px;
  border: 1px solid var(--link-color, #005cbf); background: transparent;
  color: var(--link-color, #005cbf); font-weight: 600;
}
.actions button:hover { background: var(--bg-primary, rgba(0,92,191,.08)); }
.actions button.primary { background: var(--link-color, #005cbf); color: var(--background-color, Canvas); }
.status { margin-block-start: .75rem; font-size: .85rem; min-block-size: 1.2em; }
.foot { margin-block-start: 1rem; font-size: .85rem; }
:host-context([dir="rtl"]) .dim .row { flex-direction: row-reverse; }
@media (prefers-reduced-motion: no-preference) {
  .radar .area { transition: none; }
}
:where(button, input):focus-visible { outline: 2px solid var(--focus-ring-color, var(--link-color, #005cbf)); outline-offset: 2px; }
`;

let sharedSheet = null;
function styleSheet() {
  if (!sharedSheet) {
    sharedSheet = new CSSStyleSheet();
    sharedSheet.replaceSync(SHEET_CSS);
  }
  return sharedSheet;
}

/** Regular-polygon vertex for dimension i at radial fraction f (0..1). */
function vertex(i, n, f, cx, cy, r) {
  const ang = -Math.PI / 2 + (2 * Math.PI * i) / n;
  return { x: cx + Math.cos(ang) * r * f, y: cy + Math.sin(ang) * r * f, ang };
}

class IndexScorecard extends HTMLElement {
  connectedCallback() {
    if (this._booted) return;
    this._booted = true;
    const island = this.querySelector("script.index-scorecard-data");
    if (!island) return;
    let payload;
    try {
      payload = JSON.parse(island.textContent);
    } catch {
      return;
    }
    const spec = payload && payload.spec;
    if (!spec || !Array.isArray(spec.dimensions) || spec.dimensions.length === 0) {
      return;
    }
    this._spec = spec;
    this._strings = (payload && payload.strings) || {};
    this._lang = (payload && payload.lang) || "en";
    this._dir = (payload && payload.dir) || "ltr";
    this._paramName = "s";

    if ("IntersectionObserver" in window) {
      this._io = new IntersectionObserver(
        (entries) => {
          if (entries.some((e) => e.isIntersecting)) {
            this._io.disconnect();
            this._io = null;
            this._build();
          }
        },
        { rootMargin: "300px 0px" },
      );
      this._io.observe(this);
    } else {
      this._build();
    }
  }

  disconnectedCallback() {
    if (this._io) {
      this._io.disconnect();
      this._io = null;
    }
  }

  t(key, fallback) {
    const v = this._strings[key];
    return v === undefined || v === null || v === "" ? fallback : v;
  }

  _build() {
    const spec = this._spec;
    const fromUrl = decodeState(spec, this._readParam());
    this._scores = fromUrl || defaultScores(spec);

    const root = this.attachShadow({ mode: "open" });
    root.adoptedStyleSheets = [styleSheet()];
    root.append(this._render());

    this._refresh(false);
  }

  _readParam() {
    try {
      return new URL(window.location.href).searchParams.get(this._paramName);
    } catch {
      return null;
    }
  }

  _writeParam() {
    try {
      const url = new URL(window.location.href);
      url.searchParams.set(this._paramName, encodeState(this._spec, this._scores));
      window.history.replaceState(null, "", url.toString());
    } catch {
      /* history unavailable (e.g. sandboxed) — scoring still works in-page */
    }
  }

  _render() {
    const spec = this._spec;
    const wrap = h("div", { class: "card", dir: this._dir });

    // Heading -----------------------------------------------------------------
    const head = h(
      "div",
      { class: "head" },
      h("h3", { text: this.t("scorecard.heading", "Score your institution") }),
      h("p", {
        text: this.t(
          "scorecard.intro",
          "Set each dimension to your institution's current maturity. The composite score is weighted by regulatory materiality.",
        ),
      }),
    );
    wrap.append(head);

    const grid = h("div", { class: "grid" });

    // Controls column ---------------------------------------------------------
    const controls = h("fieldset", { class: "controls" });
    controls.append(
      h("legend", { text: this.t("scorecard.dimensionsLegend", "Dimensions") }),
    );
    this._inputs = [];
    this._valOuts = [];
    this._lvlOuts = [];
    spec.dimensions.forEach((dim, i) => {
      const inputId = `sc-${spec.slug}-${dim.id}`;
      const hintId = `${inputId}-hint`;
      const valId = `${inputId}-val`;
      const val = h("span", { class: "val", id: valId });
      const label = h("label", { for: inputId, text: dim.label });
      const input = h("input", {
        type: "range",
        id: inputId,
        min: spec.scale.min,
        max: spec.scale.max,
        step: spec.scale.step || 1,
        value: this._scores[i],
        "aria-describedby": hintId,
      });
      input.addEventListener("input", () => {
        this._scores[i] = Number(input.value);
        this._refresh(true);
      });
      const lvl = h("p", { class: "lvl", id: hintId });
      this._inputs.push(input);
      this._valOuts.push(val);
      this._lvlOuts.push(lvl);
      controls.append(
        h(
          "div",
          { class: "dim" },
          h("div", { class: "row" }, label, val),
          input,
          lvl,
        ),
      );
    });
    grid.append(controls);

    // Visualisation column ----------------------------------------------------
    const viz = h("div", { class: "viz" });

    this._scoreN = h("span", { class: "n" });
    this._scoreOf = h("span", {
      class: "of",
      text: ` / ${spec.scale.max}`,
    });
    this._composite = h(
      "div",
      {
        class: "score",
        role: "status",
        "aria-live": "polite",
        "aria-atomic": "true",
      },
      h(
        "div",
        {},
        this._scoreN,
        this._scoreOf,
      ),
      (this._bandEl = h("span", { class: "band" })),
    );
    this._compositeLabel = h("p", {
      class: "band-desc",
      "aria-hidden": "false",
    });
    viz.append(
      h("p", {
        class: "band-desc",
        text: this.t("scorecard.composite", "Composite index score"),
      }),
      this._composite,
      this._compositeLabel,
    );

    // Radar (decorative; the table below is the text equivalent) --------------
    this._radarHost = h("div", {});
    viz.append(this._radarHost);

    // Text-equivalent results table -------------------------------------------
    this._equivBody = h("tbody", {});
    const table = h(
      "table",
      { class: "equiv" },
      h("caption", {
        text: this.t("scorecard.tableCaption", "Your scores by dimension"),
      }),
      h(
        "thead",
        {},
        h(
          "tr",
          {},
          h("th", { scope: "col", text: this.t("scorecard.colDimension", "Dimension") }),
          h("th", { scope: "col", text: this.t("scorecard.colLevel", "Maturity level") }),
          h("th", { scope: "col", class: "num", text: this.t("scorecard.colWeight", "Weight") }),
          h("th", { scope: "col", class: "num", text: this.t("scorecard.colScore", "Score") }),
        ),
      ),
      this._equivBody,
    );
    viz.append(table);
    grid.append(viz);
    wrap.append(grid);

    // Actions -----------------------------------------------------------------
    const reset = h("button", {
      type: "button",
      text: this.t("scorecard.reset", "Reset"),
    });
    reset.addEventListener("click", () => {
      this._scores = defaultScores(spec);
      this._inputs.forEach((inp, i) => {
        inp.value = String(this._scores[i]);
      });
      this._refresh(true);
    });
    const share = h("button", {
      type: "button",
      class: "primary",
      text: this.t("scorecard.share", "Copy shareable link"),
    });
    share.addEventListener("click", () => this._share());
    const dl = h("button", {
      type: "button",
      text: this.t("scorecard.download", "Download PNG"),
    });
    dl.addEventListener("click", () => this._download());
    wrap.append(h("div", { class: "actions" }, reset, share, dl));

    this._statusEl = h("p", {
      class: "status",
      role: "status",
      "aria-live": "polite",
    });
    wrap.append(this._statusEl);

    if (spec.source_url) {
      wrap.append(
        h(
          "p",
          { class: "foot" },
          h("a", {
            href: spec.source_url,
            text: this.t("scorecard.methodology", "Read the full index methodology"),
          }),
        ),
      );
    }
    return wrap;
  }

  _refresh(pushUrl) {
    const spec = this._spec;
    const composite = compositeScore(spec, this._scores);
    const band = bandFor(spec, composite);

    this._scoreN.textContent = String(composite);
    if (band) {
      this._bandEl.textContent = band.label;
      this._bandEl.setAttribute("data-band", band.id || "");
      this._compositeLabel.textContent = band.desc || "";
    } else {
      this._bandEl.textContent = "";
      this._compositeLabel.textContent = "";
    }

    // Per-dimension readouts + level labels + accessible value text.
    this._equivBody.replaceChildren();
    spec.dimensions.forEach((dim, i) => {
      const score = this._scores[i];
      const lvl = levelFor(dim, score);
      const lvlLabel = lvl ? lvl.label : "";
      this._valOuts[i].textContent = String(score);
      this._lvlOuts[i].textContent = lvl ? `${lvl.label}${lvl.hint ? " — " + lvl.hint : ""}` : "";
      const input = this._inputs[i];
      input.setAttribute("aria-valuetext", `${score} — ${lvlLabel}`);
      this._equivBody.append(
        h(
          "tr",
          {},
          h("th", { scope: "row", text: dim.label }),
          h("td", { text: lvlLabel }),
          h("td", { class: "num", text: `${Math.round(dim.weight * 100)}%` }),
          h("td", { class: "num", text: String(score) }),
        ),
      );
    });

    this._drawRadar();

    if (pushUrl) this._writeParam();
  }

  _drawRadar() {
    const spec = this._spec;
    const n = spec.dimensions.length;
    const size = 240;
    const cx = size / 2;
    const cy = size / 2;
    const r = size / 2 - 34;
    const max = spec.scale.max;

    const svg = h("svg", {
      class: "radar",
      viewBox: `0 0 ${size} ${size}`,
      role: "img",
      "aria-hidden": "true",
      focusable: "false",
    });
    svg.append(
      h("title", { text: this.t("scorecard.radarTitle", "Readiness radar") }),
    );

    // Concentric rings at 25/50/75/100%.
    [0.25, 0.5, 0.75, 1].forEach((f) => {
      const pts = spec.dimensions
        .map((_, i) => {
          const v = vertex(i, n, f, cx, cy, r);
          return `${v.x.toFixed(1)},${v.y.toFixed(1)}`;
        })
        .join(" ");
      svg.append(h("polygon", { class: "ring", points: pts }));
    });

    // Axes + labels.
    spec.dimensions.forEach((dim, i) => {
      const edge = vertex(i, n, 1, cx, cy, r);
      svg.append(
        h("line", {
          class: "axis",
          x1: cx,
          y1: cy,
          x2: edge.x.toFixed(1),
          y2: edge.y.toFixed(1),
        }),
      );
      const lp = vertex(i, n, 1.16, cx, cy, r);
      const anchor = Math.abs(lp.x - cx) < 1 ? "middle" : lp.x < cx ? "end" : "start";
      svg.append(
        h("text", {
          class: "axis-label",
          x: lp.x.toFixed(1),
          y: lp.y.toFixed(1),
          "text-anchor": anchor,
          "dominant-baseline": "middle",
          text: dim.short || dim.id,
        }),
      );
    });

    // Data area.
    const area = this._scores
      .map((s, i) => {
        const f = max > 0 ? Math.max(0, Math.min(max, s)) / max : 0;
        const v = vertex(i, n, f, cx, cy, r);
        return `${v.x.toFixed(1)},${v.y.toFixed(1)}`;
      })
      .join(" ");
    svg.append(h("polygon", { class: "area", points: area }));
    this._scores.forEach((s, i) => {
      const f = max > 0 ? Math.max(0, Math.min(max, s)) / max : 0;
      const v = vertex(i, n, f, cx, cy, r);
      svg.append(
        h("circle", { class: "node", cx: v.x.toFixed(1), cy: v.y.toFixed(1), r: 2.5 }),
      );
    });

    this._radarHost.replaceChildren(svg);
  }

  async _share() {
    this._writeParam();
    const url = window.location.href;
    let ok = false;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(url);
        ok = true;
      }
    } catch {
      ok = false;
    }
    this._statusEl.textContent = ok
      ? this.t("scorecard.shareCopied", "Link copied to clipboard")
      : url;
  }

  _download() {
    const canvas = this._paintCanvas();
    const finish = (blob) => {
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      const a = h("a", {
        href: url,
        download: `${this._spec.slug}-scorecard.png`,
      });
      a.click();
      URL.revokeObjectURL(url);
      this._statusEl.textContent = this.t(
        "scorecard.downloaded",
        "Scorecard image downloaded",
      );
    };
    if (canvas.toBlob) {
      canvas.toBlob(finish, "image/png");
    } else {
      finish(null);
    }
  }

  // Hand-drawn PNG (no SVG->image round trip, so no img-src dependency).
  _paintCanvas() {
    const spec = this._spec;
    const scale = 2;
    const W = 600;
    const H = 420;
    const canvas = h("canvas", { width: W * scale, height: H * scale });
    const ctx = canvas.getContext("2d");
    if (!ctx) return canvas;
    ctx.scale(scale, scale);
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "#0b1f3a";
    ctx.font = "700 22px system-ui, -apple-system, Segoe UI, sans-serif";
    ctx.fillText(spec.title || "Index scorecard", 24, 40);

    const composite = compositeScore(spec, this._scores);
    const band = bandFor(spec, composite);
    ctx.font = "800 52px system-ui, sans-serif";
    ctx.fillStyle = "#005cbf";
    ctx.fillText(`${composite}`, 24, 110);
    ctx.font = "400 20px system-ui, sans-serif";
    ctx.fillStyle = "#333";
    ctx.fillText(`/ ${spec.scale.max}`, 24 + ctx.measureText(`${composite}`).width + 88, 110);
    if (band) {
      ctx.font = "700 18px system-ui, sans-serif";
      ctx.fillStyle = "#0b1f3a";
      ctx.fillText(band.label, 24, 150);
    }

    // Radar on the right.
    const n = spec.dimensions.length;
    const cx = 430;
    const cy = 230;
    const r = 120;
    const max = spec.scale.max;
    ctx.strokeStyle = "#cbd5e1";
    ctx.lineWidth = 1;
    [0.25, 0.5, 0.75, 1].forEach((f) => {
      ctx.beginPath();
      spec.dimensions.forEach((_, i) => {
        const v = vertex(i, n, f, cx, cy, r);
        if (i === 0) ctx.moveTo(v.x, v.y);
        else ctx.lineTo(v.x, v.y);
      });
      ctx.closePath();
      ctx.stroke();
    });
    ctx.beginPath();
    this._scores.forEach((s, i) => {
      const f = max > 0 ? Math.max(0, Math.min(max, s)) / max : 0;
      const v = vertex(i, n, f, cx, cy, r);
      if (i === 0) ctx.moveTo(v.x, v.y);
      else ctx.lineTo(v.x, v.y);
    });
    ctx.closePath();
    ctx.fillStyle = "rgba(0,92,191,0.18)";
    ctx.strokeStyle = "#005cbf";
    ctx.lineWidth = 2;
    ctx.fill();
    ctx.stroke();

    // Per-dimension list on the left.
    ctx.font = "400 14px system-ui, sans-serif";
    ctx.fillStyle = "#0b1f3a";
    spec.dimensions.forEach((dim, i) => {
      const y = 190 + i * 26;
      ctx.fillText(`${dim.label}: ${this._scores[i]}`, 24, y);
    });

    ctx.font = "400 12px system-ui, sans-serif";
    ctx.fillStyle = "#64748b";
    ctx.fillText(spec.source_url || "sebastienrousseau.com", 24, H - 20);
    return canvas;
  }
}

if ("customElements" in window && !customElements.get("index-scorecard")) {
  customElements.define("index-scorecard", IndexScorecard);
}

export { IndexScorecard };
