---
title: "Automatisera skapandet av ISO 20022-betalfiler med pain001"
subtitle: "Automatisering av ISO 20022-betalningar och teknik för stora betalningar med pain001."
description: "Automatisera skapandet av ISO 20022 pain.001-betalfiler från CSV eller SQLite. pain001 är Python-biblioteket med öppen källkod som förenklar regelefterlevnaden."
date: "September 29, 2023"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "Avstängd bärbar dator på ett brunt träbord"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, betalningsautomatisering, XML-generering, XSD-validering, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

![Avstängd bärbar dator på ett brunt träbord](https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp).class=\"img-fluid clearfix\"

> **Sammanfattning / Viktigaste punkter**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) är det strukturerade XML-meddelandeformat som används för att initiera kontoöverföringar enligt SEPA (EPC:s SCT-regelverk) och CBPR+ (SWIFT:s standard för gränsöverskridande meddelanden, obligatorisk för korrespondentbanker från november 2025).
> - **[pain001 ⧉][00]** läser betalningsdata från CSV eller SQLite, mappar rader till meddelandehierarkin i pain.001.001.09 (GrpHdr → PmtInf → CdtTrfTxInf) och renderar en konform XML-fil via en mallbaserad generator: tre rader Python från data till validerad XML.
> - **XSD-validering** körs på varje genererad fil innan utdata skrivs; biblioteket kastar ett beskrivande undantag som identifierar det felande elementet, kardinaliteten eller typfelet, så att fel fångas vid genereringen i stället för vid inlämningen till banken.
> - **CtrlSum och NbOfTxs** beräknas från transaktionsmängden och matas inte in manuellt, vilket eliminerar den enskilt vanligaste orsaken till avvisade betalfiler vid SEPA- och CBPR+-gatewayer.
> - Både meddelandevarianten **SEPA Credit Transfer** (EUR, inom SEPA-området) och **CBPR+** (gränsöverskridande, flera valutor) stöds via parametern `message_type`, där skillnader i fältvalidering hanteras internt.

[**pain001 ⧉**][00] är ett Python-bibliotek med öppen källkod för att generera ISO 20022-filer för betalningsinitiering. Det läser betalningsdata från en strukturerad indatakälla (CSV eller SQLite), validerar datat, renderar ett konformt pain.001.001.09-XML-dokument och validerar utdata mot ISO 20022:s XSD-schema, allt i ett enda funktionsanrop.

Denna artikel beskriver meddelandestrukturen i ISO 20022 pain.001, hur pain001 mappar indata till meddelandeelement, valideringskedjan samt konfigurationsalternativen för SEPA respektive CBPR+.

## Meddelandestrukturen i ISO 20022 pain.001

Meddelandet ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) har tre nivåer:

**GrpHdr** (Group Header), ett per fil:

| Element | Beskrivning | Exempel |
|---|---|---|
| `MsgId` | Unik meddelandeidentifierare | `ACME20240115-001` |
| `CreDtTm` | Datum och tid för skapande | `2024-01-15T09:00:00` |
| `NbOfTxs` | Totalt antal transaktioner | `3` |
| `CtrlSum` | Summan av alla instruerade belopp | `15000.00` |
| `InitgPty/Nm` | Den initierande partens namn | `Acme Corp` |

**PmtInf** (Payment Information), ett eller flera per fil; grupperar transaktioner efter betalarkonto och betalningsdatum:

| Element | Beskrivning |
|---|---|
| `PmtInfId` | Identifierare för betalningsinformation |
| `PmtMtd` | Betalningsmetod, alltid `TRF` för kontoöverföring |
| `ReqdExctnDt/Dt` | Begärt utförandedatum |
| `Dbtr/Nm` | Betalarens (avsändarens) namn |
| `DbtrAcct/Id/IBAN` | Betalarens IBAN |
| `DbtrAgt/FinInstnId/BICFI` | Betalarbankens BIC |

**CdtTrfTxInf** (Credit Transfer Transaction Information), ett eller flera per PmtInf-block:

| Element | Beskrivning |
|---|---|
| `PmtId/EndToEndId` | End-to-end-referens (bevaras genom hela kedjan) |
| `Amt/InstdAmt` | Instruerat belopp med valutaattribut |
| `CdtrAgt/FinInstnId/BICFI` | Mottagarbankens BIC |
| `Cdtr/Nm` | Betalningsmottagarens namn |
| `CdtrAcct/Id/IBAN` | Betalningsmottagarens IBAN |
| `RmtInf/Ustrd` | Ostrukturerad remitteringsinformation (fakturareferens med mera) |

## Generera XML från CSV

Ett minimalt pain001-anrop:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

CSV-filen mappar kolumnnamn till meddelandefält. Ett minimalt exempel:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

Biblioteket läser `ctrl_sum` och `nb_of_txs` från CSV-raden för filer med en enda rad. För filer med flera rader (flera transaktioner i en och samma batch) beräknar pain001 dessa värden från transaktionsmängden i stället för att lita på indatavärdena, vilket förhindrar avvikelser.

SQLite-gränssnittet använder samma kolumnnamnskonvention. Ange `data_file_type="sqlite"` och sökvägen till en SQLite-databasfil i `data_file`; pain001 läser som standard tabellen `payment`.

## Genererad XML-struktur

Ett korrekt renderat pain.001.001.09-dokument för CSV-raden ovan:

```xml
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09">
  <CstmrCdtTrfInitn>
    <GrpHdr>
      <MsgId>ACME20240115-001</MsgId>
      <CreDtTm>2024-01-15T09:00:00</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <CtrlSum>1000.00</CtrlSum>
      <InitgPty><Nm>Acme Corp</Nm></InitgPty>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>ACME20240115-PMT-001</PmtInfId>
      <PmtMtd>TRF</PmtMtd>
      <ReqdExctnDt><Dt>2024-01-16</Dt></ReqdExctnDt>
      <Dbtr><Nm>Acme Corp</Nm></Dbtr>
      <DbtrAcct><Id><IBAN>GB29NWBK60161331926819</IBAN></Id></DbtrAcct>
      <DbtrAgt><FinInstnId><BICFI>NWBKGB2L</BICFI></FinInstnId></DbtrAgt>
      <CdtTrfTxInf>
        <PmtId><EndToEndId>ACME20240115001</EndToEndId></PmtId>
        <Amt><InstdAmt Ccy="EUR">1000.00</InstdAmt></Amt>
        <CdtrAgt><FinInstnId><BICFI>COBADEFFXXX</BICFI></FinInstnId></CdtrAgt>
        <Cdtr><Nm>Supplier Ltd</Nm></Cdtr>
        <CdtrAcct><Id><IBAN>DE89370400440532013000</IBAN></Id></CdtrAcct>
        <RmtInf><Ustrd>INV-2024-0042</Ustrd></RmtInf>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>
```

## XSD-valideringskedjan

Efter renderingen validerar pain001 utdata mot XSD-schemat för ISO 20022 pain.001.001.09. Valideringen kontrollerar:

- **Förekomst av obligatoriska element**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs och GrpHdr/CtrlSum krävs samtliga; saknas något av dem utlöses ett valideringsfel.
- **Typbegränsningar**: IBAN-format, BIC-format (8 eller 11 tecken), beloppsprecision (högst 18 siffror, 5 decimaler).
- **Kardinalitet**: minst ett `CdtTrfTxInf` per `PmtInf`; minst ett `PmtInf` per dokument.
- **Uppräkningsvärden**: `PmtMtd` måste vara `TRF` för kontoöverföringar; `Ccy` måste vara en giltig valutakod enligt ISO 4217.

När valideringen misslyckas kastar pain001 ett `ValidationError` med lxml-felmeddelandet, som identifierar det felande XPath-uttrycket, elementnamnet och begränsningen. Därmed synliggörs felkonfigurationer vid genereringen i stället för vid inlämningen till banken, där avvisningskoderna vanligen är mindre beskrivande.

## Konfiguration för SEPA respektive CBPR+

SEPA Credit Transfer (ISO 20022 pain.001.001.09 enligt EPC:s SCT-regelverk) och CBPR+ (SWIFT:s standard Cross-Border Payments and Reporting Plus) använder samma meddelandeschema men skiljer sig åt i fråga om obligatoriska fältuppsättningar och värdebegränsningar:

| Aspekt | SEPA SCT | CBPR+ |
|---|---|---|
| Valuta | Endast EUR | Flera valutor |
| IBAN obligatoriskt | Ja | Ja (betalningsmottagare) |
| BIC obligatoriskt | Nej (routning inom SEPA-området) | Ja |
| Avgiftsbärare (`ChrgBr`) | `SLEV` | `DEBT`, `CRED` eller `SHAR` |
| Omfattning | SEPA-området (36 länder) | Global korrespondentbankverksamhet |

Konfigurera meddelandetypen via parametern `payment_initiation_message_type`:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

CBPR+-efterlevnad blev obligatorisk för SWIFT:s korrespondentbankverksamhet i november 2023 för inkommande meddelanden och blir det i november 2025 för utgående. Att generera CBPR+-konforma pain.001-filer kräver att BIC-fältet är ifyllt och att elementet `ChrgBr` finns med.

## Vanliga frågor

**Vad är skillnaden mellan pain.001 och pain.008?**
pain.001 (CustomerCreditTransferInitiation) initierar en kontoöverföring: avsändarens bank debiterar avsändarens konto och krediterar mottagaren. pain.008 (CustomerDirectDebitInitiation) initierar en autogirering: betalningsmottagarens bank hämtar medel från betalaren. Biblioteket pain001 genererar enbart pain.001-filer.

**Vilken ISO 20022-version riktar sig pain001 mot?**
Det primära målet är pain.001.001.09, den version som krävs för CBPR+ och som EPC föreskriver för nya SEPA-implementationer. Biblioteket stöder även pain.001.001.03 (den äldre SEPA-versionen) via parametern `payment_initiation_message_type`, för organisationer som fortfarande använder äldre bankgränssnitt.

**Kan pain001 hantera flera betalarkonton i en och samma fil?**
Ja. Flera `PmtInf`-block med olika betalar-IBAN kan produceras genom att gruppera CSV-rader med olika värden för betalarkonto. pain001 skapar ett `PmtInf`-block per unik kombination av (betalar-IBAN, utförandedatum), med alla matchande transaktioner nästlade som `CdtTrfTxInf`-barn.

**Vad händer när XSD-valideringen misslyckas?**
pain001 kastar ett `pain001.exceptions.ValidationError` med valideringsmeddelandet från lxml. XML-filen skrivs inte till disk när valideringen misslyckas, så endast giltiga filer når utdatasökvägen. Vanliga felorsaker är: IBAN i fel format, BIC som inte är 8 eller 11 tecken, valutakod som inte ingår i ISO 4217, eller obligatoriska element som saknas när en nödvändig CSV-kolumn inte finns med.

## Referenser

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines: Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 - Financial services - Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 - ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automatisera skapandet av ISO 20022-kompatibla betalfiler"
[01]: https://www.iso20022.org/ "ISO 20022: Universellt meddelandeschema för finansbranschen"
