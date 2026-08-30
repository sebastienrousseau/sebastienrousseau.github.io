// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

// In-browser driver for the hsh WASM demo. Loads the wasm-bindgen-generated
// module, then wires the SHA-256 / BLAKE3 text fields to live keystrokes and
// the Argon2id field to an explicit button (Argon2id is intentionally slow —
// running it on every keystroke would freeze the input).
import init, { sha256_hex, blake3_hex, argon2id_phc } from "./hsh_demo.js";

const $ = (id) => document.getElementById(id);

async function boot() {
  await init();
  const input = $("input");
  const outSha = $("out-sha256");
  const outBlake = $("out-blake3");
  const outArgon = $("out-argon2");
  const argonGo = $("argon2-go");

  const refreshFast = () => {
    const v = input.value;
    if (!v) {
      outSha.textContent = "—";
      outBlake.textContent = "—";
      return;
    }
    outSha.textContent = sha256_hex(v);
    outBlake.textContent = blake3_hex(v);
  };

  input.addEventListener("input", refreshFast);

  argonGo.addEventListener("click", () => {
    const v = input.value;
    if (!v) {
      outArgon.textContent = "(type something first)";
      return;
    }
    outArgon.textContent = "computing…";
    // Defer one frame so the "computing…" state is painted before the
    // synchronous Argon2 work starts blocking the main thread.
    requestAnimationFrame(() => {
      try {
        outArgon.textContent = argon2id_phc(v);
      } catch (e) {
        outArgon.textContent = `error: ${e}`;
      }
    });
  });

  refreshFast();
}

boot().catch((e) => {
  // Build the error node with textContent so the exception message can never
  // be interpreted as HTML (js/xss-through-exception).
  const p = document.createElement("p");
  p.setAttribute("role", "alert");
  p.style.color = "#c00";
  p.textContent = "Failed to boot WASM module: " + (e && e.message ? e.message : e);
  document.body.appendChild(p);
});
