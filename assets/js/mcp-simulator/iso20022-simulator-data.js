// ISO 20022 MCP simulator data module. GENERATED from real captured MCP
// stdio transcripts; do not hand-edit the args/result payloads.
//
// Every scenario's `args` object is the exact `tools/call` arguments sent to
// a live server, and every `result.text` is the exact XML (or the exact
// all-at-once validation error) that server returned:
//
//   - iso20022-mcp 0.0.4 gateway   (uvx --from "iso20022-mcp[all]==0.0.4" iso20022-mcp)
//   - camt-exceptions 0.0.14       (uvx --from "camt-exceptions" camt-exceptions-mcp)
//
// Captured 2026-07-16 over stdio JSON-RPC (initialize / tools/call), protocol
// 2024-11-05. The component renders this data verbatim and never touches the
// network; the page's strict CSP would block it if it tried.
//
// Editorial fields (sentence, label, note, mappings) are authored, but each
// mapping's `phrase` is a literal substring of its scenario sentence and each
// entry in `marks` a literal substring of the captured result text - the
// bake script (and the unit tests) assert this, so a highlight can never
// point at something the server did not actually return.
export const SIMULATOR_DATA = {
  "capture": {
    "date": "2026-07-16",
    "method": "MCP stdio JSON-RPC tools/call (protocol 2024-11-05)",
    "servers": [
      {
        "name": "iso20022",
        "version": "0.0.4",
        "command": "uvx --from \"iso20022-mcp[all]==0.0.4\" iso20022-mcp"
      },
      {
        "name": "camt-exceptions",
        "version": "0.0.14",
        "command": "uvx --from \"camt-exceptions\" camt-exceptions-mcp"
      }
    ]
  },
  "scenarios": [
    {
      "id": "pay-supplier",
      "label": "Pay a supplier",
      "sentence": "Pay Fournier Conseil SARL 4,200 euros for invoice INV-2026-183, executing Friday.",
      "note": "A single SEPA credit transfer. The gateway validated the XML against the official pain.001.001.03 XSD before returning it.",
      "server": {
        "name": "iso20022",
        "version": "0.0.4",
        "command": "uvx --from \"iso20022-mcp[all]==0.0.4\" iso20022-mcp"
      },
      "tool": "generate",
      "args": {
        "message_type": "pain.001.001.03",
        "records": [
          {
            "id": "MSG-2026-07-16-001",
            "date": "2026-07-16T09:30:00",
            "initiator_name": "Acme Treasury GmbH",
            "initiator_street_name": "Mainzer Landstrasse",
            "initiator_building_number": "50",
            "initiator_postal_code": "60325",
            "initiator_town_name": "Frankfurt am Main",
            "initiator_country_code": "DE",
            "payment_information_id": "PMT-2026-07-16-001",
            "payment_method": "TRF",
            "batch_booking": false,
            "service_level_code": "SEPA",
            "requested_execution_date": "2026-07-17",
            "debtor_name": "Acme Treasury GmbH",
            "debtor_street_name": "Mainzer Landstrasse",
            "debtor_building_number": "50",
            "debtor_postal_code": "60325",
            "debtor_town_name": "Frankfurt am Main",
            "debtor_country_code": "DE",
            "debtor_account_IBAN": "DE89370400440532013000",
            "debtor_agent_BIC": "COBADEFFXXX",
            "payment_id": "TXN-2026-07-16-001",
            "payment_amount": "4200.00",
            "currency": "EUR",
            "charge_bearer": "SLEV",
            "creditor_name": "Fournier Conseil SARL",
            "creditor_street_name": "Rue du Faubourg Saint-Honore",
            "creditor_building_number": "8",
            "creditor_postal_code": "75008",
            "creditor_town_name": "Paris",
            "creditor_country_code": "FR",
            "creditor_account_IBAN": "FR1420041010050500013M02606",
            "creditor_agent_BIC": "BNPAFRPP",
            "purpose_code": "SUPP",
            "remittance_information": "INV-2026-183 dated 2026-07-01",
            "reference_number": "INV-2026-183",
            "reference_date": "2026-07-01"
          }
        ]
      },
      "result": {
        "kind": "xml",
        "messageType": "pain.001.001.03",
        "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Document xmlns=\"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03\"\n    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n    xsi:schemaLocation=\"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03 pain.001.001.03.xsd\">\n    <CstmrCdtTrfInitn>\n        <GrpHdr>\n            <MsgId>MSG-2026-07-16-001</MsgId>\n            <CreDtTm>2026-07-16T09:30:00</CreDtTm>\n            <NbOfTxs>1</NbOfTxs>\n            <InitgPty>\n                <Nm>Acme Treasury GmbH</Nm>\n                <PstlAdr>\n                    <StrtNm>Mainzer Landstrasse</StrtNm>\n                    <BldgNb>50</BldgNb>\n                    <PstCd>60325</PstCd>\n                    <TwnNm>Frankfurt am Main</TwnNm>\n                    <Ctry>DE</Ctry>\n                </PstlAdr>\n            </InitgPty>\n        </GrpHdr>\n        <PmtInf>\n            <PmtInfId>TXN-2026-07-16-001</PmtInfId>\n            <PmtMtd>TRF</PmtMtd>\n            <BtchBookg>\n            false</BtchBookg>\n            <ReqdExctnDt>2026-07-17</ReqdExctnDt>\n            <Dbtr>\n                <Nm>Acme Treasury GmbH</Nm>\n                <PstlAdr>\n                    <StrtNm>Mainzer Landstrasse</StrtNm>\n                    <BldgNb>50</BldgNb>\n                    <PstCd>60325</PstCd>\n                    <TwnNm>Frankfurt am Main</TwnNm>\n                    <Ctry>DE</Ctry>\n                </PstlAdr>\n            </Dbtr>\n            <DbtrAcct>\n                <Id>\n                    <Othr>\n                        <Id>DE89370400440532013000</Id>\n                    </Othr>\n                </Id>\n            </DbtrAcct>\n            <DbtrAgt>\n                <FinInstnId>\n                    <BIC>COBADEFFXXX</BIC>\n                </FinInstnId>\n            </DbtrAgt>\n            <CdtTrfTxInf>\n                <PmtId>\n                    <InstrId>TX-1</InstrId>\n                    <EndToEndId>TXN-2026-07-16-001</EndToEndId>\n                </PmtId>\n                <Amt>\n                    <InstdAmt Ccy=\"EUR\">4200.00</InstdAmt>\n                </Amt>\n                <ChrgBr>SLEV</ChrgBr>\n                <CdtrAgt>\n                    <FinInstnId>\n                        <BIC>BNPAFRPP</BIC>\n                    </FinInstnId>\n                </CdtrAgt>\n                <Cdtr>\n                    <Nm>Fournier Conseil SARL</Nm>\n                    <PstlAdr>\n                        <AdrLine>Rue du Faubourg Saint-Honore</AdrLine>\n                        <AdrLine>8</AdrLine>\n                        <AdrLine>75008</AdrLine>\n                        <AdrLine>Paris</AdrLine>\n                        <AdrLine>FR</AdrLine>\n                    </PstlAdr>\n                </Cdtr>\n                <CdtrAcct>\n                    <Id>\n                        <Othr>\n                            <Id>FR1420041010050500013M02606</Id>\n                        </Othr>\n                    </Id>\n                </CdtrAcct>\n                <Purp>\n                    <Cd>SUPP</Cd>\n                </Purp>\n                <RmtInf>\n                    <Strd>\n                        <RfrdDocInf>\n                            <Nb>INV-2026-183</Nb>\n                            <RltdDt>2026-07-01</RltdDt>\n                        </RfrdDocInf>\n                    </Strd>\n                </RmtInf>\n            </CdtTrfTxInf>\n            </PmtInf>\n    </CstmrCdtTrfInitn>\n</Document>"
      },
      "mappings": [
        {
          "id": "creditor",
          "phrase": "Fournier Conseil SARL",
          "label": "Creditor name: Cdtr/Nm",
          "marks": [
            "<Nm>Fournier Conseil SARL</Nm>"
          ]
        },
        {
          "id": "amount",
          "phrase": "4,200 euros",
          "label": "Instructed amount and currency: InstdAmt",
          "marks": [
            "<InstdAmt Ccy=\"EUR\">4200.00</InstdAmt>"
          ]
        },
        {
          "id": "invoice",
          "phrase": "invoice INV-2026-183",
          "label": "Structured remittance reference: RmtInf/Strd",
          "marks": [
            "<Nb>INV-2026-183</Nb>"
          ]
        },
        {
          "id": "when",
          "phrase": "executing Friday",
          "label": "Requested execution date: ReqdExctnDt",
          "marks": [
            "<ReqdExctnDt>2026-07-17</ReqdExctnDt>"
          ]
        }
      ]
    },
    {
      "id": "urgent-gbp",
      "label": "Urgent transfer",
      "sentence": "Send 12,500 pounds to Harrogate Data Ltd for the July consulting statement, urgent.",
      "note": "Same tool, different rails: a GBP transfer flagged urgent through the URGP service level.",
      "server": {
        "name": "iso20022",
        "version": "0.0.4",
        "command": "uvx --from \"iso20022-mcp[all]==0.0.4\" iso20022-mcp"
      },
      "tool": "generate",
      "args": {
        "message_type": "pain.001.001.03",
        "records": [
          {
            "id": "MSG-2026-07-16-002",
            "date": "2026-07-16T11:15:00",
            "initiator_name": "Acme Treasury GmbH",
            "initiator_street_name": "Mainzer Landstrasse",
            "initiator_building_number": "50",
            "initiator_postal_code": "60325",
            "initiator_town_name": "Frankfurt am Main",
            "initiator_country_code": "DE",
            "payment_information_id": "PMT-2026-07-16-002",
            "payment_method": "TRF",
            "batch_booking": false,
            "service_level_code": "URGP",
            "requested_execution_date": "2026-07-17",
            "debtor_name": "Acme Treasury GmbH",
            "debtor_street_name": "Mainzer Landstrasse",
            "debtor_building_number": "50",
            "debtor_postal_code": "60325",
            "debtor_town_name": "Frankfurt am Main",
            "debtor_country_code": "DE",
            "debtor_account_IBAN": "DE89370400440532013000",
            "debtor_agent_BIC": "COBADEFFXXX",
            "payment_id": "TXN-2026-07-16-002",
            "payment_amount": "12500.00",
            "currency": "GBP",
            "charge_bearer": "SHAR",
            "creditor_name": "Harrogate Data Ltd",
            "creditor_street_name": "Station Parade",
            "creditor_building_number": "23",
            "creditor_postal_code": "HG1 1UF",
            "creditor_town_name": "Harrogate",
            "creditor_country_code": "GB",
            "creditor_account_IBAN": "GB29NWBK60161331926819",
            "creditor_agent_BIC": "NWBKGB2LXXX",
            "purpose_code": "SCVE",
            "remittance_information": "July 2026 consulting statement",
            "reference_number": "CONS-2026-07",
            "reference_date": "2026-07-15"
          }
        ]
      },
      "result": {
        "kind": "xml",
        "messageType": "pain.001.001.03",
        "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Document xmlns=\"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03\"\n    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n    xsi:schemaLocation=\"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03 pain.001.001.03.xsd\">\n    <CstmrCdtTrfInitn>\n        <GrpHdr>\n            <MsgId>MSG-2026-07-16-002</MsgId>\n            <CreDtTm>2026-07-16T11:15:00</CreDtTm>\n            <NbOfTxs>1</NbOfTxs>\n            <InitgPty>\n                <Nm>Acme Treasury GmbH</Nm>\n                <PstlAdr>\n                    <StrtNm>Mainzer Landstrasse</StrtNm>\n                    <BldgNb>50</BldgNb>\n                    <PstCd>60325</PstCd>\n                    <TwnNm>Frankfurt am Main</TwnNm>\n                    <Ctry>DE</Ctry>\n                </PstlAdr>\n            </InitgPty>\n        </GrpHdr>\n        <PmtInf>\n            <PmtInfId>TXN-2026-07-16-002</PmtInfId>\n            <PmtMtd>TRF</PmtMtd>\n            <BtchBookg>\n            false</BtchBookg>\n            <ReqdExctnDt>2026-07-17</ReqdExctnDt>\n            <Dbtr>\n                <Nm>Acme Treasury GmbH</Nm>\n                <PstlAdr>\n                    <StrtNm>Mainzer Landstrasse</StrtNm>\n                    <BldgNb>50</BldgNb>\n                    <PstCd>60325</PstCd>\n                    <TwnNm>Frankfurt am Main</TwnNm>\n                    <Ctry>DE</Ctry>\n                </PstlAdr>\n            </Dbtr>\n            <DbtrAcct>\n                <Id>\n                    <Othr>\n                        <Id>DE89370400440532013000</Id>\n                    </Othr>\n                </Id>\n            </DbtrAcct>\n            <DbtrAgt>\n                <FinInstnId>\n                    <BIC>COBADEFFXXX</BIC>\n                </FinInstnId>\n            </DbtrAgt>\n            <CdtTrfTxInf>\n                <PmtId>\n                    <InstrId>TX-1</InstrId>\n                    <EndToEndId>TXN-2026-07-16-002</EndToEndId>\n                </PmtId>\n                <Amt>\n                    <InstdAmt Ccy=\"GBP\">12500.00</InstdAmt>\n                </Amt>\n                <ChrgBr>SHAR</ChrgBr>\n                <CdtrAgt>\n                    <FinInstnId>\n                        <BIC>NWBKGB2LXXX</BIC>\n                    </FinInstnId>\n                </CdtrAgt>\n                <Cdtr>\n                    <Nm>Harrogate Data Ltd</Nm>\n                    <PstlAdr>\n                        <AdrLine>Station Parade</AdrLine>\n                        <AdrLine>23</AdrLine>\n                        <AdrLine>HG1 1UF</AdrLine>\n                        <AdrLine>Harrogate</AdrLine>\n                        <AdrLine>GB</AdrLine>\n                    </PstlAdr>\n                </Cdtr>\n                <CdtrAcct>\n                    <Id>\n                        <Othr>\n                            <Id>GB29NWBK60161331926819</Id>\n                        </Othr>\n                    </Id>\n                </CdtrAcct>\n                <Purp>\n                    <Cd>SCVE</Cd>\n                </Purp>\n                <RmtInf>\n                    <Strd>\n                        <RfrdDocInf>\n                            <Nb>CONS-2026-07</Nb>\n                            <RltdDt>2026-07-15</RltdDt>\n                        </RfrdDocInf>\n                    </Strd>\n                </RmtInf>\n            </CdtTrfTxInf>\n            </PmtInf>\n    </CstmrCdtTrfInitn>\n</Document>"
      },
      "mappings": [
        {
          "id": "amount",
          "phrase": "12,500 pounds",
          "label": "Instructed amount and currency: InstdAmt",
          "marks": [
            "<InstdAmt Ccy=\"GBP\">12500.00</InstdAmt>"
          ]
        },
        {
          "id": "creditor",
          "phrase": "Harrogate Data Ltd",
          "label": "Creditor name: Cdtr/Nm",
          "marks": [
            "<Nm>Harrogate Data Ltd</Nm>"
          ]
        },
        {
          "id": "reference",
          "phrase": "July consulting statement",
          "label": "Remittance reference: RfrdDocInf/Nb",
          "marks": [
            "<Nb>CONS-2026-07</Nb>"
          ]
        },
        {
          "id": "urgency",
          "phrase": "urgent",
          "label": "Next-day execution requested: ReqdExctnDt",
          "marks": [
            "<ReqdExctnDt>2026-07-17</ReqdExctnDt>"
          ]
        }
      ]
    },
    {
      "id": "payroll-batch",
      "label": "Payroll batch",
      "sentence": "Run the two July salary payments to Elena Duarte and Tomas Keller as one batch on the 31st.",
      "note": "Two records, one message: the gateway computes NbOfTxs and control sums automatically.",
      "server": {
        "name": "iso20022",
        "version": "0.0.4",
        "command": "uvx --from \"iso20022-mcp[all]==0.0.4\" iso20022-mcp"
      },
      "tool": "generate",
      "args": {
        "message_type": "pain.001.001.03",
        "records": [
          {
            "id": "MSG-2026-07-16-003",
            "date": "2026-07-16T14:00:00",
            "initiator_name": "Acme Treasury GmbH",
            "initiator_street_name": "Mainzer Landstrasse",
            "initiator_building_number": "50",
            "initiator_postal_code": "60325",
            "initiator_town_name": "Frankfurt am Main",
            "initiator_country_code": "DE",
            "payment_information_id": "PMT-2026-07-16-003",
            "payment_method": "TRF",
            "batch_booking": true,
            "service_level_code": "SEPA",
            "requested_execution_date": "2026-07-31",
            "debtor_name": "Acme Treasury GmbH",
            "debtor_street_name": "Mainzer Landstrasse",
            "debtor_building_number": "50",
            "debtor_postal_code": "60325",
            "debtor_town_name": "Frankfurt am Main",
            "debtor_country_code": "DE",
            "debtor_account_IBAN": "DE89370400440532013000",
            "debtor_agent_BIC": "COBADEFFXXX",
            "payment_id": "SAL-2026-07-A",
            "payment_amount": "5850.00",
            "currency": "EUR",
            "charge_bearer": "SLEV",
            "creditor_name": "Elena Duarte",
            "creditor_street_name": "Rua Garrett",
            "creditor_building_number": "120",
            "creditor_postal_code": "1200-205",
            "creditor_town_name": "Lisboa",
            "creditor_country_code": "PT",
            "creditor_account_IBAN": "PT50000201231234567890154",
            "creditor_agent_BIC": "BPIPPTPL",
            "purpose_code": "SALA",
            "remittance_information": "July 2026 salary",
            "reference_number": "SAL-2026-07-A",
            "reference_date": "2026-07-31"
          },
          {
            "id": "MSG-2026-07-16-003",
            "date": "2026-07-16T14:00:00",
            "initiator_name": "Acme Treasury GmbH",
            "initiator_street_name": "Mainzer Landstrasse",
            "initiator_building_number": "50",
            "initiator_postal_code": "60325",
            "initiator_town_name": "Frankfurt am Main",
            "initiator_country_code": "DE",
            "payment_information_id": "PMT-2026-07-16-003",
            "payment_method": "TRF",
            "batch_booking": true,
            "service_level_code": "SEPA",
            "requested_execution_date": "2026-07-31",
            "debtor_name": "Acme Treasury GmbH",
            "debtor_street_name": "Mainzer Landstrasse",
            "debtor_building_number": "50",
            "debtor_postal_code": "60325",
            "debtor_town_name": "Frankfurt am Main",
            "debtor_country_code": "DE",
            "debtor_account_IBAN": "DE89370400440532013000",
            "debtor_agent_BIC": "COBADEFFXXX",
            "payment_id": "SAL-2026-07-B",
            "payment_amount": "6300.00",
            "currency": "EUR",
            "charge_bearer": "SLEV",
            "creditor_name": "Tomas Keller",
            "creditor_street_name": "Bahnhofstrasse",
            "creditor_building_number": "7",
            "creditor_postal_code": "8001",
            "creditor_town_name": "Zurich",
            "creditor_country_code": "CH",
            "creditor_account_IBAN": "CH9300762011623852957",
            "creditor_agent_BIC": "POFICHBEXXX",
            "purpose_code": "SALA",
            "remittance_information": "July 2026 salary",
            "reference_number": "SAL-2026-07-B",
            "reference_date": "2026-07-31"
          }
        ]
      },
      "result": {
        "kind": "xml",
        "messageType": "pain.001.001.03",
        "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Document xmlns=\"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03\"\n    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n    xsi:schemaLocation=\"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03 pain.001.001.03.xsd\">\n    <CstmrCdtTrfInitn>\n        <GrpHdr>\n            <MsgId>MSG-2026-07-16-003</MsgId>\n            <CreDtTm>2026-07-16T14:00:00</CreDtTm>\n            <NbOfTxs>2</NbOfTxs>\n            <InitgPty>\n                <Nm>Acme Treasury GmbH</Nm>\n                <PstlAdr>\n                    <StrtNm>Mainzer Landstrasse</StrtNm>\n                    <BldgNb>50</BldgNb>\n                    <PstCd>60325</PstCd>\n                    <TwnNm>Frankfurt am Main</TwnNm>\n                    <Ctry>DE</Ctry>\n                </PstlAdr>\n            </InitgPty>\n        </GrpHdr>\n        <PmtInf>\n            <PmtInfId>SAL-2026-07-A</PmtInfId>\n            <PmtMtd>TRF</PmtMtd>\n            <BtchBookg>\n            true</BtchBookg>\n            <ReqdExctnDt>2026-07-31</ReqdExctnDt>\n            <Dbtr>\n                <Nm>Acme Treasury GmbH</Nm>\n                <PstlAdr>\n                    <StrtNm>Mainzer Landstrasse</StrtNm>\n                    <BldgNb>50</BldgNb>\n                    <PstCd>60325</PstCd>\n                    <TwnNm>Frankfurt am Main</TwnNm>\n                    <Ctry>DE</Ctry>\n                </PstlAdr>\n            </Dbtr>\n            <DbtrAcct>\n                <Id>\n                    <Othr>\n                        <Id>DE89370400440532013000</Id>\n                    </Othr>\n                </Id>\n            </DbtrAcct>\n            <DbtrAgt>\n                <FinInstnId>\n                    <BIC>COBADEFFXXX</BIC>\n                </FinInstnId>\n            </DbtrAgt>\n            <CdtTrfTxInf>\n                <PmtId>\n                    <InstrId>TX-1</InstrId>\n                    <EndToEndId>SAL-2026-07-A</EndToEndId>\n                </PmtId>\n                <Amt>\n                    <InstdAmt Ccy=\"EUR\">5850.00</InstdAmt>\n                </Amt>\n                <ChrgBr>SLEV</ChrgBr>\n                <CdtrAgt>\n                    <FinInstnId>\n                        <BIC>BPIPPTPL</BIC>\n                    </FinInstnId>\n                </CdtrAgt>\n                <Cdtr>\n                    <Nm>Elena Duarte</Nm>\n                    <PstlAdr>\n                        <AdrLine>Rua Garrett</AdrLine>\n                        <AdrLine>120</AdrLine>\n                        <AdrLine>1200-205</AdrLine>\n                        <AdrLine>Lisboa</AdrLine>\n                        <AdrLine>PT</AdrLine>\n                    </PstlAdr>\n                </Cdtr>\n                <CdtrAcct>\n                    <Id>\n                        <Othr>\n                            <Id>PT50000201231234567890154</Id>\n                        </Othr>\n                    </Id>\n                </CdtrAcct>\n                <Purp>\n                    <Cd>SALA</Cd>\n                </Purp>\n                <RmtInf>\n                    <Strd>\n                        <RfrdDocInf>\n                            <Nb>SAL-2026-07-A</Nb>\n                            <RltdDt>2026-07-31</RltdDt>\n                        </RfrdDocInf>\n                    </Strd>\n                </RmtInf>\n            </CdtTrfTxInf>\n            <CdtTrfTxInf>\n                <PmtId>\n                    <InstrId>TX-2</InstrId>\n                    <EndToEndId>SAL-2026-07-B</EndToEndId>\n                </PmtId>\n                <Amt>\n                    <InstdAmt Ccy=\"EUR\">6300.00</InstdAmt>\n                </Amt>\n                <ChrgBr>SLEV</ChrgBr>\n                <CdtrAgt>\n                    <FinInstnId>\n                        <BIC>POFICHBEXXX</BIC>\n                    </FinInstnId>\n                </CdtrAgt>\n                <Cdtr>\n                    <Nm>Tomas Keller</Nm>\n                    <PstlAdr>\n                        <AdrLine>Bahnhofstrasse</AdrLine>\n                        <AdrLine>7</AdrLine>\n                        <AdrLine>8001</AdrLine>\n                        <AdrLine>Zurich</AdrLine>\n                        <AdrLine>CH</AdrLine>\n                    </PstlAdr>\n                </Cdtr>\n                <CdtrAcct>\n                    <Id>\n                        <Othr>\n                            <Id>CH9300762011623852957</Id>\n                        </Othr>\n                    </Id>\n                </CdtrAcct>\n                <Purp>\n                    <Cd>SALA</Cd>\n                </Purp>\n                <RmtInf>\n                    <Strd>\n                        <RfrdDocInf>\n                            <Nb>SAL-2026-07-B</Nb>\n                            <RltdDt>2026-07-31</RltdDt>\n                        </RfrdDocInf>\n                    </Strd>\n                </RmtInf>\n            </CdtTrfTxInf>\n            </PmtInf>\n    </CstmrCdtTrfInitn>\n</Document>"
      },
      "mappings": [
        {
          "id": "emp-a",
          "phrase": "Elena Duarte",
          "label": "First transaction creditor: Cdtr/Nm",
          "marks": [
            "<Nm>Elena Duarte</Nm>"
          ]
        },
        {
          "id": "emp-b",
          "phrase": "Tomas Keller",
          "label": "Second transaction creditor: Cdtr/Nm",
          "marks": [
            "<Nm>Tomas Keller</Nm>"
          ]
        },
        {
          "id": "batch",
          "phrase": "one batch",
          "label": "Batch booking, two transactions: BtchBookg + NbOfTxs",
          "marks": [
            "<NbOfTxs>2</NbOfTxs>"
          ]
        },
        {
          "id": "salary",
          "phrase": "salary payments",
          "label": "Purpose code: Purp/Cd SALA",
          "marks": [
            "<Cd>SALA</Cd>"
          ]
        },
        {
          "id": "when",
          "phrase": "on the 31st",
          "label": "Requested execution date: ReqdExctnDt",
          "marks": [
            "<ReqdExctnDt>2026-07-31</ReqdExctnDt>"
          ]
        }
      ]
    },
    {
      "id": "cancel-duplicate",
      "label": "Cancel a payment",
      "sentence": "Recall this morning's 4,200 euro payment to Fournier Conseil, it went out twice.",
      "note": "Exceptions and investigations: a camt.056 cancellation request from the camt-exceptions server, referencing the original pain.001 by message id.",
      "server": {
        "name": "camt-exceptions",
        "version": "0.0.14",
        "command": "uvx --from \"camt-exceptions\" camt-exceptions-mcp"
      },
      "tool": "generate_message",
      "args": {
        "message_type": "camt.056.001.12",
        "record": {
          "assignment_id": "CXL-2026-07-16-001",
          "assigner_agent_bic": "COBADEFFXXX",
          "assignee_agent_bic": "BNPAFRPP",
          "creation_date_time": "2026-07-16T10:05:00",
          "original_msg_id": "MSG-2026-07-16-001",
          "original_msg_nm_id": "pain.001.001.03",
          "original_creation_date_time": "2026-07-16T09:30:00",
          "transactions": [
            {
              "cancellation_id": "CXL-TXN-2026-07-16-001",
              "original_end_to_end_id": "TXN-2026-07-16-001",
              "original_interbank_settlement_amount": "4200.00",
              "original_interbank_settlement_currency": "EUR",
              "original_interbank_settlement_date": "2026-07-17",
              "cancellation_reason_cd": "DUPL",
              "cancellation_reason_addtl_inf": "Duplicate of TXN-2026-07-16-001 sent in error"
            }
          ]
        }
      },
      "result": {
        "kind": "xml",
        "messageType": "camt.056.001.12",
        "text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Document xmlns=\"urn:iso:std:iso:20022:tech:xsd:camt.056.001.12\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n\t<FIToFIPmtCxlReq>\n\t\t<Assgnmt>\n\t\t\t<Id>CXL-2026-07-16-001</Id>\n\t\t\t<Assgnr>\n\t\t\t\t<Agt>\n\t\t\t\t\t<FinInstnId>\n\t\t\t\t\t\t<BICFI>COBADEFFXXX</BICFI>\n\t\t\t\t\t</FinInstnId>\n\t\t\t\t</Agt>\n\t\t\t</Assgnr>\n\t\t\t<Assgne>\n\t\t\t\t<Agt>\n\t\t\t\t\t<FinInstnId>\n\t\t\t\t\t\t<BICFI>BNPAFRPP</BICFI>\n\t\t\t\t\t</FinInstnId>\n\t\t\t\t</Agt>\n\t\t\t</Assgne>\n\t\t\t<CreDtTm>2026-07-16T10:05:00</CreDtTm>\n\t\t</Assgnmt>\n\t\t<Undrlyg>\t\t\t<OrgnlGrpInfAndCxl>\n\t\t\t\t<OrgnlMsgId>MSG-2026-07-16-001</OrgnlMsgId>\n\t\t\t\t<OrgnlMsgNmId>pain.001.001.03</OrgnlMsgNmId>\t\t\t\t<OrgnlCreDtTm>2026-07-16T09:30:00</OrgnlCreDtTm>\t\t\t</OrgnlGrpInfAndCxl>\t\t\t<TxInf>\t\t\t\t<CxlId>CXL-TXN-2026-07-16-001</CxlId>\t\t\t\t<OrgnlEndToEndId>TXN-2026-07-16-001</OrgnlEndToEndId>\t\t\t\t<OrgnlIntrBkSttlmAmt Ccy=\"EUR\">4200.00</OrgnlIntrBkSttlmAmt>\t\t\t\t<OrgnlIntrBkSttlmDt>2026-07-17</OrgnlIntrBkSttlmDt>\t\t\t\t<CxlRsnInf>\n\t\t\t\t\t<Rsn>\n\t\t\t\t\t\t<Cd>DUPL</Cd>\n\t\t\t\t\t</Rsn>\t\t\t\t\t<AddtlInf>Duplicate of TXN-2026-07-16-001 sent in error</AddtlInf>\t\t\t\t</CxlRsnInf>\t\t\t</TxInf>\t\t</Undrlyg>\n\t</FIToFIPmtCxlReq>\n</Document>\n"
      },
      "mappings": [
        {
          "id": "recall",
          "phrase": "Recall",
          "label": "FI to FI payment cancellation request: camt.056",
          "marks": [
            "<FIToFIPmtCxlReq>"
          ]
        },
        {
          "id": "original",
          "phrase": "this morning's",
          "label": "Original message under cancellation: OrgnlMsgId",
          "marks": [
            "<OrgnlMsgId>MSG-2026-07-16-001</OrgnlMsgId>"
          ]
        },
        {
          "id": "amount",
          "phrase": "4,200 euro",
          "label": "Original settlement amount: OrgnlIntrBkSttlmAmt",
          "marks": [
            "<OrgnlIntrBkSttlmAmt Ccy=\"EUR\">4200.00</OrgnlIntrBkSttlmAmt>"
          ]
        },
        {
          "id": "reason",
          "phrase": "went out twice",
          "label": "Cancellation reason: CxlRsnInf/Rsn/Cd DUPL",
          "marks": [
            "<Cd>DUPL</Cd>"
          ]
        }
      ]
    },
    {
      "id": "missing-details",
      "label": "Missing details",
      "sentence": "Pay our new supplier Solstice Publishing 950 euros.",
      "note": "Validation catches everything at once: one round trip reports every missing field, so the agent asks one follow-up question, not ten.",
      "server": {
        "name": "iso20022",
        "version": "0.0.4",
        "command": "uvx --from \"iso20022-mcp[all]==0.0.4\" iso20022-mcp"
      },
      "tool": "generate",
      "args": {
        "message_type": "pain.001.001.03",
        "records": [
          {
            "id": "MSG-2026-07-16-004",
            "date": "2026-07-16T16:45:00",
            "initiator_name": "Acme Treasury GmbH",
            "initiator_street_name": "Mainzer Landstrasse",
            "initiator_building_number": "50",
            "initiator_postal_code": "60325",
            "initiator_town_name": "Frankfurt am Main",
            "initiator_country_code": "DE",
            "payment_information_id": "PMT-2026-07-16-004",
            "payment_method": "TRF",
            "service_level_code": "SEPA",
            "debtor_name": "Acme Treasury GmbH",
            "debtor_street_name": "Mainzer Landstrasse",
            "debtor_building_number": "50",
            "debtor_postal_code": "60325",
            "debtor_town_name": "Frankfurt am Main",
            "debtor_country_code": "DE",
            "debtor_account_IBAN": "DE89370400440532013000",
            "debtor_agent_BIC": "COBADEFFXXX",
            "payment_id": "TXN-2026-07-16-004",
            "payment_amount": "950.00",
            "currency": "EUR",
            "creditor_name": "Solstice Publishing"
          }
        ]
      },
      "result": {
        "kind": "error",
        "text": "Missing required fields for pain.001.001.03: requested_execution_date; row 1: creditor_agent_BIC, creditor_street_name, creditor_building_number, creditor_postal_code, creditor_town_name, creditor_country_code, creditor_account_IBAN, purpose_code, reference_number, reference_date. Provide them in one call - aliases are accepted ('amount' for payment_amount, 'currency' for payment_currency); nb_of_txs and ctrl_sum are computed automatically."
      },
      "mappings": [
        {
          "id": "unknown",
          "phrase": "new supplier",
          "label": "No bank details on file: every gap reported in one message",
          "marks": [
            "creditor_agent_BIC",
            "creditor_account_IBAN"
          ]
        },
        {
          "id": "nodate",
          "phrase": "Pay",
          "label": "No execution date given",
          "marks": [
            "requested_execution_date"
          ]
        }
      ]
    }
  ]
};

export default SIMULATOR_DATA;
