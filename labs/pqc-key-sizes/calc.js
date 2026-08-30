// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT

// PQC key-size estimator — vanilla ES module, no framework, no network.
// Sources:
//   FIPS 203 §4         — ML-KEM parameter sets
//   FIPS 204 §4         — ML-DSA parameter sets
//   NIST SP 800-57 Pt 1 — classical equivalent strengths
//   RFC 8446 §4.2.8     — TLS 1.3 key-share record framing
//
// Computation is a static lookup table — no math at runtime — because the
// FIPS parameter sets are fixed integers, not derived. Keeping them as a
// declarative table is easier to audit against the spec than a calculator.

const TLS_HANDSHAKE_BUDGET = 16384; // single TLS record max (RFC 8446)

const CLASSICAL = {
  kem: [
    { id: "rsa-2048",   label: "RSA-2048 (PKCS#1)",         pk: 256,  cat: 1, note: "Below NIST Cat 1 by 2030; deprecated for new key agreement." },
    { id: "rsa-3072",   label: "RSA-3072 (PKCS#1)",         pk: 384,  cat: 1, note: "NIST Cat 1 equivalent." },
    { id: "rsa-4096",   label: "RSA-4096 (PKCS#1)",         pk: 512,  cat: 2, note: "Between Cat 1 and Cat 3 — round up to Cat 3 for headroom." },
    { id: "ecdh-p256",  label: "ECDH P-256 (secp256r1)",    pk: 65,   cat: 1, note: "NIST Cat 1. The TLS 1.3 default for most stacks today." },
    { id: "ecdh-p384",  label: "ECDH P-384 (secp384r1)",    pk: 97,   cat: 3, note: "NIST Cat 3. Common in TLS 1.3 high-assurance profiles." },
    { id: "ecdh-p521",  label: "ECDH P-521 (secp521r1)",    pk: 133,  cat: 5, note: "NIST Cat 5. Rare outside compliance contexts." },
    { id: "x25519",     label: "X25519 (Curve25519)",       pk: 32,   cat: 1, note: "NIST Cat 1 equivalent. TLS 1.3 modern default." },
  ],
  sig: [
    { id: "rsa-2048",   label: "RSA-2048 PKCS#1 v1.5 / PSS",  pk: 256,  sig: 256,  cat: 1, note: "Below NIST Cat 1 by 2030." },
    { id: "rsa-3072",   label: "RSA-3072 PSS",                pk: 384,  sig: 384,  cat: 1, note: "NIST Cat 1 equivalent." },
    { id: "rsa-4096",   label: "RSA-4096 PSS",                pk: 512,  sig: 512,  cat: 2, note: "Between Cat 1 and Cat 3." },
    { id: "ecdsa-p256", label: "ECDSA P-256 (secp256r1)",     pk: 65,   sig: 72,   cat: 1, note: "TLS 1.3 default sig scheme." },
    { id: "ecdsa-p384", label: "ECDSA P-384 (secp384r1)",     pk: 97,   sig: 104,  cat: 3, note: "NIST Cat 3." },
    { id: "ecdsa-p521", label: "ECDSA P-521 (secp521r1)",     pk: 133,  sig: 139,  cat: 5, note: "NIST Cat 5." },
    { id: "ed25519",    label: "Ed25519 (EdDSA)",             pk: 32,   sig: 64,   cat: 1, note: "NIST Cat 1. Modern TLS / SSH / code-signing default." },
  ],
};

// FIPS 203 Table 2 (ML-KEM) and FIPS 204 Table 2 (ML-DSA).
const PQC = {
  kem: {
    1: { name: "ML-KEM-512",  fips: "FIPS 203 §4 (Table 2)", pk: 800,  ct: 768,  sk: 1632 },
    3: { name: "ML-KEM-768",  fips: "FIPS 203 §4 (Table 2)", pk: 1184, ct: 1088, sk: 2400 },
    5: { name: "ML-KEM-1024", fips: "FIPS 203 §4 (Table 2)", pk: 1568, ct: 1568, sk: 3168 },
  },
  sig: {
    1: { name: "ML-DSA-44",   fips: "FIPS 204 §4 (Table 2)", pk: 1312, sig: 2420, sk: 2560 },
    3: { name: "ML-DSA-65",   fips: "FIPS 204 §4 (Table 2)", pk: 1952, sig: 3309, sk: 4032 },
    5: { name: "ML-DSA-87",   fips: "FIPS 204 §4 (Table 2)", pk: 2592, sig: 4627, sk: 4896 },
  },
};

const CAT_LABEL = {
  1: "Cat 1 (≈ AES-128)",
  2: "Cat 2 (≈ SHA-256 collision)",
  3: "Cat 3 (≈ AES-192)",
  4: "Cat 4 (≈ SHA-384 collision)",
  5: "Cat 5 (≈ AES-256)",
};

const $ = (id) => document.getElementById(id);

function populateClassical(use) {
  const sel = $("classical");
  sel.replaceChildren();
  for (const c of CLASSICAL[use]) {
    const opt = document.createElement("option");
    opt.value = c.id;
    opt.textContent = c.label;
    sel.appendChild(opt);
  }
  sel.value = use === "kem" ? "ecdh-p256" : "ed25519";
}

function fmt(n) {
  if (n >= 1024) return `${(n / 1024).toFixed(2)} KiB (${n.toLocaleString()} B)`;
  return `${n.toLocaleString()} B`;
}

function pctDelta(pqc, classical) {
  if (classical === 0) return "—";
  const d = ((pqc - classical) / classical) * 100;
  const sign = d >= 0 ? "+" : "";
  return `${sign}${d.toFixed(0)}% vs classical`;
}

function calloutFor(use, pqc, classical) {
  const classicalWire = classical.pk + (use === "sig" ? classical.sig : classical.pk);
  const pqcWire = pqc.pk + (use === "sig" ? pqc.sig : pqc.ct);

  if (pqcWire > TLS_HANDSHAKE_BUDGET / 2) {
    return {
      warn: true,
      text: `Heads-up: combined PQC bytes (${fmt(pqcWire)}) exceed half the TLS record budget (${fmt(TLS_HANDSHAKE_BUDGET)}). ClientHello fragmentation across IP packets becomes likely — test for middlebox interop before deployment.`,
    };
  }
  if (pqcWire > classicalWire * 8) {
    return {
      warn: false,
      text: `PQC inflates the on-wire payload ≈${Math.round(pqcWire / classicalWire)}× vs classical. Workable for TLS, but plan for revisiting any code that assumes ≤1 KB key blobs (firmware update channels, SMS-class payloads, QR codes).`,
    };
  }
  return {
    warn: false,
    text: `PQC inflates the on-wire payload ≈${Math.round(pqcWire / classicalWire)}× vs classical. Within the TLS handshake budget; deploy with hybrid (classical + PQC) during transition.`,
  };
}

function render() {
  const use = document.querySelector('input[name="use"]:checked').value;
  const classicalId = $("classical").value;
  const classical = CLASSICAL[use].find((c) => c.id === classicalId);
  if (!classical) return;

  const cat = Math.min(5, Math.max(1, classical.cat === 2 ? 3 : classical.cat === 4 ? 5 : classical.cat));
  const pqc = PQC[use][cat];

  $("classical-hint").textContent = classical.note;

  $("r-cat").textContent = CAT_LABEL[cat];
  $("r-alg").textContent = pqc.name;
  $("r-fips").textContent = pqc.fips;
  $("r-pk").textContent = fmt(pqc.pk);

  const row = $("r-secret-row");
  const secretCell = $("r-secret");
  if (use === "kem") {
    row.querySelector("th").textContent = "Ciphertext (encapsulation output)";
    secretCell.textContent = fmt(pqc.ct);
  } else {
    row.querySelector("th").textContent = "Signature";
    secretCell.textContent = `${fmt(pqc.sig)} — ${pctDelta(pqc.sig, classical.sig)}`;
  }

  $("r-classical").textContent =
    use === "kem"
      ? `${classical.label}: PK ${fmt(classical.pk)}`
      : `${classical.label}: PK ${fmt(classical.pk)}, sig ${fmt(classical.sig)}`;

  const classicalWire = classical.pk + (use === "sig" ? classical.sig : classical.pk);
  const pqcWire = pqc.pk + (use === "sig" ? pqc.sig : pqc.ct);
  $("r-delta").textContent = `${fmt(pqcWire - classicalWire)} more on the wire (${pctDelta(pqcWire, classicalWire)})`;

  const c = calloutFor(use, pqc, classical);
  const cBox = $("callout");
  cBox.textContent = c.text;
  cBox.classList.toggle("warn", c.warn);
}

document.querySelectorAll('input[name="use"]').forEach((el) =>
  el.addEventListener("change", () => {
    populateClassical(el.value);
    render();
  })
);
$("classical").addEventListener("change", render);

populateClassical("kem");
render();
