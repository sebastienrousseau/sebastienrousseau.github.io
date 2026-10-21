// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/* Colour-scheme bootstrap. Runs synchronously in <head> before paint to avoid
 * a flash of the wrong scheme. Restores an explicit light or dark choice;
 * "system" is the absence of data-theme, and the stylesheet follows the
 * operating system through prefers-color-scheme. */
(function () {
  try {
    var saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") {
      document.documentElement.setAttribute("data-theme", saved);
    }
  } catch (e) {
    /* localStorage disabled. Fall through, the page follows the system. */
  }
  /* Webfonts on later views only. main.js records "wf" once the fonts
   * have been fetched after a page's load; from then on they come from
   * the HTTP cache inside font-display: optional's block period, so the
   * page paints in them with no swap. Without the record (a first view,
   * or storage disabled) the page stays in its system faces. */
  try {
    if (localStorage.getItem("wf") === "1") {
      document.documentElement.classList.add("wf");
    }
  } catch (e) {
    /* localStorage disabled: system faces. */
  }
})();
