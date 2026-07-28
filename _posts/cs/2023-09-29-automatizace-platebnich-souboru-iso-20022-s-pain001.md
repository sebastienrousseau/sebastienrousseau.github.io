---
title: "Automatizace tvorby platebních souborů ISO 20022 pomocí pain001"
subtitle: "Automatizace plateb podle ISO 20022 a inženýrství velkoobchodních plateb s pain001."
description: "Automatizujte tvorbu platebních souborů ISO 20022 pain.001 z CSV nebo SQLite. pain001 je open-source knihovna v jazyce Python, která zjednodušuje soulad s předpisy."
date: "September 29, 2023"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "Vypnutý notebook na hnědém dřevěném stole"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, automatizace plateb, generování XML, validace XSD, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---


> **Shrnutí pro vedení / Klíčové body**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) je strukturovaný formát zprávy XML používaný k iniciaci úhrad v rámci SEPA (rulebook EPC SCT) a CBPR+ (přeshraniční standard zpráv SWIFT, povinný pro korespondenční banky od listopadu 2025).
> - **[pain001 ⧉][00]** čte platební data z CSV nebo SQLite, mapuje řádky na hierarchii zprávy pain.001.001.09 (GrpHdr → PmtInf → CdtTrfTxInf) a vykresluje vyhovující soubor XML pomocí šablonového generátoru: tři řádky jazyka Python od dat po validované XML.
> - **Validace XSD** proběhne u každého vygenerovaného souboru dříve, než se výstup zapíše; knihovna vyvolá popisnou výjimku, která identifikuje chybný prvek, kardinalitu nebo nesoulad typu, takže se chyby zachytí už při generování, nikoli až při odeslání do banky.
> - **CtrlSum a NbOfTxs** se počítají ze sady transakcí, nezadávají se ručně, což odstraňuje nejčastější příčinu odmítnutí platebního souboru na zpracovatelských branách SEPA a CBPR+.
> - Podporovány jsou obě varianty zpráv, **SEPA Credit Transfer** (EUR v rámci zóny SEPA) i **CBPR+** (přeshraniční, víceměnová), a to prostřednictvím parametru `message_type`, přičemž rozdíly ve validaci na úrovni polí se řeší interně.

[**pain001 ⧉**][00] je open-source knihovna v jazyce Python pro generování souborů pro iniciaci plateb podle ISO 20022. Čte platební data ze strukturovaného vstupu (CSV nebo SQLite), validuje je, vykreslí vyhovující dokument XML pain.001.001.09 a ověří výstup proti schématu XSD normy ISO 20022, to vše v jediném volání funkce.

Tento článek popisuje strukturu zprávy ISO 20022 pain.001, způsob, jakým pain001 mapuje vstupní data na prvky zprávy, validační pipeline a možnosti konfigurace SEPA versus CBPR+.

## Struktura zprávy ISO 20022 pain.001

Zpráva ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) má tři úrovně:

**GrpHdr** (Group Header), jeden na soubor:

| Prvek | Popis | Příklad |
|---|---|---|
| `MsgId` | Jedinečný identifikátor zprávy | `ACME20240115-001` |
| `CreDtTm` | Datum a čas vytvoření | `2024-01-15T09:00:00` |
| `NbOfTxs` | Celkový počet transakcí | `3` |
| `CtrlSum` | Součet všech zadaných částek | `15000.00` |
| `InitgPty/Nm` | Název iniciující strany | `Acme Corp` |

**PmtInf** (Payment Information), jeden nebo více na soubor, seskupuje transakce podle účtu plátce a data platby:

| Prvek | Popis |
|---|---|
| `PmtInfId` | Identifikátor platební informace |
| `PmtMtd` | Platební metoda, vždy `TRF` pro úhradu |
| `ReqdExctnDt/Dt` | Požadované datum provedení |
| `Dbtr/Nm` | Jméno plátce (odesílatele) |
| `DbtrAcct/Id/IBAN` | IBAN plátce |
| `DbtrAgt/FinInstnId/BICFI` | BIC banky plátce |

**CdtTrfTxInf** (Credit Transfer Transaction Information), jeden nebo více na blok PmtInf:

| Prvek | Popis |
|---|---|
| `PmtId/EndToEndId` | Reference end-to-end (zachovaná v celém řetězci) |
| `Amt/InstdAmt` | Zadaná částka s atributem měny |
| `CdtrAgt/FinInstnId/BICFI` | BIC banky příjemce |
| `Cdtr/Nm` | Jméno příjemce |
| `CdtrAcct/Id/IBAN` | IBAN příjemce |
| `RmtInf/Ustrd` | Nestrukturovaná informace o platbě (reference faktury apod.) |

## Generování XML z CSV

Minimální volání pain001:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

Soubor CSV mapuje názvy sloupců na pole zprávy. Minimální příklad:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

Knihovna čte `ctrl_sum` a `nb_of_txs` z řádku CSV u jednořádkových souborů. U víceřádkových souborů (více transakcí v jedné dávce) pain001 tyto hodnoty vypočítá ze sady transakcí, místo aby se spoléhal na vstupní hodnoty, což zabraňuje nesouladům.

Rozhraní SQLite používá stejnou konvenci názvů sloupců. Předejte `data_file_type="sqlite"` a cestu `data_file` k souboru databáze SQLite; pain001 ve výchozím nastavení čte tabulku `payment`.

## Struktura generovaného XML

Správně vykreslený dokument pain.001.001.09 pro výše uvedený řádek CSV:

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

## Validační pipeline XSD

Po vykreslení pain001 ověří výstup proti schématu XSD ISO 20022 pain.001.001.09. Validace kontroluje:

- **Přítomnost povinných prvků**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs a GrpHdr/CtrlSum jsou všechny povinné; chybějící kterýkoli z nich vyvolá chybu validace.
- **Omezení typů**: formát IBAN, formát BIC (8 nebo 11 znaků), přesnost částky (maximálně 18 číslic, 5 desetinných míst).
- **Kardinalita**: alespoň jeden `CdtTrfTxInf` na `PmtInf`; alespoň jeden `PmtInf` na dokument.
- **Hodnoty výčtů**: `PmtMtd` musí být `TRF` u úhrad; `Ccy` musí být platný kód měny podle ISO 4217.

Když validace selže, pain001 vyvolá `ValidationError` s chybovou zprávou lxml, která identifikuje chybný výraz XPath, název prvku a omezení. Tím se chybná nastavení objeví už při generování, nikoli až při odeslání do banky, kde jsou kódy odmítnutí obvykle méně popisné.

## Konfigurace SEPA versus CBPR+

SEPA Credit Transfer (ISO 20022 pain.001.001.09 podle rulebooku EPC SCT) a CBPR+ (standard SWIFT Cross-Border Payments and Reporting Plus) používají stejné schéma zprávy, ale liší se v sadách povinných polí a v omezeních hodnot:

| Aspekt | SEPA SCT | CBPR+ |
|---|---|---|
| Měna | Pouze EUR | Víceměnová |
| IBAN povinný | Ano | Ano (příjemce) |
| BIC povinný | Ne (směrování v zóně SEPA) | Ano |
| Nositel poplatků (`ChrgBr`) | `SLEV` | `DEBT`, `CRED` nebo `SHAR` |
| Rozsah | Zóna SEPA (36 zemí) | Globální korespondenční bankovnictví |

Typ zprávy nakonfigurujte parametrem `payment_initiation_message_type`:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # výchozí; přijímá také "pain.001.001.03" pro starší SEPA
)
```

Soulad s CBPR+ se stal pro korespondenční bankovnictví SWIFT povinným v listopadu 2023 pro příchozí zprávy a v listopadu 2025 pro odchozí. Generování souborů pain.001 vyhovujících CBPR+ vyžaduje, aby bylo vyplněno pole BIC a aby byl přítomen prvek `ChrgBr`.

## Často kladené otázky

**Jaký je rozdíl mezi pain.001 a pain.008?**
pain.001 (CustomerCreditTransferInitiation) iniciuje úhradu: banka odesílatele odepíše prostředky z účtu odesílatele a připíše je příjemci. pain.008 (CustomerDirectDebitInitiation) iniciuje inkaso: banka příjemce vybere prostředky od plátce. Knihovna pain001 generuje pouze soubory pain.001.

**Na kterou verzi ISO 20022 pain001 cílí?**
Primárním cílem je pain.001.001.09, verze požadovaná pro CBPR+ a nařízená EPC pro nové implementace SEPA. Knihovna podporuje také pain.001.001.03 (starší verzi SEPA) prostřednictvím parametru `payment_initiation_message_type` pro organizace, které stále používají starší bankovní rozhraní.

**Zvládne pain001 více účtů plátce v jednom souboru?**
Ano. Více bloků `PmtInf` s různými IBAN plátců lze vytvořit seskupením řádků CSV s různými hodnotami účtu plátce. pain001 vytvoří jeden blok `PmtInf` pro každou jedinečnou kombinaci (IBAN plátce, datum provedení), přičemž všechny odpovídající transakce vnoří jako potomky `CdtTrfTxInf`.

**Co se stane, když selže validace XSD?**
pain001 vyvolá `pain001.exceptions.ValidationError` s validační zprávou lxml. Při selhání validace se soubor XML na disk nezapíše, takže do výstupní cesty se dostanou pouze platné soubory. Časté příčiny selhání jsou: IBAN ve špatném formátu, BIC bez 8 nebo 11 znaků, kód měny mimo ISO 4217 nebo chybějící povinné prvky, když chybí požadovaný sloupec CSV.

## Reference

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automatizace tvorby platebních souborů podle ISO 20022"
[01]: https://www.iso20022.org/ "ISO 20022: Univerzální schéma zpráv pro finanční sektor"
