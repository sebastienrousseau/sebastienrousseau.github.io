// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// The three browser tools (plan G-4): at least 10 fixtures each.

import assert from "node:assert/strict";
import { test } from "node:test";

import { addresses, checkAddress, checkXml } from "../../../assets/js/tools/address-check.js";
import { BUSINESS_AREAS, identify } from "../../../assets/js/tools/message-id.js";
import { formatBytes, KEMS, kemOverhead, SIGNATURES, signatureOverhead } from "../../../assets/js/tools/pqc-sizes.js";

const party = (inner, tag = "Cdtr") => `<${tag}><Nm>ACME</Nm><PstlAdr>${inner}</PstlAdr></${tag}>`;

const ADDRESS_FIXTURES = [
  ["fully structured", party("<StrtNm>High St</StrtNm><BldgNb>1</BldgNb><TwnNm>London</TwnNm><Ctry>GB</Ctry>"), "structured", 0, 0],
  ["hybrid, two lines", party("<TwnNm>Paris</TwnNm><Ctry>FR</Ctry><AdrLine>Bat A</AdrLine><AdrLine>Etage 3</AdrLine>"), "hybrid", 0, 2],
  ["hybrid, three lines", party("<TwnNm>Paris</TwnNm><Ctry>FR</Ctry><AdrLine>a</AdrLine><AdrLine>b</AdrLine><AdrLine>c</AdrLine>"), "hybrid", 1, 2],
  ["unstructured only", party("<AdrLine>1 High St</AdrLine><AdrLine>London GB</AdrLine>"), "unstructured", 2, 2],
  ["missing country", party("<StrtNm>A</StrtNm><BldgNb>1</BldgNb><TwnNm>Berlin</TwnNm>"), "unstructured", 1, 0],
  ["missing town", party("<StrtNm>A</StrtNm><BldgNb>1</BldgNb><Ctry>DE</Ctry>"), "unstructured", 1, 0],
  ["bad country code", party("<StrtNm>A</StrtNm><PstBx>9</PstBx><TwnNm>Rome</TwnNm><Ctry>Italy</Ctry>"), "structured", 1, 0],
  ["town repeated in a line", party("<StrtNm>A</StrtNm><BldgNb>1</BldgNb><TwnNm>Madrid</TwnNm><Ctry>ES</Ctry><AdrLine>Centro, Madrid</AdrLine>"), "hybrid", 0, 1],
  ["postcode repeated", party("<StrtNm>A</StrtNm><BldgNb>1</BldgNb><PstCd>1012</PstCd><TwnNm>Amsterdam</TwnNm><Ctry>NL</Ctry><AdrLine>1012 AB</AdrLine>"), "hybrid", 0, 1],
  ["PO box instead of building", party("<StrtNm>A</StrtNm><PstBx>12</PstBx><TwnNm>Oslo</TwnNm><Ctry>NO</Ctry>"), "structured", 0, 0],
  ["namespace prefixes", '<doc:Dbtr><doc:Nm>X</doc:Nm><doc:PstlAdr><doc:TwnNm>Lyon</doc:TwnNm><doc:Ctry>FR</doc:Ctry></doc:PstlAdr></doc:Dbtr>', "structured", 0, 2],
];

for (const [name, xml, format, errors, warnings] of ADDRESS_FIXTURES) {
  test(`address: ${name}`, () => {
    const [result] = checkXml(xml);
    assert.equal(result.format, format);
    assert.equal(result.errors.length, errors, JSON.stringify(result.errors));
    assert.equal(result.warnings.length, warnings, JSON.stringify(result.warnings));
  });
}

test("address: every party in a message is checked", () => {
  const xml = party("<TwnNm>A</TwnNm><Ctry>GB</Ctry>", "Dbtr") + party("<AdrLine>x</AdrLine>", "Cdtr");
  const found = addresses(xml);
  assert.deepEqual(found.map((a) => a.party), ["Dbtr", "Cdtr"]);
  assert.equal(checkXml("<Document/>").length, 0);
  assert.equal(checkAddress({ fields: { TwnNm: "A", Ctry: "GB", StrtNm: "", BldgNb: "", PstBx: "", PstCd: "" }, lines: [] }).format, "structured");
});

const NS = (id) => `<Document xmlns="urn:iso:std:iso:20022:tech:xsd:${id}">`;
const MESSAGE_FIXTURES = [
  ["pacs.008.001.08", "Payments Clearing and Settlement", 8],
  ["pacs.009.001.08", "Payments Clearing and Settlement", 8],
  ["pacs.004.001.09", "Payments Clearing and Settlement", 9],
  ["pacs.002.001.10", "Payments Clearing and Settlement", 10],
  ["pain.001.001.09", "Payments Initiation", 9],
  ["pain.002.001.10", "Payments Initiation", 10],
  ["camt.052.001.08", "Cash Management", 8],
  ["camt.053.001.08", "Cash Management", 8],
  ["camt.054.001.08", "Cash Management", 8],
  ["camt.056.001.08", "Cash Management", 8],
  ["camt.029.001.09", "Cash Management", 9],
  ["xxxx.001.001.01", "Unknown business area", 1],
];

for (const [id, area, version] of MESSAGE_FIXTURES) {
  test(`message id: ${id}`, () => {
    const [m] = identify(`${NS(id)}<x/></Document>`);
    assert.equal(m.id, id);
    assert.equal(m.businessArea, area);
    assert.equal(m.version, version);
    assert.equal(m.message, id.slice(0, 8));
  });
}

test("message id: header and document, duplicates collapsed, none found", () => {
  const xml = '<AppHdr xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.02"/>' + NS("pacs.008.001.08") + NS("pacs.008.001.08");
  assert.deepEqual(identify(xml).map((m) => m.id), ["head.001.001.02", "pacs.008.001.08"]);
  assert.deepEqual(identify("<Document/>"), []);
  assert.equal(BUSINESS_AREAS.head, "Business Application Header");
});

const SIZE_FIXTURES = [
  ["ML-KEM-512", KEMS, "ciphertext", 768],
  ["ML-KEM-768", KEMS, "publicKey", 1184],
  ["ML-KEM-1024", KEMS, "ciphertext", 1568],
  ["ML-DSA-44", SIGNATURES, "signature", 2420],
  ["ML-DSA-65", SIGNATURES, "signature", 3309],
  ["ML-DSA-87", SIGNATURES, "publicKey", 2592],
  ["RSA-2048", SIGNATURES, "signature", 256],
  ["RSA-3072", SIGNATURES, "signature", 384],
  ["ECDSA P-256", SIGNATURES, "signature", 64],
  ["X25519", KEMS, "publicKey", 32],
];

for (const [name, table, field, bytes] of SIZE_FIXTURES) {
  test(`pqc size: ${name} ${field}`, () => assert.equal(table[name][field], bytes));
}

test("pqc overheads and formatting", () => {
  assert.deepEqual(signatureOverhead("ECDSA P-256", "ML-DSA-44", 1000), { perMessage: 2356, perDay: 2356000 });
  assert.equal(kemOverhead("X25519", "ML-KEM-768"), 1184 + 1088 - 64);
  assert.throws(() => signatureOverhead("RSA-1", "ML-DSA-44", 1), /unknown signature scheme: RSA-1/);
  assert.throws(() => signatureOverhead("RSA-2048", "nope", 1), /unknown signature scheme: nope/);
  assert.throws(() => signatureOverhead("RSA-2048", "ML-DSA-44", -1), /non-negative/);
  assert.throws(() => kemOverhead("X25519", "nope"), /unknown key-establishment scheme: nope/);
  assert.throws(() => kemOverhead("nope", "X25519"), /unknown key-establishment scheme: nope/);
  assert.equal(formatBytes(512), "512 B");
  assert.equal(formatBytes(4627), "4.5 KB");
  assert.equal(formatBytes(3 * 1024 ** 2), "3.0 MB");
  assert.equal(formatBytes(2 * 1024 ** 3), "2.0 GB");
});
