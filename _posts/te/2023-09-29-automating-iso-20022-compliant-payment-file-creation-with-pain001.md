---
title: "pain001తో ISO 20022 చెల్లింపు ఫైళ్ల సృష్టిని ఆటోమేట్ చేయడం"
tags: "pain001, ISO 20022, CustomerCreditTransferInitiation, SEPACreditTransfer, CBPR, payment automation, XMLGeneration, XSDValidation, SWIFT, post-quantum cryptography, AI, open source, cross-border payments, Rust"
subtitle: "pain001తో ISO 20022 చెల్లింపు ఆటోమేషన్ మరియు హోల్‌సేల్-పేమెంట్స్ ఇంజనీరింగ్."
description: "CSV లేదా SQLite నుండి ISO 20022 pain.001 చెల్లింపు ఫైళ్ల సృష్టిని ఆటోమేట్ చేయండి. pain001 అనేది కంప్లయన్స్‌ను సులభతరం చేసే ఓపెన్-సోర్స్ Python లైబ్రరీ."
date: "Sep 29, 2023"
language: "te"
locale: "te_IN"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "గోధుమ రంగు చెక్క బల్ల మీద ఆఫ్ చేసి ఉన్న ల్యాప్‌టాప్ కంప్యూటర్"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, payment automation, XML generation, XSD validation, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

> **కార్యనిర్వాహక సారాంశం / ముఖ్యాంశాలు**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) అనేది SEPA (EPC SCT రూల్‌బుక్) మరియు CBPR+ (SWIFT యొక్క క్రాస్-బోర్డర్ మెసేజింగ్ ప్రమాణం, నవంబర్ 2025 నుండి కరస్పాండెంట్ బ్యాంకులకు తప్పనిసరి) కింద క్రెడిట్ బదిలీలను ప్రారంభించడానికి ఉపయోగించే నిర్మాణాత్మక XML మెసేజ్ ఫార్మాట్.
> - **[pain001 ⧉][00]** CSV లేదా SQLite నుండి చెల్లింపు డేటాను చదివి, వరుసలను pain.001.001.09 మెసేజ్ శ్రేణికి (GrpHdr → PmtInf → CdtTrfTxInf) మ్యాప్ చేసి, టెంప్లేటెడ్ జనరేటర్ ద్వారా అనుగుణమైన XML ఫైల్‌ను రెండర్ చేస్తుంది — డేటా నుండి ధృవీకరించిన XML వరకు మూడు లైన్ల Python.
> - ప్రతి రూపొందించిన ఫైల్‌పై అవుట్‌పుట్ వ్రాయబడటానికి ముందు **XSD validation** అమలవుతుంది; లైబ్రరీ విఫలమైన ఎలిమెంట్, కార్డినాలిటీ లేదా రకం అసమానతను గుర్తించే వివరణాత్మక ఎక్సెప్షన్‌ను లేవనెత్తుతుంది, తద్వారా లోపాలు బ్యాంకుకు సమర్పించే సమయంలో కాకుండా రూపొందించే సమయంలోనే పట్టుబడతాయి.
> - **CtrlSum మరియు NbOfTxs** లావాదేవీల సమూహం నుండి గణించబడతాయి, మాన్యువల్‌గా నమోదు చేయబడవు — ఇది SEPA మరియు CBPR+ ప్రాసెసింగ్ గేట్‌వేల వద్ద అత్యంత సాధారణ చెల్లింపు ఫైల్ తిరస్కరణ కారణాన్ని తొలగిస్తుంది.
> - **SEPA Credit Transfer** (EUR, SEPA జోన్‌లో) మరియు **CBPR+** (క్రాస్-బోర్డర్, బహుళ-కరెన్సీ) మెసేజ్ వేరియంట్‌లు రెండూ `message_type` పరామితి ద్వారా మద్దతు పొందుతాయి, ఫీల్డ్-స్థాయి ధృవీకరణ తేడాలు అంతర్గతంగా నిర్వహించబడతాయి.

[**pain001 ⧉**][00] అనేది ISO 20022 చెల్లింపు ప్రారంభ ఫైళ్లను రూపొందించడానికి ఒక ఓపెన్-సోర్స్ Python లైబ్రరీ. ఇది నిర్మాణాత్మక ఇన్‌పుట్ (CSV లేదా SQLite) నుండి చెల్లింపు డేటాను చదివి, డేటాను ధృవీకరించి, అనుగుణమైన pain.001.001.09 XML డాక్యుమెంట్‌ను రెండర్ చేసి, అవుట్‌పుట్‌ను ISO 20022 XSD స్కీమాకు వ్యతిరేకంగా ధృవీకరిస్తుంది — ఇదంతా ఒకే ఫంక్షన్ కాల్‌లో.

ఈ వ్యాసం ISO 20022 pain.001 మెసేజ్ నిర్మాణం, pain001 ఇన్‌పుట్ డేటాను మెసేజ్ ఎలిమెంట్‌లకు ఎలా మ్యాప్ చేస్తుంది, ధృవీకరణ పైప్‌లైన్, మరియు SEPA వర్సెస్ CBPR+ కాన్ఫిగరేషన్ ఎంపికలను వివరిస్తుంది.

## ISO 20022 pain.001 మెసేజ్ నిర్మాణం

ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) మెసేజ్‌కు మూడు స్థాయిలు ఉన్నాయి:

**GrpHdr** (Group Header) — ఫైల్‌కు ఒకటి:

| ఎలిమెంట్ | వివరణ | ఉదాహరణ |
|---|---|---|
| `MsgId` | ప్రత్యేక మెసేజ్ ఐడెంటిఫయర్ | `ACME20240115-001` |
| `CreDtTm` | సృష్టి తేదీ మరియు సమయం | `2024-01-15T09:00:00` |
| `NbOfTxs` | లావాదేవీల మొత్తం సంఖ్య | `3` |
| `CtrlSum` | అన్ని సూచించిన మొత్తాల మొత్తం | `15000.00` |
| `InitgPty/Nm` | ప్రారంభించే పార్టీ పేరు | `Acme Corp` |

**PmtInf** (Payment Information) — ఫైల్‌కు ఒకటి లేదా అంతకంటే ఎక్కువ, డెబ్టర్ ఖాతా మరియు చెల్లింపు తేదీ ప్రకారం లావాదేవీలను సమూహపరుస్తుంది:

| ఎలిమెంట్ | వివరణ |
|---|---|
| `PmtInfId` | చెల్లింపు సమాచార ఐడెంటిఫయర్ |
| `PmtMtd` | చెల్లింపు పద్ధతి — క్రెడిట్ బదిలీకి ఎల్లప్పుడూ `TRF` |
| `ReqdExctnDt/Dt` | అభ్యర్థించిన అమలు తేదీ |
| `Dbtr/Nm` | డెబ్టర్ (పంపేవారి) పేరు |
| `DbtrAcct/Id/IBAN` | డెబ్టర్ IBAN |
| `DbtrAgt/FinInstnId/BICFI` | డెబ్టర్ బ్యాంక్ BIC |

**CdtTrfTxInf** (Credit Transfer Transaction Information) — ప్రతి PmtInf బ్లాక్‌కు ఒకటి లేదా అంతకంటే ఎక్కువ:

| ఎలిమెంట్ | వివరణ |
|---|---|
| `PmtId/EndToEndId` | ఎండ్-టు-ఎండ్ రిఫరెన్స్ (గొలుసు అంతటా భద్రపరచబడుతుంది) |
| `Amt/InstdAmt` | కరెన్సీ లక్షణంతో సూచించిన మొత్తం |
| `CdtrAgt/FinInstnId/BICFI` | క్రెడిటర్ బ్యాంక్ BIC |
| `Cdtr/Nm` | క్రెడిటర్ (స్వీకరించేవారి) పేరు |
| `CdtrAcct/Id/IBAN` | క్రెడిటర్ IBAN |
| `RmtInf/Ustrd` | నిర్మాణరహిత రెమిటెన్స్ సమాచారం (ఇన్‌వాయిస్ రిఫరెన్స్ మొదలైనవి) |

## CSV నుండి XML రూపొందించడం

కనీస pain001 ఇన్‌వొకేషన్:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

CSV ఫైల్ కాలమ్ పేర్లను మెసేజ్ ఫీల్డ్‌లకు మ్యాప్ చేస్తుంది. కనీస ఉదాహరణ:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

ఒక-వరుస ఫైళ్ల కోసం లైబ్రరీ CSV వరుస నుండి `ctrl_sum` మరియు `nb_of_txs`ను చదువుతుంది. బహుళ-వరుస ఫైళ్ల కోసం (ఒకే బ్యాచ్‌లో బహుళ లావాదేవీలు), pain001 ఇన్‌పుట్ విలువలను నమ్మకుండా, ఈ విలువలను లావాదేవీల సమూహం నుండి గణిస్తుంది, ఇది అసమానతలను నివారిస్తుంది.

SQLite ఇంటర్‌ఫేస్ అదే కాలమ్-పేరు నియమావళిని ఉపయోగిస్తుంది. `data_file_type="sqlite"` మరియు SQLite డేటాబేస్ ఫైల్‌కు `data_file` పాత్‌ను పంపండి; pain001 అప్రమేయంగా `payment` టేబుల్‌ను చదువుతుంది.

## రూపొందించిన XML నిర్మాణం

పైన ఉన్న CSV వరుసకు సరిగ్గా రెండరైన pain.001.001.09 డాక్యుమెంట్:

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

## XSD Validation పైప్‌లైన్

రెండరింగ్ తర్వాత, pain001 అవుట్‌పుట్‌ను ISO 20022 pain.001.001.09 XSD స్కీమాకు వ్యతిరేకంగా ధృవీకరిస్తుంది. ధృవీకరణ తనిఖీలు:

- **తప్పనిసరి ఎలిమెంట్ ఉనికి**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, GrpHdr/CtrlSum అన్నీ అవసరం; వీటిలో ఏదైనా లేకపోతే ధృవీకరణ లోపం లేవనెత్తబడుతుంది.
- **రకం పరిమితులు**: IBAN ఫార్మాట్, BIC ఫార్మాట్ (8 లేదా 11 అక్షరాలు), మొత్తం ఖచ్చితత్వం (గరిష్ఠంగా 18 అంకెలు, 5 దశాంశ స్థానాలు).
- **కార్డినాలిటీ**: ప్రతి `PmtInf`కు కనీసం ఒక `CdtTrfTxInf`; ప్రతి డాక్యుమెంట్‌కు కనీసం ఒక `PmtInf`.
- **ఎన్యుమరేషన్ విలువలు**: క్రెడిట్ బదిలీలకు `PmtMtd` తప్పనిసరిగా `TRF` అయి ఉండాలి; `Ccy` తప్పనిసరిగా చెల్లుబాటు అయ్యే ISO 4217 కరెన్సీ కోడ్ అయి ఉండాలి.

ధృవీకరణ విఫలమైనప్పుడు, pain001 విఫలమైన XPath ఎక్స్‌ప్రెషన్, ఎలిమెంట్ పేరు మరియు పరిమితిని గుర్తించే lxml లోప సందేశంతో `ValidationError`ను లేవనెత్తుతుంది. ఇది తిరస్కరణ కోడ్‌లు సాధారణంగా తక్కువ వివరణాత్మకంగా ఉండే బ్యాంకుకు సమర్పించే సమయంలో కాకుండా, రూపొందించే సమయంలోనే తప్పు కాన్ఫిగరేషన్‌లను బహిర్గతం చేస్తుంది.

## SEPA vs CBPR+ కాన్ఫిగరేషన్

SEPA Credit Transfer (EPC SCT రూల్‌బుక్ కింద ISO 20022 pain.001.001.09) మరియు CBPR+ (SWIFT యొక్క Cross-Border Payments and Reporting Plus ప్రమాణం) ఒకే మెసేజ్ స్కీమాను ఉపయోగిస్తాయి కానీ తప్పనిసరి ఫీల్డ్ సెట్‌లు మరియు విలువ పరిమితులలో తేడా ఉంటాయి:

| అంశం | SEPA SCT | CBPR+ |
|---|---|---|
| కరెన్సీ | EUR మాత్రమే | బహుళ-కరెన్సీ |
| IBAN తప్పనిసరి | అవును | అవును (క్రెడిటర్) |
| BIC తప్పనిసరి | కాదు (SEPA జోన్ రూటింగ్) | అవును |
| ఛార్జ్ బేరర్ (`ChrgBr`) | `SLEV` | `DEBT`, `CRED`, లేదా `SHAR` |
| పరిధి | SEPA జోన్ (36 దేశాలు) | ప్రపంచ కరస్పాండెంట్ బ్యాంకింగ్ |

`payment_initiation_message_type` పరామితి ద్వారా మెసేజ్ రకాన్ని కాన్ఫిగర్ చేయండి:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

CBPR+ కంప్లయన్స్ SWIFT కరస్పాండెంట్ బ్యాంకింగ్‌కు ఇన్‌బౌండ్ మెసేజ్‌ల కోసం నవంబర్ 2023లో మరియు అవుట్‌బౌండ్ కోసం నవంబర్ 2025లో తప్పనిసరి అయ్యింది. CBPR+-అనుగుణమైన pain.001 ఫైళ్లను రూపొందించడానికి BIC ఫీల్డ్ నింపబడి ఉండాలి మరియు `ChrgBr` ఎలిమెంట్ ఉండాలి.

## తరచుగా అడిగే ప్రశ్నలు

**pain.001 మరియు pain.008 మధ్య తేడా ఏమిటి?**
pain.001 (CustomerCreditTransferInitiation) క్రెడిట్ బదిలీను ప్రారంభిస్తుంది — పంపేవారి బ్యాంక్ పంపేవారి ఖాతా నుండి డెబిట్ చేసి, స్వీకరించేవారికి క్రెడిట్ చేస్తుంది. pain.008 (CustomerDirectDebitInitiation) డైరెక్ట్ డెబిట్‌ను ప్రారంభిస్తుంది — క్రెడిటర్ బ్యాంక్ డెబ్టర్ నుండి నిధులను వసూలు చేస్తుంది. pain001 లైబ్రరీ pain.001 ఫైళ్లను మాత్రమే రూపొందిస్తుంది.

**pain001 ఏ ISO 20022 వెర్షన్‌ను లక్ష్యంగా చేసుకుంటుంది?**
ప్రధాన లక్ష్యం pain.001.001.09, ఇది CBPR+కి అవసరమైన వెర్షన్ మరియు కొత్త SEPA అమలుల కోసం EPC ద్వారా తప్పనిసరి చేయబడింది. పాత బ్యాంక్ ఇంటర్‌ఫేస్‌లను ఇంకా ఉపయోగిస్తున్న సంస్థల కోసం లైబ్రరీ `payment_initiation_message_type` పరామితి ద్వారా pain.001.001.03 (లెగసీ SEPA వెర్షన్)కు కూడా మద్దతు ఇస్తుంది.

**pain001 ఒకే ఫైల్‌లో బహుళ డెబ్టర్ ఖాతాలను నిర్వహించగలదా?**
అవును. వేర్వేరు డెబ్టర్ ఖాతా విలువలతో CSV వరుసలను సమూహపరచడం ద్వారా వేర్వేరు డెబ్టర్ IBANలతో బహుళ `PmtInf` బ్లాక్‌లను రూపొందించవచ్చు. pain001 ప్రతి ప్రత్యేక (డెబ్టర్ IBAN, అమలు తేదీ) కలయికకు ఒక `PmtInf` బ్లాక్‌ను సృష్టిస్తుంది, సరిపోలే అన్ని లావాదేవీలు `CdtTrfTxInf` పిల్లలుగా నెస్ట్ చేయబడతాయి.

**XSD validation విఫలమైనప్పుడు ఏమి జరుగుతుంది?**
pain001 lxml ధృవీకరణ సందేశంతో `pain001.exceptions.ValidationError`ను లేవనెత్తుతుంది. ధృవీకరణ విఫలమైనప్పుడు XML ఫైల్ డిస్క్‌కు వ్రాయబడదు, కాబట్టి చెల్లుబాటు అయ్యే ఫైళ్లు మాత్రమే అవుట్‌పుట్ పాత్‌కు చేరతాయి. సాధారణ వైఫల్య కారణాలు: తప్పు ఫార్మాట్‌లో IBAN, 8 లేదా 11 అక్షరాలు కాని BIC, ISO 4217లో లేని కరెన్సీ కోడ్, లేదా అవసరమైన CSV కాలమ్ లేనప్పుడు తప్పనిసరి ఎలిమెంట్‌లు లేకపోవడం.

## సూచనలు

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automate ISO 20022-Compliant Payment File Creation"
[01]: https://www.iso20022.org/ "ISO 20022: Universal financial industry message scheme"
