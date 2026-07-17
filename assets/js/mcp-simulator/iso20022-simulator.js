// <iso20022-simulator> - the /iso20022-mcp/ hub's interactive tool-call
// simulator, mirroring the <index-scorecard> architecture (ADR-0011):
//
//   - Progressive enhancement: the element arrives inert carrying a light-DOM
//     fallback paragraph. With JS off, the paragraph shows. When JS runs we
//     attach a Shadow DOM (hiding the fallback) and build the UI there.
//   - CSP-safe by construction: styling is a constructable stylesheet (no
//     inline <style>, no style=""), every listener is addEventListener, and
//     the module is same-origin under script-src 'self' with SRI stamped by
//     postbuild. There is no fetch: all data is the baked capture module.
//   - Theming: colours ride the page's design tokens (CSS custom properties
//     inherit across the shadow boundary), with AAA-contrast fallbacks for
//     both schemes. The dark fallbacks key off prefers-color-scheme plus a
//     data-sim-theme host attribute mirrored from the document's data-theme
//     (the site's theme toggle), so the component reacts to both.
//   - Keyboard accessible: the scenario picker is a roving-tabindex
//     radiogroup (arrows / Home / End), and every highlight is focusable so
//     the sentence-to-XML mapping works without a pointer.
//
// The pure logic (scenario lookup, segmentation, provenance strings) lives in
// iso20022-simulator-core.js, gated at 100/100/100 node coverage by build.sh.

import {
  scenarioById,
  defaultScenario,
  toolCallJson,
  toolCallSummary,
  resultKind,
  sentenceSegments,
  resultSegments,
  mappingById,
  captureNote,
  formatCaptureDate,
} from "./iso20022-simulator-core.js";
import { SIMULATOR_DATA } from "./iso20022-simulator-data.js";

/** Tiny hyperscript (attributes via setAttribute only; never inline style). */
function h(tag, attrs, ...kids) {
  const node = document.createElement(tag);
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

// Component styles. Colours ride the page tokens (--ink / --card / --border /
// --accent, defined per theme by the hub stylesheet) so light/dark theming is
// automatic; every fallback literal is AAA (>= 7:1) against its fallback
// surface. Dark fallbacks apply under prefers-color-scheme: dark and under an
// explicit data-sim-theme="dark" (mirrored from the document's data-theme),
// whichever fires first; data-sim-theme="light" wins back explicitly.
const SHEET_CSS = `
:host { display: block; container-type: inline-size;
  --sim-ink: var(--ink, #1d1d1f);
  --sim-mute: var(--ink-mute, #505058);
  --sim-card: var(--card, #ffffff);
  --sim-alt: var(--bg-alt, #f1f1f3);
  --sim-line: var(--border, #d2d2d7);
  --sim-accent: var(--link-color, #004caf);
  --sim-mark: #d9e7ff;
  --sim-mark-ink: #0b2547;
  --sim-mark-hot: #ffd60a;
  --sim-mark-hot-ink: #1d1d1f;
  --sim-err: #b3261e;
}
@media (prefers-color-scheme: dark) {
  :host {
    --sim-ink: var(--ink, #f5f5f7);
    --sim-mute: var(--ink-mute, #b0b0b8);
    --sim-card: var(--card, #161617);
    --sim-alt: var(--bg-alt, #1d1d1f);
    --sim-line: var(--border, #3a3a3c);
    --sim-accent: var(--link-color, #8cc0ff);
    --sim-mark: #14385f;
    --sim-mark-ink: #dbe9ff;
    --sim-mark-hot: #ffd60a;
    --sim-mark-hot-ink: #1d1d1f;
    --sim-err: #ff8a93;
  }
}
:host([data-sim-theme="dark"]) {
  --sim-ink: var(--ink, #f5f5f7);
  --sim-mute: var(--ink-mute, #b0b0b8);
  --sim-card: var(--card, #161617);
  --sim-alt: var(--bg-alt, #1d1d1f);
  --sim-line: var(--border, #3a3a3c);
  --sim-accent: var(--link-color, #8cc0ff);
  --sim-mark: #14385f;
  --sim-mark-ink: #dbe9ff;
  --sim-mark-hot: #ffd60a;
  --sim-mark-hot-ink: #1d1d1f;
  --sim-err: #ff8a93;
}
:host([data-sim-theme="light"]) {
  --sim-ink: var(--ink, #1d1d1f);
  --sim-mute: var(--ink-mute, #505058);
  --sim-card: var(--card, #ffffff);
  --sim-alt: var(--bg-alt, #f1f1f3);
  --sim-line: var(--border, #d2d2d7);
  --sim-accent: var(--link-color, #004caf);
  --sim-mark: #d9e7ff;
  --sim-mark-ink: #0b2547;
  --sim-mark-hot: #ffd60a;
  --sim-mark-hot-ink: #1d1d1f;
  --sim-err: #b3261e;
}
* { box-sizing: border-box; }
.sim {
  border: 1px solid var(--sim-line);
  border-radius: 16px;
  background: var(--sim-card);
  color: var(--sim-ink);
  padding: clamp(1rem, 3vw, 1.75rem);
  font-family: var(--type-body, system-ui, -apple-system, "Segoe UI", sans-serif);
}
.chips { display: flex; flex-wrap: wrap; gap: .5rem; margin-block-end: 1.1rem; }
.chip {
  font: inherit; font-size: .9rem; font-weight: 600; cursor: pointer;
  padding: .45rem .9rem; border-radius: 999px;
  border: 1px solid var(--sim-line);
  background: transparent; color: var(--sim-ink);
}
.chip[aria-checked="true"] {
  background: var(--sim-ink); color: var(--sim-card);
  border-color: var(--sim-ink);
}
.chip:focus-visible, .mk:focus-visible {
  outline: 2px solid var(--focus-ring-color, var(--sim-accent));
  outline-offset: 2px;
}
.sentence {
  font-size: clamp(1.15rem, 2.4vw, 1.45rem); line-height: 1.5;
  font-weight: 600; margin: 0 0 .4rem; max-width: 34em;
}
.note { margin: 0 0 1.1rem; font-size: .92rem; color: var(--sim-mute); max-width: 62ch; }
.grid { display: grid; gap: 1rem; grid-template-columns: 1fr; }
@container (min-width: 52rem) { .grid { grid-template-columns: 1fr 1fr; } }
.panel {
  border: 1px solid var(--sim-line); border-radius: 12px;
  background: var(--sim-alt); padding: .9rem 1rem; min-inline-size: 0;
}
.panel h3 {
  margin: 0 0 .15rem; font-size: .8rem; font-weight: 700;
  letter-spacing: .08em; text-transform: uppercase;
}
.panel .sub { margin: 0 0 .6rem; font-size: .82rem; color: var(--sim-mute); }
.panel.err { border-inline-start: 4px solid var(--sim-err); }
pre.code {
  margin: 0; padding: .75rem .9rem; border-radius: 8px;
  background: var(--sim-card); border: 1px solid var(--sim-line);
  overflow: auto; max-block-size: 24rem;
  font-family: var(--type-mono, ui-monospace, "SF Mono", Menlo, monospace);
  font-size: .78rem; line-height: 1.55; tab-size: 2;
}
pre.code code { font: inherit; white-space: pre; }
.panel.err pre.code code { white-space: pre-wrap; overflow-wrap: anywhere; }
.mk {
  background: var(--sim-mark); color: var(--sim-mark-ink);
  border-radius: 4px; padding: 0 .15em;
  box-shadow: 0 0 0 1px var(--sim-line);
  cursor: help;
}
.mk[data-hot] {
  background: var(--sim-mark-hot); color: var(--sim-mark-hot-ink);
  box-shadow: 0 0 0 1px var(--sim-mark-hot-ink);
}
.maplabel {
  margin: .9rem 0 0; font-size: .88rem; min-block-size: 1.4em;
  color: var(--sim-mute);
}
.maplabel strong { color: var(--sim-ink); }
.foot {
  margin: .9rem 0 0; padding-block-start: .75rem;
  border-block-start: 1px solid var(--sim-line);
  font-size: .8rem; color: var(--sim-mute); max-width: 80ch;
}
.badge {
  display: inline-block; font-size: .72rem; font-weight: 700;
  letter-spacing: .1em; text-transform: uppercase;
  margin-block-end: .9rem; color: var(--sim-mute);
}
@media (prefers-reduced-motion: no-preference) {
  .mk { transition: background-color .12s ease; }
}
`;

let sharedSheet = null;
function styleSheet() {
  if (!sharedSheet) {
    sharedSheet = new CSSStyleSheet();
    sharedSheet.replaceSync(SHEET_CSS);
  }
  return sharedSheet;
}

class Iso20022Simulator extends HTMLElement {
  connectedCallback() {
    if (this._booted) return;
    this._booted = true;
    this._data = SIMULATOR_DATA;
    const first = defaultScenario(this._data);
    if (!first) return;
    this._current = first.id;

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
    if (this._themeMo) {
      this._themeMo.disconnect();
      this._themeMo = null;
    }
  }

  _build() {
    const root = this.attachShadow({ mode: "open" });
    root.adoptedStyleSheets = [styleSheet()];

    this._syncTheme();
    this._themeMo = new MutationObserver(() => this._syncTheme());
    this._themeMo.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });

    const sim = h("div", { class: "sim" });
    sim.append(
      h("span", {
        class: "badge",
        text: `Real captured transcripts, ${formatCaptureDate(this._data.capture.date)}`,
      }),
    );

    // Scenario picker: roving-tabindex radiogroup.
    this._chips = [];
    const chips = h("div", {
      class: "chips",
      role: "radiogroup",
      "aria-label": "Choose a payment sentence",
    });
    for (const s of this._data.scenarios) {
      const chip = h("button", {
        type: "button",
        class: "chip",
        role: "radio",
        "data-id": s.id,
        text: s.label,
      });
      chip.addEventListener("click", () => this._select(s.id, false));
      chips.append(chip);
      this._chips.push(chip);
    }
    chips.addEventListener("keydown", (ev) => this._chipKeydown(ev));
    sim.append(chips);

    this._sentenceEl = h("p", { class: "sentence" });
    this._noteEl = h("p", { class: "note" });
    sim.append(this._sentenceEl, this._noteEl);

    const grid = h("div", { class: "grid" });
    this._callSub = h("p", { class: "sub" });
    this._callCode = h("code", {});
    grid.append(
      h(
        "section",
        { class: "panel" },
        h("h3", { text: "The MCP tool call" }),
        this._callSub,
        h("pre", { class: "code" }, this._callCode),
      ),
    );
    this._resultPanel = h("section", { class: "panel" });
    this._resultHead = h("h3", {});
    this._resultSub = h("p", { class: "sub" });
    this._resultCode = h("code", {});
    this._resultPanel.append(
      this._resultHead,
      this._resultSub,
      h("pre", { class: "code" }, this._resultCode),
    );
    grid.append(this._resultPanel);
    sim.append(grid);

    this._mapLabel = h("p", {
      class: "maplabel",
      role: "status",
      "aria-live": "polite",
    });
    sim.append(this._mapLabel);
    sim.append(h("p", { class: "foot", text: captureNote(this._data) }));

    // One delegated hover/focus pair drives the sentence-to-XML highlights.
    sim.addEventListener("mouseover", (ev) => this._hotFromEvent(ev, true));
    sim.addEventListener("mouseout", (ev) => this._hotFromEvent(ev, false));
    sim.addEventListener("focusin", (ev) => this._hotFromEvent(ev, true));
    sim.addEventListener("focusout", (ev) => this._hotFromEvent(ev, false));

    root.append(sim);
    this._select(this._current, false);
    this.setAttribute("data-ready", "");
  }

  _syncTheme() {
    const theme = document.documentElement.getAttribute("data-theme");
    if (theme === "dark" || theme === "light") {
      this.setAttribute("data-sim-theme", theme);
    } else {
      this.removeAttribute("data-sim-theme");
    }
  }

  _chipKeydown(ev) {
    const keys = ["ArrowRight", "ArrowDown", "ArrowLeft", "ArrowUp", "Home", "End"];
    if (!keys.includes(ev.key)) return;
    ev.preventDefault();
    const ids = this._data.scenarios.map((s) => s.id);
    const at = ids.indexOf(this._current);
    let next;
    if (ev.key === "ArrowRight" || ev.key === "ArrowDown") {
      next = (at + 1) % ids.length;
    } else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") {
      next = (at - 1 + ids.length) % ids.length;
    } else if (ev.key === "Home") {
      next = 0;
    } else {
      next = ids.length - 1;
    }
    this._select(ids[next], true);
  }

  _select(id, focus) {
    const scenario = scenarioById(this._data, id);
    if (!scenario) return;
    this._current = id;

    for (const chip of this._chips) {
      const on = chip.getAttribute("data-id") === id;
      chip.setAttribute("aria-checked", on ? "true" : "false");
      chip.setAttribute("tabindex", on ? "0" : "-1");
      if (on && focus) chip.focus();
    }

    // Sentence with focusable mapping highlights.
    this._sentenceEl.replaceChildren(
      ...sentenceSegments(scenario).map((seg) => this._segNode(scenario, seg)),
    );
    this._noteEl.textContent = scenario.note;

    // Tool call panel: the exact captured request.
    this._callSub.textContent =
      `${toolCallSummary(scenario)} via ${scenario.server.command}`;
    this._callCode.textContent = toolCallJson(scenario);

    // Result panel: the exact captured XML or all-at-once error.
    const kind = resultKind(scenario);
    if (kind === "error") {
      this._resultPanel.classList.add("err");
      this._resultHead.textContent = "The validation error";
      this._resultSub.textContent =
        "Every missing field reported in one round trip, verbatim.";
    } else {
      this._resultPanel.classList.remove("err");
      this._resultHead.textContent = `The result: ${scenario.result.messageType}`;
      this._resultSub.textContent =
        "Validated against the official XSD before it was returned, verbatim.";
    }
    this._resultCode.replaceChildren(
      ...resultSegments(scenario).map((seg) => this._segNode(scenario, seg)),
    );

    this._setHint();
  }

  _segNode(scenario, seg) {
    if (!seg.mappingId) return document.createTextNode(seg.text);
    const mapping = mappingById(scenario, seg.mappingId);
    return h("span", {
      class: "mk",
      tabindex: "0",
      "data-m": seg.mappingId,
      "aria-label": mapping ? `${seg.text}: ${mapping.label}` : seg.text,
      text: seg.text,
    });
  }

  _hotFromEvent(ev, on) {
    const target = ev.target;
    if (!target || !target.getAttribute) return;
    const id = target.getAttribute("data-m");
    if (!id) return;
    for (const mk of this.shadowRoot.querySelectorAll(".mk")) {
      if (on && mk.getAttribute("data-m") === id) {
        mk.setAttribute("data-hot", "");
      } else {
        mk.removeAttribute("data-hot");
      }
    }
    if (on) {
      const mapping = mappingById(scenarioById(this._data, this._current), id);
      if (mapping) {
        this._mapLabel.replaceChildren(
          h("strong", { text: mapping.phrase }),
          document.createTextNode(` maps to ${mapping.label}.`),
        );
        return;
      }
    }
    this._setHint();
  }

  _setHint() {
    this._mapLabel.textContent =
      "Hover or tab through the highlights to see how the sentence maps to the message.";
  }
}

if ("customElements" in window && !customElements.get("iso20022-simulator")) {
  customElements.define("iso20022-simulator", Iso20022Simulator);
}

export { Iso20022Simulator };
