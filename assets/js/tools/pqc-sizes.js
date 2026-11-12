// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// PQC sizing calculator (plan G-4). Sizes in bytes.
//   ML-KEM: NIST FIPS 203, section 8, Table 3 (encapsulation key,
//           decapsulation key, ciphertext; shared secret 32 bytes).
//   ML-DSA: NIST FIPS 204, section 4, Table 2 (public key, private key,
//           signature).
//   RSA: modulus-sized public key and signature (private keys vary with
//   encoding, so none is listed). ECDSA P-256: 64-byte raw
//   public key (x || y) and 64-byte raw signature (r || s); DER encoding
//   adds a few bytes. X25519: 32-byte public key.

export const KEMS = {
  "ML-KEM-512": { publicKey: 800, privateKey: 1632, ciphertext: 768 },
  "ML-KEM-768": { publicKey: 1184, privateKey: 2400, ciphertext: 1088 },
  "ML-KEM-1024": { publicKey: 1568, privateKey: 3168, ciphertext: 1568 },
  X25519: { publicKey: 32, privateKey: 32, ciphertext: 32 },
};

export const SIGNATURES = {
  "ML-DSA-44": { publicKey: 1312, privateKey: 2560, signature: 2420 },
  "ML-DSA-65": { publicKey: 1952, privateKey: 4032, signature: 3309 },
  "ML-DSA-87": { publicKey: 2592, privateKey: 4896, signature: 4627 },
  "RSA-2048": { publicKey: 256, signature: 256 },
  "RSA-3072": { publicKey: 384, signature: 384 },
  "ECDSA P-256": { publicKey: 64, privateKey: 32, signature: 64 },
};

/** Extra bytes when moving one signature per message from `from` to `to`. */
export function signatureOverhead(from, to, messagesPerDay) {
  const a = SIGNATURES[from];
  const b = SIGNATURES[to];
  if (!a || !b) throw new Error(`unknown signature scheme: ${a ? to : from}`);
  if (!Number.isFinite(messagesPerDay) || messagesPerDay < 0) throw new Error("messages per day must be a non-negative number");
  const perMessage = b.signature - a.signature;
  return { perMessage, perDay: perMessage * messagesPerDay };
}

/** Extra bytes per key exchange (one public key one way, one ciphertext back). */
export function kemOverhead(from, to) {
  const a = KEMS[from];
  const b = KEMS[to];
  if (!a || !b) throw new Error(`unknown key-establishment scheme: ${a ? to : from}`);
  return b.publicKey + b.ciphertext - (a.publicKey + a.ciphertext);
}

/** Human-readable size: 4627 -> "4.5 KB", 512 -> "512 B". */
export function formatBytes(n) {
  const abs = Math.abs(n);
  if (abs >= 1024 ** 3) return `${(n / 1024 ** 3).toFixed(1)} GB`;
  if (abs >= 1024 ** 2) return `${(n / 1024 ** 2).toFixed(1)} MB`;
  if (abs >= 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${n} B`;
}
