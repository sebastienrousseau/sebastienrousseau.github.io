<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Reviewing translations

The site's translations were drafted by machine. A native reviewer turns
them into text a reader in that language would trust. One CSV per locale:

```
python3 scripts/i18n/review_sheet.py export --lang de --out review/de.csv
# the reviewer fills approved_text (and reviewer, notes)
python3 scripts/i18n/review_sheet.py import review/de.csv
```

Columns: `file, key, english, draft, approved_text, reviewer, notes`. Fill
`approved_text` only for rows you have checked; leave it empty to skip a
row. For patches, `english` is the pattern the page is matched on (a regular
expression: `\.` is a full stop, `(?:a|b)` means either); translate the
visible words and keep any HTML in `draft` exactly as it is.

## What to check

- **Terminology:** the glossary below, and the terms already used on the
  site in that language.
- **Tone:** plain, direct, professional; the site writes for bank and
  fintech practitioners, not for a general audience.
- **Numbers, dates and units:** as in the English, in the locale's format.
- **Names stay as they are:** people, organisations, products and standard
  identifiers are never translated (HSBC, EPAA, ISO 20022, pacs.008).
- **No machine artefacts:** no left-over English, no doubled words, no
  literal translations of idioms, no em dashes.

## Glossary

| English | Keep in English? | Note |
| --- | --- | --- |
| ISO 20022 | Yes | The messaging standard |
| pacs.008, pain.001, camt.053 | Yes | Message identifiers |
| post-quantum cryptography | No | The locale's established term |
| ML-KEM, ML-DSA, FIPS 203 | Yes | Algorithm and standard names |
| wholesale payments | No | Bank-to-bank and corporate payments |
| cross-border payments | No | |
| instant payments | No | |
| open source | Usually | Use the locale's usual form |
| agentic AI | No | The locale's established term, if any |
| harvest now, decrypt later | No | Translate the idea; keep the English in brackets once |

Product names (ISO 20022 MCP suite, KyberLib, Banking On Quantum) stay in
English.

`tests/validation/test_i18n_review_state.py` fails when a string exported
for review stays unreviewed for more than 60 days.
