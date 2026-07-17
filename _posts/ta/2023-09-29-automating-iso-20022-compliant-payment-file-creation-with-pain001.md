---
title: "pain001 உடன் ISO 20022 கட்டண கோப்புகள் உருவாக்கத்தைத் தானியக்கமாக்குதல்"
tags: "pain001, ISO 20022, CustomerCreditTransferInitiation, SEPACreditTransfer, CBPR, payment automation, XMLGeneration, XSDValidation, SWIFT, post-quantum cryptography, AI, open source, cross-border payments, Rust"
subtitle: "pain001 உடன் ISO 20022 கட்டண தானியக்கம் மற்றும் மொத்த-கட்டண பொறியியல்."
description: "CSV அல்லது SQLite இலிருந்து ISO 20022 pain.001 கட்டண கோப்புகளை உருவாக்குவதைத் தானியக்கமாக்குங்கள். இணக்கத்தை எளிதாக்கும் திறந்த மூல Python நூலகம் pain001."
date: "Sep 29, 2023"
language: "ta"
locale: "ta_IN"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "பழுப்பு நிற மரமேசையின் மேல் அணைக்கப்பட்ட மடிக்கணினி"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA வரவு பரிமாற்றம், CBPR+, கட்டண தானியக்கம், XML உருவாக்கம், XSD சரிபார்ப்பு, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

> **நிர்வாகச் சுருக்கம் / முக்கியக் குறிப்புகள்**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) என்பது SEPA (EPC SCT விதிநூல்) மற்றும் CBPR+ (SWIFT இன் எல்லை தாண்டிய செய்தித்தொடர்பு தரநிலை, நவம்பர் 2025 முதல் தொடர்பாளர் வங்கிகளுக்குக் கட்டாயம்) கீழ் வரவு பரிமாற்றங்களைத் தொடங்கப் பயன்படும் கட்டமைக்கப்பட்ட XML செய்தி வடிவமாகும்.
> - **[pain001 ⧉][00]** CSV அல்லது SQLite இலிருந்து கட்டணத் தரவைப் படித்து, வரிசைகளை pain.001.001.09 செய்திப் படிநிலைக்கு (GrpHdr → PmtInf → CdtTrfTxInf) வரைபடமாக்கி, வார்ப்புரு-அடிப்படையிலான உருவாக்கி மூலம் இணக்கமான XML கோப்பை வழங்குகிறது — தரவிலிருந்து சரிபார்க்கப்பட்ட XML வரை மூன்று வரிகள் Python.
> - **XSD சரிபார்ப்பு** வெளியீடு எழுதப்படும் முன் உருவாக்கப்படும் ஒவ்வொரு கோப்பிலும் இயங்குகிறது; தோல்வியுறும் உறுப்பு, கார்டினாலிட்டி அல்லது வகைப் பொருந்தாமையை அடையாளப்படுத்தும் விளக்கமான விதிவிலக்கை நூலகம் எழுப்புகிறது, எனவே பிழைகள் வங்கிச் சமர்ப்பிப்பின்போது அல்ல, உருவாக்க நேரத்திலேயே பிடிக்கப்படுகின்றன.
> - **CtrlSum மற்றும் NbOfTxs** கைமுறையாக உள்ளிடப்படுவதில்லை, பரிவர்த்தனைத் தொகுப்பிலிருந்து கணக்கிடப்படுகின்றன — SEPA மற்றும் CBPR+ செயலாக்க நுழைவாயில்களில் மிகவும் பொதுவான கட்டண கோப்பு நிராகரிப்புக் காரணத்தை இது நீக்குகிறது.
> - **SEPA வரவு பரிமாற்றம்** (EUR, SEPA மண்டலத்திற்குள்) மற்றும் **CBPR+** (எல்லை தாண்டிய, பல-நாணய) செய்தி வகைகள் இரண்டுமே `message_type` அளபுருவின் மூலம் ஆதரிக்கப்படுகின்றன; புலம்-நிலை சரிபார்ப்பு வேறுபாடுகள் உள்ளகமாகக் கையாளப்படுகின்றன.

[**pain001 ⧉**][00] என்பது ISO 20022 கட்டணத் தொடக்கக் கோப்புகளை உருவாக்குவதற்கான திறந்த மூல Python நூலகமாகும். இது கட்டணத் தரவை ஒரு கட்டமைக்கப்பட்ட உள்ளீட்டிலிருந்து (CSV அல்லது SQLite) படித்து, தரவைச் சரிபார்த்து, இணக்கமான pain.001.001.09 XML ஆவணத்தை வழங்கி, வெளியீட்டை ISO 20022 XSD திட்டவரைவுக்கு எதிராகச் சரிபார்க்கிறது — இவை அனைத்தும் ஒரே செயற்பாட்டு அழைப்பில்.

இந்தக் கட்டுரை ISO 20022 pain.001 செய்தி அமைப்பு, pain001 உள்ளீட்டுத் தரவை செய்தி உறுப்புகளுக்கு எவ்வாறு வரைபடமாக்குகிறது, சரிபார்ப்புத் தொடர், மற்றும் SEPA எதிர் CBPR+ கட்டமைப்பு விருப்பங்கள் ஆகியவற்றை விவரிக்கிறது.

## ISO 20022 pain.001 செய்தி அமைப்பு

ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) செய்திக்கு மூன்று நிலைகள் உள்ளன:

**GrpHdr** (குழுத் தலைப்பு) — கோப்பொன்றுக்கு ஒன்று:

| உறுப்பு | விளக்கம் | எடுத்துக்காட்டு |
|---|---|---|
| `MsgId` | தனித்துவமான செய்தி அடையாளங்காட்டி | `ACME20240115-001` |
| `CreDtTm` | உருவாக்கிய தேதி மற்றும் நேரம் | `2024-01-15T09:00:00` |
| `NbOfTxs` | பரிவர்த்தனைகளின் மொத்த எண்ணிக்கை | `3` |
| `CtrlSum` | அறிவுறுத்தப்பட்ட அனைத்துத் தொகைகளின் கூட்டுத்தொகை | `15000.00` |
| `InitgPty/Nm` | தொடங்கும் தரப்பின் பெயர் | `Acme Corp` |

**PmtInf** (கட்டணத் தகவல்) — கோப்பொன்றுக்கு ஒன்று அல்லது அதற்கு மேற்பட்டவை, கடனாளி கணக்கு மற்றும் கட்டணத் தேதியின்படி பரிவர்த்தனைகளைக் குழுவாக்குகிறது:

| உறுப்பு | விளக்கம் |
|---|---|
| `PmtInfId` | கட்டணத் தகவல் அடையாளங்காட்டி |
| `PmtMtd` | கட்டண முறை — வரவு பரிமாற்றத்திற்கு எப்போதும் `TRF` |
| `ReqdExctnDt/Dt` | கோரப்பட்ட நிறைவேற்றுத் தேதி |
| `Dbtr/Nm` | கடனாளி (அனுப்புநர்) பெயர் |
| `DbtrAcct/Id/IBAN` | கடனாளியின் IBAN |
| `DbtrAgt/FinInstnId/BICFI` | கடனாளி வங்கியின் BIC |

**CdtTrfTxInf** (வரவு பரிமாற்றப் பரிவர்த்தனைத் தகவல்) — ஒவ்வொரு PmtInf தொகுதிக்கும் ஒன்று அல்லது அதற்கு மேற்பட்டவை:

| உறுப்பு | விளக்கம் |
|---|---|
| `PmtId/EndToEndId` | முனை-முதல்-முனை குறிப்பு (சங்கிலி முழுவதும் பாதுகாக்கப்படுகிறது) |
| `Amt/InstdAmt` | நாணயப் பண்புடன் அறிவுறுத்தப்பட்ட தொகை |
| `CdtrAgt/FinInstnId/BICFI` | வரவாளி வங்கியின் BIC |
| `Cdtr/Nm` | வரவாளி (பெறுநர்) பெயர் |
| `CdtrAcct/Id/IBAN` | வரவாளியின் IBAN |
| `RmtInf/Ustrd` | கட்டமைக்கப்படாத பணப்புரிதல் தகவல் (விலைப்பட்டியல் குறிப்பு போன்றவை) |

## CSV இலிருந்து XML உருவாக்குதல்

குறைந்தபட்ச pain001 அழைப்பு:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

CSV கோப்பு நெடுவரிசைப் பெயர்களை செய்தி புலங்களுக்கு வரைபடமாக்குகிறது. ஒரு குறைந்தபட்ச எடுத்துக்காட்டு:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

ஒற்றை-வரிசை கோப்புகளுக்கு நூலகம் `ctrl_sum` மற்றும் `nb_of_txs` ஐ CSV வரிசையிலிருந்து படிக்கிறது. பல-வரிசை கோப்புகளுக்கு (ஒரே தொகுதியில் பல பரிவர்த்தனைகள்), உள்ளீட்டு மதிப்புகளை நம்பாமல் pain001 இந்த மதிப்புகளைப் பரிவர்த்தனைத் தொகுப்பிலிருந்து கணக்கிடுகிறது, இது பொருந்தாமைகளைத் தடுக்கிறது.

SQLite இடைமுகம் அதே நெடுவரிசை-பெயர் மரபைப் பயன்படுத்துகிறது. `data_file_type="sqlite"` மற்றும் `data_file` பாதையை SQLite தரவுத்தளக் கோப்புக்கு அனுப்புங்கள்; pain001 இயல்பாக `payment` அட்டவணையைப் படிக்கிறது.

## உருவாக்கப்பட்ட XML அமைப்பு

மேலுள்ள CSV வரிசைக்கு சரியாக வழங்கப்பட்ட pain.001.001.09 ஆவணம்:

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

## XSD சரிபார்ப்புத் தொடர்

வழங்கிய பிறகு, pain001 வெளியீட்டை ISO 20022 pain.001.001.09 XSD திட்டவரைவுக்கு எதிராகச் சரிபார்க்கிறது. சரிபார்ப்புச் சோதனைகள்:

- **கட்டாய உறுப்பு இருப்பு**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, GrpHdr/CtrlSum அனைத்தும் தேவை; இவற்றில் ஏதேனும் இல்லாதிருந்தால் ஒரு சரிபார்ப்புப் பிழையை எழுப்புகிறது.
- **வகைக் கட்டுப்பாடுகள்**: IBAN வடிவம், BIC வடிவம் (8 அல்லது 11 எழுத்துகள்), தொகைத் துல்லியம் (அதிகபட்சம் 18 இலக்கங்கள், 5 தசம இடங்கள்).
- **கார்டினாலிட்டி**: ஒவ்வொரு `PmtInf` க்கும் குறைந்தது ஒரு `CdtTrfTxInf`; ஒவ்வொரு ஆவணத்திற்கும் குறைந்தது ஒரு `PmtInf`.
- **கணிப்பு மதிப்புகள்**: வரவு பரிமாற்றங்களுக்கு `PmtMtd` `TRF` ஆக இருக்க வேண்டும்; `Ccy` செல்லுபடியாகும் ISO 4217 நாணயக் குறியீடாக இருக்க வேண்டும்.

சரிபார்ப்பு தோல்வியடையும்போது, தோல்வியுறும் XPath வெளிப்பாடு, உறுப்பின் பெயர், மற்றும் கட்டுப்பாடு ஆகியவற்றை அடையாளப்படுத்தும் lxml பிழைச் செய்தியுடன் pain001 ஒரு `ValidationError` ஐ எழுப்புகிறது. இது தவறான கட்டமைப்புகளை, நிராகரிப்புக் குறியீடுகள் பொதுவாக குறைவான விளக்கத்துடன் இருக்கும் வங்கிச் சமர்ப்பிப்பின்போது அல்ல, உருவாக்க நேரத்திலேயே வெளிப்படுத்துகிறது.

## SEPA எதிர் CBPR+ கட்டமைப்பு

SEPA வரவு பரிமாற்றம் (EPC SCT விதிநூலின் கீழ் ISO 20022 pain.001.001.09) மற்றும் CBPR+ (SWIFT இன் Cross-Border Payments and Reporting Plus தரநிலை) ஒரே செய்தித் திட்டவரைவைப் பயன்படுத்துகின்றன, ஆனால் கட்டாயப் புலத் தொகுப்புகள் மற்றும் மதிப்புக் கட்டுப்பாடுகளில் வேறுபடுகின்றன:

| அம்சம் | SEPA SCT | CBPR+ |
|---|---|---|
| நாணயம் | EUR மட்டும் | பல-நாணயம் |
| IBAN கட்டாயம் | ஆம் | ஆம் (வரவாளி) |
| BIC கட்டாயம் | இல்லை (SEPA மண்டல வழிசெலுத்தல்) | ஆம் |
| கட்டணச் சுமையாளர் (`ChrgBr`) | `SLEV` | `DEBT`, `CRED`, அல்லது `SHAR` |
| எல்லை | SEPA மண்டலம் (36 நாடுகள்) | உலகளாவிய தொடர்பாளர் வங்கிச் சேவை |

`payment_initiation_message_type` அளபுருவின் மூலம் செய்தி வகையைக் கட்டமைக்கவும்:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

CBPR+ இணக்கம் SWIFT தொடர்பாளர் வங்கிச் சேவைக்கு உள்வரும் செய்திகளுக்கு நவம்பர் 2023 இலும், வெளிச்செல்லும் செய்திகளுக்கு நவம்பர் 2025 இலும் கட்டாயமாகியது. CBPR+-இணக்கமான pain.001 கோப்புகளை உருவாக்க, BIC புலம் நிரப்பப்பட்டிருக்க வேண்டும், மேலும் `ChrgBr` உறுப்பு இருக்க வேண்டும்.

## அடிக்கடி கேட்கப்படும் கேள்விகள்

**pain.001 மற்றும் pain.008 க்கு இடையே உள்ள வேறுபாடு என்ன?**
pain.001 (CustomerCreditTransferInitiation) ஒரு வரவு பரிமாற்றத்தைத் தொடங்குகிறது — அனுப்புநரின் வங்கி அனுப்புநரின் கணக்கிலிருந்து பற்று வைத்து பெறுநருக்கு வரவு வைக்கிறது. pain.008 (CustomerDirectDebitInitiation) ஒரு நேரடிப் பற்றைத் தொடங்குகிறது — வரவாளியின் வங்கி கடனாளியிடமிருந்து நிதியைச் சேகரிக்கிறது. pain001 நூலகம் pain.001 கோப்புகளை மட்டுமே உருவாக்குகிறது.

**pain001 எந்த ISO 20022 பதிப்பை இலக்காகக் கொண்டுள்ளது?**
முதன்மை இலக்கு pain.001.001.09 ஆகும், இது CBPR+ க்குத் தேவைப்படும் மற்றும் புதிய SEPA அமலாக்கங்களுக்கு EPC ஆல் கட்டாயமாக்கப்பட்ட பதிப்பாகும். பழைய வங்கி இடைமுகங்களை இன்னும் பயன்படுத்தும் நிறுவனங்களுக்காக `payment_initiation_message_type` அளபுருவின் மூலம் நூலகம் pain.001.001.03 (பாரம்பரிய SEPA பதிப்பு) ஐயும் ஆதரிக்கிறது.

**ஒரே கோப்பில் பல கடனாளி கணக்குகளை pain001 கையாள முடியுமா?**
ஆம். வெவ்வேறு கடனாளி கணக்கு மதிப்புகளைக் கொண்ட CSV வரிசைகளைக் குழுவாக்குவதன் மூலம் வெவ்வேறு கடனாளி IBAN களைக் கொண்ட பல `PmtInf` தொகுதிகளை உருவாக்க முடியும். ஒவ்வொரு தனித்துவமான (கடனாளி IBAN, நிறைவேற்றுத் தேதி) சேர்க்கைக்கும் pain001 ஒரு `PmtInf` தொகுதியை உருவாக்குகிறது, பொருந்தும் அனைத்துப் பரிவர்த்தனைகளும் `CdtTrfTxInf` குழந்தைகளாக உள்ளடக்கப்படுகின்றன.

**XSD சரிபார்ப்பு தோல்வியடையும்போது என்ன நடக்கும்?**
lxml சரிபார்ப்புச் செய்தியுடன் pain001 ஒரு `pain001.exceptions.ValidationError` ஐ எழுப்புகிறது. சரிபார்ப்பு தோல்வியடையும்போது XML கோப்பு வட்டில் எழுதப்படாது, எனவே செல்லுபடியாகும் கோப்புகள் மட்டுமே வெளியீட்டுப் பாதையை அடைகின்றன. பொதுவான தோல்விக் காரணங்கள்: தவறான வடிவத்தில் IBAN, 8 அல்லது 11 எழுத்துகள் இல்லாத BIC, ISO 4217 இல் இல்லாத நாணயக் குறியீடு, அல்லது தேவையான CSV நெடுவரிசை இல்லாதபோது கட்டாய உறுப்புகள் விடுபடுதல்.

## குறிப்புகள்

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automate ISO 20022-Compliant Payment File Creation"
[01]: https://www.iso20022.org/ "ISO 20022: Universal financial industry message scheme"
