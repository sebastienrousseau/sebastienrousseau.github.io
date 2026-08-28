---
title: "pain001 सह ISO 20022 पेमेंट फाइल्स निर्मितीचे स्वयंचलन"
tags: "pain001, ISO 20022, CustomerCreditTransferInitiation, SEPACreditTransfer, CBPR, payment automation, XMLGeneration, XSDValidation, SWIFT, post-quantum cryptography, AI, open source, cross-border payments, Rust"
subtitle: "pain001 सह ISO 20022 पेमेंट स्वयंचलन आणि होलसेल-पेमेंट्स अभियांत्रिकी."
description: "CSV किंवा SQLite वरून ISO 20022 pain.001 पेमेंट फाइल्सची निर्मिती स्वयंचलित करा. pain001 ही ओपन-सोर्स Python लायब्ररी अनुपालन सुलभ करते."
date: "Sep 29, 2023"
language: "mr"
locale: "mr_IN"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "तपकिरी लाकडी टेबलावर ठेवलेला बंद केलेला लॅपटॉप संगणक"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Credit Transfer, CBPR+, पेमेंट स्वयंचलन, XML निर्मिती, XSD प्रमाणीकरण, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

> **कार्यकारी सारांश / मुख्य मुद्दे**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) हे SEPA (EPC SCT रूलबुक) आणि CBPR+ (SWIFT चे सीमापार संदेशवहन मानक, जे नोव्हेंबर 2025 पासून कॉरस्पॉन्डंट बँकांसाठी अनिवार्य आहे) अंतर्गत क्रेडिट ट्रान्सफर सुरू करण्यासाठी वापरले जाणारे संरचित XML संदेश स्वरूप आहे.
> - **[pain001 ⧉][00]** CSV किंवा SQLite वरून पेमेंट डेटा वाचते, ओळींना pain.001.001.09 संदेश श्रेणीक्रमाशी (GrpHdr → PmtInf → CdtTrfTxInf) मॅप करते, आणि टेम्प्लेट-आधारित जनरेटरद्वारे अनुरूप XML फाइल रेंडर करते — डेटापासून प्रमाणित XML पर्यंत तीन ओळींचे Python.
> - **XSD प्रमाणीकरण** आउटपुट लिहिण्यापूर्वी प्रत्येक निर्मित फाइलवर चालते; लायब्ररी अपयशी घटक, कार्डिनॅलिटी, किंवा प्रकार-विसंगती ओळखणारा वर्णनात्मक अपवाद उभा करते, जेणेकरून त्रुटी बँकेकडे सादरीकरणाच्या वेळेऐवजी निर्मितीच्या वेळीच पकडल्या जातात.
> - **CtrlSum आणि NbOfTxs** व्यवहार-संचावरून मोजले जातात, हाताने प्रविष्ट केले जात नाहीत — SEPA आणि CBPR+ प्रक्रिया गेटवेवरील पेमेंट फाइल नाकारल्या जाण्याचे सर्वात सामान्य एकमेव कारण दूर करून.
> - **SEPA Credit Transfer** (EUR, SEPA क्षेत्रात) आणि **CBPR+** (सीमापार, बहु-चलन) या दोन्ही संदेश प्रकारांना `message_type` पॅरामीटरद्वारे समर्थन दिले जाते, आणि फील्ड-स्तरीय प्रमाणीकरणातील फरक अंतर्गतरित्या हाताळले जातात.

[**pain001 ⧉**][00] ही ISO 20022 पेमेंट इनिशिएशन फाइल्स तयार करण्यासाठीची एक ओपन-सोर्स Python लायब्ररी आहे. ती एका संरचित इनपुट (CSV किंवा SQLite) वरून पेमेंट डेटा वाचते, डेटा प्रमाणित करते, एक अनुरूप pain.001.001.09 XML दस्तऐवज रेंडर करते, आणि आउटपुटला ISO 20022 XSD स्कीमाच्या विरुद्ध प्रमाणित करते — हे सर्व एकाच फंक्शन कॉलमध्ये.

हा लेख ISO 20022 pain.001 संदेश रचना, pain001 इनपुट डेटाला संदेश घटकांशी कशी मॅप करते, प्रमाणीकरण पाइपलाइन, आणि SEPA विरुद्ध CBPR+ कॉन्फिगरेशन पर्याय यांचे वर्णन करतो.

## ISO 20022 pain.001 संदेश रचना

ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) संदेशाला तीन स्तर असतात:

**GrpHdr** (Group Header) — प्रति फाइल एक:

| घटक | वर्णन | उदाहरण |
|---|---|---|
| `MsgId` | अद्वितीय संदेश ओळखकर्ता | `ACME20240115-001` |
| `CreDtTm` | निर्मिती दिनांक आणि वेळ | `2024-01-15T09:00:00` |
| `NbOfTxs` | व्यवहारांची एकूण संख्या | `3` |
| `CtrlSum` | सर्व निर्देशित रकमांची बेरीज | `15000.00` |
| `InitgPty/Nm` | सुरू करणाऱ्या पक्षाचे नाव | `Acme Corp` |

**PmtInf** (Payment Information) — प्रति फाइल एक किंवा अधिक, व्यवहारांना डेबिटर खाते आणि पेमेंट दिनांकानुसार गटबद्ध करते:

| घटक | वर्णन |
|---|---|
| `PmtInfId` | पेमेंट माहिती ओळखकर्ता |
| `PmtMtd` | पेमेंट पद्धत — क्रेडिट ट्रान्सफरसाठी नेहमी `TRF` |
| `ReqdExctnDt/Dt` | विनंती केलेला अंमलबजावणी दिनांक |
| `Dbtr/Nm` | डेबिटर (पाठवणारा) नाव |
| `DbtrAcct/Id/IBAN` | डेबिटर IBAN |
| `DbtrAgt/FinInstnId/BICFI` | डेबिटर बँकेचा BIC |

**CdtTrfTxInf** (Credit Transfer Transaction Information) — प्रति PmtInf ब्लॉक एक किंवा अधिक:

| घटक | वर्णन |
|---|---|
| `PmtId/EndToEndId` | एंड-टू-एंड संदर्भ (साखळीभर जपला जातो) |
| `Amt/InstdAmt` | चलन विशेषतेसह निर्देशित रक्कम |
| `CdtrAgt/FinInstnId/BICFI` | क्रेडिटर बँकेचा BIC |
| `Cdtr/Nm` | क्रेडिटर (प्राप्तकर्ता) नाव |
| `CdtrAcct/Id/IBAN` | क्रेडिटर IBAN |
| `RmtInf/Ustrd` | असंरचित रेमिटन्स माहिती (इनव्हॉइस संदर्भ इत्यादी) |

## CSV वरून XML तयार करणे

एक किमान pain001 इन्व्होकेशन:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

CSV फाइल स्तंभ-नावांना संदेश-फील्ड्सशी मॅप करते. एक किमान उदाहरण:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

एकल-ओळ फाइल्ससाठी लायब्ररी CSV ओळीतून `ctrl_sum` आणि `nb_of_txs` वाचते. बहु-ओळ फाइल्ससाठी (एका बॅचमध्ये अनेक व्यवहार), pain001 इनपुट मूल्यांवर विसंबून न राहता ही मूल्ये व्यवहार-संचावरून मोजते, ज्यामुळे विसंगती टाळल्या जातात.

SQLite इंटरफेस तेच स्तंभ-नाव संमेलन वापरतो. `data_file_type="sqlite"` आणि `data_file` मार्ग एका SQLite डेटाबेस फाइलकडे द्या; pain001 पूर्वनिर्धारितपणे `payment` टेबल वाचते.

## निर्मित XML रचना

वरील CSV ओळीसाठी योग्यरित्या रेंडर केलेला pain.001.001.09 दस्तऐवज:

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

## XSD प्रमाणीकरण पाइपलाइन

रेंडरिंगनंतर, pain001 आउटपुटला ISO 20022 pain.001.001.09 XSD स्कीमाच्या विरुद्ध प्रमाणित करते. प्रमाणीकरण तपासणी:

- **अनिवार्य घटकांची उपस्थिती**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, GrpHdr/CtrlSum हे सर्व आवश्यक आहेत; यापैकी कोणतेही गहाळ असल्यास प्रमाणीकरण त्रुटी उभी होते.
- **प्रकार निर्बंध**: IBAN स्वरूप, BIC स्वरूप (8 किंवा 11 वर्ण), रक्कम अचूकता (कमाल 18 अंक, 5 दशांश स्थाने).
- **कार्डिनॅलिटी**: प्रति `PmtInf` किमान एक `CdtTrfTxInf`; प्रति दस्तऐवज किमान एक `PmtInf`.
- **गणन मूल्ये**: क्रेडिट ट्रान्सफरसाठी `PmtMtd` हे `TRF` असणे आवश्यक; `Ccy` हे वैध ISO 4217 चलन कोड असणे आवश्यक.

प्रमाणीकरण अपयशी झाल्यास, pain001 अपयशी XPath अभिव्यक्ती, घटक-नाव, आणि निर्बंध ओळखणाऱ्या lxml त्रुटी-संदेशासह एक `ValidationError` उभा करते. यामुळे चुकीचे कॉन्फिगरेशन बँकेकडे सादरीकरणाच्या वेळेऐवजी निर्मितीच्या वेळीच समोर येतात, जिथे नकार-कोड सहसा कमी वर्णनात्मक असतात.

## SEPA विरुद्ध CBPR+ कॉन्फिगरेशन

SEPA Credit Transfer (EPC SCT रूलबुक अंतर्गत ISO 20022 pain.001.001.09) आणि CBPR+ (SWIFT चे Cross-Border Payments and Reporting Plus मानक) एकच संदेश स्कीमा वापरतात परंतु अनिवार्य फील्ड-संच आणि मूल्य-निर्बंधांमध्ये भिन्न असतात:

| पैलू | SEPA SCT | CBPR+ |
|---|---|---|
| चलन | फक्त EUR | बहु-चलन |
| IBAN अनिवार्य | होय | होय (क्रेडिटर) |
| BIC अनिवार्य | नाही (SEPA क्षेत्र राउटिंग) | होय |
| शुल्क वाहक (`ChrgBr`) | `SLEV` | `DEBT`, `CRED`, किंवा `SHAR` |
| व्याप्ती | SEPA क्षेत्र (36 देश) | जागतिक कॉरस्पॉन्डंट बँकिंग |

`payment_initiation_message_type` पॅरामीटरद्वारे संदेश प्रकार कॉन्फिगर करा:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

CBPR+ अनुपालन SWIFT कॉरस्पॉन्डंट बँकिंगसाठी इनबाउंड संदेशांकरिता नोव्हेंबर 2023 पासून आणि आउटबाउंडकरिता नोव्हेंबर 2025 पासून अनिवार्य झाले. CBPR+-अनुरूप pain.001 फाइल्स तयार करण्यासाठी BIC फील्ड भरलेले असणे आणि `ChrgBr` घटक उपस्थित असणे आवश्यक आहे.

## वारंवार विचारले जाणारे प्रश्न

**pain.001 आणि pain.008 यांच्यात काय फरक आहे?**
pain.001 (CustomerCreditTransferInitiation) एक क्रेडिट ट्रान्सफर सुरू करते — पाठवणाऱ्याची बँक पाठवणाऱ्याच्या खात्यातून रक्कम डेबिट करते आणि प्राप्तकर्त्याला क्रेडिट करते. pain.008 (CustomerDirectDebitInitiation) एक डायरेक्ट डेबिट सुरू करते — क्रेडिटरची बँक डेबिटरकडून निधी वसूल करते. pain001 ही लायब्ररी फक्त pain.001 फाइल्स तयार करते.

**pain001 कोणत्या ISO 20022 आवृत्तीला लक्ष्य करते?**
प्राथमिक लक्ष्य pain.001.001.09 आहे, जी CBPR+ साठी आवश्यक आणि EPC ने नवीन SEPA अंमलबजावणीसाठी अनिवार्य केलेली आवृत्ती आहे. जुन्या बँक इंटरफेसचा वापर करणाऱ्या संस्थांसाठी लायब्ररी `payment_initiation_message_type` पॅरामीटरद्वारे pain.001.001.03 (जुनी SEPA आवृत्ती) लाही समर्थन देते.

**pain001 एका फाइलमध्ये अनेक डेबिटर खाती हाताळू शकते का?**
होय. वेगवेगळ्या डेबिटर खाते मूल्यांसह CSV ओळी गटबद्ध करून वेगवेगळ्या डेबिटर IBAN असलेले अनेक `PmtInf` ब्लॉक तयार करता येतात. pain001 प्रत्येक अद्वितीय (डेबिटर IBAN, अंमलबजावणी दिनांक) संयोजनासाठी एक `PmtInf` ब्लॉक तयार करते, आणि जुळणारे सर्व व्यवहार `CdtTrfTxInf` उपघटक म्हणून त्यात नेस्ट केले जातात.

**XSD प्रमाणीकरण अपयशी झाल्यास काय होते?**
pain001 lxml प्रमाणीकरण संदेशासह एक `pain001.exceptions.ValidationError` उभा करते. प्रमाणीकरण अपयशी झाल्यास XML फाइल डिस्कवर लिहिली जात नाही, त्यामुळे फक्त वैध फाइल्सच आउटपुट मार्गापर्यंत पोहोचतात. सामान्य अपयश कारणे अशी आहेत: चुकीच्या स्वरूपातील IBAN, 8 किंवा 11 वर्ण नसलेला BIC, ISO 4217 मध्ये नसलेला चलन कोड, किंवा आवश्यक CSV स्तंभ अनुपस्थित असताना गहाळ अनिवार्य घटक.

## संदर्भ

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automate ISO 20022-Compliant Payment File Creation"
[01]: https://www.iso20022.org/ "ISO 20022: Universal financial industry message scheme"
