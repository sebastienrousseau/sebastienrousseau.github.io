// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// Structured-address checker (plan G-4). Runs in the browser only; no data
// leaves the page. Rules: the CBPR+ structured-address requirements set
// out in /2026-05-12-iso-20022-pacs008-structured-address-deadline/. Swift
// had planned to remove unstructured addresses in its November 2026
// release and delayed that release on 27 August 2026 (Bank of England,
// "Delay to the November 2026 RTGS standards release"); the rules below
// are the target format, whatever the final date:
//   - TwnNm and Ctry are mandatory in their structured elements;
//   - Ctry is an ISO 3166-1 alpha-2 code;
//   - hybrid addresses may add at most two AdrLine elements;
//   - an address held only in AdrLine (no TwnNm or Ctry) is rejected;
//   - structured values must not be repeated inside AdrLine;
//   - StrtNm, and BldgNb or PstBx, are strongly recommended.

const FIELDS = ["StrtNm", "BldgNb", "BldgNm", "PstBx", "PstCd", "TwnNm", "CtrySubDvsn", "Ctry"];

function texts(block, tag) {
  const re = new RegExp(`<(?:[\\w-]+:)?${tag}>([^<]*)</(?:[\\w-]+:)?${tag}>`, "g");
  return [...block.matchAll(re)].map((m) => m[1].trim());
}

function containsWord(line, value) {
  const escaped = value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(^|[^\\p{L}\\p{N}])${escaped}($|[^\\p{L}\\p{N}])`, "iu").test(line);
}

/** Every <PstlAdr> block in an XML fragment, with its party element name. */
export function addresses(xml) {
  const re = /<(?:[\w-]+:)?(\w+)>\s*(?:<(?:[\w-]+:)?Nm>[^<]*<\/(?:[\w-]+:)?Nm>\s*)?<(?:[\w-]+:)?PstlAdr>([\s\S]*?)<\/(?:[\w-]+:)?PstlAdr>/g;
  return [...xml.matchAll(re)].map((m) => {
    const fields = {};
    for (const f of FIELDS) fields[f] = texts(m[2], f)[0] || "";
    return { party: m[1], fields, lines: texts(m[2], "AdrLine") };
  });
}

/** Check one address. Returns {format, errors[], warnings[]}. */
export function checkAddress({ fields, lines }) {
  const errors = [];
  const warnings = [];
  const structured = Boolean(fields.TwnNm && fields.Ctry);
  if (!fields.TwnNm) errors.push("Town name (TwnNm) is missing: the structured format requires it.");
  if (!fields.Ctry) errors.push("Country (Ctry) is missing: the structured format requires it.");
  else if (!/^[A-Z]{2}$/.test(fields.Ctry)) errors.push(`Country "${fields.Ctry}" is not an ISO 3166-1 alpha-2 code (two capital letters).`);
  if (lines.length > 2) errors.push(`${lines.length} address lines (AdrLine): a hybrid address may carry at most two.`);
  for (const f of ["TwnNm", "PstCd", "StrtNm"]) {
    const v = fields[f];
    if (v && lines.some((l) => containsWord(l, v))) {
      warnings.push(`${f} "${v}" is repeated inside an address line; structured values must not be duplicated there.`);
    }
  }
  if (!fields.StrtNm) warnings.push("Street name (StrtNm) is strongly recommended.");
  if (!fields.BldgNb && !fields.PstBx) warnings.push("Building number (BldgNb) or PO box (PstBx) is strongly recommended.");
  let format = "unstructured";
  if (structured) format = lines.length ? "hybrid" : "structured";
  return { format, errors, warnings };
}

/** Check every address in a fragment. */
export function checkXml(xml) {
  const found = addresses(xml);
  return found.map((a) => ({ party: a.party, ...checkAddress(a) }));
}
