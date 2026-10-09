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
})();
