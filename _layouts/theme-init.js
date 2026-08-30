// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

/* Theme bootstrap. Runs synchronously in <head> before paint to avoid a flash
 * of the wrong colour scheme. Reads the saved preference, falling back to the
 * user's OS-level setting. */
(function () {
  try {
    var saved = localStorage.getItem("theme");
    var prefersDark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    var theme = saved || (prefersDark ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);
  } catch (e) {
    /* localStorage disabled. Fall through, page renders light. */
  }
})();
