---
title: "خودکارسازی ساخت فایل‌های پرداخت ISO 20022 با pain001"
tags: "pain001, ISO 20022, CustomerCreditTransferInitiation, SEPACreditTransfer, CBPR, payment automation, XMLGeneration, XSDValidation, SWIFT, post-quantum cryptography, AI, open source, cross-border payments, Rust"
subtitle: "خودکارسازی پرداخت ISO 20022 و مهندسی پرداخت‌های عمده با pain001."
description: "ساخت فایل‌های پرداخت ISO 20022 pain.001 را از CSV یا SQLite خودکار کنید. pain001 کتابخانهٔ متن‌باز پایتون است که انطباق را ساده می‌کند."
date: "Sep 29, 2023"
language: "fa"
locale: "fa_IR"
banner: "https://cloudcdn.pro/stocks/images/andrea-de-santis-T3Qen8vVgRc.webp"
banner_alt: "رایانه لپ‌تاپ خاموش روی میز چوبی قهوه‌ای"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, انتقال اعتباری SEPA, CBPR+, خودکارسازی پرداخت, تولید XML, اعتبارسنجی XSD, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---

> **خلاصهٔ مدیریتی / نکات کلیدی**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation) قالب پیام XML ساختاریافته‌ای است که برای آغاز انتقال‌های اعتباری تحت SEPA (کتاب قواعد EPC SCT) و CBPR+ (استاندارد پیام‌رسانی فرامرزی SWIFT، که از نوامبر ۲۰۲۵ برای بانک‌های کارگزار الزامی است) به کار می‌رود.
> - **[pain001 ⧉][00]** داده‌های پرداخت را از CSV یا SQLite می‌خواند، ردیف‌ها را به سلسله‌مراتب پیام pain.001.001.09 (GrpHdr ← PmtInf ← CdtTrfTxInf) نگاشت می‌کند و از طریق یک مولد قالب‌محور یک فایل XML منطبق تولید می‌کند — سه خط پایتون از داده تا XML اعتبارسنجی‌شده.
> - **اعتبارسنجی XSD** پیش از نوشتن خروجی روی هر فایل تولیدشده اجرا می‌شود؛ کتابخانه یک استثنای توصیفی صادر می‌کند که عنصر ناموفق، تعداد رخداد (cardinality) یا ناهمخوانی نوع را مشخص می‌کند، تا خطاها در زمان تولید گرفته شوند نه هنگام ارسال به بانک.
> - **CtrlSum و NbOfTxs** از مجموعهٔ تراکنش‌ها محاسبه می‌شوند نه به‌صورت دستی وارد — که رایج‌ترین علت رد فایل پرداخت را در دروازه‌های پردازش SEPA و CBPR+ از میان برمی‌دارد.
> - هر دو گونهٔ پیام **انتقال اعتباری SEPA** (یورو، درون منطقهٔ SEPA) و **CBPR+** (فرامرزی، چندارزی) از طریق پارامتر `message_type` پشتیبانی می‌شوند و تفاوت‌های اعتبارسنجی در سطح فیلد به‌صورت داخلی مدیریت می‌شود.

[**pain001 ⧉**][00] یک کتابخانهٔ متن‌باز پایتون برای تولید فایل‌های آغازگری پرداخت ISO 20022 است. داده‌های پرداخت را از یک ورودی ساختاریافته (CSV یا SQLite) می‌خواند، داده‌ها را اعتبارسنجی می‌کند، یک سند XML منطبق با pain.001.001.09 را رندر می‌کند و خروجی را در برابر شمای XSD مربوط به ISO 20022 اعتبارسنجی می‌کند — همه در یک فراخوانی تابع واحد.

این مقاله ساختار پیام ISO 20022 pain.001، نحوهٔ نگاشت داده‌های ورودی به عناصر پیام توسط pain001، خط لولهٔ اعتبارسنجی و گزینه‌های پیکربندی SEPA در برابر CBPR+ را شرح می‌دهد.

## ساختار پیام ISO 20022 pain.001

پیام ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) سه سطح دارد:

**GrpHdr** (سرآیند گروه) — یکی به‌ازای هر فایل:

| عنصر | توضیح | نمونه |
|---|---|---|
| `MsgId` | شناسهٔ یکتای پیام | `ACME20240115-001` |
| `CreDtTm` | تاریخ و زمان ایجاد | `2024-01-15T09:00:00` |
| `NbOfTxs` | تعداد کل تراکنش‌ها | `3` |
| `CtrlSum` | مجموع همهٔ مبالغ دستوری | `15000.00` |
| `InitgPty/Nm` | نام طرف آغازگر | `Acme Corp` |

**PmtInf** (اطلاعات پرداخت) — یک یا چند مورد به‌ازای هر فایل، تراکنش‌ها را بر اساس حساب بدهکار و تاریخ پرداخت گروه‌بندی می‌کند:

| عنصر | توضیح |
|---|---|
| `PmtInfId` | شناسهٔ اطلاعات پرداخت |
| `PmtMtd` | روش پرداخت — همواره `TRF` برای انتقال اعتباری |
| `ReqdExctnDt/Dt` | تاریخ اجرای درخواست‌شده |
| `Dbtr/Nm` | نام بدهکار (فرستنده) |
| `DbtrAcct/Id/IBAN` | IBAN بدهکار |
| `DbtrAgt/FinInstnId/BICFI` | BIC بانک بدهکار |

**CdtTrfTxInf** (اطلاعات تراکنش انتقال اعتباری) — یک یا چند مورد به‌ازای هر بلوک PmtInf:

| عنصر | توضیح |
|---|---|
| `PmtId/EndToEndId` | مرجع سرتاسری (که در طول زنجیره حفظ می‌شود) |
| `Amt/InstdAmt` | مبلغ دستوری همراه با ویژگی ارز |
| `CdtrAgt/FinInstnId/BICFI` | BIC بانک بستانکار |
| `Cdtr/Nm` | نام بستانکار (گیرنده) |
| `CdtrAcct/Id/IBAN` | IBAN بستانکار |
| `RmtInf/Ustrd` | اطلاعات حواله بدون ساختار (مرجع فاکتور و غیره) |

## تولید XML از CSV

یک فراخوانی کمینهٔ pain001:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

فایل CSV نام ستون‌ها را به فیلدهای پیام نگاشت می‌کند. یک نمونهٔ کمینه:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

کتابخانه برای فایل‌های تک‌ردیفی مقادیر `ctrl_sum` و `nb_of_txs` را از ردیف CSV می‌خواند. برای فایل‌های چندردیفی (چند تراکنش در یک دسته)، pain001 این مقادیر را به‌جای اعتماد به مقادیر ورودی، از مجموعهٔ تراکنش‌ها محاسبه می‌کند که مانع از ناهمخوانی می‌شود.

رابط SQLite از همان قرارداد نام ستون استفاده می‌کند. مقدار `data_file_type="sqlite"` و مسیر `data_file` به یک فایل پایگاه‌دادهٔ SQLite را ارسال کنید؛ pain001 به‌طور پیش‌فرض جدول `payment` را می‌خواند.

## ساختار XML تولیدشده

یک سند pain.001.001.09 که برای ردیف CSV بالا به‌درستی رندر شده است:

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

## خط لولهٔ اعتبارسنجی XSD

پس از رندر، pain001 خروجی را در برابر شمای XSD مربوط به ISO 20022 pain.001.001.09 اعتبارسنجی می‌کند. بررسی‌های اعتبارسنجی:

- **حضور عناصر اجباری**: GrpHdr/MsgId، GrpHdr/CreDtTm، GrpHdr/NbOfTxs، GrpHdr/CtrlSum همگی الزامی‌اند؛ نبود هر یک خطای اعتبارسنجی ایجاد می‌کند.
- **محدودیت‌های نوع**: قالب IBAN، قالب BIC (۸ یا ۱۱ نویسه)، دقت مبلغ (حداکثر ۱۸ رقم، ۵ رقم اعشار).
- **تعداد رخداد (cardinality)**: دست‌کم یک `CdtTrfTxInf` به‌ازای هر `PmtInf`؛ دست‌کم یک `PmtInf` به‌ازای هر سند.
- **مقادیر شمارشی**: `PmtMtd` باید برای انتقال‌های اعتباری `TRF` باشد؛ `Ccy` باید یک کد ارز معتبر ISO 4217 باشد.

هنگام شکست اعتبارسنجی، pain001 یک `ValidationError` همراه با پیام خطای lxml صادر می‌کند که عبارت XPath ناموفق، نام عنصر و محدودیت را مشخص می‌کند. این کار پیکربندی‌های نادرست را در زمان تولید آشکار می‌کند نه هنگام ارسال به بانک، جایی که کدهای رد معمولاً کمتر توصیفی‌اند.

## پیکربندی SEPA در برابر CBPR+

انتقال اعتباری SEPA (ISO 20022 pain.001.001.09 تحت کتاب قواعد EPC SCT) و CBPR+ (استاندارد Cross-Border Payments and Reporting Plus شرکت SWIFT) از یک شمای پیام یکسان استفاده می‌کنند اما در مجموعه فیلدهای اجباری و محدودیت‌های مقدار تفاوت دارند:

| جنبه | SEPA SCT | CBPR+ |
|---|---|---|
| ارز | فقط یورو | چندارزی |
| IBAN اجباری | بله | بله (بستانکار) |
| BIC اجباری | خیر (مسیریابی درون منطقهٔ SEPA) | بله |
| متحمل‌شوندهٔ کارمزد (`ChrgBr`) | `SLEV` | `DEBT`، `CRED` یا `SHAR` |
| دامنه | منطقهٔ SEPA (۳۶ کشور) | بانکداری کارگزار جهانی |

نوع پیام را از طریق پارامتر `payment_initiation_message_type` پیکربندی کنید:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # default; also accepts "pain.001.001.03" for legacy SEPA
)
```

انطباق با CBPR+ برای بانکداری کارگزار SWIFT در نوامبر ۲۰۲۳ برای پیام‌های ورودی و در نوامبر ۲۰۲۵ برای پیام‌های خروجی الزامی شد. تولید فایل‌های pain.001 منطبق با CBPR+ مستلزم آن است که فیلد BIC پر شده باشد و عنصر `ChrgBr` حاضر باشد.

## پرسش‌های پرتکرار

**تفاوت میان pain.001 و pain.008 چیست؟**
pain.001 (CustomerCreditTransferInitiation) یک انتقال اعتباری را آغاز می‌کند — بانک فرستنده از حساب فرستنده برداشت و به حساب گیرنده واریز می‌کند. pain.008 (CustomerDirectDebitInitiation) یک برداشت مستقیم را آغاز می‌کند — بانک بستانکار وجوه را از بدهکار جمع‌آوری می‌کند. کتابخانهٔ pain001 تنها فایل‌های pain.001 را تولید می‌کند.

**pain001 کدام نسخهٔ ISO 20022 را هدف قرار می‌دهد؟**
هدف اصلی pain.001.001.09 است، نسخه‌ای که برای CBPR+ لازم است و توسط EPC برای پیاده‌سازی‌های جدید SEPA الزامی شده است. کتابخانه همچنین از pain.001.001.03 (نسخهٔ قدیمی SEPA) از طریق پارامتر `payment_initiation_message_type` برای سازمان‌هایی که هنوز از رابط‌های بانکی قدیمی‌تر استفاده می‌کنند پشتیبانی می‌کند.

**آیا pain001 می‌تواند چند حساب بدهکار را در یک فایل واحد مدیریت کند؟**
بله. با گروه‌بندی ردیف‌های CSV دارای مقادیر حساب بدهکار متفاوت، می‌توان چند بلوک `PmtInf` با IBANهای بدهکار مختلف تولید کرد. pain001 به‌ازای هر ترکیب یکتای (IBAN بدهکار، تاریخ اجرا) یک بلوک `PmtInf` می‌سازد که همهٔ تراکنش‌های منطبق به‌صورت فرزندان `CdtTrfTxInf` در آن تودرتو قرار می‌گیرند.

**هنگام شکست اعتبارسنجی XSD چه اتفاقی می‌افتد؟**
pain001 یک `pain001.exceptions.ValidationError` همراه با پیام اعتبارسنجی lxml صادر می‌کند. هنگام شکست اعتبارسنجی، فایل XML روی دیسک نوشته نمی‌شود، بنابراین تنها فایل‌های معتبر به مسیر خروجی می‌رسند. علل رایج شکست عبارت‌اند از: IBAN در قالب نادرست، BIC که ۸ یا ۱۱ نویسه نیست، کد ارزی که در ISO 4217 نیست، یا نبود عناصر اجباری هنگامی که یک ستون CSV لازم غایب باشد.

## منابع

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: Automate ISO 20022-Compliant Payment File Creation"
[01]: https://www.iso20022.org/ "ISO 20022: Universal financial industry message scheme"
