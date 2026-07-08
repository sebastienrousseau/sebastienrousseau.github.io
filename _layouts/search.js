/*
 * On-site search runtime — sebastienrousseau.com
 * ------------------------------------------------
 * Dependency-free, client-side full-text search over the per-locale
 * `search-index.json` the build already emits (see ADR-0010, DX plan Phase 2).
 *
 * Loaded LAZILY (injected on first Cmd/Ctrl-K, or on the /search page) so it
 * adds 0 to initial LCP on every other page. Same-origin, under the site's
 * hash-strict `script-src 'self'` — no CSP relaxation, no inline handlers.
 *
 * Provides:
 *   - a Cmd/Ctrl-K command-palette overlay (role=dialog + role=listbox),
 *   - progressive enhancement of the /search page,
 *   - locale-aware search (active language by default; "all languages" toggle),
 *   - full keyboard navigation (arrows / Enter / Esc / Home / End), focus trap,
 *   - prefers-reduced-motion-aware result scrolling.
 *
 * UI strings come from /<lang>/search-ui.json (projected from strings.json).
 */
(function () {
  "use strict";

  var REDUCED = false;
  try {
    REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) {}

  // ---- locale + data --------------------------------------------------------

  function currentSegment() {
    var parts = location.pathname.split("/").filter(Boolean);
    return parts.length ? parts[0] : "";
  }

  function fetchJSON(url) {
    return fetch(url, { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status + " for " + url);
      return r.json();
    });
  }

  var _uiPromise = null;
  function loadUI() {
    if (_uiPromise) return _uiPromise;
    var seg = currentSegment();
    var localized = seg ? "/" + seg + "/search-ui.json" : "/search-ui.json";
    _uiPromise = fetchJSON(localized).catch(function () {
      // Not a locale root (e.g. /articles/...) → fall back to the EN manifest.
      return fetchJSON("/search-ui.json");
    });
    return _uiPromise;
  }

  var _indexCache = {}; // url -> Promise<entries[]>
  function loadIndex(url) {
    if (!_indexCache[url]) {
      _indexCache[url] = fetchJSON(url).then(function (data) {
        var entries = (data && data.entries) || [];
        // Precompute a lowercased haystack once per entry.
        for (var i = 0; i < entries.length; i++) {
          var e = entries[i];
          e._t = String(e.title || "").toLowerCase();
          e._h = (e.headings || []).join(" · ").toLowerCase();
          e._c = String(e.content || "").toLowerCase();
        }
        return entries;
      });
    }
    return _indexCache[url];
  }

  // ---- ranking --------------------------------------------------------------

  function tokenize(q) {
    // Split on whitespace + common punctuation. Keep CJK/undelimited scripts as
    // whole tokens; a substring pass (below) recovers those matches.
    return q
      .toLowerCase()
      .split(/[\s,.;:!?/()"'`’–—\[\]{}<>|]+/)
      .filter(function (t) {
        return t.length > 0;
      });
  }

  function scoreEntry(entry, terms, rawQuery) {
    var score = 0;
    var matchedAll = true;
    for (var i = 0; i < terms.length; i++) {
      var term = terms[i];
      var hit = 0;
      if (entry._t.indexOf(term) !== -1) {
        hit += 8;
        if (entry._t.indexOf(term) === 0 || entry._t.indexOf(" " + term) !== -1) hit += 4;
      }
      if (entry._h.indexOf(term) !== -1) hit += 4;
      var idx = entry._c.indexOf(term);
      if (idx !== -1) {
        hit += 2;
        // small bonus for a second occurrence, capped
        if (entry._c.indexOf(term, idx + term.length) !== -1) hit += 1;
      }
      if (hit === 0) matchedAll = false;
      score += hit;
    }
    // Substring fallback: rescues no-space scripts and multi-word phrases.
    if (rawQuery.length >= 2) {
      if (entry._t.indexOf(rawQuery) !== -1) score += 6;
      else if (entry._c.indexOf(rawQuery) !== -1) score += 3;
      else if (entry._h.indexOf(rawQuery) !== -1) score += 3;
    }
    return matchedAll ? score : score >= 6 ? score * 0.5 : 0;
  }

  function search(entries, rawQuery, limit) {
    var q = rawQuery.trim().toLowerCase();
    if (!q) return [];
    var terms = tokenize(q);
    var scored = [];
    for (var i = 0; i < entries.length; i++) {
      var s = scoreEntry(entries[i], terms, q);
      if (s > 0) scored.push({ e: entries[i], s: s });
    }
    scored.sort(function (a, b) {
      return b.s - a.s;
    });
    return scored.slice(0, limit || 30);
  }

  // ---- snippet (XSS-safe: text nodes + <mark>, never innerHTML) --------------

  function snippetFragment(content, terms, rawQuery) {
    var lc = content.toLowerCase();
    var pos = -1;
    var hitLen = 0;
    for (var i = 0; i < terms.length; i++) {
      var p = lc.indexOf(terms[i]);
      if (p !== -1 && (pos === -1 || p < pos)) {
        pos = p;
        hitLen = terms[i].length;
      }
    }
    if (pos === -1 && rawQuery.length >= 2) {
      pos = lc.indexOf(rawQuery);
      hitLen = rawQuery.length;
    }
    var start = 0;
    var win;
    if (pos !== -1) {
      start = Math.max(0, pos - 60);
      win = content.slice(start, pos + hitLen + 120);
      if (start > 0) win = "…" + win;
      if (pos + hitLen + 120 < content.length) win = win + "…";
    } else {
      win = content.slice(0, 160) + (content.length > 160 ? "…" : "");
    }
    var frag = document.createDocumentFragment();
    // Highlight all term occurrences within the window, case-insensitive.
    var lcWin = win.toLowerCase();
    var cursor = 0;
    var lowered = terms.slice();
    if (rawQuery.length >= 2 && lowered.indexOf(rawQuery) === -1) lowered.push(rawQuery);
    while (cursor < win.length) {
      var best = -1;
      var bestLen = 0;
      for (var t = 0; t < lowered.length; t++) {
        var idx = lcWin.indexOf(lowered[t], cursor);
        if (idx !== -1 && (best === -1 || idx < best)) {
          best = idx;
          bestLen = lowered[t].length;
        }
      }
      if (best === -1) {
        frag.appendChild(document.createTextNode(win.slice(cursor)));
        break;
      }
      if (best > cursor) frag.appendChild(document.createTextNode(win.slice(cursor, best)));
      var mark = document.createElement("mark");
      mark.textContent = win.slice(best, best + bestLen);
      frag.appendChild(mark);
      cursor = best + bestLen;
    }
    return frag;
  }

  // ---- shared controller ----------------------------------------------------

  function makeEl(tag, cls, attrs) {
    var el = document.createElement(tag);
    if (cls) el.className = cls;
    if (attrs) {
      for (var k in attrs) if (attrs.hasOwnProperty(k)) el.setAttribute(k, attrs[k]);
    }
    return el;
  }

  // A Results view binds an <input>, a listbox <ul>, a status region and an
  // empty-state node, plus the data model, and handles querying + keyboard.
  function ResultsView(opts) {
    this.ui = opts.ui;
    this.input = opts.input;
    this.list = opts.list;
    this.status = opts.status;
    this.empty = opts.empty;
    this.allToggle = opts.allToggle; // checkbox or null
    this.onNavigate = opts.onNavigate || function () {};
    this.active = -1;
    this.results = [];
    this.terms = [];
    this.raw = "";
    this.idPrefix = opts.idPrefix || "ss-opt-";
    this._debounce = null;
    this._bind();
  }

  ResultsView.prototype._localeEntries = function () {
    var ui = this.ui;
    var all = this.allToggle && this.allToggle.checked;
    if (all) {
      var proms = ui.locales.map(function (loc) {
        return loadIndex(loc.index).then(function (entries) {
          return { loc: loc, entries: entries };
        });
      });
      return Promise.all(proms).then(function (sets) {
        var merged = [];
        sets.forEach(function (set) {
          for (var i = 0; i < set.entries.length; i++) {
            var e = set.entries[i];
            e._loc = set.loc.label;
            e._rtl = set.loc.rtl;
            merged.push(e);
          }
        });
        return merged;
      });
    }
    var mine = ui.locales.filter(function (l) {
      return l.code === ui.lang;
    })[0] || ui.locales[0];
    return loadIndex(mine.index).then(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        entries[i]._loc = mine.label;
        entries[i]._rtl = mine.rtl;
      }
      return entries;
    });
  };

  ResultsView.prototype.query = function (raw) {
    var self = this;
    this.raw = raw;
    if (!raw.trim()) {
      this.render([], []);
      this.setStatus(this.ui.ui.hint || "");
      return;
    }
    this.setStatus(this.ui.ui.searching || "");
    this._localeEntries().then(function (entries) {
      // Ignore stale responses if the query changed meanwhile.
      if (self.raw !== raw) return;
      var terms = tokenize(raw.trim().toLowerCase());
      var results = search(entries, raw, 30);
      self.terms = terms;
      self.render(results, terms);
    });
  };

  ResultsView.prototype.render = function (results, terms) {
    var self = this;
    this.results = results;
    this.active = -1;
    this.list.textContent = "";
    this.input.setAttribute("aria-expanded", results.length ? "true" : "false");
    this.input.removeAttribute("aria-activedescendant");
    if (!this.raw.trim()) {
      this.empty.hidden = true;
      return;
    }
    if (!results.length) {
      this.empty.textContent = this.ui.ui.noResults || "No results found.";
      this.empty.hidden = false;
      this.setStatus(this.ui.ui.noResults || "");
      return;
    }
    this.empty.hidden = true;
    var showLang = this.allToggle && this.allToggle.checked;
    results.forEach(function (r, i) {
      var e = r.e;
      // APG listbox pattern: options are NON-interactive (no nested <a>), so
      // axe's nested-interactive rule stays clean. Activation is via JS on
      // click / Enter, mediated by onNavigate. aria-selected tracks the cursor.
      var li = makeEl("li", "ss-opt ss-opt-link", {
        role: "option",
        id: self.idPrefix + i,
        "aria-selected": "false",
      });
      if (e._rtl) li.setAttribute("dir", "rtl");
      var title = makeEl("span", "ss-opt-title");
      title.textContent = e.title || e.url;
      li.appendChild(title);
      var snip = makeEl("p", "ss-opt-snippet");
      snip.appendChild(snippetFragment(e.content || "", self.terms, self.raw.trim().toLowerCase()));
      li.appendChild(snip);
      var meta = makeEl("span", "ss-opt-meta");
      meta.textContent = showLang && e._loc ? e._loc + "  ·  " + e.url : e.url;
      li.appendChild(meta);
      // Pointer selection mirrors keyboard selection.
      li.addEventListener("mouseenter", function () {
        self.setActive(i, false);
      });
      li.addEventListener("click", function () {
        self.onNavigate(e.url);
      });
      self.list.appendChild(li);
    });
    var n = results.length;
    var tmpl = this.ui.ui.resultsLabel || "Search results";
    this.setStatus(n + " — " + tmpl);
  };

  ResultsView.prototype.setStatus = function (text) {
    if (this.status) this.status.textContent = text;
  };

  ResultsView.prototype.setActive = function (idx, scroll) {
    var items = this.list.children;
    if (this.active >= 0 && items[this.active]) {
      items[this.active].classList.remove("is-active");
      items[this.active].setAttribute("aria-selected", "false");
    }
    this.active = idx;
    if (idx < 0 || !items[idx]) {
      this.input.removeAttribute("aria-activedescendant");
      return;
    }
    items[idx].classList.add("is-active");
    items[idx].setAttribute("aria-selected", "true");
    this.input.setAttribute("aria-activedescendant", this.idPrefix + idx);
    if (scroll !== false) {
      items[idx].scrollIntoView({ block: "nearest", behavior: REDUCED ? "auto" : "smooth" });
    }
  };

  ResultsView.prototype.move = function (delta) {
    var n = this.results.length;
    if (!n) return;
    var next = this.active + delta;
    if (next < 0) next = n - 1;
    if (next >= n) next = 0;
    this.setActive(next, true);
  };

  ResultsView.prototype.openActive = function () {
    var i = this.active >= 0 ? this.active : 0;
    if (this.results[i]) this.onNavigate(this.results[i].e.url);
  };

  ResultsView.prototype._bind = function () {
    var self = this;
    this.input.addEventListener("input", function () {
      if (self._debounce) clearTimeout(self._debounce);
      var v = self.input.value;
      self._debounce = setTimeout(function () {
        self.query(v);
      }, 120);
    });
    this.input.addEventListener("keydown", function (ev) {
      switch (ev.key) {
        case "ArrowDown":
          ev.preventDefault();
          self.move(1);
          break;
        case "ArrowUp":
          ev.preventDefault();
          self.move(-1);
          break;
        case "Home":
          if (self.results.length) {
            ev.preventDefault();
            self.setActive(0, true);
          }
          break;
        case "End":
          if (self.results.length) {
            ev.preventDefault();
            self.setActive(self.results.length - 1, true);
          }
          break;
        case "Enter":
          if (self.results.length) {
            ev.preventDefault();
            self.openActive();
          }
          break;
      }
    });
    if (this.allToggle) {
      this.allToggle.addEventListener("change", function () {
        self.query(self.input.value);
      });
    }
  };

  // ---- overlay (command palette) -------------------------------------------

  var overlay = null; // { root, view, lastFocus }

  function buildOverlay(ui) {
    var root = makeEl("div", "ss-overlay", { hidden: "" });
    var backdrop = makeEl("div", "ss-backdrop");
    backdrop.setAttribute("data-ss-close", "");
    var panel = makeEl("div", "ss-panel", {
      role: "dialog",
      "aria-modal": "true",
      "aria-label": ui.ui.dialogLabel || "Site search",
    });

    var row = makeEl("div", "ss-row");
    var icon = makeEl("span", "ss-icon");
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = "⌕"; // ⌕
    var input = makeEl("input", "ss-input", {
      type: "search",
      role: "combobox",
      "aria-expanded": "false",
      "aria-controls": "ss-results",
      "aria-autocomplete": "list",
      "aria-label": ui.ui.label || "Search",
      autocomplete: "off",
      autocapitalize: "off",
      autocorrect: "off",
      spellcheck: "false",
      placeholder: ui.ui.placeholder || "Search…",
    });
    var clearBtn = makeEl("button", "ss-clear", {
      type: "button",
      "aria-label": ui.ui.clear || "Clear",
      hidden: "",
    });
    clearBtn.textContent = "×";
    var closeBtn = makeEl("button", "ss-close", {
      type: "button",
      "aria-label": ui.ui.close || "Close",
    });
    closeBtn.setAttribute("data-ss-close", "");
    closeBtn.textContent = "Esc";
    row.appendChild(icon);
    row.appendChild(input);
    row.appendChild(clearBtn);
    row.appendChild(closeBtn);

    var toolbar = makeEl("div", "ss-toolbar");
    var allLabel = makeEl("label", "ss-all");
    var allCb = makeEl("input", null, { type: "checkbox" });
    var allText = makeEl("span", null);
    allText.textContent = ui.ui.allLocales || "Search all languages";
    allLabel.appendChild(allCb);
    allLabel.appendChild(allText);
    var status = makeEl("span", "ss-status", { role: "status", "aria-live": "polite" });
    toolbar.appendChild(allLabel);
    toolbar.appendChild(status);

    var list = makeEl("ul", "ss-results", {
      id: "ss-results",
      role: "listbox",
      "aria-label": ui.ui.resultsLabel || "Search results",
    });
    var empty = makeEl("div", "ss-empty", { hidden: "" });

    var hint = makeEl("div", "ss-hint");
    hint.textContent = ui.ui.hint || "";

    panel.appendChild(row);
    panel.appendChild(toolbar);
    panel.appendChild(list);
    panel.appendChild(empty);
    panel.appendChild(hint);
    root.appendChild(backdrop);
    root.appendChild(panel);
    document.body.appendChild(root);

    var view = new ResultsView({
      ui: ui,
      input: input,
      list: list,
      status: status,
      empty: empty,
      allToggle: allCb,
      idPrefix: "ss-opt-",
      onNavigate: function (url) {
        location.assign(url);
      },
    });

    clearBtn.addEventListener("click", function () {
      input.value = "";
      clearBtn.hidden = true;
      view.query("");
      input.focus();
    });
    input.addEventListener("input", function () {
      clearBtn.hidden = !input.value;
    });

    // Close affordances.
    root.addEventListener("click", function (ev) {
      var t = ev.target;
      if (t && t.nodeType === 1 && t.hasAttribute && t.hasAttribute("data-ss-close")) closeOverlay();
    });

    // Focus trap + Esc, scoped to the panel.
    root.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeOverlay();
        return;
      }
      if (ev.key === "Tab") {
        var focusables = panel.querySelectorAll(
          'input, button:not([hidden]), [href], [tabindex]:not([tabindex="-1"])'
        );
        var visible = [];
        for (var i = 0; i < focusables.length; i++) {
          if (focusables[i].offsetParent !== null || focusables[i] === document.activeElement)
            visible.push(focusables[i]);
        }
        if (!visible.length) return;
        var first = visible[0];
        var last = visible[visible.length - 1];
        if (ev.shiftKey && document.activeElement === first) {
          ev.preventDefault();
          last.focus();
        } else if (!ev.shiftKey && document.activeElement === last) {
          ev.preventDefault();
          first.focus();
        }
      }
    });

    return { root: root, view: view, input: input, lastFocus: null };
  }

  function openOverlay() {
    loadUI().then(function (ui) {
      if (!overlay) overlay = buildOverlay(ui);
      overlay.lastFocus = document.activeElement;
      overlay.root.hidden = false;
      document.documentElement.classList.add("ss-open");
      // Defer focus so the show transition doesn't swallow it.
      window.requestAnimationFrame(function () {
        overlay.input.focus();
        overlay.input.select();
        if (overlay.input.value) overlay.view.query(overlay.input.value);
        else overlay.view.setStatus(ui.ui.hint || "");
      });
    });
  }

  function closeOverlay() {
    if (!overlay || overlay.root.hidden) return;
    overlay.root.hidden = true;
    document.documentElement.classList.remove("ss-open");
    if (overlay.lastFocus && overlay.lastFocus.focus) {
      try {
        overlay.lastFocus.focus();
      } catch (e) {}
    }
  }

  // ---- /search page enhancement --------------------------------------------

  function enhancePage(mount) {
    loadUI().then(function (ui) {
      mount.classList.add("ss-enhanced");
      var live = makeEl("div", "ss-page-live");

      var row = makeEl("div", "ss-row ss-row--page");
      var input = makeEl("input", "ss-input", {
        type: "search",
        role: "combobox",
        "aria-expanded": "false",
        "aria-controls": "ss-page-results",
        "aria-autocomplete": "list",
        "aria-label": ui.ui.label || "Search",
        autocomplete: "off",
        spellcheck: "false",
        placeholder: ui.ui.placeholder || "Search…",
      });
      row.appendChild(input);

      var toolbar = makeEl("div", "ss-toolbar");
      var allLabel = makeEl("label", "ss-all");
      var allCb = makeEl("input", null, { type: "checkbox" });
      var allText = makeEl("span", null);
      allText.textContent = ui.ui.allLocales || "Search all languages";
      allLabel.appendChild(allCb);
      allLabel.appendChild(allText);
      var status = makeEl("span", "ss-status", { role: "status", "aria-live": "polite" });
      toolbar.appendChild(allLabel);
      toolbar.appendChild(status);

      var list = makeEl("ul", "ss-results ss-results--page", {
        id: "ss-page-results",
        role: "listbox",
        "aria-label": ui.ui.resultsLabel || "Search results",
      });
      var empty = makeEl("div", "ss-empty", { hidden: "" });

      live.appendChild(row);
      live.appendChild(toolbar);
      live.appendChild(list);
      live.appendChild(empty);
      mount.appendChild(live);

      var view = new ResultsView({
        ui: ui,
        input: input,
        list: list,
        status: status,
        empty: empty,
        allToggle: allCb,
        idPrefix: "ss-page-opt-",
        onNavigate: function (url) {
          location.assign(url);
        },
      });

      // Deep-link / prefill from ?q=
      var params = new URLSearchParams(location.search);
      var q = params.get("q") || "";
      if (q) {
        input.value = q;
        view.query(q);
      } else {
        view.setStatus(ui.ui.hint || "");
      }
      // Keep the URL shareable as the reader types (no history spam).
      input.addEventListener("input", function () {
        var u = new URL(location.href);
        if (input.value) u.searchParams.set("q", input.value);
        else u.searchParams.delete("q");
        history.replaceState(null, "", u);
      });
      input.focus();
    });
  }

  // ---- public API + boot ----------------------------------------------------

  window.SiteSearch = {
    open: openOverlay,
    close: closeOverlay,
  };

  // If a Cmd/Ctrl-K arrived before this module finished loading, honour it.
  if (window.__ssPendingOpen) {
    window.__ssPendingOpen = false;
    openOverlay();
  }

  // Self-enhance the /search page when present.
  var pageMount = document.getElementById("search-page");
  if (pageMount) enhancePage(pageMount);

  // Announce readiness so the eager bootstrap in main.js can chain .open().
  try {
    document.dispatchEvent(new CustomEvent("sitesearch:ready"));
  } catch (e) {}
})();
