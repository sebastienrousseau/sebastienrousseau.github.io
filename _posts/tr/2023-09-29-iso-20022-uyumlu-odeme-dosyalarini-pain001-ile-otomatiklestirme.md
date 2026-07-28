---
title: "ISO 20022 uyumlu ödeme dosyalarını pain001 ile otomatikleştirme"
subtitle: "pain001 ile ISO 20022 ödeme otomasyonu ve toptan ödeme mühendisliği."
description: "CSV veya SQLite kaynaklarından ISO 20022 pain.001 ödeme dosyalarının oluşturulmasını otomatikleştirin. pain001, uyumu kolaylaştıran açık kaynaklı Python kütüphanesidir."
date: "Sep 29, 2023"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Yapılandırılmış ödeme verilerinin ekran görüntüsü"
keywords: "pain001, ISO 20022, pain.001.001.09, CustomerCreditTransferInitiation, SEPA Kredi Transferi, CBPR+, ödeme otomasyonu, XML üretimi, XSD doğrulama, GrpHdr, PmtInf, CdtTrfTxInf, CtrlSum, SWIFT"
---


> **Yönetici Özeti / Önemli Çıkarımlar**
>
> - **ISO 20022 pain.001** (CustomerCreditTransferInitiation), SEPA (EPC SCT kural kitabı) ve CBPR+ (SWIFT'in sınır ötesi mesajlaşma standardı; muhabir bankalar için Kasım 2025'ten itibaren zorunlu) kapsamında kredi transferlerini başlatmak için kullanılan yapılandırılmış XML mesaj biçimidir.
> - **[pain001 ⧉][00]**, ödeme verilerini CSV veya SQLite'tan okur, satırları pain.001.001.09 mesaj hiyerarşisine (GrpHdr → PmtInf → CdtTrfTxInf) eşler ve şablon tabanlı bir üreticiyle uyumlu bir XML dosyası oluşturur. Veriden doğrulanmış XML'e üç satır Python.
> - **XSD doğrulaması**, çıktı yazılmadan önce üretilen her dosyada çalışır; kütüphane, başarısız olan öğeyi, kardinaliteyi veya tür uyuşmazlığını tanımlayan açıklayıcı bir istisna fırlatır; böylece hatalar banka gönderiminde değil üretim anında yakalanır.
> - **CtrlSum ve NbOfTxs** elle girilmez, işlem kümesinden hesaplanır. Bu, SEPA ve CBPR+ işleme ağ geçitlerinde en yaygın ödeme dosyası reddi nedenini ortadan kaldırır.
> - Hem **SEPA Kredi Transferi** (SEPA bölgesi içinde EUR) hem de **CBPR+** (sınır ötesi, çoklu para birimi) mesaj varyantları `message_type` parametresi aracılığıyla desteklenir ve alan düzeyindeki doğrulama farkları dahili olarak ele alınır.

[**pain001 ⧉**][00], ISO 20022 ödeme başlatma dosyaları üretmeye yönelik açık kaynaklı bir Python kütüphanesidir. Yapılandırılmış bir girdiden (CSV veya SQLite) ödeme verilerini okur, verileri doğrular, uyumlu bir pain.001.001.09 XML belgesi oluşturur ve çıktıyı ISO 20022 XSD şemasına göre doğrular. Tümü tek bir fonksiyon çağrısında gerçekleşir.

Bu makale, ISO 20022 pain.001 mesaj yapısını, pain001'in girdi verilerini mesaj öğelerine nasıl eşlediğini, doğrulama hattını ve SEPA'ya karşı CBPR+ yapılandırma seçeneklerini açıklar.

## ISO 20022 pain.001 Mesaj Yapısı

ISO 20022 pain.001.001.09 (CustomerCreditTransferInitiation) mesajının üç düzeyi vardır:

**GrpHdr** (Group Header), dosya başına bir adet:

| Öğe | Açıklama | Örnek |
|---|---|---|
| `MsgId` | Benzersiz mesaj tanımlayıcısı | `ACME20240115-001` |
| `CreDtTm` | Oluşturma tarihi ve saati | `2024-01-15T09:00:00` |
| `NbOfTxs` | Toplam işlem sayısı | `3` |
| `CtrlSum` | Talimat verilen tutarların toplamı | `15000.00` |
| `InitgPty/Nm` | Başlatan taraf adı | `Acme Corp` |

**PmtInf** (Payment Information), dosya başına bir veya daha fazla; işlemleri borçlu hesabına ve ödeme tarihine göre gruplar:

| Öğe | Açıklama |
|---|---|
| `PmtInfId` | Ödeme bilgisi tanımlayıcısı |
| `PmtMtd` | Ödeme yöntemi; kredi transferi için her zaman `TRF` |
| `ReqdExctnDt/Dt` | Talep edilen yürütme tarihi |
| `Dbtr/Nm` | Borçlu (gönderen) adı |
| `DbtrAcct/Id/IBAN` | Borçlu IBAN |
| `DbtrAgt/FinInstnId/BICFI` | Borçlu banka BIC |

**CdtTrfTxInf** (Credit Transfer Transaction Information), PmtInf bloğu başına bir veya daha fazla:

| Öğe | Açıklama |
|---|---|
| `PmtId/EndToEndId` | Uçtan uca referans (zincir boyunca korunur) |
| `Amt/InstdAmt` | Para birimi özniteliğiyle talimat verilen tutar |
| `CdtrAgt/FinInstnId/BICFI` | Alacaklı banka BIC |
| `Cdtr/Nm` | Alacaklı (alıcı) adı |
| `CdtrAcct/Id/IBAN` | Alacaklı IBAN |
| `RmtInf/Ustrd` | Yapılandırılmamış havale bilgisi (fatura referansı vb.) |

## CSV'den XML Üretme

Minimal bir pain001 çağrısı:

```python
from pain001 import create_xml_v9

create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml"
)
```

CSV dosyası sütun adlarını mesaj alanlarına eşler. Minimal bir örnek:

```csv
id,date,nb_of_txs,ctrl_sum,initiating_party_name,debtor_name,debtor_account_IBAN,debtor_agent_BIC,creditor_name,creditor_account_IBAN,creditor_agent_BIC,instd_amt,instd_amt_ccy,end_to_end_id,remittance_info
1,2024-01-15,1,1000.00,Acme Corp,Acme Corp,GB29NWBK60161331926819,NWBKGB2L,Supplier Ltd,DE89370400440532013000,COBADEFFXXX,1000.00,EUR,ACME20240115001,INV-2024-0042
```

Kütüphane, tek satırlı dosyalar için `ctrl_sum` ve `nb_of_txs` değerlerini CSV satırından okur. Çok satırlı dosyalarda (tek bir toplu işlemde birden fazla işlem) pain001, girdi değerlerine güvenmek yerine bu değerleri işlem kümesinden hesaplar; bu da uyuşmazlıkları önler.

SQLite arayüzü aynı sütun adı kuralını kullanır. `data_file_type="sqlite"` değerini ve `data_file` yolunu bir SQLite veritabanı dosyasına iletin; pain001 varsayılan olarak `payment` tablosunu okur.

## Üretilen XML Yapısı

Yukarıdaki CSV satırı için doğru şekilde oluşturulmuş bir pain.001.001.09 belgesi:

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

## XSD Doğrulama Hattı

Oluşturmanın ardından pain001, çıktıyı ISO 20022 pain.001.001.09 XSD şemasına göre doğrular. Doğrulama denetimleri:

- **Zorunlu öğe varlığı**: GrpHdr/MsgId, GrpHdr/CreDtTm, GrpHdr/NbOfTxs, GrpHdr/CtrlSum öğelerinin tümü gereklidir; herhangi birinin eksikliği bir doğrulama hatası fırlatır.
- **Tür kısıtlamaları**: IBAN biçimi, BIC biçimi (8 veya 11 karakter), tutar hassasiyeti (en fazla 18 basamak, 5 ondalık hane).
- **Kardinalite**: `PmtInf` başına en az bir `CdtTrfTxInf`; belge başına en az bir `PmtInf`.
- **Numaralandırma değerleri**: kredi transferleri için `PmtMtd` değeri `TRF` olmalıdır; `Ccy` geçerli bir ISO 4217 para birimi kodu olmalıdır.

Doğrulama başarısız olduğunda pain001, başarısız olan XPath ifadesini, öğe adını ve kısıtlamayı tanımlayan lxml hata mesajıyla birlikte bir `ValidationError` fırlatır. Bu, yanlış yapılandırmaları, reddetme kodlarının genellikle daha az açıklayıcı olduğu banka gönderiminde değil üretim anında ortaya çıkarır.

## SEPA'ya Karşı CBPR+ Yapılandırması

SEPA Kredi Transferi (EPC SCT kural kitabı kapsamındaki ISO 20022 pain.001.001.09) ve CBPR+ (SWIFT'in Cross-Border Payments and Reporting Plus standardı) aynı mesaj şemasını kullanır ancak zorunlu alan kümeleri ve değer kısıtlamaları bakımından farklılık gösterir:

| Yön | SEPA SCT | CBPR+ |
|---|---|---|
| Para birimi | Yalnızca EUR | Çoklu para birimi |
| IBAN zorunlu | Evet | Evet (alacaklı) |
| BIC zorunlu | Hayır (SEPA bölgesi yönlendirmesi) | Evet |
| Masraf tarafı (`ChrgBr`) | `SLEV` | `DEBT`, `CRED` veya `SHAR` |
| Kapsam | SEPA bölgesi (36 ülke) | Küresel muhabir bankacılık |

Mesaj türünü `payment_initiation_message_type` parametresi aracılığıyla yapılandırın:

```python
create_xml_v9(
    data_file="payments.csv",
    data_file_type="csv",
    xml_file_path="output/pain001.xml",
    payment_initiation_message_type="pain.001.001.09"  # varsayılan; eski SEPA için "pain.001.001.03" değerini de kabul eder
)
```

CBPR+ uyumu, SWIFT muhabir bankacılığı için gelen mesajlarda Kasım 2023'te, giden mesajlarda Kasım 2025'te zorunlu hale geldi. CBPR+ uyumlu pain.001 dosyaları üretmek, BIC alanının doldurulmasını ve `ChrgBr` öğesinin bulunmasını gerektirir.

## Sık Sorulan Sorular

**pain.001 ile pain.008 arasındaki fark nedir?**
pain.001 (CustomerCreditTransferInitiation) bir kredi transferini başlatır: gönderenin bankası gönderenin hesabından borç kaydeder ve alıcının hesabına alacak kaydeder. pain.008 (CustomerDirectDebitInitiation) bir doğrudan borçlandırmayı başlatır: alacaklının bankası borçludan fon tahsil eder. pain001 kütüphanesi yalnızca pain.001 dosyaları üretir.

**pain001 hangi ISO 20022 sürümünü hedefler?**
Birincil hedef, CBPR+ için gereken ve EPC tarafından yeni SEPA uygulamaları için zorunlu kılınan pain.001.001.09 sürümüdür. Kütüphane ayrıca, hâlâ eski banka arayüzlerini kullanan kuruluşlar için `payment_initiation_message_type` parametresi aracılığıyla pain.001.001.03 (eski SEPA sürümü) desteği de sunar.

**pain001 tek bir dosyada birden fazla borçlu hesabını işleyebilir mi?**
Evet. Farklı borçlu IBAN'larına sahip birden fazla `PmtInf` bloğu, farklı borçlu hesabı değerlerine sahip CSV satırları gruplanarak üretilebilir. pain001, benzersiz her (borçlu IBAN, yürütme tarihi) bileşimi için bir `PmtInf` bloğu oluşturur ve eşleşen tüm işlemleri `CdtTrfTxInf` alt öğeleri olarak iç içe yerleştirir.

**XSD doğrulaması başarısız olduğunda ne olur?**
pain001, lxml doğrulama mesajıyla birlikte bir `pain001.exceptions.ValidationError` fırlatır. Doğrulama başarısız olduğunda XML dosyası diske yazılmaz, dolayısıyla çıktı yoluna yalnızca geçerli dosyalar ulaşır. Yaygın başarısızlık nedenleri şunlardır: yanlış biçimde IBAN, 8 veya 11 karakter olmayan BIC, ISO 4217'de bulunmayan para birimi kodu veya gerekli bir CSV sütunu eksik olduğunda zorunlu öğelerin bulunmaması.

## Kaynaklar

1. European Payments Council. *SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines (v1.1)*. EPC, 2023. https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-credit-transfer-scheme-customer-bank
2. SWIFT. *CBPR+ Usage Guidelines — Customer Credit Transfer Initiation (pain.001)*. SWIFT Standards, 2023. https://www.swift.com/standards/iso-20022/cbpr-plus-usage-guidelines
3. ISO. *ISO 20022 — Financial services — Universal financial industry message scheme*. ISO.org, 2023. https://www.iso20022.org/
4. Rousseau, S. *pain001 — ISO 20022 payment file generator*. GitHub, 2023. https://github.com/sebastienrousseau/pain001

[00]: https://pain001.com/ "pain001: ISO 20022 uyumlu ödeme dosyası oluşturmayı otomatikleştirin"
[01]: https://www.iso20022.org/ "ISO 20022: Evrensel finansal sektör mesaj şeması"
