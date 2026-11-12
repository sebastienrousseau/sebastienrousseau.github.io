// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// /tools/ page wiring for the three browser tools. Everything runs here, in
// the reader's browser: nothing pasted into these forms is sent anywhere.
// Results are written with textContent, never as HTML.

import { checkXml } from "./address-check.js";
import { identify } from "./message-id.js";
import { formatBytes, KEMS, kemOverhead, SIGNATURES, signatureOverhead } from "./pqc-sizes.js";

function list(out, items) {
  out.replaceChildren();
  const ul = document.createElement("ul");
  for (const text of items) {
    const li = document.createElement("li");
    li.textContent = text;
    ul.append(li);
  }
  out.append(ul);
}

function bind(formId, handler) {
  const form = document.getElementById(formId);
  if (!form) return;
  const out = form.querySelector("output");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    try {
      list(out, handler(new FormData(form)));
    } catch (err) {
      list(out, [String(err.message || err)]);
    }
  });
}

bind("tool-address", (data) => {
  const results = checkXml(String(data.get("xml") || ""));
  if (!results.length) return ["No <PstlAdr> block found. Paste a party element that contains one."];
  return results.flatMap((r) => [
    `${r.party}: ${r.format}${r.errors.length ? ", will be rejected" : ", passes"}`,
    ...r.errors.map((e) => `Error: ${e}`),
    ...r.warnings.map((w) => `Advice: ${w}`),
  ]);
});

bind("tool-message", (data) => {
  const found = identify(String(data.get("xml") || ""));
  if (!found.length) return ["No ISO 20022 message namespace found (urn:iso:std:iso:20022:tech:xsd:...)."];
  return found.map((m) => `${m.id}: ${m.message}, version ${m.version}, ${m.businessArea}`);
});

function fillSelect(id, names, chosen) {
  const select = document.getElementById(id);
  if (!select) return;
  for (const name of names) select.add(new Option(name, name, false, name === chosen));
}

fillSelect("pqc-from", Object.keys(SIGNATURES), "ECDSA P-256");
fillSelect("pqc-to", Object.keys(SIGNATURES), "ML-DSA-44");
fillSelect("kem-from", Object.keys(KEMS), "X25519");
fillSelect("kem-to", Object.keys(KEMS), "ML-KEM-768");

bind("tool-pqc", (data) => {
  const volume = Number(data.get("volume"));
  const sig = signatureOverhead(String(data.get("from")), String(data.get("to")), volume);
  const kem = kemOverhead(String(data.get("kemFrom")), String(data.get("kemTo")));
  return [
    `Signature: ${formatBytes(sig.perMessage)} more per message, ${formatBytes(sig.perDay)} more per day at ${volume.toLocaleString("en-GB")} messages.`,
    `Key establishment: ${formatBytes(kem)} more per handshake (public key plus ciphertext).`,
  ];
});
