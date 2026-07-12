---
title: "ISO 20022-kompatibilis fizetési fájlok létrehozásának automatizálása a pain001 segítségével"
tags: "pain001, ISO 20022, CustomerCreditTransferInitiation, SEPACreditTransfer, CBPR, payment automation, XMLGeneration, XSDValidation, SWIFT, post-quantum cryptography, AI, open source, cross-border payments, Rust"
subtitle: "ISO 20022 fizetésautomatizálás és nagyértékű fizetések fejlesztése a pain001 könyvtárral."
description: "Automatizálja az ISO 20022 pain.001 fizetési fájlok létrehozását CSV-ből vagy SQLite-ból. A pain001 az a nyílt forráskódú Python-könyvtár, amely leegyszerűsíti a megfelelőséget."
date: "Sep 29, 2023"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "Kikapcsolt hordozható számítógép egy barna fából készült asztal tetején"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, fizetésautomatizálás, XML-generálás, XSD-validáció, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

> **Vezetői összefoglaló / Legfontosabb tanulságok**
>
> - Az **ISO 20022 pain.001** (CustomerCreditTransferInitiation) az a strukturált XML-üzenetformátum, amelyet átutalások kezdeményezésére használnak a SEPA (EPC SCT szabálykönyv) és a CBPR+ (a SWIFT határokon átnyúló üzenetküldési szabványa, amely a levelező bankok számára 2025 novemberétől kötelező) keretében.
> - A **[pain001 ⧉][00]** beolvassa a fizetési adatokat CSV-ből vagy SQLite-ból, a sorokat a pain.001.001.09 üzenethierarchiához (GrpHdr → PmtInf → CdtTrfTxInf) rendeli, és egy sablonalapú generátoron keresztül megfelelő XML-fájlt jelenít meg: három sor Python az adattól a validált XML-ig.
> - Az **XSD-validáció** minden generált fájlon lefut a kimenet kiírása előtt; a könyvtár leíró kivételt vált ki, amely azonosítja a hibás elemet, a számosságot vagy a típuseltérést, így a hibák a generálás idején kerülnek elfogásra, nem pedig a banki benyújtáskor.
> - A **CtrlSum és NbOfTxs** értékeit a tranzakciókészletből számítja ki, nem kézzel adják meg őket: ezzel kiküszöbölhető a fizetési fájlok elutasításának leggyakoribb oka a SEPA és CBPR+ feldolgozási átjáróknál.
> - Mind a **SEPA Credit Transfer** (EUR, a SEPA-zónán belül), mind a **CBPR+** (határokon átnyúló, több devizás) üzenetváltozat támogatott a `message_type` paraméteren keresztül, a mezőszintű validációs különbségeket belsőleg kezelve.

A [**pain001 ⧉**][00] egy nyílt forráskódú Python-könyvtár ISO 20022 fizetéskezdeményezési fájlok generálásához. Beolvassa a fizetési adatokat egy strukturált bemenetből (CSV vagy SQLite), validálja az adatokat, megfelelő pain.001.001.09 XML-dokumentumot jelenít meg, és validálja a kimenetet az ISO 20022 XSD-sémával szemben, mindezt egyetlen függvényhívásban.

Ez a cikk leírja az ISO 20022 pain.001 üzenet szerkezetét, azt, hogy a pain001 hogyan rendeli a bemeneti adatokat az üzenetelemekhez, a validációs folyamatot, valamint a SEPA és CBPR+ közötti konfigurációs beállításokat.

## Az ISO 20022 pain.001 üzenet szerkezete

Az ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) üzenet három szintből áll:

**GrpHdr** (csoportfejléc) - egy fájlonként:

| Elem | Leírás | Példa |
|---|---|---|
| `MsgId` | Egyedi üzenetazonosító | `ACME20240115-001` |
| `CreDtTm` | Létrehozás dátuma és ideje | `2024-01-15T09:00:00` |
| `NbOfTxs` | A tranzakciók teljes száma | `3` |
| `CtrlSum` | Az összes utasított összeg összege | `15000.00` |
| `InitgPty/Nm` | A kezdeményező fél neve | `Acme Corp` |

**PmtInf** (fizetési információ) - egy vagy több fájlonként, a tranzakciókat terhelt számla és fizetési dátum szerint csoportosítja:

| Elem | Leírás |
|---|---|
| `PmtInfId` | Fizetési információ azonosítója |
| `PmtMtd` | Fizetési mód - átutalás esetén mindig `TRF` |
| `ReqdExctnDt/Dt` | Kért teljesítési dátum |
| `Dbtr/Nm` | Terhelt fél (küldő) neve |
| `DbtrAcct/Id/IBAN` | Terhelt fél IBAN-ja |
| `DbtrAgt/FinInstnId/BICFI` | Terhelt fél bankjának BIC-je |

**CdtTrfTxInf** (átutalási tranzakció információ) - egy vagy több minden PmtInf blokkonként:

| Elem | Leírás |
|---|---|
| `PmtId/EndToEndId` | Végponttól végpontig terjedő hivatkozás (a láncon át megőrizve) |
| `Amt/InstdAmt` | Utasított összeg deviza attribútummal |
| `CdtrAgt/FinInstnId/BICFI` | Jóváírt fél bankjának BIC-je |
| `Cdtr/Nm` | Jóváírt fél (fogadó) neve |
| `CdtrAcct/Id/IBAN` | Jóváírt fél IBAN-ja |
| `RmtInf/Ustrd` | Strukturálatlan átutalási információ (számlahivatkozás stb.) |

## XML generálása CSV-ből

Egy minimális pain001-hívás:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

A CSV-fájl az oszlopneveket üzenetmezőkhöz rendeli. Egy minimális példa:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

A könyvtár a `ctrl_sum` és `nb_of_txs` értékeit a CSV-sorból olvassa be az egysoros fájlok esetében. Több soros fájloknál (több tranzakció egyetlen kötegben) a pain001 ezeket az értékeket a tranzakciókészletből számítja ki, ahelyett, hogy megbízna a bemeneti értékekben, ami megelőzi az eltéréseket.

Az SQLite-illesztés ugyanazt az oszlopnév-konvenciót használja. Adja át a `data_file_type="sqlite"` paramétert és a `data_file` útvonalat egy SQLite-adatbázisfájlhoz; a pain001 alapértelmezés szerint a `payment` táblát olvassa be.

## A generált XML szerkezete

A fenti CSV-sorhoz helyesen megjelenített pain.001.001.09 dokumentum:

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

## XSD-validációs folyamat

A megjelenítés után a pain001 validálja a kimenetet az ISO 20022 pain.001.001.09 XSD-sémával szemben. A validáció ellenőrzi:

- **Kötelező elemek jelenléte**: a GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, GrpHdr/CtrlSum mind kötelező; bármelyik hiánya validációs hibát vált ki.
- **Típuskorlátozások**: IBAN-formátum, BIC-formátum (8 vagy 11 karakter), összegpontosság (legfeljebb 18 számjegy, 5 tizedesjegy).
- **Számosság**: legalább egy `CdtTrfTxInf` minden `PmtInf`-hez; legalább egy `PmtInf` dokumentumonként.
- **Felsorolási értékek**: a `PmtMtd` értékének átutalások esetén `TRF`-nek kell lennie; a `Ccy` értékének érvényes ISO 4217 devizakódnak kell lennie.

Ha a validáció sikertelen, a pain001 egy `ValidationError` kivételt vált ki az lxml hibaüzenettel, amely azonosítja a hibás XPath-kifejezést, elemnevet és korlátozást. Ez a hibás konfigurációkat a generálás idején hozza felszínre, nem pedig a banki benyújtáskor, ahol az elutasítási kódok jellemzően kevésbé leírók.

## SEPA vs. CBPR+ konfiguráció

A SEPA Credit Transfer (ISO 20022 pain.001.001.09 az EPC SCT szabálykönyv alapján) és a CBPR+ (a SWIFT Cross-Border Payments and Reporting Plus szabványa) ugyanazt az üzenetsémát használja, de a kötelező mezőkészletekben és az értékkorlátozásokban különböznek:

| Szempont | SEPA SCT | CBPR+ |
|---|---|---|
| Deviza | Csak EUR | Több deviza |
| IBAN kötelező | Igen | Igen (jóváírt fél) |
| BIC kötelező | Nem (SEPA-zóna útválasztás) | Igen |
| Költségviselő (`ChrgBr`) | `SLEV` | `DEBT`, `CRED` vagy `SHAR` |
| Hatókör | SEPA-zóna (36 ország) | Globális levelező banki tevékenység |

Konfigurálja az üzenettípust a `payment_initiation_message_type` paraméterrel:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

A CBPR+ megfelelőség a SWIFT levelező banki tevékenység esetében a bejövő üzenetekre 2023 novemberétől, a kimenő üzenetekre pedig 2025 novemberétől vált kötelezővé. A CBPR+-kompatibilis pain.001 fájlok generálásához szükséges, hogy a BIC-mező ki legyen töltve, és hogy a `ChrgBr` elem jelen legyen.

## Gyakran ismételt kérdések

**Mi a különbség a pain.001 és a pain.008 között?**
A pain.001 (CustomerCreditTransferInitiation) átutalást kezdeményez: a küldő bankja megterheli a küldő számláját és jóváírja a fogadónál. A pain.008 (CustomerDirectDebitInitiation) beszedést kezdeményez: a jóváírt fél bankja beszedi a pénzeszközöket a terhelt féltől. A pain001 könyvtár kizárólag pain.001 fájlokat generál.

**Melyik ISO 20022-verziót célozza a pain001?**
Az elsődleges cél a pain.001.001.09, az a verzió, amelyet a CBPR+ megkövetel, és amelyet az EPC az új SEPA-implementációkhoz előír. A könyvtár a `payment_initiation_message_type` paraméteren keresztül támogatja a pain.001.001.03-at is (a régi SEPA-verzió) azon szervezetek számára, amelyek még mindig régebbi banki illesztéseket használnak.

**Kezelhet-e a pain001 több terhelt számlát egyetlen fájlban?**
Igen. Több `PmtInf` blokk különböző terhelt IBAN-okkal állítható elő úgy, hogy a különböző terhelt számlaértékekkel rendelkező CSV-sorokat csoportosítja. A pain001 minden egyedi (terhelt IBAN, teljesítési dátum) kombinációhoz egy `PmtInf` blokkot hoz létre, az összes megfelelő tranzakcióval `CdtTrfTxInf` gyermekelemekként beágyazva.

**Mi történik, ha az XSD-validáció sikertelen?**
A pain001 egy `pain001.exceptions.ValidationError` kivételt vált ki az lxml validációs üzenettel. Az XML-fájl nem kerül a lemezre írásra, ha a validáció sikertelen, így csak érvényes fájlok jutnak el a kimeneti útvonalra. Gyakori hibaokok: az IBAN rossz formátumú, a BIC nem 8 vagy 11 karakter, a devizakód nem szerepel az ISO 4217-ben, vagy hiányoznak a kötelező elemek, amikor egy szükséges CSV-oszlop hiányzik.

## Hivatkozások

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automate ISO 20022-Compliant Payment File Creation"
[01]: https://www.iso20022.org/ "ISO 20022: Universal financial industry message scheme"

