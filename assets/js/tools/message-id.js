// SPDX-FileCopyrightText: 2007-2026 Sebastien Rousseau
// SPDX-License-Identifier: Apache-2.0 OR MIT
//
// ISO 20022 message identifier (plan G-4). Reads the message namespaces in
// pasted XML (urn:iso:std:iso:20022:tech:xsd:<area>.<msg>.<variant>.<version>)
// and names the message, version and business area. Runs in the browser
// only; no data leaves the page.

export const BUSINESS_AREAS = {
  acmt: "Account Management",
  admi: "Administration",
  auth: "Authorities",
  camt: "Cash Management",
  colr: "Collateral Management",
  head: "Business Application Header",
  pacs: "Payments Clearing and Settlement",
  pain: "Payments Initiation",
  reda: "Reference Data",
  remt: "Payments Remittance Advice",
  seev: "Securities Events",
  semt: "Securities Management",
  sese: "Securities Settlement",
  setr: "Securities Trade",
  trea: "Treasury",
  tsmt: "Trade Services Management",
};

const NS_RE = /urn:iso:std:iso:20022:tech:xsd:([a-z]{4})\.(\d{3})\.(\d{3})\.(\d{2})/g;

/** One entry per distinct ISO 20022 message namespace in the XML. */
export function identify(xml) {
  const seen = new Map();
  for (const m of xml.matchAll(NS_RE)) {
    const [, area, msg, variant, version] = m;
    const id = `${area}.${msg}.${variant}.${version}`;
    if (!seen.has(id)) {
      seen.set(id, {
        id,
        message: `${area}.${msg}`,
        version: Number(version),
        area,
        businessArea: BUSINESS_AREAS[area] || "Unknown business area",
      });
    }
  }
  return [...seen.values()];
}
